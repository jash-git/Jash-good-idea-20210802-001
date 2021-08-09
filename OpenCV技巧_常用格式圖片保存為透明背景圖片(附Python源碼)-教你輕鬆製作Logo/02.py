import cv2
import numpy as np

img = cv2.imread("flower.jpg")
cv2.imshow('src', img)
print(img.shape)

result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

B,G,R = cv2.split(img)

_, Alpha= cv2.threshold(R, 200, 255, cv2.THRESH_BINARY)
cv2.imshow('thres', Alpha)

B2,G2,R2,A2 = cv2.split(result)
A2 = Alpha
result = cv2.merge([B2,G2,R2,A2]) #通道合并

cv2.imwrite('result.png', result)
print(result.shape)
cv2.imshow('result', result)
B,G,R,A = cv2.split(result)
cv2.imshow('B', B)
cv2.imshow('G', G)
cv2.imshow('R', R)
cv2.imshow('A', A)
 
cv2.waitKey()
cv2.destroyAllWindows()