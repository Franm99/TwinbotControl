import numpy as np
import cv2 as cv
from urllib.request import urlopen
from threading import Thread
import tkinter as tk
import PIL.Image, PIL.ImageTk
import time


class CameraClient(Thread):

    def __init__(self, root, name, url):
        Thread.__init__(self)
        self.root = root
        self.name = name
        self.url = url
        self.cameraWindow = tk.Toplevel(root)
        self.label = tk.Label(self.cameraWindow, text=url)
        self.label.grid(row=0, column=0, columnspan=3)

        self.urlOperation = url + 'cameracolor.jpg'
        self.mirror = False
        self.isImageColor = True
        self.imageScalePercentage = 50
        self.rotationAngleClockWise = 0
        self.salir = False
        self.gap = 0.2
        self.image = None

        self.buttonColorOrGray = tk.Button(self.cameraWindow, text="Color/Gray", command=self.switchColorOrGray)
        self.buttonColorOrGray.grid(row=1, rowspan=1, column=1, columnspan=2, sticky="nswe")

        self.buttonIncreaseSize = tk.Button(self.cameraWindow, text="+ Size", command=self.increaseSize)
        self.buttonIncreaseSize.grid(row=2, rowspan=1, column=1, columnspan=1, sticky="nswe")

        self.buttonDecreaseSize = tk.Button(self.cameraWindow, text="- Size", command=self.decreaseSize)
        self.buttonDecreaseSize.grid(row=2, rowspan=1, column=2, columnspan=1, sticky="nswe")

        self.buttonIncreaseGap = tk.Button(self.cameraWindow, text="+ Gap", command=self.increaseGap)
        self.buttonIncreaseGap.grid(row=3, rowspan=1, column=1, columnspan=1, sticky="nswe")

        self.buttonDecreaseGap = tk.Button(self.cameraWindow, text="- Gap", command=self.decreaseGap)
        self.buttonDecreaseGap.grid(row=3, rowspan=1, column=2, columnspan=1, sticky="nswe")

        self.buttonRotateClockwise = tk.Button(self.cameraWindow, text="CW", command=self.rotateClockWise)
        self.buttonRotateClockwise.grid(row=4, rowspan=1, column=1, columnspan=1, sticky="nswe")

        self.buttonNotRotateClockWise = tk.Button(self.cameraWindow, text="ACW", command=self.rotateNotClockWise)
        self.buttonNotRotateClockWise.grid(row=4, rowspan=1, column=2, columnspan=1, sticky="nswe")

        self.buttonMirrorImg = tk.Button(self.cameraWindow, text="Mirror",command=self.mirrorImg)
        self.buttonMirrorImg.grid(row=5, rowspan=1, column=1, columnspan=2, sticky="nswe")

        self.cameraWindow.title(name)
        self.width = 315
        self.height = 235
        self.canvas = tk.Canvas(self.cameraWindow, width=self.width, height=self.height)
        self.canvas.grid(row=1, rowspan=5, column=0, columnspan=1, sticky="nswe")

    def getImage(self):

        img = self.url_to_image(self.url)

        if (not self.isImageColor):
            tmp = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            img[:,:,0] = tmp
            img[:,:,1] = tmp
            img[:,:,2] = tmp

        w = int(img.shape[1] * (self.imageScalePercentage / 100))
        h = int(img.shape[0] * (self.imageScalePercentage / 100))
        img = cv.resize(img, dsize=(w, h), interpolation=cv.INTER_AREA)
        transformationMatrix = cv.getRotationMatrix2D((w / 2, h / 2),
                                                      self.rotationAngleClockWise, 1)
        img = cv.warpAffine(img, transformationMatrix, (w, h))
        if self.mirror:
            img = cv.flip(img, 1)
        return img

    def url_to_image(self, url, readFlag=cv.IMREAD_COLOR):
        with urlopen(url) as resp:
            resp = urlopen(url)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv.imdecode(image, readFlag)
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            # return the image
        return image

    def run(self):
        while (not self.salir):
            self.image = self.getImage()
            imageForCanvas = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.image))
            self.canvas.create_image(self.width/2, self.height/2, image=imageForCanvas, anchor=tk.CENTER)
            self.checkDisabledbuttons()
            time.sleep(self.gap)

    # Methods for buttons
    def switchColorOrGray(self):
        self.isImageColor = not self.isImageColor

    def increaseSize(self):
        if (self.imageScalePercentage + 5 <= 100):
            self.imageScalePercentage += 5

    def decreaseSize(self):
        if (self.imageScalePercentage - 5 > 0):
            self.imageScalePercentage -= 5

    def decreaseGap(self):
        if (self.gap - 0.01 > 0):
            self.gap -= 0.01

    def increaseGap(self):
        if (self.gap + 0.01 < 0.5):
            self.gap += 0.01

    def rotateClockWise(self):
        self.rotationAngleClockWise -= 5

    def rotateNotClockWise(self):
        self.rotationAngleClockWise += 5

    def mirrorImg(self):
        self.mirror = not self.mirror

    def checkDisabledbuttons(self):
        # Increase scale
        if (self.imageScalePercentage + 5 <= 100):
            self.buttonIncreaseSize.config(state=tk.NORMAL)
        else:
            self.buttonIncreaseSize.config(state=tk.DISABLED)
        # Decrease scale
        if (self.imageScalePercentage - 5 >= 20):
            self.buttonDecreaseSize.config(state=tk.NORMAL)
        else:
            self.buttonDecreaseSize.config(state=tk.DISABLED)

        # Decrease gap
        if (self.gap - 0.01 > 0):
            self.buttonDecreaseGap.config(state=tk.NORMAL)
        else:
            self.buttonDecreaseGap.config(state=tk.DISABLED)
        # Increase gap
        if (self.gap + 0.01 < 0.5):
            self.buttonIncreaseGap.config(state=tk.NORMAL)
        else:
            self.buttonIncreaseGap.config(state=tk.DISABLED)




