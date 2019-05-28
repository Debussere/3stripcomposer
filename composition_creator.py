import random
import math
import numpy as np
from possible_combinations import NR_STRIP, possible_keys, MAX_LENGHT

# how many planks we can have in 1 strip of the composed face
NR_SEQ_PL = 9
# how many different layouts will be generated
NR_OF_GENERATED_COMPOSITIONS = 5

# read all pools from text file
def read_combinations():
    # [1, 1, 2, 3, 2, 3, 2, 1, 2, 0]
    with open('compositions.txt', 'r') as f:
        for line in f:
            combinations_container = [0]*10
            line = line.split()
            yield line
    
def list_expand(pool, digits):
    '''creating list of pool*digits
    pool = ["A", "B", "C"]
    digits = [1, 2, 3]
    => ["A", "B", "B", "C", "C", "C"]'''
    # list of integers
    digits = list(map(int, digits))
    # create container with correct lenght
    expanded_list = [0]*np.sum(digits)
    # counters for looping thourgh arrays
    count1 = 0 
    count2 = 0
    # filling container
    for item in pool:
        for j in range(0, digits[count1]):
            expanded_list[count2] = item
            count2 +=1
        count1 +=1
    return expanded_list


def is_allowed_composed_3strip(composed_face, lenght):
    '''checking for no overlap between 2 adjacent lamellas on the long side AND if lenght per strip is equal to desired lenght composed face
    evaluates True if there if both conditions apply'''
    # checking for desired lenght
    if np.count_nonzero(np.sum(composed_face, axis=1) == lenght/50) == NR_STRIP:
        # checking for overlapping adjacent lamellas
        composed_face = np.cumsum(composed_face, axis=1)
        r = 1
        c = 0
        # check for empty face
        if composed_face[0, 0] == 0:
            return False
        # comparing strip ends of middle strip with lower and upper strip
        # [[ 9 13 25 36 44 44 44 44 44]
        #  [ 5 14 21 30 34 44 44 44 44]
        #  [ 6 13 20 26 36 44 44 44 44]]
        if np.intersect1d(composed_face[r,:], composed_face[r-1,:]).size <= 1:
            if np.intersect1d(composed_face[r,:], composed_face[r+1,:]).size <= 1:
                return True
        return False
    else:
        return False


def print_composedface(composedface):
    # printing the layout of the composed face in the command line
    print(" ", end="")
    print("_"*int((MAX_LENGHT/50-1)))
    for row in composedface:
        print("|", end="")
        for item in row:
            if item != 0:
                print((item-1)*"_", end="|")
        print("")

# create 3x9 container to represent a composed face, reading left to right
strip_container = np.zeros(NR_STRIP*NR_SEQ_PL, dtype=int).reshape(NR_STRIP, NR_SEQ_PL)



def composition_creator(possiblecombinations):
    f = open("3strip.txt", "a")
    for combination in possiblecombinations:
        # generating multiple compositions
        for i in range(0, NR_OF_GENERATED_COMPOSITIONS):
            # list of integers
            combination = list(map(int, combination))
            # create pool of all lenghts
            # pool = [1, 1, 2, 3, 2, 3, 2, 1, 2, 0]
            # => [12, 11, 10, 10, 9, 9, 9, 8, 8, 7, 7, 7, 6, 6, 5, 4, 4]
            lenght_pool = list_expand(possible_keys, combination)
            random.shuffle(lenght_pool)
            nr_of_loops = 0
            # check if container is allowed
            while True:
                random.shuffle(lenght_pool)
                # reset container
                strip_container.fill(0)
                # fill container with pool
                # [[ 9  4 12 11  8  0  0  0  0]
                #  [ 5  9  7  9  4 10  0  0  0]
                #  [ 6  7  7  6 10  8  0  0  0]]
                count = 0
                for item in lenght_pool:
                    x = count % NR_STRIP
                    y = int(count / NR_STRIP)
                    strip_container[x, y] = item
                    count +=1
                np.random.shuffle(strip_container)
                nr_of_loops +=1
                # check if face is allowed
                if is_allowed_composed_3strip(strip_container, MAX_LENGHT) == True:
                    if i == 0:
                        # print("_"*80)
                        # print("combination: ",combination)
                        # print("")
                        # write to txt file
                        f.write("\n")
                        for item in combination:
                            f.write("{}\t".format(str(item)))
                        f.write("\t")
                    # print("possibility: ",i+1)
                    # print(strip_container)
                    # print()
                    for array in strip_container:
                        for item in array:
                            f.write("{}\t".format(str(item)))
                        f.write("\t")
                    break
                if nr_of_loops > 50000:
                    break
            if nr_of_loops > 50000:
                break
        print("added: ",combination)
    f.close()



if __name__ == '__main__':
    composition_creator(read_combinations())