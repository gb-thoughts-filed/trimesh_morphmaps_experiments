import polyscope as ps
import trimesh
import numpy as np
from utilities import normalize_coords, centre

rotation_x = np.array([[1, 0, 0],[0, np.cos(180), -np.sin(180)],[0, np.sin(180), np.cos(180)]])
rotation_y = np.array([[np.cos(180), 0, np.sin(180)],[0, 1, 0],[-np.sin(180), 0, np.cos(180)]])
rotation_z = np.array([[np.cos(180), -np.sin(180), 0],[np.sin(180), np.cos(180), 0],[0, 0, 1]])
reflections = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])

Brown_And_White_Akita_Dog_alph = trimesh.load('dogs_results/dogs/Brown-And-White-Akita-Dog_alph.ply')
dog2 = trimesh.load('dogs_results/dogs/dog2.ply')
dog_alph = trimesh.load('dogs_results/dogs/dog_alph.ply')
fox = trimesh.load('dogs_results/dogs/fox.ply')
fox_05 = trimesh.load('dogs_results/dogs/fox-05.ply')
fox_06 = trimesh.load('dogs_results/dogs/fox-06.ply')
fox_alph = trimesh.load('dogs_results/dogs/fox_alph.ply')
muybridge_097_01 = trimesh.load('dogs_results/dogs/muybridge_097_01.ply')
muybridge_097_02 = trimesh.load('dogs_results/dogs/muybridge_097_02.ply')
muybridge_101_03 = trimesh.load('dogs_results/dogs/muybridge_101_03.ply')
muybridge_102_03 = trimesh.load('dogs_results/dogs/muybridge_102_03.ply')
muybridge_104_04 = trimesh.load('dogs_results/dogs/muybridge_104_04.ply')
NORTHERN_INUIT_DOG_3 = trimesh.load('dogs_results/dogs/NORTHERN-INUIT-DOG-3.ply')
stalking_wolf_cub_by_nieme = trimesh.load('dogs_results/dogs/stalking_wolf_cub_by_nieme.ply')
wolf_alph2 = trimesh.load('dogs_results/dogs/wolf_alph2.ply')
wolf_alph3 = trimesh.load('dogs_results/dogs/wolf_alph3.ply')

Brown_And_White_Akita_Dog_alph.vertices = normalize_coords(Brown_And_White_Akita_Dog_alph.vertices, move_to_centre=True)
dog2.vertices = normalize_coords(dog2.vertices, move_to_centre=True)

dog_alph.vertices = normalize_coords(dog_alph.vertices, move_to_centre=True)
# dog_alph.vertices = dog_alph.vertices @ np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]])
# dog_alph.vertices = centre(dog_alph.vertices)
fox.vertices = normalize_coords(fox.vertices, move_to_centre=True)

fox_05.vertices = normalize_coords(fox_05.vertices, move_to_centre=True)
fox_06.vertices = normalize_coords(fox_06.vertices, move_to_centre=True)
fox_alph.vertices = normalize_coords(fox_alph.vertices, move_to_centre=True)
muybridge_097_01.vertices = normalize_coords(muybridge_097_01.vertices, move_to_centre=True)
muybridge_097_02.vertices = normalize_coords(muybridge_097_02.vertices, move_to_centre=True)
muybridge_101_03.vertices = normalize_coords(muybridge_101_03.vertices, move_to_centre=True)
muybridge_102_03.vertices = normalize_coords(muybridge_102_03.vertices, move_to_centre=True)
muybridge_104_04.vertices = normalize_coords(muybridge_104_04.vertices, move_to_centre=True)
NORTHERN_INUIT_DOG_3.vertices = normalize_coords(NORTHERN_INUIT_DOG_3.vertices, move_to_centre=True)
stalking_wolf_cub_by_nieme.vertices = normalize_coords(stalking_wolf_cub_by_nieme.vertices, move_to_centre=True)
wolf_alph2.vertices = normalize_coords(wolf_alph2.vertices, move_to_centre=True)
wolf_alph3.vertices = normalize_coords(wolf_alph3.vertices, move_to_centre=True)


ps.init()

Brown_And_White_Akita_Dog_alph_vis = ps.register_surface_mesh("Brown_And_White_Akita_Dog_alph", Brown_And_White_Akita_Dog_alph.vertices, Brown_And_White_Akita_Dog_alph.faces, enabled=False)
dog2_vis = ps.register_surface_mesh("dog2", dog2.vertices, dog2.faces, enabled=False)
dog_alph_vis = ps.register_surface_mesh("dog_alph", dog_alph.vertices, dog_alph.faces)
fox_vis = ps.register_surface_mesh("fox", fox.vertices, fox.faces)
fox_05_vis = ps.register_surface_mesh("fox_05", fox_05.vertices, fox_05.faces, enabled=False)
fox_06_vis = ps.register_surface_mesh("fox_06", fox_06.vertices, fox_06.faces, enabled=False)
fox_alph_vis = ps.register_surface_mesh("fox_alph", fox_alph.vertices, fox_alph.faces, enabled=False)
muybridge_097_01_vis = ps.register_surface_mesh("muybridge_097_01", muybridge_097_01.vertices, muybridge_097_01.faces, enabled=False)
muybridge_097_02_vis = ps.register_surface_mesh("muybridge_097_02", muybridge_097_02.vertices, muybridge_097_02.faces, enabled=False)
muybridge_101_03_vis = ps.register_surface_mesh("muybridge_101_03", muybridge_101_03.vertices, muybridge_101_03.faces, enabled=False)
muybridge_102_03_vis = ps.register_surface_mesh("muybridge_102_03", muybridge_102_03.vertices, muybridge_102_03.faces, enabled=False)
muybridge_104_04_vis = ps.register_surface_mesh("muybridge_104_04", muybridge_104_04.vertices, muybridge_104_04.faces, enabled=False)
NORTHERN_INUIT_DOG_3_vis = ps.register_surface_mesh("NORTHERN_INUIT_DOG_3", NORTHERN_INUIT_DOG_3.vertices, NORTHERN_INUIT_DOG_3.faces, enabled=False)
stalking_wolf_cub_by_nieme_vis = ps.register_surface_mesh("stalking_wolf_cub_by_nieme", stalking_wolf_cub_by_nieme.vertices, stalking_wolf_cub_by_nieme.faces, enabled=False)
wolf_alph2_vis = ps.register_surface_mesh("wolf_alph2", wolf_alph2.vertices, wolf_alph2.faces, enabled=False)
wolf_alph3_vis = ps.register_surface_mesh("wolf_alph3", wolf_alph3.vertices, wolf_alph3.faces, enabled=False)
ps.set_up_dir("neg_y_up")
ps.set_front_dir("neg_y_front")
ps.show()

# fox and fox6 a decent match
# fox6 and fox_alph also pretty close
# Northern Inuit Dog, wolf2, very similar poses different scales




