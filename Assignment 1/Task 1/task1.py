from PIL import Image
import cv2
import copy
import numpy as np

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# distance transform function
def distance_transform(image, distance_measure, representative_points):
    first_pass = np.ones((image.shape[0],image.shape[1])) * np.inf
    for i in range(0, len(representative_points)):
        first_pass[representative_points[i][0]][representative_points[i][1]] = 0
    
    # first pass
    for row in range(1, image.shape[0]-1):
        for column in range(1, image.shape[1]):
            distances = []
            current = first_pass[row][column]
            top = 1 + first_pass[row-1][column]
            top_left = (np.sqrt(2) if distance_measure == "euclidean" else 2 if distance_measure == "city" else 1) + first_pass[row-1][column-1]
            left = 1 + first_pass[row][column-1]
            bottom_left = (np.sqrt(2) if distance_measure == "euclidean" else 2 if distance_measure == "city" else 1) + first_pass[row+1][column-1]
            distances += [current] + [top] + [top_left] + [left] + [bottom_left]
            first_pass[row][column] = np.min(np.array(distances))
    
    # second pass
    second_pass = copy.deepcopy(first_pass)
    for row in range(image.shape[0]-2, 0, -1):
        for column in range(image.shape[1]-2, -1, -1):
            distances = []
            current = second_pass[row][column]
            bottom = 1 + second_pass[row+1][column]
            bottom_right = (np.sqrt(2) if distance_measure == "euclidean" else 2 if distance_measure == "city" else 1) + second_pass[row+1][column+1]
            right = 1 + second_pass[row][column+1]
            top_right = (np.sqrt(2) if distance_measure == "euclidean" else 2 if distance_measure == "city" else 1) + second_pass[row-1][column+1]
            distances += [current] + [bottom] + [bottom_right] + [right] + [top_right]
            second_pass[row][column] = np.min(np.array(distances))
    
    return first_pass, second_pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# reading an image, converting it to grayscale, applying edge detection
image = cv2.imread('Suez Canal.png', cv2.IMREAD_GRAYSCALE)
image = cv2.Canny(image, 100, 200)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# normalize distance transform between 0 and 255 to save as bmp image
def NormalizeData(data):
    unique = np.sort(np.unique(data))
    data[np.where(data == np.inf)] = unique[unique.shape[0]-2]
    data = (data - np.min(data)) / (np.max(data) - np.min(data))
    return (data * 255)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# calculating distance transform matrix for representative point (150, 200) and (310, 175)
first_pass, second_pass = distance_transform(image, "euclidean", [(150, 200), (310, 175)])
Image.fromarray(NormalizeData(first_pass).astype('uint8')).save("Suez_1_Euclidean.bmp")
Image.fromarray(NormalizeData(second_pass).astype('uint8')).save("Suez_final_Euclidean.bmp")

first_pass, second_pass = distance_transform(image, "city", [(150, 200), (310, 175)])
Image.fromarray(NormalizeData(first_pass).astype('uint8')).save("Suez_1_City.bmp")
Image.fromarray(NormalizeData(second_pass).astype('uint8')).save("Suez_final_City.bmp")

first_pass, second_pass = distance_transform(image, "chess", [(150, 200), (310, 175)])
Image.fromarray(NormalizeData(first_pass).astype('uint8')).save("Suez_1_Chess.bmp")
Image.fromarray(NormalizeData(second_pass).astype('uint8')).save("Suez_final_Chess.bmp")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# getting big ship left side coordinates, as well as left bank coordinates for big ship
big_left_side = None
big_left_bank = None

last_white_pixel = 200
consecutive_black_count = 0
for i in range(200, -1, -1):
    if image[150][i] == 255 and consecutive_black_count > 30:
        big_left_side = last_white_pixel
        big_left_bank = i
        break
    elif image[150][i] == 255:
        last_white_pixel = i
        consecutive_black_count = 0
    elif image[150][i] == 0:
        consecutive_black_count += 1

# getting small ship left side coordinates, as well as left bank coordinates for small ship
small_left_side = None
small_left_bank = None

last_white_pixel = 175
consecutive_black_count = 0
for i in range(175, -1, -1):
    if image[310][i] == 255 and consecutive_black_count > 30:
        small_left_side = last_white_pixel
        small_left_bank = i
        break
    elif image[310][i] == 255:
        last_white_pixel = i
        consecutive_black_count = 0
    elif image[310][i] == 0:
        consecutive_black_count += 1

# getting big ship right side coordinates, as well as right bank coordinates for big ship
big_right_side = None
big_right_bank = None

last_white_pixel = 200
consecutive_black_count = 0
for i in range(200, image.shape[1]):
    if image[150][i] == 255 and consecutive_black_count > 30:
        big_right_side = last_white_pixel
        big_right_bank = i
        break
    elif image[150][i] == 255:
        last_white_pixel = i
        consecutive_black_count = 0
    elif image[150][i] == 0:
        consecutive_black_count += 1

# getting small ship right side coordinates, as well as right bank coordinates for small ship
small_right_side = None
small_right_bank = None

last_white_pixel = 175
consecutive_black_count = 0
for i in range(175, image.shape[1]):
    if image[310][i] == 255 and consecutive_black_count > 30:
        small_right_side = last_white_pixel
        small_right_bank = i
        break
    elif image[310][i] == 255:
        last_white_pixel = i
        consecutive_black_count = 0
    elif image[310][i] == 0:
        consecutive_black_count += 1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# getting distance between two ships using (euclidean - city - chess) distance measures
first_pass, second_pass = distance_transform(image, "euclidean", [(150, 200)])
two_ships_euclidean = second_pass[310][175]
print("Distance between two ships (Euclidean): ", two_ships_euclidean)
first_pass, second_pass = distance_transform(image, "city", [(150, 200)])
two_ships_city = second_pass[310][175]
print("Distance between two ships (City): ", two_ships_city)
first_pass, second_pass = distance_transform(image, "chess", [(150, 200)])
two_ships_chess = second_pass[310][175]
print("Distance between two ships (Chess): ", two_ships_chess)

# getting distance between big ship and left shore
first_pass, second_pass = distance_transform(image, "euclidean", [(150, big_left_side)])
big_left_distance = second_pass[150][big_left_bank]
print("\nDistance between big ship and left bank (Euclidean): ", big_left_distance)

# getting distance between big ship and right shore
first_pass, second_pass = distance_transform(image, "euclidean", [(150, big_right_side)])
big_right_distance = second_pass[150][big_right_bank]
print("Distance between big ship and right bank (Euclidean): ", big_right_distance)

# getting distance between small ship and left shore
first_pass, second_pass = distance_transform(image, "euclidean", [(310, small_left_side)])
small_left_distance = second_pass[310][small_left_bank]
print("\nDistance between small ship and left bank (Euclidean): ", small_left_distance)

# getting distance between small ship and right shore
first_pass, second_pass = distance_transform(image, "euclidean", [(310, small_right_side)])
small_right_distance = second_pass[310][small_right_bank]
print("Distance between small ship and right bank (Euclidean): ", small_right_distance)
