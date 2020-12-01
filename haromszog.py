# https://www.geeksforgeeks.org/find-co-ordinates-of-contours-using-opencv-python/
# https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
# https://www.nkp.hu/tankonyv/matematika_11/lecke_04_068

import numpy as np
import cv2

# Reading image
font = cv2.QT_FONT_NORMAL
img2 = cv2.imread('test.jpg', cv2.IMREAD_COLOR)

# Reading same image in another variable and converting to gray scale.
img = cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)

# Converting image to a binary image ( black and white only image).
_, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)

# Detecting contours in image.
_, contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Going through every contours found in the image.
for cnt in contours:

    M = cv2.moments(cnt)
    if (M["m00"] == 0):
        M["m00"] = 1
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # draw the contour and center of the shape on the image
    cv2.drawContours(img2, [cnt], -1, (0, 255, 0), 2)

    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)

    # draws boundary of contours.
    cv2.drawContours(img2, [approx], 0, (0, 0, 255), 5)

    # Used to flatted the array containing the co-ordinates of the vertices.
    n = approx.ravel()
    i = 0
    points = []

    for j in n:
        if i < 3:
            # Calculating the angle from the vector co-ordinates.
            v1x = n[0 + i] - n[2 + i]
            v2x = n[4 + i] - n[2 + i]
            v1y = n[1 + i] - n[3 + i]
            v2y = n[5 + i] - n[3 + i]
            v1v2 = (v1x * v2x) + (v1y * v2y)
            abs_v1v2 = np.sqrt(np.square(v1x) + np.square(v1y)) * np.sqrt(np.square(v2x) + np.square(v2y))
            cos_alpha = v1v2/abs_v1v2
            angle = np.degrees(np.arccos(cos_alpha))
            rounded_angle = str(np.round(angle, 2))
        if (i % 2 == 0):
            x = n[i]
            y = n[i + 1]
            cv2.putText(img2, rounded_angle, (x, y), font, 0.5, (0, 255, 0))
        i = i + 1
    cv2.putText(img2, str(i//2), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Showing the final image.
cv2.imshow('image2', img2)
# Exiting the window if 'q' is pressed on the keyboard.
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()