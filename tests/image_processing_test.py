import unittest
from pathlib import Path

import image_processing
from shutil import rmtree

MB = 1024 ** 2


class MyTestCase(unittest.TestCase):
    def test_processing_compress_ratio(self):
        photo_input_dir = "test_photos"
        photo_output_dir = "test_photos/" + image_processing.ImageCompressor.OUTPUT_DIR

        image_processing.main(working_dir=photo_input_dir, target_pixel_count=1000 ** 2, quality=80)

        input_size = self.sum_of_file_sizes_in(photo_input_dir)
        output_size = self.sum_of_file_sizes_in(photo_output_dir)

        print("compressed from ", round(input_size/MB, 2), "MB to ", round(output_size/MB, 2), "MB, ",
              round(output_size / input_size, 4) * 100, "% of original size")

        rmtree(photo_output_dir)
        # self.assertEqual(True, False)

    @staticmethod
    def sum_of_file_sizes_in(path):
        p = Path(path)
        return sum(file.stat().st_size for file in p.iterdir() if file.is_file())


if __name__ == '__main__':
    unittest.main()
