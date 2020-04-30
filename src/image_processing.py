import os
from pathlib import Path

from PIL import Image, UnidentifiedImageError, ImageFile
from shutil import copyfile, rmtree

OUTPUT_DIR = "image_processing_output"

FORMATS = (".jpg", ".bmp", ".gif", "png")

TARGET_PIXEL_COUNT = 600 * 600

QUALITY = 70

ImageFile.LOAD_TRUNCATED_IMAGES = True


def process_all_images():
    current_dir = Path(".")
    mk_dir()
    file_count = find_file_count(current_dir)
    i = 1
    for path in current_dir.iterdir():
        if is_processable_file(path):
            processing(path)
            print("processed: " + str(i) + " of " + str(file_count), end="\r")
            i += 1


def processing(img_path):
    output_img_path = OUTPUT_DIR + "/" + str(img_path.name)
    try:
        img = Image.open(img_path.absolute())

        if is_need_resize(img):
            img = resize_img(img)

        img = img.convert("RGB")
        img.save(output_img_path, 'JPEG', optimize=True, quality=QUALITY)

    except Exception as e:
        print("Cannot process image: " + str(img_path.name) + " " + str(e))
        print("")
        copyfile(img_path, output_img_path)


def is_need_resize(img):
    return img.width * img.height > TARGET_PIXEL_COUNT


def resize_img(img):
    k_resize = (img.width * img.height) / TARGET_PIXEL_COUNT
    k_resize = k_resize ** 0.5
    new_width = round(img.width / k_resize)
    new_height = round(img.height / k_resize)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    return img


def find_file_count(current_dir):
    return len([path for path in current_dir.iterdir() if is_processable_file(path)])


def is_processable_file(path):
    return path.is_file() and FORMATS.__contains__(path.suffix)


def mk_dir():
    output_dir_path = Path(OUTPUT_DIR)
    if output_dir_path.exists():
        rmtree(output_dir_path)
    os.mkdir(output_dir_path)


try:
    process_all_images()

    print("")
    print("Job's done. Press enter to exit")
except Exception as e:
    print()
    print("finished with error: " + str(e) + ". Press enter to exit")
    input()
