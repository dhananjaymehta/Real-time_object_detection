# Author - Dhananjay Mehta and Swapnil Kumar
from facedetector import FaceDetector
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required = True,
	help = "path to where the face cascade resides")
ap.add_argument("-v", "--video",
	help = "path to the (optional) video file")
args = vars(ap.parse_args())

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

fd = FaceDetector(args["face"])
time.sleep(0.1)

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	frame = f.array
	frame = imutils.resize(frame, width = 300)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faceRects = fd.detect(gray, scaleFactor = 1.1, minNeighbors = 5,
		minSize = (30, 30))
	frameClone = frame.copy()
	for (fX, fY, fW, fH) in faceRects:
		cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (0, 255, 0), 2)

	cv2.imshow("Face", frameClone)
	rawCapture.truncate(0)
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break