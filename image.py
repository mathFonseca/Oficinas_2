#!/usr/bin/python
#-*- coding: utf-8 -*-

# IMPORTS

import numpy as np  # Numeric Operations Library
import cv2  # Open CV v2 for images Operations
import os   # Operational System Library.
import commands  # For utilizing terminal commands inside here

# IMPORTS DISCONTINUED

import argparse
from matplotlib import pyplot as plt

# DEFINES AND GLOBAL VARIABLES
image_address = 'first_maze.jpeg'  # Address for acessing the image that
# will be used in the application

# In OpenCV, it utilizes the following order: Blue Green Redself.
# It stills RGB, but in the reverse order.

lower_blue = [50, 0, 0]    # Lower parameters for acceptable blue color
upper_blue = [255, 10, 125]    # Upper parameters for acceptable blue color
lower_red = [0, 50, 50]  # Lower parameters for acceptable red color
upper_red = [10, 255, 255]  # Upper parameters for acceptable red color

# Default settings for the Raspberry Camera.
quality = 30    # 30% of the original pictura quality
height = 600
width = 800
file_name = "img"    # The name of the file after the picture shoot.
file_extension = "png"    # The extension of the picture saved.

# Default setting for the binarization and grey scale functions

binary_type = 1
binary_type_name = "Otsu's Binarization"

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
        ret, binary_image = cv2.threshold(grey_scale_image,
                                          threshold_value, 255, cv2.THRESH_BINARY)
        if save_flag == True:
            cv2.imwrite('simple_binarization.png', binary_image)
    elif binary_type == 1:
        ret, binary_image = cv2.threshold(grey_scale_image, 0, 255,
                                          cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if save_flag == True:
            cv2.imwrite('otsu_binarization.png', binary_image)
    elif binary_type == 2:
        binary_image = cv2.adaptiveThreshold(grey_scale_image, 255,
                                             cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        if save_flag == True:
            cv2.imwrite('adaptative_binarzation_mean.png', binary_image)
    elif binary_type == 3:
        binary_image = cv2.adaptiveThreshold(grey_scale_image, 255,
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
    print("If you want to modify, press 1. \n\
To keep this setting and proceed, press 2.")
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
    print("If you want to modify, press 1.\n\
To keep this setting and proceed,\
    press 2.")
    option = input()
    if option == 1:
        print("Still not implemented. Come back later")
    elif option == 2:
        print("Keeping default setting. Proceeding to the next step...")

# Function that detect the blue color on a given image.


def blue_detection(original_image, save_flag, lower_blue, upper_blue):
    hsv_type_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    lower = np.array(lower_blue)
    upper = np.array(upper_blue)

    mask_0 = cv2.inRange(original_image, lower, upper)

    output_image = hsv_type_image.copy()
    output_image[np.where(mask_0 == 0)] = 0

    if save_flag == True:
        cv2.imwrite('blue_region_image.png', output_image)

    return output_image

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


def find_colored_pixel(original_image):
    height, width = original_image.shape

    not_colored_pixels = np.array([-1,-1])
    first_colored_pixel = None

    for line in range(0, height):
        for column in range(0, width):
            if original_image[line][column] != 0:
                not_colored_pixels = (line, column)
                if(first_colored_pixel != None):
                    if line < first_colored_pixel[0]:
                        first_colored_pixel[0] = line
                    if column < first_colored_pixel[1]:
                        first_colored_pixel[1] = column
                else:
                    first_colored_pixel = not_colored_pixels
    return first_colored_pixel

# Function that returns the center coordinate of a 3x3 colored pixel grid

def coordinatePixel(original_image):
    height, width = original_image.shape
    colored_pixel = np.array([-1,-1])
    holder_pixel = np.array([-1,-1])
    possible_holder_pixel = np.array([-1,-1])

    for line in range(0, height):
        for column in range(0, width):
            if original_image[line][column] != 0:
                '''
                Checks if the given position the COLOR of the pixel is or isn't black.
                if YES, then proceeds to next step
                if NOT, rolls over to the next pixel.
                '''
                if ((holder_pixel[0] != -1) and (holder_pixel[1] != -1)):
                    '''
                    Checks if we already found out a holder_pixel.
                    if YES, checks if this holder pixel holds a 3x3 grid with it.
                    if NOT, what we found may be a holder pixel.
                    Set the possible_holder_pixel variable then proceeds to find out a 3x3 grid
                    '''
                    if((line < holder_pixel[0]) and (column < holder_pixel[1])):
                        '''
                        First, we check if this pixel we are in (image[line][column]) are more
                        further to [0,0] than the holder pixel we found sometime earlier.
                        if YES, than we set the position we are in as a possible_holder_pixel
                        And runs the grid finder.
                        If the grid finder returns TRUE, we found out a new acceptable holder pixel
                        if not, we stick with the old one.
                        '''
                        possible_holder_pixel = (line, column)
                        if(findsGrid(original_image, possible_holder_pixel)):
                            holder_pixel = possible_holder_pixel
                else:
                    '''
                    This is the first holder pixel we found.
                    Set possible_holder_pixel and then runs the 3x3 grid finder.
                    '''
                    possible_holder_pixel = (line, column)
                    '''
                    If findsGrid returns TRUE, the possible_holder_pixel was actually
                    and true holder pixel. Set the holder pixel and proceeds
                    '''
                    if(findsGrid(original_image, possible_holder_pixel)):
                        holder_pixel = possible_holder_pixel

    '''
    if, after running through all the image, the holder_pixel
    still with his original value (-1, -1), we did not succeed to find out the 3x3 grid
    Try to run the 1 pixel function instead.
    '''
    if( (holder_pixel[0] == -1) and (holder_pixel[1] == -1) ):
        return False
    else:
        '''
        If we did find out a trully holder pixel, then returns the CENTER of the 3x3 grid
        Walking 1 pixel LEFT and 1 pixel DOWN.
        '''
        holder_pixel = (holder_pixel[0] + 1, holder_pixel[1] + 1)
        return holder_pixel


# Function that checks if exits a 3x3 grid <expanded downwards> not blank_grid

def findsGrid(original_image, holder_pixel):
    '''
    Creates a flag called invalid_grid, that begins with False.
    We create the range for the FOR with a space of 2. Beggining at self and walking 2 pixels
    at X (LINE) and Y (COLUMN).
    If we find out at this run some pixel that are BLACK (not colored), we set the invalid_grid to False.
    If not, we walked through a 3x3 grid, starting from the holder pixel, going LEFT and DOWNWARDS
    and we not found any black pixel. With means that are a fully 3x3 COLORED GRID.
    We then set the invalid_grid to TRUE.
    '''
    invalid_grid = False
    holder_line = holder_pixel[0]
    holder_column = holder_pixel[1]
    for line in range(holder_line, holder_line + 2):
        for column in range(holder_column, holder_column + 2):
            if( (original_image[holder_line][holder_column] != 0) and (invalid_grid == False) ):
                invalid_grid = False
            else:
                invalid_grid = True

    '''
    if invalid_grid is TRUE, return TRUE. If not, do not.
    '''
    if invalid_grid != True:
        return False
    else:
        return True


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
#main_menu()
print("\nConfiguration section finished.")
print("Step 1 - Shoot the image.")
take_picture(quality, height, width, file_name, file_extension)
original_image = load_image(image_address)

print("Step 2 - Finding Blue, Red pixels")
blue_image = blue_detection(original_image, save_flag, lower_blue, upper_blue)
red_image = red_detection(original_image, save_flag, lower_red, upper_red)

blue_image_grey_scale = apply_grey_scale(blue_image, save_flag)
red_image_grey_scale = apply_grey_scale(red_image, save_flag)

blue_result = coordinatePixel(blue_image_grey_scale)
if(blue_result == False):
    print("We did not succeed to find a 3x3 grid on a blue spot.\n \
Running the function that returns the 1 pixel instead.")
    blue_pixel = find_colored_pixel(blue_image_grey_scale)
else:
    print("We did it! We find out a 3x3 grid. yay!")
    blue_pixel = blue_result

red_result = coordinatePixel(red_image_grey_scale)
if(red_result == False):
    print("We did not succeed to find a 3x3 grid on a red spot.\n \
Running the function that returns the 1 pixel instead.")
    red_pixel = find_colored_pixel(red_image_grey_scale)
else:
    print("We did it! We find out a 3x3 grid on a RED spot . yay!")
    red_pixel = red_result

print("Blue Pixel Found at: ")
print(blue_pixel)
print("Red Pixel Found at: ")
print(red_pixel)

print("Step 3 - Grey scale and binarization.")
grey_scale_image = apply_grey_scale(original_image, save_flag)
binarized_image = binarization(grey_scale_image, threshold_value,
                               binary_type, save_flag)


# continues...
