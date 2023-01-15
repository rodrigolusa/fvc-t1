import cv2
import numpy as np
 
# Read source image.
im_src = cv2.imread('img/foto1_cap1.jpg')

# Four corners of source image
# TODO: Find the four courners automatically
pts_src = np.array([[837, 1065], [2645, 669],[2837, 2461], [797, 2465]])

# Four corners of destination image
#TODO: Determinate the result size automatically
pts_dst = np.array([[0, 0],[2048, 0],[2048, 1536],[0, 1536]])

# Calculate Homography
h, status = cv2.findHomography(pts_src, pts_dst)

# Warp source image to destination based on homography
im_out = cv2.warpPerspective(im_src, h, (3024,4032))

# Save cropped image result
cv2.imwrite('output.jpg', im_out[0:1536, 0:2048])