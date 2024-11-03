import cv2
import matplotlib.pyplot as plt
import numpy as np

import cv2

# Dictionary mapping mountain range IDs to names
mountain_range = {
    "1": "Blanca",
    "2": "Huallanca",
    "3": "Huayhuash",
    "4": "Raura",
    "5": "Huagoruncho",
    "6": "La_Viuda",
    "7": "Central",
    "8": "Huaytapallana",
    "9": "Chonta",
    "10": "Ampato",
    "11": "Vilcabamba",
    "12": "Urubamba",
    "13": "Huanzo",
    "14": "Chila",
    "15": "Raya",
    "16": "Vilcanota",
    "17": "Carabaya",
    "18": "Apolobamba",
    "19": "Volcanica",
    "20": "Barroso"
}

def load_glacier_images(mountain_range_id="1"):
    """
    Loads glacier images from the specified path based on mountain range ID and retrieves the mountain range name.
    
    Parameters:
    mountain_range_id (str): ID representing the mountain range (e.g., "1" for Blanca).
    
    Returns:
    tuple: Tuple containing the mountain range name, image from 1989, and image from 2020.
           If images are not found, returns (None, None, None).
    
    Raises:
    FileNotFoundError: If the images for the specified mountain range ID do not exist.
    """
    # Get the name of the mountain range
    mountain_name = mountain_range.get(mountain_range_id, None)
    
    if mountain_name is None:
        print(f"Error: Mountain range ID {mountain_range_id} is not valid.")
        return None, None, None
    
    # Construct paths for images from 1989 and 2020
    image_path_1989 = f"../data/raw/{mountain_range_id}_{mountain_name}/1989.png"
    image_path_2020 = f"../data/raw/{mountain_range_id}_{mountain_name}/2020.png"
    
    try:
        # Load images from specified paths
        image_1989 = cv2.imread(image_path_1989, cv2.IMREAD_COLOR)
        image_2020 = cv2.imread(image_path_2020, cv2.IMREAD_COLOR)
        
        # Check if images are successfully loaded
        if image_1989 is None or image_2020 is None:
            raise FileNotFoundError(f"Images for mountain range ID {mountain_range_id} ({mountain_name}) not found at the specified paths.")
        
        return mountain_name, image_1989, image_2020
    
    except FileNotFoundError as e:
        # Print error message for missing images
        print(f"Error: {e}")
        return None, None, None


def crop_glacier_images(image_1989, image_2020):
    """
    Crops the given glacier images based on fixed dimensions, differentiating between horizontal and vertical orientations.
    
    Parameters:
    image_1989 (numpy.ndarray): The image of the glacier from 1989.
    image_2020 (numpy.ndarray): The image of the glacier from 2020.
    
    Returns:
    tuple: Cropped images (cropped_image_1989, cropped_image_2020) based on the orientation.
    """
    # Determine orientation based on the dimensions of the 1989 image
    if image_1989.shape[0] < image_1989.shape[1]:  # Horizontal orientation
        x_start, x_end = 500, 11500
        y_start, y_end = 500, 7000
    else:  # Vertical orientation
        x_start, x_end = 390, 7950
        y_start, y_end = 700, 9425
    
    # Crop images based on the specified coordinates
    cropped_image_1989 = image_1989[y_start:y_end, x_start:x_end]
    cropped_image_2020 = image_2020[y_start:y_end, x_start:x_end]
    
    return cropped_image_1989, cropped_image_2020



def extract_mountain_range_border(cropped_image_1989):
    """
    Extracts the external border of a mountain range in the image by filtering the green color.
    
    Parameters:
    cropped_image_1989 (numpy.ndarray): Cropped image of the glacier from 1989.
    
    Returns:
    numpy.ndarray: Masked image showing only the green border of the mountain range.
    """
    # Define HSV color range for green
    lower_green = np.array([50, 100, 20])   # Lower bound for green
    upper_green = np.array([90, 255, 255])  # Upper bound for green

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(cropped_image_1989, cv2.COLOR_BGR2HSV)

    # Create a mask for the green color
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Apply dilation to thicken the detected green border
    kernel = np.ones((5, 5), np.uint8)  # Adjust kernel size to change thickness
    green_mask_dilated = cv2.dilate(green_mask, kernel, iterations=1)

    # Apply the dilated mask to the original cropped image
    green_border_only = cv2.bitwise_and(cropped_image_1989, cropped_image_1989, mask=green_mask_dilated)
    
    return green_border_only


def create_mountain_mask(green_border_only):
    """
    Creates a mask by detecting and filling the largest contour in the given image.
    
    Parameters:
    green_border_only (numpy.ndarray): Image containing only the green border of the mountain range.
    
    Returns:
    numpy.ndarray: Binary mask where the largest contour is filled in white, with the rest in black.
    """
    # Convert to grayscale to facilitate contour detection
    gray_image = cv2.cvtColor(green_border_only, cv2.COLOR_BGR2GRAY)

    # Detect contours in the grayscale image
    contours, _ = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour by area
    largest_contour = max(contours, key=cv2.contourArea)

    # Create an empty mask (black) with the same size as the grayscale image
    mask_filled = np.zeros_like(gray_image)

    # Fill the largest contour with white on the mask
    cv2.drawContours(mask_filled, [largest_contour], -1, (255), thickness=cv2.FILLED)
    
    return mask_filled


def extract_glacier_1989_area(cropped_image_1989):
    """
    Extracts the glacier area in the 1989 image by filtering the pink color.
    
    Parameters:
    cropped_image_1989 (numpy.ndarray): Cropped image of the glacier from 1989.
    
    Returns:
    numpy.ndarray: Masked image showing only the pink areas representing glaciers in 1989.
    """
    # Define HSV color range for pink (glacier color in 1989)
    lower_pink = np.array([140, 50, 50])  
    upper_pink = np.array([180, 255, 255])
    
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(cropped_image_1989, cv2.COLOR_BGR2HSV)

    # Create a mask for the pink color
    pink_mask = cv2.inRange(hsv_image, lower_pink, upper_pink)

    # Apply the mask to the original cropped image
    glacier_1989_area = cv2.bitwise_and(cropped_image_1989, cropped_image_1989, mask=pink_mask)
    
    return glacier_1989_area

def extract_glacier_2020_area(cropped_image_2020):
    """
    Extracts the glacier area in the 2020 image by filtering the light blue color.
    
    Parameters:
    cropped_image_2020 (numpy.ndarray): Cropped image of the glacier from 2020.
    
    Returns:
    numpy.ndarray: Masked image showing only the light blue areas representing glaciers in 2020.
    """
    # Define HSV color range for light blue (glacier color in 2020)
    lower_blue = np.array([88, 50, 50])  
    upper_blue = np.array([110, 255, 255]) 

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(cropped_image_2020, cv2.COLOR_BGR2HSV)

    # Create a mask for the light blue color
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Apply the mask to the original cropped image
    glacier_2020_area = cv2.bitwise_and(cropped_image_2020, cropped_image_2020, mask=blue_mask)
    
    return glacier_2020_area

def reports_graphs(mountain_name, cropped_image_1989, cropped_image_2020, green_border_only, glacier_1989_area, glacier_2020_area, mask_filled):
    """
    Generates a graphical report comparing the mountain range in 1989 and 2020, highlighting glacier areas.
    
    Parameters:
    mountain_name (str): Name of the mountain range.
    cropped_image_1989 (numpy.ndarray): Cropped original image of the glacier from 1989.
    cropped_image_2020 (numpy.ndarray): Cropped original image of the glacier from 2020.
    green_border_only (numpy.ndarray): Masked image showing only the green border of the mountain range.
    glacier_1989_area (numpy.ndarray): Masked image showing glacier area in 1989.
    glacier_2020_area (numpy.ndarray): Masked image showing glacier area in 2020.
    mask_filled (numpy.ndarray): Binary mask where the largest contour is filled.
    """
    
    plt.figure(figsize=(12, 10))
    
    # Display the 1989 cropped image
    plt.subplot(2, 2, 1)
    plt.imshow(cv2.cvtColor(cropped_image_1989, cv2.COLOR_BGR2RGB))
    plt.title(f"Mountain Range {mountain_name} - 1989")
    plt.axis("off")

    # Overlay the glacier and border areas for 1989
    image_1989_with_border = cv2.bitwise_or(glacier_1989_area, green_border_only, mask=mask_filled)
    plt.subplot(2, 2, 2)
    plt.imshow(cv2.cvtColor(image_1989_with_border, cv2.COLOR_BGR2RGB))
    plt.title(f"{mountain_name} Glaciers - 1989")
    plt.axis("off")

    # Display the 2020 cropped image
    plt.subplot(2, 2, 3)
    plt.imshow(cv2.cvtColor(cropped_image_2020, cv2.COLOR_BGR2RGB))
    plt.title(f"Mountain Range {mountain_name} - 2020")
    plt.axis("off")

    # Overlay the glacier and border areas for 2020
    image_2020_with_border = cv2.bitwise_or(glacier_2020_area, green_border_only, mask=mask_filled)
    plt.subplot(2, 2, 4)
    plt.imshow(cv2.cvtColor(image_2020_with_border, cv2.COLOR_BGR2RGB))
    plt.title(f"{mountain_name} Glaciers - 2020")
    plt.axis("off")
    
    # Adjust layout to ensure images are closer together
    plt.tight_layout()
    plt.show()


def draw_histograms(glacier_1989_area, glacier_2020_area, mask_filled):
    """
    Generates histograms for the glacier areas in 1989 and 2020, calculates the pixel count for glacier areas,
    and displays the percentage difference.
    
    Parameters:
    glacier_1989_area (numpy.ndarray): Masked image showing glacier area in 1989.
    glacier_2020_area (numpy.ndarray): Masked image showing glacier area in 2020.
    mask_filled (numpy.ndarray): Binary mask where the largest contour is filled.
    """
    
    # Extract the red channel (glacier area color in 1989) and filter out background
    glacier_1989_masked = cv2.bitwise_and(glacier_1989_area, glacier_1989_area, mask=mask_filled)
    red_channel_1989 = glacier_1989_masked[:, :, 2]
    red_channel_filtered_1989 = red_channel_1989[red_channel_1989 > 20]
    hist_red_1989, bins_red = np.histogram(red_channel_filtered_1989, bins=256, range=[0, 256])

    # Extract the blue channel (glacier area color in 2020) and filter out background
    glacier_2020_masked = cv2.bitwise_and(glacier_2020_area, glacier_2020_area, mask=mask_filled)
    blue_channel_2020 = glacier_2020_masked[:, :, 0]
    blue_channel_filtered_2020 = blue_channel_2020[blue_channel_2020 > 20]
    hist_blue_2020, bins_blue = np.histogram(blue_channel_filtered_2020, bins=256, range=[0, 256])

    # Calculate total glacier pixels for 1989 and 2020
    total_pixels_1989 = np.sum(hist_red_1989[hist_red_1989 > 0])
    total_pixels_2020 = np.sum(hist_blue_2020[hist_blue_2020 > 0])

    # Plot the histograms
    plt.figure(figsize=(15, 6))

    # Red channel histogram for 1989
    plt.subplot(1, 2, 1)
    plt.plot(bins_red[:-1], hist_red_1989, color='red')
    plt.title("Glacier Histogram - 1989")
    plt.xlabel("Intensity Level")
    plt.ylabel("Frequency")

    # Blue channel histogram for 2020
    plt.subplot(1, 2, 2)
    plt.plot(bins_blue[:-1], hist_blue_2020, color='blue')
    plt.title("Glacier Histogram - 2020")
    plt.xlabel("Intensity Level")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()

    # Print pixel counts and percentage change
    print(f"Glacier Pixels in 1989: {total_pixels_1989}")
    print(f"Glacier Pixels in 2020: {total_pixels_2020}")
    percentage_change = round((total_pixels_1989 - total_pixels_2020) / total_pixels_1989 * 100, 2)
    print(f"Percentage change in glacier area: {percentage_change} %")
