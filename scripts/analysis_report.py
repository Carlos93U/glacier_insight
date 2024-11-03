import cv2  
import matplotlib.pyplot as plt  
import numpy as np
from utils_script import *

# put mountain_range_id 
mountain_range_id = "3"

# load and crop glacier images
mountain_name, image_1989, image_2020 = load_glacier_images(mountain_range_id)
cropped_image_1989, cropped_image_2020 = crop_glacier_images(image_1989, image_2020)

# find border and mask 
green_border_only = extract_mountain_range_border(cropped_image_1989)
mask_filled = create_mountain_mask(green_border_only)

# extract glaciers 1989 and 2020
glacier_1989_area = extract_glacier_1989_area(cropped_image_1989)
glacier_2020_area = extract_glacier_2020_area(cropped_image_2020)

# reports
reports_graphs(mountain_range_id, mountain_name, cropped_image_1989, cropped_image_2020, green_border_only, glacier_1989_area, glacier_2020_area, mask_filled)
draw_histograms(mountain_range_id, glacier_1989_area, glacier_2020_area, mask_filled)