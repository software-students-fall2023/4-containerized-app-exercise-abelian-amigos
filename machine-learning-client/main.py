from model import Model
import cv2

model = Model()

image = cv2.imread('a.jpg')
output = model.run(image)
cv2.imwrite('output.jpg', output)