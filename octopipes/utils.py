import pathlib


def write_image(image, filename):
    import cv2

    path = pathlib.Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(filename, image)
