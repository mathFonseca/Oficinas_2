#!/usr/bin/python
#-*- coding: utf-8 -*-

# IMPORTS

import numpy as np  # Numeric Operations Library
import cv2  # Open CV v2 for images Operations
import os   # Operational System Library.
import commands # For utilizing terminal commands inside here

# IMPORTS DISCONTINUED

import argparse
from matplotlib import pyplot as plt

# DEFINES AND GLOBAL VARIABLES
image_address = 'image.jpg' # Address for acessing the image that
# will be used in the application

# In OpenCV, it utilizes the following order: Blue Green Redself.
# It stills RGB, but in the reverse order.

lower_blue = [80, 65, 0]    # Lower parameters for acceptable blue color
upper_blue = [255, 255, 125]    # Upper parameters for acceptable blue color
lower_red = [0, 50, 50] # Lower parameters for acceptable red color
upper_red = [10, 255, 255]  # Upper parameters for acceptable red color

# Default settings for the Raspberry Camera.
quality = 30    # 30% of the original pictura quality
height = 600
width = 800
file_name = "img"    # The name of the file after the picture shoot.
file_extension = "png"    # The extension of the picture saved.

# Default setting for the binarization and grey scale functions

binary_type = 3
binary_type_name = "Adaptative Binarzation using Gaussian Function."

# Type of binarizations implemented an their name
# 0 - Simple Binarization.
# 1 - Otsu's Binarization.
# 2 - Adaptative Binarzation using median
# 3 - Adaptative Binarzation using Gaussian Function.

# Flags and other defauts variables

save_flag = True
threshold_value = 127

# FUNCTIONS

# Connects with the OS inside the Raspberry and take a picture.
# It utilizes the default setting described above.

def take_picture(quality, height, width, file_name, file_extension):
    string = ("raspistill -q "
              + str(quality)
              + " -w "
              + str(width)
              + " -h "
              + str(height)
              + " -o "
              + file_name
              + "."
              + file_extension)
    sucessful = True
    sucessful = os.system(string)

    # Taking the picture takes a time.
    # Maybe adding a timer in here? It doesn't seem that stubborn.

    if sucessful:
        print("It was not possible to take the picture.")
    else:
        print("Picture was shoot sucessfuly")
    return sucessful

# Loads the image_file into a proper variable.

def load_image(image_address):
    original_image = cv2.imread(image_address)
    return original_image

# Applys Grey Sacle filter on the image given.
# It utilizes the normal grey scale algorithm from OpenCV

def apply_grey_scale(original_image, save_flag):
    grey_scale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    if save_flag == True:
        cv2.imwrite('grey_scale_image.jpg', grey_scale_image)
    return grey_scale_image

# Applys the default binarzation to a given grey scale image.

def binarization(grey_scale_image, threshold_value, binary_type, save_flag):
    if binary_type == 0:
        ret, binary_image = cv2.threshold(grey_scale_image, \
        threshold_value, 255, cv2.THRESH_BINARY)
        if save_flag == True:
            cv2.imwrite('simple_binarization.png', binary_image)
    elif binary_type == 1:
        ret, binary_img = cv2.threshold(grey_scale_image, 0, 255, \
        cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if save_flag == True:
            cv2.imwrite('otsu_binarization.png', binary_image)
    elif binary_type == 2:
        binary_img = cv2.adaptiveThreshold(grey_scale_image, 255, \
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        if save_flag == True:
            cv2.imwrite('adaptative_binarzation_mean.png', binary_image)
    elif binary_type == 3:
        binary_img = cv2.adaptiveThreshold(grey_scale_image, 255, \
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        if save_flag == True:
            cv2.imwrite('adaptative_binarzation_gaussian.png', binary_image)

    return binary_image

# Function for setting the camera parameters

def configure_cam():
    print("\nStarting Camera...")
    print("Default Camera Setting:\nQuality: "
            + str(quality)
            + "\nHeight (pixels): "
            + str(height)
            + "\nWidth (pixels): "
            + str(width)
            + "\nFile name: "
            + file_name
            + "."
            + file_extension
            + "")
    print("If you want to modify, press 1. To keep this setting and proceed\
            , press 2.")
    option = input()
    if option == 1:
        print("Still not implemented. Come back later")
    elif option == 2:
        print("Keeping default setting. Proceeding to the next step...")

# Function for setting the filters parameters

def configure_filter():
    print("\nStaring filters...")
    print("Default settings:\nBinarization type: "
            + binary_type_name
            + "\nThreshold Value: "
            + str(threshold_value)
            + "\nAutomatic save all the intermediate files: "
            + str(save_flag))
    print("If you want to modify, press 1. To keep this setting and proceed,\
        press 2.")
    option = input()
    if option == 1:
        print("Still not implemented. Come back later")
    elif option == 2:
        print("Keeping default setting. Proceeding to the next step...")

# Function that detect the blue color on a given image.

def blue_detection(original_image, save_flag, lower_blue, upper_blue):
    lower = np.array(lower_blue, dtype="uint8")
    upper = np.array(upper_blue, dtype="uint8")
    mask = cv2.inRange(original_image, lower, upper)
    blue_region_image = cv2.bitwise_and(original_image, original_imagem,\
     mask=mask)
    if save_flag == True:
        cv2.imwrite('blue_region_image.png', blue_region_image)

    return blue_region_image

# Function that detect the red color on a given image.

def red_detection(original_image, save_flag, lower_red, upper_red):
    hsv_type_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    lower = np.array(lower_red)
    upper = np.array(upper_red)

    mask_0 = cv2.inRange(hsv_type_image, lower, upper)

    output_image = hsv_type_image.copy()
    output_image[np.where(mask_0 == 0)] = 0

    if save_flag == True:
        cv2.imwrite('red_region_image.png', output_image)

    return output_image

# Function that returns the first colored pixel found in the given image.
#
def find_colored_pixel(original_image):
    height, width = imagem.shape

    not_colored_pixels = [1, 1]
    not_colored_pixels[0] = -1
    not_colored_pixels[1] = -1
    first_colored_pixel = None

    for line in range(0, height):
        for column in range(0, width):
            if original_image[line][column] != 0:
                not_colored_pixels[0] = line
                not_colored_pixels[1] = column
                if(first_colored_pixel != None):
                    if line < first_colored_pixel[0]:
                        first_colored_pixel[0] = line
                    if column < first_colored_pixel[1]:
                        first_colored_pixel[1] = column
                else:
                    first_colored_pixel = not_colored_pixels
    return first_colored_pixel

# Main menu of the program as a function.

def main_menu():
    main_loop = True
    print("Starting the main code...")
    print("Camera settings menu.")
    configure_cam()
    print("Filter settings menu.")
    configure_filter()
    main_loop = False

# FUNCTIONS DISCONTINUED

def histogram(original_image):
    # ******************************
    # Histograma.
    plt.subplot(2, 1, 1), plt.imshow(original_image, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(2, 1, 2), plt.hist(imagem.ravel(), 256)
    plt.title('Histogram'), plt.xticks([]), plt.yticks([])
    plt.show()

# ******************************
# MAIN CODE
main_menu()
print("\nConfiguration section finished.")
print("Step 1 - Shoot the image.")
take_picture(quality, height, width, file_name, file_extension)
original_image = load_image(image_address)
print("Step 2 - Finding Blue, Red pixels")
blue_image = blue_detection(original_image, save_flag, lower_blue, upper_blue)
red_image = red_detection(original_image, save_flag, lower_red, upper_red)
blue_image_grey_scale = grey_scale_image(blue_image, save_flag)
red_image_grey_scale = grey_scale_image(red_image, save_flag)
blue_pixel = find_colored_pixel(blue_image_grey_scale)
red_pixel = find_colored_pixel(red_image_grey_scale)
print("Step 3 - Grey scale and binarization.")
grey_scale_image = grey_scale_image(original_image, save_flag)
binarized_image = binarzation(grey_scale_image, threshold_value,\
 binary_type, save_flag)

# continues...
