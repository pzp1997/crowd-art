import cv2

infile = 'horse_orig.jpg'
outfile = 'horse_canny.jpg'

image = cv2.imread(infile)
image_edges = cv2.Canny(image, 100, 200)
cv2.imwrite(outfile, image_edges)
