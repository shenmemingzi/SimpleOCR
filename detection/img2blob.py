import os
import cv2
import numpy as np

def ResizeImage(img):
    """
    Resize image to HMAX = 600 and WMAX = 2000.

    Input: image data
    Output : image data
    """

    img_shape = img.shape
    img_min = np.min(img_shape[0 : 2])
    img_max = np.max(img_shape[0 : 2])
    img_scale = np.array([600, 2000]) / np.array([img_min, img_max])
    img_scale = np.min(img_scale)

    img = cv2.resize(img, None, fx=img_scale, fy=img_scale)
    return img, img_scale

def GroundTruthtoTupleList(filename):
    """
    Read an img file and its txt file and 
    turn each ground truth to tuple (x, y, h, w, theta).
        (x, y) : geometric center of the bounding box
        h : short side of the bounding box
        w : long side of the bounding box
        theta : [-pi / 4, 3 * pi / 4)

    Input : filename

    Output : img from cv.imread, 
             list of tuples
    """

    filename_img = "image_1000/" + filename
    filename_txt = "txt_1000/" + filename.split(".jpg")[0] + ".txt"
    img = cv2.imread(filename_img)
    l = list()

    with open(filename_txt, 'r') as f:
        data = f.readlines()
        for line in data :
            position = line.split(",")[0 : 8]
            position = [int(float(position[i])) for i in range(8)]
            X = [position[0], position[2], position[4], position[6]]
            Y = [position[1], position[3], position[5], position[7]]

            cnt = np.array([[X[0], Y[0]], [X[1], Y[1]], [X[2], Y[2]], [X[3], Y[3]]])
            [[X_center, Y_center], [h, w], angle] = cv2.minAreaRect(cnt)

            if h > w :
                h, w = w, h
                angle += 90

            if angle < -45.0 :
                angle += 180

            t = (X_center, Y_center, h, w, angle)
            l.append(t)
    return img, l

def GetBlobs(filename):
    """
    Given a filename and return blobs of the file.
    'Blobs' is a dict contains imagedata, groundtruth and imageinfo.

    Input : filename

    Output : blobs
    """

    img, l = GroundTruthtoTupleList(filename)
    img, s = ResizeImage(img)
    blobs = {'data': img, 'gt_list': l, 'im_info': np.array([img.shape[0], img.shape[1], s])}
    # NOTE : The list of groundtruth box is using the origion data.
    return blobs

if __name__ == "__main__":
    for filename in os.listdir('image_1000/'):
        blobs = GetBlobs(filename)
        print(blobs)
        cv2.imshow('img', blobs['data'])
        cv2.waitKey(0)
