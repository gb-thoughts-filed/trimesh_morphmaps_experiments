import polyscope as ps
import trimesh
import numpy as np
from utilities import normalize_coords, centre

rotation_x = np.array([[1, 0, 0],[0, np.cos(180), -np.sin(180)],[0, np.sin(180), np.cos(180)]])
rotation_y = np.array([[np.cos(180), 0, np.sin(180)],[0, 1, 0],[-np.sin(180), 0, np.cos(180)]])
rotation_z = np.array([[np.cos(180), -np.sin(180), 0],[np.sin(180), np.cos(180), 0],[0, 0, 1]])
reflections = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])

ferrari00028740 = trimesh.load('horses_results/horses/00028740_ferrari.ply')
ferrari00047093 = trimesh.load('horses_results/horses/00047093_ferrari.ply')
ferrari00049424 = trimesh.load('horses_results/horses/00049424_ferrari.ply')
ferrari00057894 = trimesh.load('horses_results/horses/00057894_ferrari.ply')
grazing = trimesh.load('horses_results/horses/grazing.ply')
muybridge_014_01 = trimesh.load('horses_results/horses/muybridge_014_01.ply')
muybridge_030_02 = trimesh.load('horses_results/horses/muybridge_030_02.ply')
muybridge_071_04 = trimesh.load('horses_results/horses/muybridge_071_04.ply')
muybridge_074_01 = trimesh.load('horses_results/horses/muybridge_074_01.ply')
muybridge_075_04 = trimesh.load('horses_results/horses/muybridge_075_04.ply')

ferrari00028740.vertices = normalize_coords(ferrari00028740.vertices, move_to_centre=True)
ferrari00047093.vertices = normalize_coords(ferrari00047093.vertices, move_to_centre=True)

ferrari00049424.vertices = normalize_coords(ferrari00049424.vertices, move_to_centre=True)



ferrari00057894.vertices = normalize_coords(ferrari00057894.vertices, move_to_centre=True)
grazing.vertices = normalize_coords(grazing.vertices, move_to_centre=True)
muybridge_014_01.vertices = normalize_coords(muybridge_014_01.vertices, move_to_centre=True)
muybridge_030_02.vertices = normalize_coords(muybridge_030_02.vertices, move_to_centre=True)
muybridge_030_02.vertices = muybridge_030_02.vertices @ np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])
muybridge_030_02.vertices = centre(muybridge_030_02.vertices)
muybridge_071_04.vertices = normalize_coords(muybridge_071_04.vertices, move_to_centre=True)
muybridge_074_01.vertices = normalize_coords(muybridge_074_01.vertices, move_to_centre=True)
muybridge_075_04.vertices = normalize_coords(muybridge_075_04.vertices, move_to_centre=True)


ps.init()

ferrari00028740_vis = ps.register_surface_mesh("ferrari00028740", ferrari00028740.vertices, ferrari00028740.faces, enabled=False)
ferrari00047093_vis = ps.register_surface_mesh("ferrari00047093", ferrari00047093.vertices, ferrari00047093.faces, enabled=False)
ferrari00049424_vis = ps.register_surface_mesh("ferrari00049424", ferrari00049424.vertices, ferrari00049424.faces, enabled=False)
ferrari00057894_vis = ps.register_surface_mesh("ferrari00057894", ferrari00057894.vertices, ferrari00057894.faces, enabled=False)
grazing_vis = ps.register_surface_mesh("grazing", grazing.vertices, grazing.faces, enabled=False)
muybridge_014_01_vis = ps.register_surface_mesh("muybridge_014_01", muybridge_014_01.vertices, muybridge_014_01.faces, enabled=True)
muybridge_030_02_vis = ps.register_surface_mesh("muybridge_030_02", muybridge_030_02.vertices, muybridge_030_02.faces, enabled=True)
muybridge_071_04_vis = ps.register_surface_mesh("muybridge_071_04", muybridge_071_04.vertices, muybridge_071_04.faces, enabled=False)
muybridge_074_01_vis = ps.register_surface_mesh("muybridge_074_01", muybridge_074_01.vertices, muybridge_074_01.faces, enabled=False)
muybridge_075_04_vis = ps.register_surface_mesh("muybridge_075_04", muybridge_075_04.vertices, muybridge_075_04.faces, enabled=False)
ps.set_up_dir("neg_y_up")
ps.set_front_dir("neg_y_front")
ps.show()




# muybridge_014_01, muybridge_030_02, slight size difference, works with adjustment

