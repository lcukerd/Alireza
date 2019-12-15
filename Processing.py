import numpy as np
import math
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

def lonely(image, i, j):
    count = 0;
    if (image[i,j] == 255):
        if (image[i-1, j] == 255 ):
            count+=1
        if (image[i-1, j-1] == 255 ):
            count+=1
        if (image[i-1, j+1] == 255 ):
            count+=1
        if (image[i, j+1] == 255 ):
            count+=1
        if (image[i, j-1] == 255 ):
            count+=1
        if (image[i+1, j] == 255 ):
            count+=1
        if (image[i+1, j-1] == 255 ):
            count+=1
        if (image[i+1, j+1] == 255 ):
            count+=1
    return count;

def findLine(image, i, j, dist):
    (h, w) = np.shape(image);

    for y in range(dist):
        k = i-y if i-y > 0 else 0
        for x in range(w):
            if (lonely(image, k, x) == 1):
                cv.line(image, (i,j), (k, x), (0,0,255), 3, cv.LINE_AA)
                return image;
        k = i+y if i+y < h else h
        for x in range(w):
            if (lonely(image, k, x) == 1):
                cv.line(image, (i,j), (k, x), (0,0,255), 3, cv.LINE_AA)
                return image;
    other = findEnd(image, i, j);
    ends = [j, other[1]];
    ends.sort()
    if (ends[0] < w/2 and ends[1] > w/2):
        if (ends[0] == j):
            cv.line(image, (i,0), (i, j), (0,0,255), 3, cv.LINE_AA)
            cv.line(image, (other[0],w), (other[0], other[1]), (0,0,255), 3, cv.LINE_AA)
        else:
            cv.line(image, (i,w), (i, j), (0,0,255), 3, cv.LINE_AA)
            cv.line(image, (other[0],0), (other[0], other[1]), (0,0,255), 3, cv.LINE_AA)
        return image;
    return image;
