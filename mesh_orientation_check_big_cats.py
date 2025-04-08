import polyscope as ps
import trimesh
import numpy as np
from utilities import normalize_coords, centre

rotation_x = np.array([[1, 0, 0],[0, np.cos(180), -np.sin(180)],[0, np.sin(180), np.cos(180)]])
rotation_y = np.array([[np.cos(180), 0, np.sin(180)],[0, 1, 0],[-np.sin(180), 0, np.cos(180)]])
rotation_z = np.array([[np.cos(180), -np.sin(180), 0],[np.sin(180), np.cos(180), 0],[0, 0, 1]])
reflections = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])

lions_natural_habitat = trimesh.load('big_cats/450-122410176-lions-natural-habitat.ply')
ferrari = trimesh.load('big_cats/00211799_ferrari.ply')
cougar = trimesh.load('big_cats/cougar.ply')
lion3 = trimesh.load('big_cats/lion3.ply')
lion6 = trimesh.load('big_cats/lion6.ply')
lion_yawn = trimesh.load('big_cats/lion_yawn.ply')
MaleLion800 = trimesh.load('big_cats/MaleLion800.ply')
muybridge_107_110_03 = trimesh.load('big_cats/muybridge_107_110_03.ply')
muybridge_132_133_07 = trimesh.load('big_cats/muybridge_132_133_07.ply')

lions_natural_habitat.vertices = normalize_coords(lions_natural_habitat.vertices, move_to_centre=True)
ferrari.vertices = normalize_coords(ferrari.vertices, move_to_centre=True)

cougar.vertices = normalize_coords(cougar.vertices, move_to_centre=True)
# cougar.vertices = cougar.vertices @ np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])
# cougar.vertices = centre(cougar.vertices)
lion3.vertices = normalize_coords(lion3.vertices, move_to_centre=True)

lion6.vertices = normalize_coords(lion6.vertices, move_to_centre=True)
lion_yawn.vertices = normalize_coords(lion_yawn.vertices, move_to_centre=True)
MaleLion800.vertices = normalize_coords(MaleLion800.vertices, move_to_centre=True)
muybridge_107_110_03.vertices = normalize_coords(muybridge_107_110_03.vertices, move_to_centre=True)
muybridge_132_133_07.vertices = normalize_coords(muybridge_132_133_07.vertices, move_to_centre=True)


ps.init()

lions_natural_habitat_vis = ps.register_surface_mesh("lions_natural_habitat", lions_natural_habitat.vertices, lions_natural_habitat.faces, enabled=False)
ferrari_vis = ps.register_surface_mesh("ferrari", ferrari.vertices, ferrari.faces, enabled=False)
cougar_vis = ps.register_surface_mesh("cougar", cougar.vertices, cougar.faces)
lion3_vis = ps.register_surface_mesh("lion3", lion3.vertices, lion3.faces)
lion6_vis = ps.register_surface_mesh("lion6", lion6.vertices, lion6.faces, enabled=False)
lion_yawn_vis = ps.register_surface_mesh("lion_yawn", lion_yawn.vertices, lion_yawn.faces, enabled=False)
MaleLion800_vis = ps.register_surface_mesh("MaleLion800", MaleLion800.vertices, MaleLion800.faces, enabled=False)
muybridge_107_110_03_vis = ps.register_surface_mesh("muybridge_107_110_03", muybridge_107_110_03.vertices, muybridge_107_110_03.faces, enabled=False)
muybridge_132_133_07_vis = ps.register_surface_mesh("muybridge_132_133_07", muybridge_132_133_07.vertices, muybridge_132_133_07.faces, enabled=False)

ps.set_up_dir("neg_y_up")
ps.set_front_dir("neg_y_front")
ps.show()

# Good Matches
# muybridge_107_110_03, muybridge_132_133_07
# cougar, ferrari
# MaleLion800, lion_yawn, lion6

