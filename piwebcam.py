#!/usr/bin/env python3
"""
picam: Face Detection Using webcam on Raspberry pi 
with python-opencv

;-------------------------------------------------------------------------------
; Developed by: Eduardo S. Pereira
; version: 0.0.1
; e-mail: pereira.somoza@gmail.com
; date: 26/05/2018
;
; Copyright 2018 Eduardo S. Pereira
;
; Licensed under the Apache License, Version 2.0 (the "License");
; you may not use this file except in compliance with the License.
; You may obtain a copy of the License at
;
; http://www.apache.org/licenses/LICENSE-2.0
;
; Unless required by applicable law or agreed to in writing, software
; distributed under the License is distributed on an "AS IS" BASIS,
; WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
; See the License for the specific language governing permissions and
; limitations under the License.
;-------------------------------------------------------------------------------
"""

import cv2
from threading import Thread 

class PiWebcam(Thread):
	def __init__(self, facemodel="haarcascade_frontalface_default.xml"):
		Thread.__init__(self)
		self._cam = cv2.VideoCapture(0)
		self._cam.set(3,100)
		self._cam.set(4,100)
		self._image = None
		self._ret = None
		self._stopCam = False
		self._cam_window = None
		self.face_c = cv2.CascadeClassifier(facemodel)

		self._facerec = None

		
	def cam_window(self):
		if self._cam_window is None:
			self._cam_window = cv2.namedWindow("camera", 
										        cv2.WINDOW_AUTOSIZE)
		if self._image is not None:

			if self._facerec is not None:
				for (x,y,w,h) in self._facerec:	
					cv2.rectangle(self._image,(x,y),(x+w,y+h),(244,0,0),2)

			cv2.imshow("camera", self._image)

		#Tecla esc para sair
		if cv2.waitKey(1) == 27:
			cv2.destroyAllWindows()
			self.start_stop()
			
	def face_detection(self):
		gray = self.get_gray()		
		self._facerec  = self.face_c.detectMultiScale(gray, 1.3,5)

	def run(self):
		while True:		
			self.cam_window()			
			self._ret, self._image = self._cam.read()
			
			if self._stopCam is True:
				break
				
	def is_running(self):
		return not self._stopCam
				
	def start_stop(self):
		self._stopCam = True if self._stopCam is False else False
		
	def get_image(self):
		return self._image
		
	def get_gray(self):
		if self._image is not None:
			return cv2.cvtColor(self._image,cv2.COLOR_BGR2GRAY)
			
		
	def set_image(self, image):
		self._image = image


if __name__ == "__main__":
	mycam = PiWebcam()
	mycam.setDaemon(True)
	mycam.start()

	while True:
		img = mycam.get_image()
		if img is not None:	

			mycam.face_detection()			

					
		if mycam.is_running() is False:
			break