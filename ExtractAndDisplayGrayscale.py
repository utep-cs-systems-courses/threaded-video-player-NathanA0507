#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue
from ThreadingQueue import ThreadingQueue

def extractFrames(fileName, color_frames, maxFramesToLoad=9999):
    # Initialize frame count
    count = 0
    global extractionDone
    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()

    print(f'Reading frame {count} {success}')
    while success:
        # add the frame to the buffer
        color_frames.enqueue(image)

        success,image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1

    print('Frame extraction complete')


def convertToGray(color_frames, gray_frames):
    count = 0
    while True:
        print(f'Converting frame {count}')

        inputFrame = color_frames.dequeue()

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)

        gray_frames.enqueue(grayscaleFrame)

        count += 1


def displayFrames(grey_frames):
    # initialize frame count
    count = 0

    # go through each frame in the buffer until the buffer is empty
    while True:
        # get the next frame
        frame = grey_frames.dequeue()

        print(f'Displaying frame {count}')

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

    print('Finished displaying all frames')
    # cleanup the windows
    cv2.destroyAllWindows()



# filename of clip to load
filename = 'clip.mp4'

color_frames = ThreadingQueue()
grey_frames = ThreadingQueue()

read = threading.Thread(target = extractFrames, args = (filename, color_frames))
convert = threading.Thread(target = convertToGray, args = (color_frames,grey_frames))
display = threading.Thread(target = displayFrames, args = (grey_frames,))

read.start()
convert.start()
display.start()
