#!/usr/bin/env python#
#import rospy
#from std_msgs.msg import Int32MultiArray
#import time
import cv2
import numpy as np

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def canny(img, low_threshold, high_threshold):
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):

    mask = np.zeros_like(img)

    if len(img.shape) > 2:
        color = color3
    else:
        color = color1

    cv2.fillPoly(mask, vertices, color)

    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image


avg = 0
def find_contour(img):
    global avg
    a=[]
    contours, hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        cv2.drawContours(img,[cnt],-1,(255,0,0),3)
        for i in range (0,len(cnt),1):
            a.append(cnt[i][0][0])
            sum = 0
            for j in a:
                sum += j
            avg = sum/len(a)
    return avg


def Decide_Angle(img,cnt):
    global angle
    height, width = img.shape[:2]
    if cnt < width/2:
        angle = -50
    else:
        angle = 50
    return angle



cap = cv2.VideoCapture('C:\\Users\\erick\\OneDrive\\Documents\\track-s.mkv')
while (cap.isOpened()):
    ret, image = cap.read()

    if type(image) == type(None):
        break

    height, width = image.shape[:2]

    gray_img = grayscale(image)

    blur_img = gaussian_blur(gray_img, 3)

    canny_img = canny(blur_img, 70, 210)

    vertices = np.array(
        [[(100, height), (width / 2 - 100, height - 50), (width / 2 + 100, height - 50), (width - 100, height)]],
        dtype=np.int32)
    ROI_img = region_of_interest(canny_img, vertices)
    print(find_contour(ROI_img))
    print(Decide_Angle(ROI_img,find_contour(ROI_img)))
    cv2.imshow('result',ROI_img)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

# Releasecd
cap.release()
cv2.destroyAllWindows()
