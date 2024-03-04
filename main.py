from email import parser
from winreg import QueryValueEx
from icrawler.builtin import GoogleImageCrawler
import os
import sys
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout, QLineEdit 
)

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPalette, QColor

from PIL import Image

app = QApplication([])

palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.black)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.black)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)

win = QWidget()       
win.resize(700, 500) 
win.setWindowTitle('Search pictures')
lb_image = QLabel("<b>Картинки</b>")
lb_image_text = QLabel("<b>Картинки которые вы ищите будут сохраненны в папку под названием 'saved_pictures' на вышем рабочем столе которая будет созданна автоматически</b>")
lb_image2 = QLabel("<b>Поиск может занять до нескольких минут в зависимости от количества фотографий которые вы ищите, убедительная просьба, не нажимайте ничего пока не появиться надпись 'Всё найденно и загруженно'</b>")
lb_image1 = QLabel('')
btn_dir = QPushButton("Обновить содержимое папки")
lw_files = QListWidget()
btn = QPushButton('По какому запросу искать фото?(Нажми что б принять запрос фотографий)')
btn1 = QPushButton('Сколько нужно искать фото?(Нажми что б принять количество фотографий)')
btn2 = QPushButton('Искать фотграфии')

le = QLineEdit()
le1 = QLineEdit()
le.setStyleSheet("color: rgb(0, 0, 0);")
le1.setStyleSheet("color: rgb(0, 0, 0);")

row1 = QVBoxLayout()         # Основная строка

row = QHBoxLayout()          
col1 = QVBoxLayout()         # делится на два столбца
col2 = QHBoxLayout()
col3 = QHBoxLayout()
col4 = QHBoxLayout()
col5 = QHBoxLayout()
col6 = QHBoxLayout()
col7 = QHBoxLayout()
col67 = QVBoxLayout()
col66 = QHBoxLayout()
col77 = QHBoxLayout()
col88 = QHBoxLayout()
col99 = QHBoxLayout()
col110 = QHBoxLayout()

col1.addWidget(btn_dir)      # в первом - кнопка выбора директории
col1.addWidget(lw_files)     # и список файлов
col2.addWidget(lb_image_text, 95) # вo втором - картинка

col6.addWidget(lb_image1, 95)
col7.addWidget(lb_image2, 95)
col66.addWidget(lb_image1)
col77.addWidget(lb_image1)
col88.addWidget(lb_image1)
col99.addWidget(lb_image1)
col110.addWidget(lb_image1)
col3.addWidget(btn)
col4.addWidget(btn1)
col3.addWidget(le)
col4.addWidget(le1)
col5.addWidget(btn2)
col67.addLayout(col2)
col67.addLayout(col7)
col67.addLayout(col66)
col67.addLayout(col77)
col67.addLayout(col88)
col67.addWidget(lb_image, 95) #-------------------
col67.addLayout(col99)
col67.addLayout(col110)
col67.addLayout(col6)
row.addLayout(col1, 20)
row.addLayout(col2, 80)
row.addLayout(col67)


row1.addLayout(row)
row1.addLayout(col4)
row1.addLayout(col3)
row1.addLayout(col5)
win.setLayout(row1)
 
win.show()

folder_name = '' 
path = ''

def create_floder(folder_name, path):
    _fold_name = folder_name.replace(':', ' ').replace('.', ' ')
    _path = path

    if not(os.path.exists(_path+'/'+_fold_name)):
        os.chdir(_path)
        os.mkdir(_fold_name)
    else:
        print('Folder named '+folder_name+' already exists')

folder_names = ['saved_pictures']
pathh = 'C:/Users/User/Desktop'

for name in folder_names:
    create_floder(name, pathh)
create_floder(folder_name, path)
workdir = 'C:/Users/User/Desktop/saved_pictures'

def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result
 
def chooseWorkdir():
    global workdir

def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)
 
   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)
       chooseWorkdir()

showFilenamesList()
btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():

    def __init__(self):
        self.windows = []
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
        self.count = -1
        self.actions = list()

    def loadImage(self, filename):
        ''' при загрузке запоминаем путь и имя файла '''
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)

    def saveImage(self):
        ''' сохраняет копию файла в подпапке '''
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

def showChosenImage():
    if lw_files.currentRow() >= 0:
       filename = lw_files.currentItem().text()
       workimage.loadImage(filename)
       workimage.showImage(os.path.join(workdir, workimage.filename))

def parser_photo():
    google_crawler = GoogleImageCrawler(storage={'root_dir' : 'C:/Users/User/Desktop/saved_pictures'})
    quantity = int(le1.text())
    name = str(le.text())
    google_crawler.crawl(keyword=name, max_num=quantity)
    print('all done')
    lb_image1.setText('<b><u>Всё найденно и загруженно</u></b>')

def number_of_photos():
    quantity = int(le1.text())
    print(str(quantity))

def photo_title():
    name = str(le.text())
    print(name)

workimage = ImageProcessor() #текущая рабочая картинка для работы

lw_files.currentRowChanged.connect(showChosenImage)
 
btn.clicked.connect(photo_title)
btn1.clicked.connect(number_of_photos)
btn2.clicked.connect(parser_photo)

app.exec()
