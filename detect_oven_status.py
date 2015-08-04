
import os
import argparse
import numpy as np
import cv2

def create_hue_mask(image, lower_color, upper_color):
    lower = np.array(lower_color, np.uint8)
    upper = np.array(upper_color, np.uint8)
 
    # Create a mask from the colors
    mask = cv2.inRange(image, lower, upper)
    output_image = cv2.bitwise_and(image, image, mask = mask)
    return output_image

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-i", "--image_path", dest = 'image_path', required = True)
    parser.add_argument("-o", "--output_dir", dest = 'output_dir', required = False)
    
    args = parser.parse_args()

    # Load image
    image = cv2.imread(args.image_path)

    # Blur image to make it easier to detect objects
    blur_image = cv2.medianBlur(image, 3)
    if args.output_dir:
        result_image_path = os.path.join(args.output_dir, "blur_image.jpg")
        cv2.imwrite(result_image_path, blur_image)

    # Convert to HSV in order to 
    hsv_image = cv2.cvtColor(blur_image, cv2.COLOR_BGR2HSV)
    if args.output_dir:
        result_image_path = os.path.join(args.output_dir, "hsv_image.jpg")
        cv2.imwrite(result_image_path, hsv_image)

    # Get lower red hue
    lower_red_hue = create_hue_mask(hsv_image, [0, 100, 100], [10, 255, 255])
    if args.output_dir:
        result_image_path = os.path.join(args.output_dir, "lower_red_hue.jpg")
        cv2.imwrite(result_image_path, lower_red_hue)

    # Get higher red hue
    higher_red_hue = create_hue_mask(hsv_image, [160, 100, 100], [179, 255, 255])    
    if args.output_dir:
        result_image_path = os.path.join(args.output_dir, "higher_red_hue.jpg")
        cv2.imwrite(result_image_path, higher_red_hue)

    # ...
    full_image = cv2.addWeighted(lower_red_hue, 1.0, higher_red_hue, 1.0, 0.0)
    if args.output_dir:
        result_image_path = os.path.join(args.output_dir, "full_image.jpg")
        cv2.imwrite(result_image_path, full_image)

    # Blur the final image to reduce noise from image
    full_image = cv2.GaussianBlur(full_image, (9, 9), 2, 2)
    if args.output_dir:
        result_image_path = os.path.join(args.output_dir, "full_image_blur.jpg")
        cv2.imwrite(result_image_path, full_image)

    # Convert image to gray in order to find circles in the image
    image_gray = cv2.cvtColor(full_image, cv2.COLOR_BGR2GRAY)
    if args.output_dir:
        result_image_path = os.path.join(args.output_dir, "full_image_gray.jpg")
        cv2.imwrite(result_image_path, image_gray)
    
    # Find circles in the image
    circles = cv2.HoughCircles(image_gray, 3, 1.2, 100)

    # If we didn't find circles, the oven status is "OFF"
    if circles is None:
        print "Oven is OFF"
        return

    # If we did find circles, the oven is "ON"
    print "Oven is ON"

    if args.output_dir:
        # Draw the circles on the original image
        circles = np.round(circles[0, :]).astype("int")
        for (center_x, center_y, radius) in circles:
            cv2.circle(image, (center_x, center_y), radius, (0, 255, 0), 4)
        result_image_path = os.path.join(args.output_dir, "original_image_with_circles.jpg")
        cv2.imwrite(result_image_path, image)

if __name__ == '__main__':
    main()
