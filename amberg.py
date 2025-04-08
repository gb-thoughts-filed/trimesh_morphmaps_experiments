def nricp_amberg(
    source_mesh,
    target_geometry,
    source_landmarks=None,
    target_positions=None,
    steps=None,
    eps=0.0001,
    gamma=1,
    distance_threshold=0.1,
    return_records=False,
    use_faces=True,
    use_vertex_normals=True,
    neighbors_count=8,
):
    """
    Non Rigid Iterative Closest Points

    Implementation of "Amberg et al. 2007: Optimal Step
    Nonrigid ICP Algorithms for Surface Registration."
    Allows to register non-rigidly a mesh on another or
    on a point cloud. The core algorithm is explained
    at the end of page 3 of the paper.

    Comparison between nricp_amberg and nricp_sumner:
    * nricp_amberg fits to the target mesh in less steps
    * nricp_amberg can generate sharp edges
      * only vertices and their neighbors are considered
    * nricp_sumner tend to preserve more the original shape
    * nricp_sumner parameters are easier to tune
    * nricp_sumner solves for triangle positions whereas
      nricp_amberg solves for vertex transforms
    * nricp_sumner is less optimized when wn > 0

    Parameters
    ----------
    source_mesh : Trimesh
        Source mesh containing both vertices and faces.
    target_geometry : Trimesh or PointCloud or (n, 3) float
        Target geometry. It can contain no faces or be a PointCloud.
    source_landmarks : (n,) int or ((n,) int, (n, 3) float)
        n landmarks on the the source mesh.
        Represented as vertex indices (n,) int.
        It can also be represented as a tuple of triangle
        indices and barycentric coordinates ((n,) int, (n, 3) float,).
    target_positions : (n, 3) float
        Target positions assigned to source landmarks
    steps : Core parameters of the algorithm
        Iterable of iterables (ws, wl, wn, max_iter,).
        ws is smoothness term, wl weights landmark importance, wn normal importance
        and max_iter is the maximum number of iterations per step.
    eps : float
        If the error decrease if inferior to this value, the current step ends.
    gamma : float
        Weight the translation part against the rotational/skew part.
        Recommended value : 1.
    distance_threshold : float
        Distance threshold to account for a vertex match or not.
    return_records : bool
        If True, also returns all the intermediate results. It can help debugging
        and tune the parameters to match a specific case.
    use_faces : bool
        If True and if target geometry has faces, use proximity.closest_point to find
        matching points. Else use scipy's cKDTree object.
    use_vertex_normals : bool
        If True and if target geometry has faces, interpolate the normals of the target
        geometry matching points.
        Else use face normals or estimated normals if target geometry has no faces.
    neighbors_count : int
        number of neighbors used for normal estimation. Only used if target geometry has
        no faces or if use_faces is False.

    Returns
    ----------
    result : (n, 3) float or List[(n, 3) float]
        The vertices positions of source_mesh such that it is registered non-rigidly
        onto the target geometry.
        If return_records is True, it returns the list of the vertex positions at each
        iteration.
    """

    def _solve_system(M_kron_G, D, vertices_weight, nearest, ws, nE, nV, Dl, Ul, wl):
        # Solve for Eq. 12
        U = nearest * vertices_weight[:, None]
        use_landmarks = Dl is not None and Ul is not None
        A_stack = [ws * M_kron_G, D.multiply(vertices_weight[:, None])]
        B_shape = (4 * nE + nV, 3)
        if use_landmarks:
            A_stack.append(wl * Dl)
            B_shape = (4 * nE + nV + Ul.shape[0], 3)
        A = sparse.csr_matrix(sparse.vstack(A_stack))
        B = sparse.lil_matrix(B_shape, dtype=np.float32)
        B[4 * nE : (4 * nE + nV), :] = U
        if use_landmarks:
            B[4 * nE + nV : (4 * nE + nV + Ul.shape[0]), :] = Ul * wl
        X = sparse.linalg.spsolve(A.T * A, A.T * B).toarray()
        return X

    def _node_arc_incidence(mesh, do_weight):
        # Computes node-arc incidence matrix of mesh (Eq.10)
        nV = mesh.edges.max() + 1
        nE = len(mesh.edges)
        rows = np.repeat(np.arange(nE), 2)
        cols = mesh.edges.flatten()
        data = np.ones(2 * nE, np.float32)
        data[1::2] = -1
        if do_weight:
            edge_lengths = np.linalg.norm(
                mesh.vertices[mesh.edges[:, 0]] - mesh.vertices[mesh.edges[:, 1]], axis=-1
            )
            data *= np.repeat(1 / edge_lengths, 2)
        return sparse.coo_matrix((data, (rows, cols)), shape=(nE, nV))

    def _create_D(vertex_3d_data):
        # Create Data matrix (Eq. 8)
        nV = len(vertex_3d_data)
        rows = np.repeat(np.arange(nV), 4)
        cols = np.arange(4 * nV)
        data = np.concatenate((vertex_3d_data, np.ones((nV, 1))), axis=-1).flatten()
        return sparse.csr_matrix((data, (rows, cols)), shape=(nV, 4 * nV))

    def _create_X(nV):
        # Create Unknowns Matrix (Eq. 1)
        X_ = np.concatenate((np.eye(3), np.array([[0, 0, 0]])), axis=0)
        return np.tile(X_, (nV, 1))

    def _create_Dl_Ul(D, source_mesh, source_landmarks, target_positions):
        # Create landmark terms (Eq. 11)
        Dl, Ul = None, None

        if source_landmarks is None or target_positions is None:
            # If no landmarks are provided, return None for both
            return Dl, Ul

        if isinstance(source_landmarks, tuple):
            source_tids, source_barys = source_landmarks
            source_tri_vids = source_mesh.faces[source_tids]
            # u * x1, v * x2 and w * x3 combined
            Dl = D[source_tri_vids.flatten(), :]
            Dl.data *= source_barys.flatten().repeat(np.diff(Dl.indptr))
            x0 = source_mesh.vertices[source_tri_vids[:, 0]]
            x1 = source_mesh.vertices[source_tri_vids[:, 1]]
            x2 = source_mesh.vertices[source_tri_vids[:, 2]]
            Ul0 = (
                target_positions
                - x1 * source_barys[:, 1, None]
                - x2 * source_barys[:, 2, None]
            )
            Ul1 = (
                target_positions
                - x0 * source_barys[:, 0, None]
                - x2 * source_barys[:, 2, None]
            )
            Ul2 = (
                target_positions
                - x0 * source_barys[:, 0, None]
                - x1 * source_barys[:, 1, None]
            )
            Ul = np.zeros((Ul0.shape[0] * 3, 3))
            Ul[0::3] = Ul0  # y - v * x2 + w * x3
            Ul[1::3] = Ul1  # y - u * x1 + w * x3
            Ul[2::3] = Ul2  # y - u * x1 + v * x2
        else:
            Dl = D[source_landmarks, :]
            Ul = target_positions
        return Dl, Ul

    target_geometry, target_positions, centroid, scale = _normalize_by_source(
        source_mesh, target_geometry, target_positions
    )

    # Number of edges and vertices in source mesh
    nE = len(source_mesh.edges)
    nV = len(source_mesh.vertices)

    # Initialize transformed vertices
    transformed_vertices = source_mesh.vertices.copy()
    # Node-arc incidence (M in Eq. 10)
    M = _node_arc_incidence(source_mesh, True)
    # G (Eq. 10)
    G = np.diag([1, 1, 1, gamma])
    # M kronecker G (Eq. 10)
    M_kron_G = sparse.kron(M, G)
    # D (Eq. 8)
    D = _create_D(source_mesh.vertices)
    # D but for normal computation from the transformations X
    DN = _create_D(source_mesh.vertex_normals)
    # Unknowns 4x3 transformations X (Eq. 1)
    X = _create_X(nV)
    # Landmark related terms (Eq. 11)
    Dl, Ul = _create_Dl_Ul(D, source_mesh, source_landmarks, target_positions)

    # Parameters of the algorithm (Eq. 6)
    # order : Alpha, Beta, normal weighting, and max iteration for step
    if steps is None:
        steps = [
            [0.01, 10, 0.5, 10],
            [0.02, 5, 0.5, 10],
            [0.03, 2.5, 0.5, 10],
            [0.01, 0, 0.0, 10],
        ]
    if return_records:
        records = [transformed_vertices]

    # Main loop
    for ws, wl, wn, max_iter in steps:
        # If normals are estimated from points and if there are less
        # than 3 points per query, avoid normal estimation
        if not use_faces and neighbors_count < 3:
            wn = 0

        last_error = np.finfo(np.float32).max
        error = np.finfo(np.float16).max
        cpt_iter = 0

        # Current step iterations loop
        while last_error - error > eps and (max_iter is None or cpt_iter < max_iter):
            qres = _from_mesh(
                target_geometry,
                transformed_vertices,
                from_vertices_only=not use_faces,
                return_normals=wn > 0,
                return_interpolated_normals=wn > 0 and use_vertex_normals,
                neighbors_count=neighbors_count,
            )

            # Data weighting
            vertices_weight = np.ones(nV)
            vertices_weight[qres["distances"] > distance_threshold] = 0

            if wn > 0 and "normals" in qres:
                target_normals = qres["normals"]
                if use_vertex_normals and "interpolated_normals" in qres:
                    target_normals = qres["interpolated_normals"]
                # Normal weighting = multiplying weights by cosines^wn
                source_normals = DN * X
                dot = util.diagonal_dot(source_normals, target_normals)
                # Normal orientation is only known for meshes as target
                dot = np.clip(dot, 0, 1) if use_faces else np.abs(dot)
                vertices_weight = vertices_weight * dot**wn

            # Actual system solve
            X = _solve_system(
                M_kron_G, D, vertices_weight, qres["nearest"], ws, nE, nV, Dl, Ul, wl
            )
            transformed_vertices = D * X
            last_error = error
            error_vec = np.linalg.norm(qres["nearest"] - transformed_vertices, axis=-1)
            error = (error_vec * vertices_weight).mean()
            if return_records:
                records.append(transformed_vertices)
            cpt_iter += 1
            print(cpt_iter)

    if return_records:
        result = records
    else:
        result = transformed_vertices

    result = _denormalize_by_source(
        source_mesh, target_geometry, target_positions, result, centroid, scale
    )
    return result