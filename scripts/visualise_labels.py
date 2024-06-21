import os
import argparse
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
from pynput.keyboard import Listener, Key


def load_image_label_pairs(image_dir, label_dir):
    """
    Generator to load image and label pairs from specified directories.

    Args:
        image_dir (str): Directory containing image files (.jpeg).
        label_dir (str): Directory containing label files (.txt).

    Yields:
        tuple: A tuple containing the image (as a PIL Image) and its corresponding label text.
    """
    # List all JPEG images in the image directory
    for image_filename in os.listdir(image_dir):
        if image_filename.lower().endswith(".jpeg"):
            # Construct the full path to the image file
            image_path = os.path.join(image_dir, image_filename)
            # Derive the corresponding label filename
            label_filename = os.path.splitext(image_filename)[0] + ".txt"
            # Construct the full path to the label file
            label_path = os.path.join(label_dir, label_filename)

            # Check if the corresponding label file exists
            if os.path.exists(label_path):
                # Open the image file using Pillow
                with Image.open(image_path) as image:
                    # Read the label file
                    with open(label_path, "r") as label_file:
                        label_text = label_file.read()

                    # Yield the image and label as a tuple
                    yield (image, label_text)


def get_image_label_pairs(image_dir, label_dir):
    pairs = []
    for image_filename in os.listdir(image_dir):
        if image_filename.lower().endswith(".jpg") or image_filename.lower().endswith(
            ".jpeg"
        ):
            image_path = os.path.join(image_dir, image_filename)
            label_filename = os.path.splitext(image_filename)[0] + ".txt"
            label_path = os.path.join(label_dir, label_filename)
            if os.path.exists(label_path):
                pairs.append((image_path, label_path))
    return pairs


def show_image_label(image_path, label_path):
    with Image.open(image_path) as image:
        # with open(label_path, 'r') as label_file:
        #    label_text = label_file.read()
        plt.imshow(image)
        # plt.title(label_text)
        plt.draw()


def press(event, paths, viewer_state):
    if event.key == "right":
        viewer_state["index"] = (viewer_state["index"] + 1) % len(paths)
        image_path, label_path = paths[viewer_state["index"]]
        show_image_label(image_path, label_path)
    elif event.key == "left":
        viewer_state["index"] = (viewer_state["index"] - 1) % len(paths)
        image_path, label_path = paths[viewer_state["index"]]
        show_image_label(image_path, label_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load image and label pairs from directories."
    )
    parser.add_argument(
        "path",
        help="The parent directory containing 'image' and 'label' subdirectories.",
    )
    args = parser.parse_args()

    from ultralytics.data import YOLODataset, YOLOConcatDataset
    from ultralytics.utils.plotting import Annotator
    import yaml

    from ultralytics.utils.instance import Instances

    class VisualiseDataset(YOLODataset):

        def __getitem__(self, index):
            return self.get_image_and_label(index)

    def load_all(root_path):
        def _load_all(config):
            for split in ["train", "val", "test"]:
                path = config.get(split, None)
                # there is a wierd bug with the yolo file format. .. is not necessary but it is used for some reason...
                if path.startswith(".."):
                    path = path[3:]
                if path:
                    path = str(Path(root_path, path).resolve())
                    yield VisualiseDataset(path, data=config, task="segment")

        with open(os.path.join(root_path, "data.yaml"), "r") as f:
            config = yaml.safe_load(f)
            return YOLOConcatDataset(list(_load_all(config))), config["names"]

    dataset, classes = load_all(args.path)
    for item in dataset:
        image = item["img"]
        cls = item["cls"].astype(int)
        item["instances"].convert_bbox("xyxy")  # required for plotting
        segments = item["instances"].segments
        bboxes = item["instances"].bboxes
        # this is used for drawing annotations on the image
        annotator = Annotator(image)

        h, w = image.shape[:2]
        # show segmentation if they exist
        for seg in segments:
            # segments since are shape [1000, 2], it might be better to just use labels directly. Its not so easy to get this from the dataset...
            seg[::2] = seg[::2] * w
            seg[1::2] = seg[1::2] * h
            annotator.draw_region(seg)
        # show bboxes if they exist
        for c, box in zip(cls, bboxes):
            box[::2] = box[::2] * w
            box[1::2] = box[1::2] * h
            annotator.box_label(box, label=classes[c[0]], color=(255, 0, 0))
        annotator.show()
        break

    # run with e.g. >> python ./scripts/visualise_labels.py /home/ben/.dataset/chessboard.v5i.yolov8

    # # Construct the paths to the image and label directories
    #
    # label_directory = os.path.join(args.path, 'labels')

    # image_label_pairs = get_image_label_pairs(image_directory, label_directory)

    # fig = plt.figure()
    # initial_index = 0
    # show_image_label(*image_label_pairs[initial_index])
    # viewer_state = {'index': initial_index}
    # fig.canvas.mpl_connect('key_press_event', lambda event: press(event, image_label_pairs, viewer_state))
    # plt.show()

    # with Listener(on_press=lambda key: on_press(key, image_label_pairs, viewer_state)) as listener:
    #    listener.join()
