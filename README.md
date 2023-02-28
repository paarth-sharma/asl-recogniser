# Asl-recogniser

## This project aims to convert ASL gestures to phrases/sentences in real-time without human intervention to facilitate communication

### What the program looks like while running

![](/assets/demo.png)

I am Paarth Sharma and this is my A.I. project for the 4th semester of my college in Thapar. This project is my attempt at making a prgram that converts ASL signs to text in real-time, eliminating the need for translators and hopefully speed up the communication process for the specially-abled.

### Python Libraries used

[open-cv](https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html)

[numpy](https://numpy.org/doc/stable/user/quickstart.html) basic functions and their usage

[keras](https://www.tensorflow.org/api_docs/python/tf/keras/models/load_model)

- Since I had a .h5 file with abundant data, load_models was the best choice to work with it

>A  '.h5' file, contains large amounts of data
( consists of t contains multidimensional arrays of scientific data.
H5 files are commonly used in aerospace, physics, engineering, finance,
academic research, genomics, astronomy, electronics instruments, and medical fields).
This particular file contains approximately 1200 gestures for 1 letter

[tensorflow](https://developers.google.com/machine-learning/crash-course/first-steps-with-tensorflow/toolkit)

[pyspellchecker](https://pyspellchecker.readthedocs.io/en/latest/) has been  used to make the words into meaningful sentences using natural language as reference.

### Model Training

For classification model **Canny Edge Detector** was applied on images.

![](/assets/model_imgs.jpg)

## How to  use this tool?

* Once started adjust the threshold values for edge detection so you can see just the edges of your palm and fingers.
>  ![](/assets/edge-detector.png)

* Press `S` to start/pause the output generation.
* Press `D` to erase the output section.
* Press `Q` to quit the script.
* `del`, `space` and `nothing` do what they suppose to do.
* Input double `space` to apply `pyspellchecker` on the last word.
