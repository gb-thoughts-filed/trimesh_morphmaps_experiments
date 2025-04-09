import trimesh
import polyscope as ps
import numpy as np
import utilities as utils

def normalize_coords(coords_unnorm, move_to_centre=False):
    # find min max
    min_coord = np.min(coords_unnorm, axis=0)
    max_coord = np.max(coords_unnorm, axis=0)

    diff_coords = max_coord - min_coord

    max_diff = np.max(diff_coords)

    coord_norm = coords_unnorm.copy()

    coord_norm -= min_coord

    coord_norm /= (max_diff)

    if move_to_centre:
        min_coord = np.min(coord_norm, axis=0)
        max_coord = np.max(coord_norm, axis=0)
        actual_mid = (min_coord + max_coord) / 2
        desired_mid = np.full_like(actual_mid, fill_value=0.5)
        coord_norm -= (actual_mid - desired_mid)

    return coord_norm
def centre(coord_norm):

    min_coord = np.min(coord_norm, axis=0)
    max_coord = np.max(coord_norm, axis=0)
    actual_mid = (min_coord + max_coord) / 2
    desired_mid = np.full_like(actual_mid, fill_value=0.5)
    coord_norm -= (actual_mid - desired_mid)

    return coord_norm

source = trimesh.load('dogs_results/dogs/fox-05.ply')
target = trimesh.load('dogs_results/dogs/fox-05.ply')
source.vertices = normalize_coords(source.vertices, move_to_centre=True)
# source.vertices *= 0.8
# source.vertices = centre(source.vertices)
# batsy2.vertices = np.stack([batsy.vertices[:, 0], batsy.vertices[:, 1], batsy.vertices[:, 2]*5], axis=1)
target.vertices = normalize_coords(target.vertices, move_to_centre=True)
# target.vertices *= 0.8
# target.vertices = centre(target.vertices)


reg = trimesh.registration.nricp_amberg(source, target, distance_threshold=0.1, return_records=True)
iters = np.array(reg)
reg1= trimesh.registration.nricp_amberg(source, target, distance_threshold=0.1)
# print(iters[-1])

#mesh vertices, and mesh topology, just be able to cover the mesh at every single step
# max_iter set to None so it keeps going and converges
# Ablation keep everything fixed change one thing, ablation search?
# set range of alphas, video, screenshots, messages, config file
for i in np.arange(iters.shape[0]):
    ps.init()

    b_vis = ps.register_surface_mesh("source", source.vertices, source.faces, enabled=False)
    w_vis = ps.register_surface_mesh("target", target.vertices, target.faces, transparency=0.5)
    reg_vis0 = ps.register_surface_mesh("r", iters[i], target.faces)


    ps.set_up_dir("neg_y_up")
    ps.set_front_dir("neg_y_front")
    ps.set_screenshot_extension(".png")
    ps.screenshot(filename=f"20250404_fox_dog/{i}.png")
    ps.show(1)

for i in np.arange(iters.shape[0]):
    ps.init()

    b_vis = ps.register_surface_mesh("source", source.vertices, source.faces, enabled=False)
    w_vis = ps.register_surface_mesh("target", target.vertices, target.faces, transparency=0.5)
    reg_vis0 = ps.register_surface_mesh("r", iters[i], target.faces)


    ps.set_up_dir("neg_y_up")
    ps.set_front_dir("y_front")
    ps.set_screenshot_extension(".png")
    ps.screenshot(filename=f"20250404_fox_dog/{i + iters.shape[0]}.png")
    ps.show(1)

for i in np.arange(iters.shape[0]):
    ps.init()

    b_vis = ps.register_surface_mesh("source", source.vertices, source.faces, enabled=False)
    w_vis = ps.register_surface_mesh("target", target.vertices, target.faces, transparency=0.5)
    reg_vis0 = ps.register_surface_mesh("r", iters[i], target.faces)


    ps.set_up_dir("neg_y_up")
    ps.set_front_dir("z_front")
    ps.set_screenshot_extension(".png")
    ps.screenshot(filename=f"20250404_fox_dog/{i + 2*iters.shape[0]}.png")
    ps.show(1)

for i in np.arange(iters.shape[0]):
    ps.init()

    b_vis = ps.register_surface_mesh("source", source.vertices, source.faces, enabled=False)
    w_vis = ps.register_surface_mesh("target", target.vertices, target.faces, transparency=0.5)
    reg_vis0 = ps.register_surface_mesh("r", iters[i], target.faces)


    ps.set_up_dir("neg_y_up")
    ps.set_front_dir("neg_z_front")
    ps.set_screenshot_extension(".png")
    ps.screenshot(filename=f"20250404_fox_dog/{i + 3*iters.shape[0]}.png")
    ps.show(1)