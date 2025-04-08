import polyscope as ps
import trimesh
import numpy as np
from utilities import normalize_coords, centre

rotation_x = np.array([[1, 0, 0],[0, np.cos(180), -np.sin(180)],[0, np.sin(180), np.cos(180)]])
rotation_y = np.array([[np.cos(180), 0, np.sin(180)],[0, 1, 0],[-np.sin(180), 0, np.cos(180)]])
rotation_z = np.array([[np.cos(180), -np.sin(180), 0],[np.sin(180), np.cos(180), 0],[0, 0, 1]])
reflections = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])

hippo5 = trimesh.load('hippos_results/hippos/hippo5.ply')
hippo_alpha = trimesh.load('hippos_results/hippos/hippo_alpha.ply')
hippo_alpha_mouthopen2 = trimesh.load('hippos_results/hippos/hippo_alpha_mouthopen2.ply')
Hippo_for_Nat = trimesh.load('hippos_results/hippos/Hippo_for_Nat.ply')
hippo_walking = trimesh.load('hippos_results/hippos/hippo_walking.ply')
hippos = trimesh.load('hippos_results/hippos/hippos.ply')


hippo5.vertices = normalize_coords(hippo5.vertices, move_to_centre=True)
hippo_alpha.vertices = normalize_coords(hippo_alpha.vertices, move_to_centre=True)

hippo_alpha_mouthopen2.vertices = normalize_coords(hippo_alpha_mouthopen2.vertices, move_to_centre=True)
# hippo_alpha_mouthopen2.vertices = hippo_alpha_mouthopen2.vertices @ np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])
# hippo_alpha_mouthopen2.vertices = centre(hippo_alpha_mouthopen2.vertices)
Hippo_for_Nat.vertices = normalize_coords(Hippo_for_Nat.vertices, move_to_centre=True)

hippo_walking.vertices = normalize_coords(hippo_walking.vertices, move_to_centre=True)
hippos.vertices = normalize_coords(hippos.vertices, move_to_centre=True)


ps.init()

hippo5_vis = ps.register_surface_mesh("hippo5", hippo5.vertices, hippo5.faces, enabled=False)
hippo_alpha_vis = ps.register_surface_mesh("hippo_alpha", hippo_alpha.vertices, hippo_alpha.faces, enabled=False)
hippo_alpha_mouthopen2_vis = ps.register_surface_mesh("hippo_alpha_mouthopen2", hippo_alpha_mouthopen2.vertices, hippo_alpha_mouthopen2.faces)
Hippo_for_Nat_vis = ps.register_surface_mesh("Hippo_for_Nat", Hippo_for_Nat.vertices, Hippo_for_Nat.faces)
hippo_walking_vis = ps.register_surface_mesh("hippo_walking", hippo_walking.vertices, hippo_walking.faces, enabled=False)
hippos_vis = ps.register_surface_mesh("hippos", hippos.vertices, hippos.faces, enabled=False)
ps.set_up_dir("neg_y_up")
ps.set_front_dir("neg_y_front")
ps.show()

# hippo_alph, hippo_walking good match





