from PIL import Image
from PIL import ImageFile
import os
import zipfile
import time
import shutil
import cairosvg
from tqdm import tqdm
from pathlib import Path

Image.MAX_IMAGE_PIXELS = None

input_dir = "/Users/jackperry/Desktop/ART PACKs/Playtime Barbie Themed Pack 1 - Set 6"

start_time = time.time()

def crop():
    sizes = {
        "2:3": [(60, 90)],
        "3:4": [(60, 80)],
        "4:5": [(60, 75)],
        "ISO": [(59.4, 84.1)],
        "Original Size": []
    }
    #accepts png or jpg, amend to extend input functionality.
    all_files = [f for f in os.listdir(input_dir) if f.endswith(('.jpg', '.png'))]
    total_files = len(all_files)

    print("Starting cropping and processing...")
    for dirpath, dirnames, filenames in os.walk(input_dir):
        all_files = [f for f in filenames if f.endswith(('.jpg', '.png'))]
        total_files = len(all_files)

        for filename in tqdm(all_files, total=total_files, ncols=75):
            filepath = os.path.join(dirpath, filename)
            image_dir = os.path.join(dirpath, filename[:-4] + '_cropped')  # Creates a subfolder for cropped images
            os.makedirs(image_dir, exist_ok=True)
            with Image.open(filepath) as img:  # Open the image here
                width, height = img.size

                for aspect_ratio, dimensions in sizes.items():
                    for dimension in dimensions:
                        center_x = width / 2
                        center_y = height / 2

                        aspect_ratio_width = dimension[0]
                        aspect_ratio_height = dimension[1]

                        if width > height:
                            aspect_ratio_width, aspect_ratio_height = aspect_ratio_height, aspect_ratio_width

                        # Crop process
                        crop_width = min(height * aspect_ratio_width / aspect_ratio_height, width)
                        crop_height = crop_width * aspect_ratio_height / aspect_ratio_width

                        left = (width - crop_width) / 2
                        top = (height - crop_height) / 2
                        right = (width + crop_width) / 2
                        bottom = (height + crop_height) / 2

                        cropped_img = img.crop((left, top, right, bottom))

                        # Print diagnostic information before conversion
                        print("Before conversion:", cropped_img.mode, cropped_img.size)

                        # Check if the image is in RGBA mode and convert to RGB if necessary
                        if cropped_img.mode == 'RGBA':
                            cropped_img = cropped_img.convert('RGB')

                        # Print diagnostic information after conversion
                        print("After conversion:", cropped_img.mode, cropped_img.size)

                        output_filename = "{}_{}x{}_{}.jpg".format(filename[:-4], width, height, aspect_ratio)
                        output_filepath = os.path.join(image_dir, output_filename)
                        cropped_img.save(output_filepath, quality=95) # You can set the value between 0 and 100


                        if aspect_ratio == "Original Size" and (width, height) not in dimensions:
                            dimensions.append((width, height))
                            output_filename = "{}_{}x{}_{}.jpg".format(filename[:-4], width, height, aspect_ratio)
                            output_filepath = os.path.join(image_dir, output_filename)
                    
crop()

end_time = time.time()
total_time = end_time - start_time

print("Total time taken: ", total_time, " seconds")
