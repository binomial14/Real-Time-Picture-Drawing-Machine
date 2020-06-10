"""
Performs Deep Learning based Edge Detection using HED (Holistically Nested Edge Detection)

HED uses Trimmed VGG-like CNN (for image to prediction)

Author: krshrimali
Motivation: https://cv-tricks.com/opencv-dnn/edge-detection-hed/ (by Ankit Sachan)
"""

import cv2
from PIL import Image,ImageEnhance
import numpy as np
from utils.preprocessing import CannyP
from utils.preprocessing import CropLayer

import sys
import os

if __name__ == "__main__":
    # get image path
    if(len(sys.argv) != 3):
        print("ERROR: invalid number of arguments")
        print("usage: python main.py <input_image_path> <convert_image_path>")
        exit(1)

    src_path = sys.argv[1]
    out_path = sys.argv[2]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # read image
    img = cv2.imread(src_path, 1)
    if(img is None):
        print("Image not read properly")
        sys.exit(0)

    # initialize preprocessing object
    obj = CannyP(img)
    
    width = 500
    height = 500
    
    # remove noise
    img = obj.noise_removal(filterSize=(5, 5))
    prototxt = "./deploy.prototxt"
    caffemodel = "./hed_pretrained_bsds.caffemodel"

    cv2.dnn_registerLayer('Crop', CropLayer)
    net = cv2.dnn.readNet(prototxt, caffemodel)

    inp = cv2.dnn.blobFromImage(img, scalefactor=1.0, size=(width, height), \
            mean=(104.00698793, 116.66876762, 122.67891434), \
            swapRB=False, crop=False)

    net.setInput(inp)
    out = net.forward()
    out = out[0, 0]
    out = cv2.resize(out, (img.shape[1], img.shape[0]))
    out = 255 * out
    out = out.astype(np.uint8)
    out=cv2.cvtColor(out,cv2.COLOR_GRAY2BGR)
    out_r = cv2.bitwise_not(out)
    out_r = out_r.astype(np.uint8)
    #out = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    # con = np.concatenate((img, out), axis=1)
    #cv.imshow("HED", out)
    #cv.imshow("original", img)
    #cv2.imwrite('output/hed.png',out)
    #cv2.imwrite('output/hed_invert.png',out_r)
    #cv2.imwrite('output/origin.png',img)

    cv2_im = cv2.cvtColor(out_r,cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im)
    enh_con = ImageEnhance.Sharpness(pil_im)
    sharpness = 10
    out_r = enh_con.enhance(sharpness)
    enh_con = ImageEnhance.Brightness(pil_im)
    brightness = 1
    out_r = enh_con.enhance(brightness)
    out_r = cv2.cvtColor(np.asarray(out_r),cv2.COLOR_RGB2BGR)

    blur = cv2.GaussianBlur(out_r,(5,3), 1)
    mask=cv2.inRange(blur,(0,0,0),(150,150,150))
    res = 255 - mask
    convert = cv2.medianBlur(res,3)
    cv2.imwrite(out_path,convert)

'''
    import matplotlib.pyplot as plt
    fig,axes = plt.subplots(2,2,figsize=(15,15))
    axes[0,0].set_title('Original')
    axes[0,1].set_title('HED')
    axes[1,0].set_title('HED invert')
    axes[1,1].set_title('Add GaussianBlur')
    axes[0,0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[0,1].imshow(out,plt.cm.gray)
    axes[1,0].imshow(out_r,plt.cm.gray)
    axes[1,1].imshow(convert,plt.cm.gray)
    plt.tight_layout()
    plt.savefig('output/compare.png')
'''
