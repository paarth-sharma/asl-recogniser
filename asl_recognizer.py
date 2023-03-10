import cv2
import sys
import numpy as np
import keras
from keras.models import load_model
from spellchecker import SpellChecker

# when there is no hand gesture in the edged-box
def nothing(v):
    pass

"""
Function returns the key (Letter: 'a', 'b', 'c'...) value from the alphabet dictionary
based on its class index (1, 2, 3 ...) and so on.
"""
def get_class_label(val, dictionary):
    for key, value in dictionary.items():
        if value == val:
            return key

""" 
loading the model with .h5 file, contains large amounts of data 
(consists of t contains multidimensional arrays of scientific data. 
H5 files are commonly used in aerospace, physics, engineering, finance, 
academic research, genomics, astronomy, electronics instruments, and medical fields.)

This particular file conatains approximately 1200 gestures for 1 letter
"""

model = load_model('train_data.h5')
spell = SpellChecker("en")


"""
making an alphabet dictionary to label alphabets {a:1, b:2, .... 29:nothing}

del: to delete a character
nothing: when no gesture id detected on screen
space: to introduce space into words to make phrases
"""
alphabet = {chr(i+96).upper():i for i in range(1,27)}
alphabet['del'] = 27
alphabet['nothing'] = 28
alphabet['space'] = 29

"""
Video capturing, making a boxed area where the gesture will be detected
setting ratios up for the detection box

Using py-canny to detect gestures in real-time, works by noise-reduction
"""

video_capture = cv2.VideoCapture(0)
cv2.namedWindow('Model Image')

video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

cv2.createTrackbar('lower_threshold', 'Model Image', 0, 255, nothing)
cv2.createTrackbar('upper_threshold', 'Model Image', 0, 255, nothing)
cv2.setTrackbarPos('lower_threshold', 'Model Image', 100)
cv2.setTrackbarPos('upper_threshold', 'Model Image', 0)

"""
Variable initialization
THRESHOLD - ratio of the same letter in the last N_FRAMES predicted letters
"""

THRESHOLD = 0.85
N_FRAMES = 25

IMG_SIZE = 100
SENTENCE = '' # string that will hold the final output
letter = '' # temporary letter
LETTERS = np.array([], dtype='object') # array with predicted letters

START = False # start/pause controller

# supportive text
description_text_1 = "Press 'S' to Start/Pause gesture recognition."
description_text_2 = "Press 'D' to erase the output. "
description_text_3 = "Press 'Q' to quit."

while True:
    blank_image = np.zeros((100,800,3), np.uint8) # black image for the output
    ret, frame = video_capture.read() # capture frame-by-frame
    
    # set the corners for the square to initialize the model picture frame
    x_0 = int(frame.shape[1] * 0.1)
    y_0 = int(frame.shape[0] * 0.25)
    x_1 = int(x_0 + 200)
    y_1 = int(y_0 + 200)

    #Model image generation
    hand = frame.copy()[y_0:y_1, x_0:x_1]
    gray = cv2.cvtColor(hand, cv2.COLOR_BGR2GRAY) #convert input to grayscale

    # noise reduction
    blured = cv2.GaussianBlur(gray, (5, 5), 0)
    blured = cv2.erode(blured, None, iterations=2)
    blured = cv2.dilate(blured, None, iterations=2)
    
    #get the values from tack bar
    lower = cv2.getTrackbarPos('lower_threshold', 'Model Image')
    upper = cv2.getTrackbarPos('upper_threshold', 'Model Image')
    edged = cv2.Canny(blured,lower,upper) # apply the edge detector(drawing the box)

    # invert colors
    model_image = ~edged 
    model_image = cv2.resize(
        model_image,
        dsize = (IMG_SIZE, IMG_SIZE),
        interpolation = cv2.INTER_CUBIC
    )
    model_image = np.array(model_image)
    model_image = model_image.astype('float32') / 255.0

    try:
        model_image = model_image.reshape(1, IMG_SIZE, IMG_SIZE, 1)
        predict = model.predict(model_image)
        for values in predict:

            if np.all(values < 0.5):
                # if probability of each class is less than .5 return a message
                letter = 'Cannot classify:('
            
            else:
                predict = np.argmax(predict, axis = 1) + 1
                letter = get_class_label(predict, alphabet)
                LETTERS = np.append(LETTERS, letter)
    
    except:
        pass


    if START == True:
        # append the final output with the letter
        if (np.mean(LETTERS[-N_FRAMES:] == letter) >= THRESHOLD) & (len(LETTERS) >= N_FRAMES):
            if letter == 'space':
                SENTENCE = SENTENCE[:-1] + ' ' + '_'
                LETTERS = np.array([], dtype='object')
            elif letter == 'del':
                SENTENCE = SENTENCE[:-2] + '_'
                LETTERS = np.array([], dtype='object')
            elif letter == 'nothing':
                pass
            else:
                SENTENCE = SENTENCE[:-1] + letter + '_'
                LETTERS = np.array([], dtype='object')

        # apply spell checker after double space
        if len(SENTENCE) > 2:
            if SENTENCE[-3:] == '  _':
                SENTENCE = SENTENCE.split(' ')
                word = SENTENCE[-3]
                corrected_word = spell.correction(word)
                SENTENCE[-3] = word.upper()
                SENTENCE = ' '.join(SENTENCE[:-2]) + ' _'


    if START == False:
        paused_text = 'Paused'
    else:
        paused_text = ''

    # Text Initialization
    # paused text
    cv2.putText(
        img = frame,
        text = paused_text,
        org = (x_0+140,y_0+195),
        fontFace = cv2.FONT_HERSHEY_PLAIN,
        color = (0,0,255),
        fontScale = 1
    )

    # helper texts
    cv2.putText(
        img = frame,
        text = description_text_1,
        org = (10,440),
        fontFace = cv2.FONT_HERSHEY_PLAIN,
        color = (255,255,255),
        fontScale = 1
    )

    cv2.putText(
        img = frame,
        text = description_text_2,
        org = (10,455),
        fontFace = cv2.FONT_HERSHEY_PLAIN,
        color = (255,255,255),
        fontScale = 1
    )

    cv2.putText(
        img = frame,
        text = description_text_3,
        org = (10,470),
        fontFace = cv2.FONT_HERSHEY_PLAIN,
        color = (255,255,255),
        fontScale = 1
    )

    cv2.putText(
        img = frame,
        text = 'Place your hand here:',
        org = (x_0-30,y_0-10),
        fontFace = cv2.FONT_HERSHEY_COMPLEX_SMALL,
        color = (255,255,255),
        fontScale = 1
    )

    # current letter
    cv2.putText(
        img = frame,
        text = letter,
        org = (x_0+10,y_0+20),
        fontFace = cv2.FONT_HERSHEY_PLAIN,
        color = (255,255,255),
        fontScale = 1
    )

    # final output
    cv2.putText(
        img = blank_image,
        text = 'Result: ' + SENTENCE,
        org = (10, 50),
        fontFace = cv2.FONT_HERSHEY_COMPLEX_SMALL,
        thickness = 1,
        color = (0,0,255),
        fontScale = 1
    ) 

    # draw rectangle for hand placement
    cv2.rectangle(frame, (x_0, y_0), (x_1, y_1), (0, 255, 0), 2)

    # display the resulting frames
    cv2.imshow('Main Image', frame)
    cv2.imshow('Model Image', edged)
    cv2.imshow('Output', blank_image)

    if cv2.waitKey(30) & 0xFF == ord('s'):
        START = not START

    if cv2.waitKey(30) & 0xFF == ord('d'):
        SENTENCE = ''

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

# save the resulted string into the file
text_file = open("Output.txt", "w")
text_file.write("You said: %s" % SENTENCE)
text_file.close()