"""expand_mnist.py
~~~~~~~~~~~~~~~~~~

Take the 50,000 MNIST training images, and create an expanded set of
250,000 images, by displacing each training image up, down, left and
right, by one pixel.  Save the resulting file to
../data/mnist_expanded.pkl.gz.

Note that this program is memory intensive, and may not run on small
systems.

"""

from __future__ import print_function


import cv2 #for rotations


#### Libraries

# Standard library
import cPickle
import gzip
import os.path
import random
import math
import sys, getopt
# Third-party libraries
import numpy as np

#import cv2
#import matplotlib.cm as cm
#import matplotlib.pyplot as plt





def main(argv):
    outputpath = "../data/mnist_shuffled"
    outputpathpostfix = ".pkl.gz"
    partitions = 3
    shift_flag = 0 #for default expansion change this flag to 1. This adds 4 shifts for each image
    shift_and_rotate_flag = 0 #for more expansion change this flag to 1. This adds 10 rotations to each of the 4 shifts

    try:
        opts, args = getopt.getopt(argv,"hp:sr",["help=","partitions=","shift_flag","shift_and_rotate_flag"])
    except getopt.GetoptError:
        print("eror with parsing options. going with defaults. partitions=",partitions," shift_flag =",shift_flag," shift_and_rotate_flag=",shift_and_rotate_flag)
#    if not("-p" in opts or "--partitions" in opts):
#        print("partitions option not specified, going with the default of ",partitions)

    for opt, arg in opts:
        if opt in ("-h","--help"):
            print ('mnist_shuffle.py -p <# of partitions> -s -r')
            sys.exit()
        elif opt in ("-p", "--partitions"):
            partitions = arg
            partitions=int(partitions) #partitions as a command line arguement is read as a float. we expect it to be an int
            print("partitions=",partitions)
        elif opt in ("-s", "--shift_flag"):
            shift_flag=1
            print("shift_flag=",shift_flag)
        elif opt in ("-r", "--shift_and_rotate_flag"):
            shift_and_rotate_flag=1
            print("shift_and_rotate_flag=",shift_and_rotate_flag)
    
    if os.path.exists(outputpath):
        print("The shuffled training set already exists.  Exiting.")
    else:
        print("expanding and Shuffling the MNIST training set")
        f = gzip.open("../data/mnist.pkl.gz", 'rb')
        training_data, validation_data, test_data = cPickle.load(f)
        f.close()
        expanded_training_pairs = []
        j = 0 # counter
        expansion_counter = 0
        for x, y in zip(training_data[0], training_data[1]):
            j += 1
            if j % 1000 == 0: 
                print("Expanding image number", j)
            
            expanded_training_pairs.append((x, y))
            expansion_counter=expansion_counter+1
            image = np.reshape(x, (-1, 28))
            # iterate over data telling us the details of how to
            # do the displacement
            if (shift_flag ==1 or shift_and_rotate_flag ==1) :
                for d, axis, index_position, index in [
                        (1,  0, "first", 0),
                        (-1, 0, "first", 27),
                        (1,  1, "last",  0),
                        (-1, 1, "last",  27)]:
                    new_img = np.roll(image, d, axis)
                    if index_position == "first": 
                        new_img[index, :] = np.zeros(28)
                    else: 
                        new_img[:, index] = np.zeros(28)
                    expanded_training_pairs.append((np.reshape(new_img, 784), y))
                    expansion_counter=expansion_counter+1
    
                    if shift_and_rotate_flag ==1 :
                        for rotation in [ -10,-8,-6,-4, -2, 2, 4,6,8,10]:
                        
                            rows,cols = new_img.shape
                
                            M = cv2.getRotationMatrix2D((cols/2,rows/2),rotation,1)
                            dst = cv2.warpAffine(new_img,M,(cols,rows))
                            #plt.imshow(dst, cmap = cm.Greys_r)
                            #plt.show()
                            expanded_training_pairs.append((np.reshape(dst, 784), y))
                            expansion_counter=expansion_counter+1
            
    
        random.shuffle(expanded_training_pairs)
        print("Shuffling done, total images after expansion=",expansion_counter)
        
        partition_size = int(math.ceil(float(len(expanded_training_pairs))/partitions))    
            
        expanded_training_data = [list(d) for d in zip(*expanded_training_pairs)]
        print("Saving shuffled data in "+str(partitions)+" partitions. This may take a few minutes.")
        for x in range(0,partitions):
            filename = outputpath+str(x)+outputpathpostfix
            f = gzip.open(filename, "w")
            partition_begin = x*partition_size
            partition_end =(x+1)*partition_size
            partitioned_expanded_training_data =  []
            if x != partitions-1:#this is so we don't accidently grab something out of bounds. in the final case we just go to the end.
                partitioned_expanded_training_data = (expanded_training_data[partition_begin:partition_end])
            else:
                partitioned_expanded_training_data = (expanded_training_data[partition_begin:])
                
            cPickle.dump((partitioned_expanded_training_data, validation_data, test_data), f)
    
            f.close()
            print("done with saving file " + str(x) + " at location"+ filename) 
            
        print("Saving done")

if __name__ == "__main__":
   main(sys.argv[1:])