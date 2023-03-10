from PIL import Image
import copy
import numpy as np
from matplotlib import pyplot as plt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def dilate(image, kernel_size):
    output = copy.deepcopy(image)
    margin = kernel_size // 2
    rows = image.shape[0]
    columns = image.shape[1]
    
    for row in range(margin, rows-margin):
        for col in range(margin, columns-margin):
            temp_R = []
            temp_G = []
            temp_B = []
            for i in range(row-margin, row+margin+1):
                for j in range(col-margin, col+margin+1):
                    temp_R += [image[i][j][0]]
                    temp_G += [image[i][j][1]]
                    temp_B += [image[i][j][2]]
            temp_R_np = np.array(temp_R)
            temp_G_np = np.array(temp_G)
            temp_B_np = np.array(temp_B)
            output[row][col][0], output[row][col][1], output[row][col][2] = np.max(temp_R_np), np.max(temp_G_np), np.max(temp_B_np)
    
    return output


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def erode(image, kernel_size):
    output = copy.deepcopy(image)
    margin = kernel_size // 2
    rows = image.shape[0]
    columns = image.shape[1]
    
    for row in range(margin, rows-margin):
        for col in range(margin, columns-margin):
            temp_R = []
            temp_G = []
            temp_B = []
            for i in range(row-margin, row+margin+1):
                for j in range(col-margin, col+margin+1):
                    temp_R += [image[i][j][0]]
                    temp_G += [image[i][j][1]]
                    temp_B += [image[i][j][2]]
            temp_R_np = np.array(temp_R)
            temp_G_np = np.array(temp_G)
            temp_B_np = np.array(temp_B)
            output[row][col][0], output[row][col][1], output[row][col][2] = np.min(temp_R_np), np.min(temp_G_np), np.min(temp_B_np)
    
    return output

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def open(image, kernel_size):
    img_copy = copy.deepcopy(image)
    img_eroded = erode(img_copy, kernel_size)
    return dilate(img_eroded, kernel_size)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def close(image, kernel_size):
    img_copy = copy.deepcopy(image)
    img_dilated = dilate(img_copy, kernel_size)
    return erode(img_dilated, kernel_size)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

image = np.array(Image.open('Suez Canal.png'), dtype='int64')

output_3_1_1 = image + (image - open(image, 3)) - (close(image, 3) - image)
output_9_1_1 = image + (image - open(image, 9)) - (close(image, 9) - image)
output_3_5_1 = image + (5*(image - open(image, 3))) - (close(image, 3) - image)
output_3_1_5 = image + (image - open(image, 3)) - (5*(close(image, 3) - image))

plt.subplots(nrows=2, ncols=2, figsize=(20, 20))

plt.subplot(2,2,1)
plt.imshow(output_3_1_1)
plt.title("3x3 a=1 b=1")

plt.subplot(2,2,2)
plt.imshow(output_9_1_1)
plt.title("9x9 a=1 b=1")

plt.subplot(2,2,3)
plt.imshow(output_3_5_1)
plt.title("3x3 a=5 b=1")

plt.subplot(2,2,4)
plt.imshow(output_3_1_5)
plt.title("3x3 a=1 b=5")

plt.show()