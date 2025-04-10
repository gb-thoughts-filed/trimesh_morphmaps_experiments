import os
import cv2
import numpy as np



def video_from_image_dir(
    image_folder, video_name=None, fps=1, width=None, height=None, mogrify=False
):
    """Make a video from a folder of images."""
    if video_name is None:
        video_name = os.path.join(image_folder, "video.mp4")

    if os.path.exists(image_folder):
        images = [img for img in os.listdir(image_folder) if img.endswith(".png")]

        if not images:
            print("No PNG images found in the specified folder.")
            return

        # Sort the images based on their filenames (assuming filenames are integers)
        images.sort(key=lambda x: int(x.split(".")[0]))

        frame = cv2.imread(os.path.join(image_folder, images[0]))
        h, w, layers = frame.shape

        if height is None or width is None:
            height = h
            width = w

        video = cv2.VideoWriter(
            video_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
        )

        for image in images:
            img_path = os.path.join(image_folder, image)

            # Read the image using cv2.IMREAD_UNCHANGED to handle images with an alpha channel
            img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

            if mogrify:
                if img.shape[2] == 4:  # If image has alpha channel
                    alpha_channel = img[:, :, 3]
                    img[alpha_channel < 10] = [
                        255,
                        255,
                        255,
                        255,
                    ]  # Set transparent pixels to white

                    # also set all black to white
                    img[
                        (img[:, :, 0] < 10) & (img[:, :, 1] < 10) & (img[:, :, 2] < 10)
                    ] = [255, 255, 255, 255]

            if img.shape[2] == 4:  # If image has alpha channel
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

            # Resize the image
            img = cv2.resize(img, (width, height))

            # If the image has an alpha channel, remove it to avoid potential issues
            if img.shape[-1] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            video.write(img)

        cv2.destroyAllWindows()
        video.release()
    else:
        print(f"The specified image folder '{image_folder}' does not exist.")

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