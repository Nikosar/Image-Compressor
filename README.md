# Image-Compressor
This programm was created for compressing images.
You can use it easily - just place in the same directory with images and run.
```bat
image_processing.exe -s "D:\Downloads\photo" -q 60 -p 2000000
```
* -s image source directory, default = current directory
* -q output quality of image (1-100) not recommended above 95, default = 70
* -p how many pixels will be in result image (it won't be more then original).
Aspect ratio of original image will be saved. Default 360 000 (600 * 600)
