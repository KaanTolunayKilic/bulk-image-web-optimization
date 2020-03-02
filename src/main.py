import argparse
import os
from termcolor import colored, cprint
from PIL import Image

IMAGE_FORMATS = (".jpg", ".jpeg", ".png", ".tiff", ".psd")
JPEG_SUFFIX = ".jpg"

arg_parse = argparse.ArgumentParser(description="Command line tool for bulk image processing across all subfolders")

arg_parse.add_argument("source_dir", type=str, help="A string path to source folder")
arg_parse.add_argument("target_dir", type=str, help="A string path to target folder")
arg_parse.add_argument("width", type=int, help="An required inter to specify the images width")
arg_parse.add_argument("quality", type=int, nargs="?", help="An optional integer to specify the image quality")

args = arg_parse.parse_args()

abs_source_path = os.path.abspath(args.source_dir)

for current_path, sub_folders, file_names in os.walk(abs_source_path):
    for filename in file_names:
        source_file_path = os.path.join(current_path, filename)
        sub_path = os.path.relpath(current_path, abs_source_path) if current_path != abs_source_path else ""
        target_file_path = os.path.join(args.target_dir, sub_path, os.path.splitext(filename)[0] + JPEG_SUFFIX)

        if source_file_path.endswith(IMAGE_FORMATS):
            original_image = Image.open(source_file_path)

            wPercentage = args.width / float(original_image.size[0])
            width = args.width
            height = float(original_image.size[1]) * wPercentage
            size = (int(width), int(height))

            target_image = original_image.convert('RGB')
            target_image.thumbnail(size, Image.ANTIALIAS)

            target_dir = os.path.dirname(target_file_path)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            resolution = args.quality if args.quality else 95
            target_image.save(target_file_path, quality=resolution)
            cprint("Writing " + source_file_path + " --> " + target_file_path + " " + u"\u2713", "green")


