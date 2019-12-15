import cv2 as cv
import numpy as np
import math
from statistics import mean

from matplotlib import pyplot as plt
from Processing import *

def findComponents(image):
    edgyImg = cv.Canny(image, 50, 200, None, 3)
    edgyColor = cv.cvtColor(edgyImg, cv.COLOR_GRAY2BGR)

    DemoImg = np.zeros_like(edgyColor);

    num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(edgyImg);
    avg_width = 0;
    for stat in stats:
        avg_width += stat[cv.CC_STAT_WIDTH]
    avg_width /= num_labels
    print ("Found " + str(num_labels) + " components with height " + str(avg_width) + " in image")

    # if centroids is not None:
    #     for centroid in centroids:
    #         DemoImg[int(centroid[1]), int(centroid[0])] = [255,255,255]
    #
    # plt.imshow(DemoImg)
    # plt.show()

    return avg_width;

def putGLM(image, width):
    (h, w) = np.shape(image);
    strips = int (w/width);
    if (w % width != 0):
        strips += 1;
    for i in range(strips):
        for j in range(h):
            avg_gray = 0;
            strip_width = ((i+1) * width if (((i+1) * width) < w) else w) - i*width + 1;

            for k in range(i*width, (i+1) * width if (((i+1) * width) < w) else w):
                avg_gray = image[j,k];

            avg_gray = int (avg_gray / strip_width);

            for k in range(i*width, (i+1) * width if (((i+1) * width) < w) else w):
                image[j,k] = avg_gray;
    return image, strips;

def filterWhite(image, strips, width):
    (h, w) = np.shape(image);
    value = 255;

    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        heights = [];
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
            continue;

        start = -1;
        for j in range(h):
            if (image[j,l] == value):
                if (start == -1):
                    start = j;
                tempH += 1;
            elif (tempH != 0):
                if (tempH < mode):
                    image[start:j,l:r] = np.ones((j-start, r-l)) * 0;
                tempH = 0;
                start = -1;
    return image;

def filterBlack(image, strips, width):
    (h, w) = np.shape(image);
    value = 0;

    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        heights = [];
        tempH = 0;
        for j in range(h):
            if (image[j,l] == value):
                tempH += 1;
            elif (tempH != 0):
                heights.append(tempH);
                tempH = 0;

        if (heights != []):
            m = int (mean([heights[i] for i in range(len(heights)) if i%8 ==0]))
        else:
            continue;

        start = -1;
        for j in range(h):
            if (image[j,l] == value):
                if (start == -1):
                    start = j;
                tempH += 1;
            elif (tempH != 0):
                if ((tempH < m) or (tempH < 3*m and checkDangle(image[start:j,l-1 if l!= 0 else 0:r+1 if r!=w else w]))):
                    image[start:j,l:r] = np.ones((j-start, r-l)) * 255;
                tempH = 0;
                start = -1;
    return image;

def removeBlack(image, strips, width):
    (h, w) = np.shape(image);
    value = 0;

    height = avgBlackH(np.copy(image), strips, width);

    for i in range(strips):
        l = i * width;
        r = (i+1) * width if (((i+1) * width) < w) else w;
        tempH = 0;

        start = -1;
        for j in range(h):
            if (image[j,l] == value):
                if (start == -1):
                    start = j;
                tempH += 1;
            elif (tempH != 0):
                if (tempH >= 2 * height):
                    image[start:j,l:r] = np.ones((j-start, r-l)) * 255;
                tempH = 0;
                start = -1;
    return image;

def constructLines(image, strips, width, height):
    (h, w) = np.shape(image);
    dist = int (height);

    for i in range(1,h-1):
        for j in range(1,w-1):
            if lonelyStart(image, i, j) == 0:
                image = findLine(image, i, j, dist);
            elif lonelyEnd(image, i, j) == 0 and j < w/2:
                cv.line(image, (0, i), (j, i), 1, 1, cv.LINE_AA)
    plt.imshow(image);
    return image;
