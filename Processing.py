import numpy as np
import math
import cv2 as cv
from statistics import mean

def checkDangle(image):
    for row in image:
        if (row[0] == 0 or row[-1] == 0):
            return False;
    return True;

def modeWhite(image, strips, width):
    (h, w) = np.shape(image);
    value = 255;
    heights = [];
    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        tempH = 0;
        for j in range(h):
            if (image[j,l] == value):
                tempH += 1;
            elif (tempH != 0):
                heights.append(tempH);
                tempH = 0;

    if (heights != []):
        mode = max(set(heights), key=heights.count);
    else:
        mode = 0;
    return mode

def avgBlackH(image, strips, width):
    (h, w) = np.shape(image);
    value = 0;
    heights = [];

    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        tempH = 0;
        for j in range(h):
            if (image[j,l] == value):
                tempH += 1;
            elif (tempH != 0):
                heights.append(tempH);
                tempH = 0;

    if (heights != []):
        return mean(heights);
    else:
        return 0;

def avgWhiteH(image, strips, width):
    (h, w) = np.shape(image);
    value = 255;
    heights = [];

    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        tempH = 0;
        for j in range(h):
            if (image[j,l] == value):
                tempH += 1;
            elif (tempH != 0):
                heights.append(tempH);
                tempH = 0;

    if (heights != []):
        return mean(heights);
    else:
        return 0;

def lonelyStart(image, i, j):
    (h, w) = np.shape(image);
    count = -1;
    if (image[i,j] == 1):
        count = 0;
        if (i-1 > 0 and image[i-1, j] == 1 ):
            count+=1
        if (j+1 < w and image[i, j+1] == 1 ):
            count+=1
        if (i+1 < h and image[i+1, j] == 1 ):
            count+=1
        if (i-1 > 0 and j+1 < w and image[i-1, j+1] == 1 ):
            count+=1
        if (i+1 < h and j+1 < w and image[i+1, j+1] == 1 ):
            count+=1
    return count;

def lonelyEnd(image, i, j):
    (h, w) = np.shape(image);
    count = -1;
    if (image[i,j] == 1):
        count = 0;
        if (i-1 > 0 and image[i-1, j] == 1 ):
            count+=1
        if (j-1 > 0 and image[i, j-1] == 1 ):
            count+=1
        if (i+1 < h and image[i+1, j] == 1 ):
            count+=1
        if (i-1 > 0 and j-1 > 0 and image[i-1, j-1] == 1 ):
            count+=1
        if (i+1 < h and j-1 > 0 and image[i+1, j-1] == 1 ):
            count+=1
    return count;

def findLine(image, i, j, dist):
    (h, w) = np.shape(image);

    for y in range(dist):
        k = i-y if i-y > 0 else 0
        for x in range(j+1,w):
            if (lonelyEnd(image, k, x) == 0):
#                 print (str((i, j)) +  str((k, x)));
                cv.line(image, (j, i), (x, k), 1, 1, cv.LINE_AA)
                return image;
        k = i+y if i+y < h else h-1
        for x in range(j+1, w):
            if (lonelyEnd(image, k, x) == 0):
#                 print (str((i, j)) +  str((k, x)));
                cv.line(image, (j, i), (x, k), 1, 1, cv.LINE_AA)
                return image;
    if (j > w/2):
        cv.line(image, (w, i), (j, i), 1, 1, cv.LINE_AA)
    return image;
