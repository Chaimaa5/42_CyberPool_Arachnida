import sys
import os
import piexif
import exiftool
from PIL import Image, ExifTags

class colors:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'


def scorpion(ac, av):
    for image in av.images:
        try:
            if av.delete:
                    img = Image.open(image)
                    img_without_exif = Image.new("RGB", img.size)
                    img_without_exif.paste(img)
                    img_without_exif.save("out.png")
                    print("Exif data removed successfully.")
            else:
                with exiftool.ExifToolHelper() as et:
                    metadata = et.get_metadata(image)
                for item in metadata:
                    print(colors.OKBLUE + "Metadata for image:", image + colors.ENDC)
                    for key, value in item.items():
                        print(f"{key}: {value}")
        except Exception as e:
            print(colors.WARNING + "Error "  + colors.ENDC)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog = "Scorpion",
        description = "Search for EXIF data and other metadata.")
    parser.add_argument("-D", "--delete", action="store_true", help="Delete exif data")
    parser.add_argument("images", type=str, nargs="+", help="Images files to check")
    av = parser.parse_args()
    scorpion(len(sys.argv) , av)
