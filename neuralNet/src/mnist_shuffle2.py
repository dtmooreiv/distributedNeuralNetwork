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
    shifts = 0 #
    rotations = 0 #

####################################################################################################################################################################
    try:
        opts, args = getopt.getopt(argv,"hp:s:r:",["help=","partitions=","shifts","rotations"])
    except getopt.GetoptError:
        print("eror with parsing options. going with defaults. partitions=",partitions," shifts =",shifts," rotations=",rotations)
#    if not("-p" in opts or "--partitions" in opts):
#        print("partitions option not specified, going with the default of ",partitions)

    for opt, arg in opts:
        if opt in ("-h","--help"):
            print ('mnist_shuffle.py -p <# of partitions> -s<# max distance of shifts> -r<# of rotations>')
            sys.exit()
        elif opt in ("-p", "--partitions"):
            partitions = arg
            partitions=int(partitions) #partitions as a command line arguement is read as a float. we expect it to be an int
            print("partitions=",partitions)
        elif opt in ("-s", "--shifts"):
            shifts= arg
            shifts = int(shifts)
            print("shifts=",shifts)
        elif opt in ("-r", "--rotations"):
            rotations=arg
            rotations=int(rotations)
            print("rotations=",rotations)
        
    partition_size = int(math.ceil((50000+50000*4*shifts+50000*4*rotations)/partitions))    

####################################################################################################################################################################    
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
        partition_counter = 0
        for x, y in zip(training_data[0], training_data[1]):
            j += 1
            if j % 1000 == 0: 
                print("Expanding image number", j)
            
            if len(expanded_training_pairs)>partition_size:
                print ("len(expanded_training_pairs)",len(expanded_training_pairs)," is greater than partition_size ",partition_size," time to randomize and write.")
                random.shuffle(expanded_training_pairs)
                expanded_training_data = [list(d) for d in zip(*expanded_training_pairs)]
                
                filename = outputpath+str(partition_counter)+outputpathpostfix
                f = gzip.open(filename, "w")
                cPickle.dump((expanded_training_data, validation_data, test_data), f)
                f.close()
                print("done with saving file " + str(partition_counter) + " at location"+ filename)
                partition_counter=partition_counter+1
                
                while len(expanded_training_pairs) > 0 : expanded_training_pairs.pop() #clears out the list                 
            
            expanded_training_pairs.append((x, y))
            expansion_counter=expansion_counter+1
            image = np.reshape(x, (-1, 28))
            # iterate over data telling us the details of how to
            # do the displacement
            if (shifts >=1 or rotations >=1) :
                if rotations >=1 and shifts == 0:
                    shifts = 1
                    print("changing shifts to ",shifts)
                for distance in range(1,shifts+1):
                    for d, axis, index_position, index in [
                            (distance,  0, "first1", 0),
                            (-distance, 0, "first2", 27),
                            (distance,  1, "last1",  0),
                            (-distance, 1, "last2",  27)]:
                        new_img = np.roll(image, d, axis)
                        if index_position == "first1": 
                            new_img[index:index+distance, :] = np.zeros(28*distance).reshape((distance,28))
                        elif index_position == "first2": 
                            new_img[index-distance:index, :] = np.zeros(28*distance).reshape((distance,28))
                        elif index_position == "last1": 
                            new_img[:, index:index+distance] = np.zeros((28*distance)).reshape((28,distance))
                        elif index_position == "last2": 
                            new_img[:, index-distance:index] = np.zeros((28*distance)).reshape((28,distance))
                        expanded_training_pairs.append((np.reshape(new_img, 784), y))
                        expansion_counter=expansion_counter+1
        
                        if rotations >=1 :
                            for rotation in range(-rotations,rotations,2) : #step size 2 because we go both ways from zero, also so the rotations aren't too close to each other
                            
                                rows,cols = new_img.shape
                    
                                M = cv2.getRotationMatrix2D((cols/2,rows/2),rotation,1)
                                dst = cv2.warpAffine(new_img,M,(cols,rows))
                                #plt.imshow(dst, cmap = cm.Greys_r)
                                #plt.show()
                                expanded_training_pairs.append((np.reshape(dst, 784), y))
                                expansion_counter=expansion_counter+1
                
    
        random.shuffle(expanded_training_pairs)
        print("Shuffling done, total images after expansion=",expansion_counter)
        expanded_training_data = [list(d) for d in zip(*expanded_training_pairs)]
        
        filename = outputpath+str(partition_counter)+outputpathpostfix
        f = gzip.open(filename, "w")
        cPickle.dump((expanded_training_data, validation_data, test_data), f)
        f.close()
        print("done with saving file " + str(partition_counter) + " at location"+ filename)
        expansion_counter=expansion_counter+1
            
        print("Saving done")

if __name__ == "__main__":
   main(sys.argv[1:])