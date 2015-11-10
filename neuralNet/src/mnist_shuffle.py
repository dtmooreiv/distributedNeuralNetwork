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

#### Libraries

# Standard library
import cPickle
import gzip
import os.path
import random

# Third-party libraries
#import numpy as np

#import cv2
#import matplotlib.cm as cm
#import matplotlib.pyplot as plt




print("Shuffling the MNIST training set")
outputpath = "../data/mnist_shuffled.pkl.gz"

if os.path.exists(outputpath):
    print("The shuffled training set already exists.  Exiting.")
else:
    f = gzip.open("../data/mnist.pkl.gz", 'rb')
    training_data, validation_data, test_data = cPickle.load(f)
    f.close()
    expanded_training_pairs = []
    j = 0 # counter
    for x, y in zip(training_data[0], training_data[1]):
        j += 1
        if j % 1000 == 0: print("opening image number", j)
        expanded_training_pairs.append((x, y))
        
    random.shuffle(expanded_training_pairs)
    expanded_training_data = [list(d) for d in zip(*expanded_training_pairs)]
    print("Saving shuffled data. This may take a few minutes.")
    f = gzip.open(outputpath, "w")
    cPickle.dump((expanded_training_data, validation_data, test_data), f)
    f.close()
    print("Shuffling done")
