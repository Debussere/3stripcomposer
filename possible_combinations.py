import numpy as np

# composed face
NR_STRIP = 3
# smalles piece, basically lenght/50
START = 3
# largest piece, basically lenght/50, note +1 because last number is NOT included in range
END = 12+1

# limitations
# lenght of composed face
MAX_LENGHT = 2200
MAX_PIECES_OF_150_200_250mm = 4
# max number of pieces with certain lenght
MAX_150mm = 2
MAX_200mm = 2
MAX_250mm = 2
MAX_300mm = 9
MAX_350mm = 17
MAX_400mm = 15
MAX_450mm = 9
MAX_500mm = 2
MAX_550mm = 1
MAX_600mm = 1

# creating list of keys
# [12, 11, 10, 9, 8, 7, 6, 5, 3]
# where every item in the list is the length/50
possible_keys = []
for i in range(START, END):
     possible_keys.append(i)
possible_keys.sort(reverse=True)

if __name__ == '__main__':
    # generated list
    # where every item in the list stands for a certain lenght
    # [600, 550, 500, 450, 400, 350, 300, 250, 200, 150]
    # !! When adding a new lenght, add new loop in descending order
    def generated_list():
        combinations_container = [0]*(END-START)
        for i in range(0, MAX_600mm+1):
            combinations_container[0] = i
            for j in range(0, MAX_550mm+1):
                combinations_container[1] = j
                for k in range(0, MAX_500mm+1):
                    combinations_container[2] = k
                    for l in range(0, MAX_450mm+1):
                        combinations_container[3] = l
                        for m in range(0, MAX_400mm+1):
                            combinations_container[4] = m
                            for n in range(0, MAX_350mm+1):
                                combinations_container[5] = n
                                for o in range(0, MAX_300mm+1):
                                    combinations_container[6] = o
                                    for p in range(0, MAX_250mm+1):
                                        combinations_container[7] = p
                                        for q in range(0, MAX_200mm+1):
                                            combinations_container[8] = q
                                            for r in range(0, MAX_150mm+1):
                                                combinations_container[9] = r
                                                yield combinations_container
    
    
    # write to txt file
    # file will be written to current directory
    with open('compositions.txt', 'w') as f:
        for item in generated_list():
            tmplist = list(item)
            # specify limitations
            # limitation 1: sum of all lenghts must be equal to lenght of the composed face x number of strips
            # limitation 2: Max 4 pieces of the smallest 3 pieces (150/200/250mm)
            if np.sum(np.multiply(tmplist, possible_keys))*50 == MAX_LENGHT*3  and np.sum(np.array(tmplist[-3:])) <= 4:
                print(tmplist)
                for item in tmplist:
                    f.write("{}\t".format(str(item)))
                f.write("\n")
