from PyQt5.QtWidgets import (QApplication, QPushButton,QVBoxLayout, QHBoxLayout, QWidget, QApplication, QListWidget, QLabel, QFileDialog)
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt 
from PIL import Image, ImageFilter

aplic = QApplication([])
wid = QWidget()
klick1 = QPushButton('Папка')
klick2 = QPushButton('Лево')
klick3 = QPushButton('Право')
klick4 = QPushButton('Зеркало')
klick5 = QPushButton('Резкость')
klick6 = QPushButton('Ч/Б')
label = QLabel('Картинка')
klick7 = QPushButton('Отрисовка')
klick8 = QPushButton('Контурока')
klick9 = QPushButton('Рельеф')



listen = QListWidget()
lin1=QVBoxLayout()
lin2=QVBoxLayout()
lin3=QHBoxLayout()
lin4=QHBoxLayout()

lin1.addWidget(klick1)
lin1.addWidget(listen)

lin3.addWidget(klick1)
lin3.addWidget(klick2)
lin3.addWidget(klick3)
lin3.addWidget(klick4)
lin3.addWidget(klick5)
lin3.addWidget(klick6)
lin3.addWidget(klick7)
lin3.addWidget(klick8)
lin3.addWidget(klick9)


lin2.addWidget(label)
lin2.addLayout(lin3)

lin4.addLayout(lin1)
lin4.addLayout(lin2)
wid.setLayout(lin4)

workdir = ''
def filter(filenames, extensions):
    result = []
    for neme in filenames:
        for ext in extensions:
            if neme.endswith(ext):
                result.append(neme)
    return result
def choosedir():
    global workdir
    workdir = QFileDialog().getExistingDirectory()
def finale():
    extensions = ['.jpg', '.gif', '.png']
    choosedir()
    filenames = filter(os.listdir(workdir), extensions)
    for name in filenames:
        listen.addItem(name)
klick1.clicked.connect(finale)

class ImageProcessor():
    def __init__(self):
        self.Image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'
    def loadImage(self, dir, filename):
        self.dir = dir 
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        label.hide()
        pixmapimage = QPixmap(path)
        w, h = label.width(), label.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        label.setPixmap(pixmapimage)
        label.show()
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)


    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_mirow(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)


    def do_resko(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    
    def do_otrisovka(self):
        self.image = self.image.filter(ImageFilter.CONTOUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_kontr(self):
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_relief(self):
        self.image = self.image.filter(ImageFilter.EMBOSS)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if listen.currentRow() >= 0:
        filename = listen.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)





listen.currentRowChanged.connect(showChosenImage)

klick6.clicked.connect(workimage.do_bw)
klick4.clicked.connect(workimage.do_mirow)
klick3.clicked.connect(workimage.do_right)
klick2.clicked.connect(workimage.do_left)
klick5.clicked.connect(workimage.do_resko)
klick7.clicked.connect(workimage.do_otrisovka)
klick8.clicked.connect(workimage.do_kontr)
klick9.clicked.connect(workimage.do_relief)
wid.show()
aplic.exec_()
