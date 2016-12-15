#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 08.12.2016

:author: Paul Pasler
:organization: Reutlingen University
'''

import random

from PyQt4 import QtGui, QtCore
import cv2

import numpy as np


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Video():
    def __init__(self,capture):
        self.capture = capture
        self.currentFrame=np.array([])

    def captureNextFrame(self):
        ret, readFrame=self.capture.read()
        if(ret==True):
            self.currentFrame=cv2.cvtColor(readFrame,cv2.COLOR_BGR2RGB)

    def convertFrame(self):
        '''converts frame to format suitable for QtGui'''
        try:
            height,width = self.currentFrame.shape[:2]
            img=QtGui.QImage(self.currentFrame, width, height, QtGui.QImage.Format_RGB888)
            img=QtGui.QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except:
            return None

class VideoPlayer(QtGui.QWidget):
    def __init__(self, parent, videoUrl):
        super(VideoPlayer, self).__init__()
        self.parent = parent
        self.video = Video(cv2.VideoCapture(videoUrl))
        self.videoFrame = QtGui.QLabel(self)
        self.videoFrame.setGeometry(self.geometry())
        self.videoFrame.setObjectName(_fromUtf8("videoFrame"))

    def play(self):
        try:
            self.video.captureNextFrame()
            self.videoFrame.setPixmap(self.video.convertFrame())
            self.videoFrame.setScaledContents(True)
        except TypeError:
            print "No frame"

class VideoWidget(QtGui.QWidget):

    def __init__(self):
        super(VideoWidget, self).__init__()
        self.mainLayout = QtGui.QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.setObjectName(_fromUtf8("videolwidget"))

    def setPlayers(self, videoPlayers):
        for videoPlayer in videoPlayers:
            self.mainLayout.addWidget(videoPlayer)