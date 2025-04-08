import numpy as np
import yaml
import trimesh
import polyscope as ps
import os
from datetime import datetime
import utilities as utils



class TriMeshExperiment:

    def __init__(self, config):
        settings = yaml.safe_load(open(config, "r"))
        # print(settings)
        # Experiment Needs
        self.dimension = settings["dimension"]
        self.source_file = settings["source_file"]
        self.target_file = settings["target_file"]
        self.source_name = settings["source_name"]
        self.target_name = settings["target_name"]
        self.scale_source = settings["scale_source"]
        self.scale_target = settings["scale_target"]
        self.warp_source = settings["warp_source"]
        self.warp_target = settings["warp_target"]
        self.source_scale_amount = settings["source_scale_amount"]
        self.target_scale_amount = settings["target_scale_amount"]
        self.warp_source_amount = settings["warp_source_amount"]
        self.warp_target_amount = settings["warp_target_amount"]
        self.source_mesh_adjustment = settings["source_mesh_adjustment"]
        self.target_mesh_adjustment = settings["target_mesh_adjustment"]
        self.fps: 1
        self.process_num = np.random.randint(1000,9999)

        #Trimesh Specific Needs
        self.source_landmarks = settings["source_landmarks"]
        self.target_positions = settings["target_positions"]
        self.steps = settings["steps"]
        self.eps = settings["eps"]
        self.gamma = settings["gamma"]
        self.distance_threshold = settings["distance_threshold"]
        self.use_faces = settings["use_faces"]
        self.use_vertex_normals = settings["use_vertex_normals"]
        self.neighbors_count = settings["neighbors_count"]
        self.d = datetime.now().strftime("%Y%m%d%H%M")
        self.folder_name = f"{self.d}_{self.process_num}_{self.source_name}_{self.target_name}"

        #Experiment Setup
        os.mkdir(self.folder_name)
        src = trimesh.load(self.source_file)
        trgt = trimesh.load(self.target_file)
        src.vertices = utils.normalize_coords(src.vertices, move_to_centre=True)
        trgt.vertices = utils.normalize_coords(trgt.vertices, move_to_centre=True)

        if self.source_mesh_adjustment is not None:
            for i in np.arange(len(self.source_mesh_adjustment)):
                src.vertices = src.vertices @ np.array(self.source_mesh_adjustment)[i]
            src.vertices = utils.centre(src.vertices)

        if self.target_mesh_adjustment is not None:
            for i in np.arange(len(self.target_mesh_adjustment)):
                trgt.vertices = trgt.vertices @ np.array(self.target_mesh_adjustment)[i]
            trgt.vertices = utils.centre(trgt.vertices)


        if self.scale_source == True:
            src.vertices *= self.source_scale_amount
            src.vertices = utils.centre(src.vertices)
        elif self.warp_source == True:
            src.vertices = np.stack(
                [src.vertices[:, 0]*self.warp_source_amount[0],
                 src.vertices[:, 1]*self.warp_source_amount[1],
                 src.vertices[:, 2]*self.warp_source_amount[2]], axis=1)
            src.vertices = utils.centre(src.vertices)


        if self.scale_target == True:
            trgt.vertices *= self.target_scale_amount
            trgt.vertices = utils.centre(trgt.vertices)
        elif self.warp_target == True:
            trgt.vertices = np.stack(
                [trgt.vertices[:, 0]*self.warp_target_amount[0],
                 trgt.vertices[:, 1]*self.warp_target_amount[1],
                 trgt.vertices[:, 2]*self.warp_target_amount[2]], axis=1)
            trgt.vertices = utils.centre(trgt.vertices)

        #Experiment
        reg = trimesh.registration.nricp_amberg(
            src,
            trgt,
            return_records=True,
            source_landmarks=self.source_landmarks,
            target_positions=self.target_positions,
            steps=self.steps,
            eps=self.eps,
            gamma=self.gamma,
            distance_threshold=self.distance_threshold,
            use_faces=self.use_faces,
            use_vertex_normals=self.use_vertex_normals,
            neighbors_count=self.neighbors_count

        )
        iters = np.array(reg)
        np.save(f"{self.folder_name}/{self.folder_name}_iters.npy", iters)

        # Visualization

        for i in np.arange(iters.shape[0]):
            ps.init()

            b_vis = ps.register_surface_mesh("src", src.vertices, src.faces, enabled=False)
            w_vis = ps.register_surface_mesh("trgt", trgt.vertices, trgt.faces, transparency=0.5)
            reg_vis0 = ps.register_surface_mesh("r", iters[i], trgt.faces)

            ps.set_up_dir("neg_y_up")
            ps.set_front_dir("neg_y_front")
            ps.set_screenshot_extension(".png")
            ps.screenshot(filename=f"{self.folder_name}/{i}.png")
            ps.show(1)

        for i in np.arange(iters.shape[0]):
            ps.init()

            b_vis = ps.register_surface_mesh("src", src.vertices, src.faces, enabled=False)
            w_vis = ps.register_surface_mesh("trgt", trgt.vertices, trgt.faces, transparency=0.5)
            reg_vis0 = ps.register_surface_mesh("r", iters[i], trgt.faces)

            ps.set_up_dir("neg_y_up")
            ps.set_front_dir("y_front")
            ps.set_screenshot_extension(".png")
            ps.screenshot(filename=f"{self.folder_name}/{i + iters.shape[0]}.png")
            ps.show(1)

        for i in np.arange(iters.shape[0]):
            ps.init()

            b_vis = ps.register_surface_mesh("src", src.vertices, src.faces, enabled=False)
            w_vis = ps.register_surface_mesh("trgt", trgt.vertices, trgt.faces, transparency=0.5)
            reg_vis0 = ps.register_surface_mesh("r", iters[i], trgt.faces)

            ps.set_up_dir("neg_y_up")
            ps.set_front_dir("z_front")
            ps.set_screenshot_extension(".png")
            ps.screenshot(filename=f"{self.folder_name}/{i + 2 * iters.shape[0]}.png")
            ps.show(1)

        for i in np.arange(iters.shape[0]):
            ps.init()

            b_vis = ps.register_surface_mesh("src", src.vertices, src.faces, enabled=False)
            w_vis = ps.register_surface_mesh("trgt", trgt.vertices, trgt.faces, transparency=0.5)
            reg_vis0 = ps.register_surface_mesh("r", iters[i], trgt.faces)

            ps.set_up_dir("neg_y_up")
            ps.set_front_dir("neg_z_front")
            ps.set_screenshot_extension(".png")
            ps.screenshot(filename=f"{self.folder_name}/{i + 3 * iters.shape[0]}.png")
            ps.show(1)

        utils.video_from_image_dir(self.folder_name, f"{self.folder_name}/{self.folder_name}.mp4")


exp1 = TriMeshExperiment("muybridge_014_01_to_muybridge_030_02_no_alt_20250407_experiment_config.yaml")