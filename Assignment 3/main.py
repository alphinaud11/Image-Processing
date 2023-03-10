from PIL import Image
import numpy as np
import math

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def LZW(image):
    dictionary = {}
    for i in range(256):
        dictionary[str(i)] = str(i)

    current_index = 0
    current_sequence = 256
    output_code = []

    while current_index < len(image):
        # getting the longest string in input that matches a string in dictionary
        longest_string = []
        while True:
            longest_string += [str(image[current_index])]
            w = '-'.join(longest_string)
            if not (w in dictionary):
                current_index -= 1
                del longest_string[-1]
                break
            if current_index == (len(image) - 1):
                break
            else:
                current_index += 1
        
        # output the sequence of longest string
        w = '-'.join(longest_string)
        output_code += [dictionary[w]]

        # adding w followed by next symbol in input to dictionary
        current_index += 1
        if not (current_index == len(image)):
            longest_string += [str(image[current_index])]
            w = '-'.join(longest_string)
            dictionary[w] = str(current_sequence)
            current_sequence += 1
    
    # calculating compression ratio
    compression_ratio = (8 * len(image)) / (math.ceil(math.log(len(dictionary), 2)) * len(output_code))

    return dictionary, output_code, compression_ratio
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

image = np.array(Image.open('Camera2.jpg')).flatten()

dictionary, output_code, compression_ratio = LZW(image)

# saving dictionary
with open('Dict.txt', 'w') as f:
    longest_code_length = -1
    for code in dictionary.keys():
        longest_code_length = len(code) if len(code) > longest_code_length else longest_code_length
    str1 = 'Code'
    str2 = ''
    filler = '~'
    f.write(f'{str1.ljust(longest_code_length)}\tSequence\n{str2.ljust(longest_code_length, filler)}~~~~~~~~~~~~~\n')
    for code, sequence in dictionary.items():
        f.write(f'{code.ljust(longest_code_length)}\t{sequence}\n')

# saving output code
with open('LZWCode.txt', 'w') as f:
    f.write(' '.join(output_code))

# saving compression ratio
with open('CompRatio.txt', 'w') as f:
    f.write(str(compression_ratio))