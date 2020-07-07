import os
from pathlib import Path
import cli.app
from PIL import Image, ImageFile
from shutil import copyfile, rmtree


class ImageCompressor:
    OUTPUT_DIR = "image_processing_output"
    FORMATS = (".jpg", "jpeg", ".bmp", ".gif", "png")
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    def __init__(self, working_dir_path, target_pixel_count, quality):
        self.quality = quality
        self.target_pixel_count = target_pixel_count
        self.working_dir_path = working_dir_path

    def process_all_images(self):
        output_dir_path = self.mk_dir()
        file_count = self.find_file_count(self.working_dir_path)
        i = 1
        for path in self.working_dir_path.iterdir():
            if self.is_processable_file(path):
                self.process_img(path, output_dir_path)
                print("processed: " + str(i) + " of " + str(file_count), end="\r")
                i += 1

    def process_img(self, img_path, output_dir_path):
        output_img_path = output_dir_path.joinpath(img_path.name)
        try:
            img = Image.open(img_path.absolute())

            if self.is_need_resize(img):
                img = self.resize_img(img)

            img = img.convert("RGB")
            img.save(output_img_path, 'JPEG', optimize=True, quality=self.quality)

        except Exception as e:
            print("Cannot process image: " + str(img_path.name) + " " + str(e))
            print("")
            copyfile(img_path, output_img_path)

    def is_need_resize(self, img):
        return img.width * img.height > self.target_pixel_count

    def resize_img(self, img):
        k_resize = (img.width * img.height) / self.target_pixel_count
        k_resize = k_resize ** 0.5
        new_width = round(img.width / k_resize)
        new_height = round(img.height / k_resize)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        return img

    def find_file_count(self, current_dir):
        return len([path for path in current_dir.iterdir() if self.is_processable_file(path)])

    def is_processable_file(self, path):
        return path.is_file() and self.FORMATS.__contains__(path.suffix)

    def mk_dir(self):
        output_dir_path = self.working_dir_path.joinpath(self.OUTPUT_DIR)
        if output_dir_path.exists():
            rmtree(output_dir_path)
        os.mkdir(output_dir_path)
        return output_dir_path
