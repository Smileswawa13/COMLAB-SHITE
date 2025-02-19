# Author: Neil Justin V. Bermoy
# Created: 12-14-24
# Program: Grayscale Image!
# Instructions:
# 1.Open this link > Image Processing Files and download all files into your computer.
#   There are six files in total, do not delete any files in the link.
# 2. Search and download a .gif photo from any web browsers (Google, Safari, and Firefox)
#   and save it on the same folder in instruction no. 1. Please ensure that all images are
#   suitable images that contribute positively to the learning environment. Example: smokey.gif
# 3. Open PyCharm and open all files downloaded in instruction no. 1.
# 4.Run each Python files in this order: grayscale, invert, posterize, testblackandwhite, and
#   testdetectededges. No need to run “images.py”. It is part of the PIL library.
# 5. For Python files grayscale, invert, and posterize. Enter the file name of your .gif file (instruction no. 2) here.
# 6.For Python files testblackandwhite, and testdetectededges.
#   Change the “smokey.gif” with the file name of your .gif file (instruction no. 2)
#   and after running the file, close the generated window to see the converted images.
# 7. Save all .py files ("InitialsfirstnameLastname_LabExer4" as the filename)
#   and a screenshot of your output on your OneDrive or GDrive week 4 folder,
#   then submit the folders link to BBL submission bin.

# Import the proper module
from PIL import Image

#Our Grayscale function
def grayscale(image_path):
    try:
        with Image.open(image_path) as i:
            if i.mode != 'RGB':
                i = i.convert('RGB')
            for y in range(i.height):
                for x in range(i.width):
                    r, g, b = i.getpixel((x, y))
                    intensity = int(r * 0.299 + g * 0.587 + b * 0.114)
                    i.putpixel((x, y), (intensity, intensity, intensity))
            i.show()
    except FileNotFoundError:
        print(f"File not found: {image_path}")
    except AttributeError:
        print(f"Error loading image: {image_path}")

#Reality Holder
if __name__ == "__main__":
    grayscale("turtles.gif")