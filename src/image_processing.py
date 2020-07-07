from pathlib import Path

import cli.app

from image_compressor import ImageCompressor

QUALITY_DEFAULT = 80
TARGET_PIXEL_COUNT_DEFAULT = 1000 * 1000


def main(working_dir, target_pixel_count, quality):
    working_dir_path = Path(working_dir)
    img_compressor = ImageCompressor(working_dir_path, target_pixel_count, quality)

    try:
        img_compressor.process_all_images()

        print("\nJob's done. ")
    except Exception as e:
        print("\nfinished with error: " + str(e))


def check_params(s, quality, pixels):
    if quality < 1 or quality > 100:
        raise AttributeError("Wrong quality value: " + quality)


@cli.app.CommandLineApp
def cli_app(app):
    source = app.params.s
    quality = int(app.params.quality)
    pixels = int(app.params.pixels)

    check_params(source, quality, pixels)
    main(source, pixels, quality)
    print("Press enter to exit")
    input()


cli_app.add_param("-s", help="img source directory", default=".")
cli_app.add_param("-q", "--quality", help="output quality of image (1-100) not recommended above 95, default = 70",
                  default=QUALITY_DEFAULT)
cli_app.add_param("-p", "--pixels", help="how many pixels will be in result image (it won't be more then original)."
                                         " Aspect ratio of original image will be saved. Default 360 000 (600 * 600)",
                  default=TARGET_PIXEL_COUNT_DEFAULT)

if __name__ == '__main__':
    cli_app.run()