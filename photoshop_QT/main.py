from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QComboBox, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os
from PIL import Image, ImageEnhance, ImageFilter

app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("photoshop")
main_window.resize(999, 777)

btn_folder = QPushButton("Folder")
file_list = QListWidget()

btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
mirror = QPushButton("Mirror")
sharpness = QPushButton("Sharpness")
gray = QPushButton("Gray")
saturation = QPushButton("Saturation")
contrast = QPushButton("Contrast")
blur = QPushButton("Blur")

filter_box = QComboBox()
filter_box.addItems(["Original", "Left", "Right", "Mirror", "Sharpness", "Gray", "Saturation", "Contrast", "Blur"])

picture_box = QLabel("Image will appear here")
picture_box.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the label text/image

master_layout = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_folder)
col1.addWidget(file_list)
col1.addWidget(filter_box)
col1.addWidget(btn_left)
col1.addWidget(btn_right)
col1.addWidget(mirror)
col1.addWidget(sharpness)
col1.addWidget(gray)
col1.addWidget(saturation)
col1.addWidget(contrast)
col1.addWidget(blur)

col2.addWidget(picture_box)

master_layout.addLayout(col1,20)
master_layout.addLayout(col2,80)

main_window.setLayout(master_layout)

working_dir = ""

def filter(files, extention):
    results = []
    for file in files:
        for ext in extention:
            if file.endswith(ext):
                results.append(file)
    return results
    
def getworkdir():
    global working_dir
    working_dir = QFileDialog.getExistingDirectory()
    extentions = ['.jpg','.jpeg','.png','.svg']
    filenames = filter(os.listdir(working_dir),extentions)
    file_list.clear()
    for filename in filenames:
        file_list.addItem(filename)
        
class Editor():
    def __init__(self):
        self.image = None
        self.Original = None
        self.filename = None
        self.save_folder = "edits/"
        
    def load_image(self, filename):
        self.filename = filename
        fullname = os.path.join(working_dir, self.filename)
        self.image = Image.open(fullname)
        self.Original = self.image.copy()
        
    def save_image(self):
        path = os.path.join(working_dir, self.save_folder)
        if not(os.path.exists(path) and os.path.isdir(path)):
            os.mkdir(path)
        
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
  
    def show_image(self, path):
        picture_box.hide()
        image = QPixmap(path)
        w, h =picture_box.width(), picture_box.height()
        image = image.scaled(w, h,  Qt.AspectRatioMode.KeepAspectRatio)
        picture_box.setPixmap(image)
        picture_box.show()

    def gray (self):
        self.image = self.image.convert("L")
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)

    def left (self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)

    def right (self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)

    def mirror (self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)

    def sharpen (self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)

    def blur (self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)

    def color (self):
        self.image = ImageEnhance.Color(self.image).enhance(1.2)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)

    def contrast (self):
        self.image = ImageEnhance.Contrast(self.image).enhance(1.2)
        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)

    def apply_filter(self, filter_name):
        mapping = {
            "Gray": lambda image: image.convert("L"),
            "Saturation": lambda image: ImageEnhance.Color(image).enhance(1.2),
            "Contrast": lambda image: ImageEnhance.Contrast(image).enhance(1.2),
            "Blur": lambda image: image.filter(ImageFilter.BLUR),
            "Sharpness": lambda image: image.filter(ImageFilter.SHARPEN),
            "Left": lambda image: image.transpose(Image.ROTATE_90),
            "Right": lambda image: image.transpose(Image.ROTATE_270),
            "Mirror": lambda image: image.transpose(Image.FLIP_LEFT_RIGHT),
        }
        
        if filter_name == "Original":
            self.image = self.Original.copy()
        else:
            filter_function = mapping.get(filter_name)
            if filter_function:
                self.image = filter_function(self.image)

        self.save_image()
        image_path = os.path.join(working_dir, self.save_folder, self.filename)
        self.show_image(image_path)

        

def handle_filter():
    if file_list.currentRow() >= 0:
        select_filter = filter_box.currentText()
        main.apply_filter(select_filter)

def displayImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        main.load_image(filename)
        main.show_image(os.path.join(working_dir, main.filename))

main = Editor()

btn_folder.clicked.connect(getworkdir)
file_list.currentRowChanged.connect(displayImage)
filter_box.currentTextChanged.connect(handle_filter)

gray.clicked.connect(main.gray)
btn_left.clicked.connect(main.left)
btn_right.clicked.connect(main.right)
mirror.clicked.connect(main.mirror)
sharpness.clicked.connect(main.sharpen)
blur.clicked.connect(main.blur)
contrast.clicked.connect(main.contrast)
saturation.clicked.connect(main.color)

main_window.show()  
app.exec()
