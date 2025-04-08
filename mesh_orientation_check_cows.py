import polyscope as ps
import trimesh
import numpy as np
from utilities import normalize_coords, centre

rotation_x = np.array([[1, 0, 0],[0, np.cos(180), -np.sin(180)],[0, np.sin(180), np.cos(180)]])
rotation_y = np.array([[np.cos(180), 0, np.sin(180)],[0, 1, 0],[-np.sin(180), 0, np.cos(180)]])
rotation_z = np.array([[np.cos(180), -np.sin(180), 0],[np.sin(180), np.cos(180), 0],[0, 0, 1]])

cow2 = trimesh.load('cows_results/cows/cow2.ply')
cow_alph = trimesh.load('cows_results/cows/cow_alph.ply')
cow_alph4 = trimesh.load('cows_results/cows/cow_alph4.ply')
cow_alph5 = trimesh.load('cows_results/cows/cow_alph5.ply')
davis_cow = trimesh.load('cows_results/cows/Davis_cow_00000.ply')
muybridge_076_04 = trimesh.load('cows_results/cows/muybridge_076_04.ply')
muybridge_087_04 = trimesh.load('cows_results/cows/muybridge_087_04.ply')

cow2.vertices = normalize_coords(cow2.vertices, move_to_centre=True)
cow_alph.vertices = normalize_coords(cow_alph.vertices, move_to_centre=True)

cow_alph4.vertices = normalize_coords(cow_alph4.vertices, move_to_centre=True)
# cow_alph4.vertices = cow_alph4.vertices @ np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])
# cow_alph4.vertices = centre(cow_alph4.vertices)
cow_alph5.vertices = normalize_coords(cow_alph5.vertices, move_to_centre=True)

davis_cow.vertices = normalize_coords(davis_cow.vertices, move_to_centre=True)
muybridge_076_04.vertices = normalize_coords(muybridge_076_04.vertices, move_to_centre=True)
muybridge_087_04.vertices = normalize_coords(muybridge_087_04.vertices, move_to_centre=True)


ps.init()

cow2_vis = ps.register_surface_mesh("cow2", cow2.vertices, cow2.faces, enabled=False)
cow_alph_vis = ps.register_surface_mesh("cow_alph", cow_alph.vertices, cow_alph.faces, enabled=False)
cow_alph4_vis = ps.register_surface_mesh("cow_alph4", cow_alph4.vertices, cow_alph4.faces)
cow_alph5_vis = ps.register_surface_mesh("cow_alph5", cow_alph5.vertices, cow_alph5.faces)
davis_cow_vis = ps.register_surface_mesh("davis_cow", davis_cow.vertices, davis_cow.faces, enabled=False)
muybridge_076_04_vis = ps.register_surface_mesh("muybridge_076_04", muybridge_076_04.vertices, muybridge_076_04.faces, enabled=False)
muybridge_087_04_vis = ps.register_surface_mesh("muybridge_087_04", muybridge_087_04.vertices, muybridge_087_04.faces, enabled=False)


ps.set_up_dir("neg_y_up")
ps.set_front_dir("neg_y_front")
ps.show()

#cow alph 4 and 5 good match and size match