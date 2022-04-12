from pdf2image import convert_from_path
import numpy as np
import cv2
import math
import skimage.exposure
import os

pi = math.pi


# Defining coordinates for circle at center (center_x, center_y) and radius r
# and checking if the circle points fall on the real circle in the pdf
def check_circle(gray, r, center_x, center_y, n=100):
    points = [(int(math.cos(2 * pi / n * x) * r), int(math.sin(2 * pi / n * x) * r)) for x in range(0, n + 1)]
    # counting how many black points are on the circle
    black_counter = 0
    for check in points:
        # check each point on circumference, if intensity on grayscale is less than 10 (out of 255)
        # then its considered black
        if gray[check[1] + center_y][check[0] + center_x] < 10:
            black_counter += 1
        pass
    return black_counter


# Perform a gaussian blur so circles are more of smudges
# motivation is that right now real circles center is not the same as detected
# circle centers so need to make the circle transition more so that the black
# point counter catches the points
def blur_image(img):
    blur = cv2.GaussianBlur(img, (0, 0), sigmaX=1, sigmaY=1, borderType=cv2.BORDER_DEFAULT)
    result = skimage.exposure.rescale_intensity(blur, in_range=(253, 255), out_range=(0, 255))
    return result
    # save output
    # cv2.imwrite('bw_image_antialiased.png', result)

    # Display various images to see the steps
    # result = cv2.resize(result, (1920, 1200))  # Resize image
    # cv2.imshow('result', result)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


# detection of circle centers and radius using HoughCircles method in OpenCV module
def circles_centers(path, page_num, pop_path):
    centers_x = []
    centers_y = []
    # Optimized parameters for HoughCircles method
    dp_var = 1.005
    min_distance_var = 8

    # Read page
    pages = convert_from_path(path,
                              poppler_path=pop_path)
    # Get current page and turn it into jpeg (as openCV can't read pdf's)
    page = pages[page_num]
    page.save("page_image.jpg", format="jpeg")
    sheet_height = page.size[1]

    # Defining different HoughCircles parameters for different sheet sizes
    if sheet_height > 3000:  # Big sheets like A2
        param1_var = 50
        param2_var = 20
        min_radius_var = 36
        max_radius_var = 41
    else:  # Smaller sheets
        param1_var = 10
        param2_var = 20
        # Optimizing circles radius window according to experimentation
        radius_coef = (page.size[0] ** 2 + int(page.size[1]) ** 2) ** 0.5
        min_radius_var = round(radius_coef / 136)-1
        max_radius_var = min_radius_var + 12

    filename = "page_image.jpg"
    # Load the image
    src = cv2.imread(cv2.samples.findFile(filename), cv2.IMREAD_COLOR)

    # Check if the image is loaded fine
    if src is None:
        print('Error opening image!')
        print('Usage: hough_circle.py [image_name -- default ' + filename + '] \n')

    # Turn to grayscale
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # Perform blur
    gray = cv2.medianBlur(gray, 5)

    # HoughCircles method - detect circles according to previous defined parameters
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=dp_var, minDist=min_distance_var,
                               param1=param1_var, param2=param2_var,
                               minRadius=min_radius_var, maxRadius=max_radius_var)
    # Further blur the image
    blurred = blur_image(gray)
    # If circles were detected
    if circles is not None:
        # Convert circles to uint16
        circles = np.uint16(np.around(circles))
        # Go through every circle
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            # Check how many points of the circle are black (out of n points)
            circle_complete_index = check_circle(blurred, radius, center[0], center[1], n=50)
            # 35 points out of n points (currently 70% of circle
            # must have black points to be considered a real circle)
            if circle_complete_index > 35:
                # Draw circle center
                cv2.circle(src, center, 1, (0, 100, 100), 3)
                # Draw circle outline
                cv2.circle(src, center, radius, (255, 0, 255), 3)
                # Add center to a list of real centers
                centers_x.append(int(i[0]) / page.size[0])
                centers_y.append(1 - int(i[1]) / page.size[1])

    ## Show image
    # im_s = cv2.resize(src, (1920, 1200))  # Resize image
    # cv2.imshow("detected circles", im_s)
    #
    # # Wait for a key press
    # cv2.waitKey(0)
    # #
    # # Remove image
    os.remove("page_image.jpg")

    return [centers_x, centers_y]