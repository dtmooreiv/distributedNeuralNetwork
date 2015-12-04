#!/bin/sh

cd /home/ubuntu/opencv
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_C_EXAMPLE=ON _D INSTALL_PYTHON_EXAMPLES=ON -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -D BUILD_EXAMPLE=ON -D BUILD_EXAMPLES=ON ..
make -j4
sudo make install
sudo ldconfig