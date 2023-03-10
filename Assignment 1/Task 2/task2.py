import copy
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# reading an image

image = plt.imread('GUC.jpg')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ideal filter function

def ideal(distance, cutoff_distance):
    return 1 if distance <= cutoff_distance else 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# butterworth filter function

def butterworth(order, distance, cutoff_distance):
    power = 2*order
    return (1/(1+((distance/cutoff_distance)**power)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# gaussian filter function

def gaussian(distance, cutoff_distance):
    numerator = (-1) * (distance**2)
    denominator = (2) * (cutoff_distance**2)
    return np.exp((numerator/denominator))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# low-pass filter function

def low_pass(image, type, order, cutoff_distance):
    img = copy.deepcopy(image)
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    m = fshift.shape[0]
    n = fshift.shape[1]

    for u in range(0, m):
        for v in range(0, n):
            distance = np.sqrt(np.square(u-(m/2)) + np.square(v-(n/2)))
            if type == "ideal":
                fshift[u][v] *= ideal(distance, cutoff_distance)
            elif type == "butterworth":
                fshift[u][v] *= butterworth(order, distance, cutoff_distance)
            else:
                fshift[u][v] *= gaussian(distance, cutoff_distance)
    
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    return img_back.real

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

output1 = low_pass(image, "ideal", 1, 5)
output2 = low_pass(image, "ideal", 1, 30)
output3 = low_pass(image, "ideal", 1, 50)

output4 = low_pass(image, "butterworth", 1, 5)
output5 = low_pass(image, "butterworth", 1, 30)
output6 = low_pass(image, "butterworth", 1, 50)

output7 = low_pass(image, "gaussian", 1, 5)
output8 = low_pass(image, "gaussian", 1, 30)
output9 = low_pass(image, "gaussian", 1, 50)

Image.fromarray(output1.astype('uint8')).save("GUC_ILPF_5.jpg")
Image.fromarray(output2.astype('uint8')).save("GUC_ILPF_30.jpg")
Image.fromarray(output3.astype('uint8')).save("GUC_ILPF_50.jpg")

Image.fromarray(output4.astype('uint8')).save("GUC_BLPF_5.jpg")
Image.fromarray(output5.astype('uint8')).save("GUC_BLPF_30.jpg")
Image.fromarray(output6.astype('uint8')).save("GUC_BLPF_50.jpg")

Image.fromarray(output7.astype('uint8')).save("GUC_GLPF_5.jpg")
Image.fromarray(output8.astype('uint8')).save("GUC_GLPF_30.jpg")
Image.fromarray(output9.astype('uint8')).save("GUC_GLPF_50.jpg")
