import sys
from typing import Self
from PyQt5.QtWidgets import (QApplication, QFileDialog, QInputDialog, 
                            QMainWindow, QFrame, QLabel, QLineEdit, 
                            QPushButton, QComboBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PIL import Image
import os
import PIL

class App(QMainWindow):
    def __init__(self):
        super().__init__()          
        self.title = 'Image Compressor'
        self.left = 10  
        self.top = 10
        self.width = 400
        self.height = 600
        self.statusBar().showMessage("Message:")
        self.statusBar().setObjectName("status")
        self.image_width = 0
        self.setFixedSize(self.width, self.height)
        self.setObjectName("main_window")
        
        # Load stylesheet
        stylesheet = ""
        with open("design.qss", "r") as f:
            stylesheet =  f.read()
        self.setStyleSheet(stylesheet)
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Main window elements
        self.single_bubble = QFrame(self)
        self.single_bubble.setObjectName("bubble")
        self.single_bubble.move(50, 100)
        self.single_bubble.mousePressEvent = self.single_bubble_clicked

        self.single_bubble_heading = QLabel(self.single_bubble)
        self.single_bubble_heading.setObjectName("bubble_heading")
        self.single_bubble_heading.setText("Compress Image")
        self.single_bubble_heading.move(90, 8)

        self.single_bubble_para = QLabel(self.single_bubble)
        self.single_bubble_para.setObjectName("bubble_para")
        self.single_bubble_para.setText("Click here to compress single image!")
        self.single_bubble_para.move(25, 32)

        self.dir_bubble = QFrame(self)
        self.dir_bubble.setObjectName("bubble")
        self.dir_bubble.move(50, 275)
        self.dir_bubble.mousePressEvent = self.dir_bubble_clicked

        self.dir_bubble_heading = QLabel(self.dir_bubble)
        self.dir_bubble_heading.setObjectName("bubble_heading")
        self.dir_bubble_heading.setText("Compress Multiple Images")
        self.dir_bubble_heading.move(55, 8)

        self.dir_bubble_para = QLabel(self.dir_bubble)
        self.dir_bubble_para.setText("Want to compress multiple images at once? Select the folder and get compressed version of the images in another folder.")
        self.dir_bubble_para.setWordWrap(True)
        self.dir_bubble_para.setObjectName("bubble_para")
        self.dir_bubble_para.move(10, 32)
        
        # Single bubble expanded
        self.single_bubble_expanded = QFrame(self)
        self.single_bubble_expanded.setObjectName("bubble_expanded")
        self.single_bubble_expanded.move(50, 100)
        self.single_bubble_expanded.setVisible(False)

        self.back_arrow_s = QLabel(self.single_bubble_expanded)
        self.back_arrow_s.move(25, 0)
        self.back_arrow_s.setObjectName("back_arrow")
        self.back_arrow_s.setTextFormat(Qt.RichText)
        self.back_arrow_s.setText("&#8592;")
        self.back_arrow_s.mousePressEvent = self.back_arrow_clicked

        self.single_bubble_heading_expanded = QLabel(self.single_bubble_expanded)
        self.single_bubble_heading_expanded.setObjectName("bubble_heading")
        self.single_bubble_heading_expanded.setText("Compress Image")
        self.single_bubble_heading_expanded.move(90, 8)

        self.select_image_label = QLabel(self.single_bubble_expanded)
        self.select_image_label.setObjectName("bubble_para")
        self.select_image_label.setText("Choose Image")
        self.select_image_label.move(30, 50)
        
        self.image_path = QLineEdit(self.single_bubble_expanded)
        self.image_path.setObjectName("path_text")
        self.image_path.move(60, 85)

        self.browse_button = QPushButton(self.single_bubble_expanded)
        self.browse_button.setText("...")
        self.browse_button.setObjectName("browse_button")
        self.browse_button.clicked.connect(self.select_file)
        self.browse_button.move(240, 85)

        self.select_image_quality = QLabel(self.single_bubble_expanded)
        self.select_image_quality.setObjectName("bubble_para")
        self.select_image_quality.setText("Choose Quality")
        self.select_image_quality.move(30, 130)
        
        self.quality_path = QLineEdit(self.single_bubble_expanded)
        self.quality_path.setObjectName("quality_path_text")
        self.quality_path.move(60, 160)

        self.quality_combo = QComboBox(self.single_bubble_expanded)
        self.quality_combo.addItem("High")
        self.quality_combo.addItem("Medium")
        self.quality_combo.addItem("Low")
        self.quality_combo.move(170, 160)
        self.quality_combo.currentIndexChanged.connect(self.quality_current_value)
        self.quality_combo.setObjectName("quality_combo")
        self.quality_combo.resize(96, 26)

        self.btn_compress = QPushButton(self.single_bubble_expanded) 
        self.btn_compress.setText("Compress")
        self.btn_compress.setObjectName("compress_button")
        self.btn_compress.clicked.connect(self.resize_pic)
        self.btn_compress.move(100, 260)


        # Directory bubble expanded
        self.dir_bubble_expanded = QFrame(self)
        self.dir_bubble_expanded.setObjectName("bubble_expanded")
        self.dir_bubble_expanded.move(50, 100)
        self.dir_bubble_expanded.setVisible(False)

        self.back_arrow_d = QLabel(self.dir_bubble_expanded)
        self.back_arrow_d.move(25, 0)
        self.back_arrow_d.setObjectName("back_arrow")
        self.back_arrow_d.setTextFormat(Qt.RichText)
        self.back_arrow_d.setText("&#8592;")
        self.back_arrow_d.mousePressEvent = self.back_arrow_clicked

        self.dir_bubble_heading_expanded = QLabel(self.dir_bubble_expanded)
        self.dir_bubble_heading_expanded.setObjectName("bubble_heading")
        self.dir_bubble_heading_expanded.setText("Compress Multiple Images")
        self.dir_bubble_heading_expanded.move(70, 8)

        self.select_source_label = QLabel(self.dir_bubble_expanded)
        self.select_source_label.setObjectName("bubble_para")
        self.select_source_label.setText("Choose source directory")
        self.select_source_label.move(30, 50)
        
        self.source_path = QLineEdit(self.dir_bubble_expanded)
        self.source_path.setObjectName("path_text")
        self.source_path.move(60, 85)

        self.browse_source_button = QPushButton(self.dir_bubble_expanded)
        self.browse_source_button.setText("...")
        self.browse_source_button.setObjectName("browse_button")
        self.browse_source_button.clicked.connect(self.select_folder_source)
        self.browse_source_button.move(240, 85)
        
        self.select_dest_label = QLabel(self.dir_bubble_expanded)
        self.select_dest_label.setObjectName("bubble_para")
        self.select_dest_label.setText("Choose destination directory")
        self.select_dest_label.move(30, 130)
        
        self.dest_path = QLineEdit(self.dir_bubble_expanded)
        self.dest_path.setObjectName("path_text")
        self.dest_path.move(60, 160)

        self.browse_dest_button = QPushButton(self.dir_bubble_expanded)
        self.browse_dest_button.setText("...")
        self.browse_dest_button.setObjectName("browse_button")
        self.browse_dest_button.clicked.connect(self.select_folder_dest)
        self.browse_dest_button.move(240, 160)

        self.select_dir_quality = QLabel(self.dir_bubble_expanded)
        self.select_dir_quality.setObjectName("bubble_para")
        self.select_dir_quality.setText("Choose Quality")
        self.select_dir_quality.move(30, 205)
        
        self.quality_dir_path = QLineEdit(self.dir_bubble_expanded)
        self.quality_dir_path.setObjectName("quality_path_text")
        self.quality_dir_path.move(60, 235)

        self.quality_dir_combo = QComboBox(self.dir_bubble_expanded)
        self.quality_dir_combo.addItem("High")
        self.quality_dir_combo.addItem("Medium")
        self.quality_dir_combo.addItem("Low")
        self.quality_dir_combo.move(170, 235)
        self.quality_dir_combo.currentIndexChanged.connect(self.quality_current_value)
        self.quality_dir_combo.setObjectName("quality_combo")
        self.quality_dir_combo.resize(96, 26)

        self.btn_compress_dir = QPushButton(self.dir_bubble_expanded)
        self.btn_compress_dir.setText("Compress")
        self.btn_compress_dir.clicked.connect(self.resize_folder)
        self.btn_compress_dir.setObjectName("compress_button")
        self.btn_compress_dir.move(100, 290)

        self.show()

    # Functional methods
    def select_file(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", 
            "Image Files (*.jpg *.jpeg *.png)"
        )
        if fileName:
            self.image_path.setText(fileName)
            with Image.open(fileName) as img:
                self.image_width = img.width
                self.quality_path.setText(str(self.image_width))

    def select_folder_source(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if folder:
            self.source_path.setText(folder)
            files = os.listdir(folder)
            if files:
                try:
                    first_pic = os.path.join(folder, files[0])
                    with Image.open(first_pic) as img:
                        self.image_width = img.width
                        self.quality_dir_path.setText(str(self.image_width))
                except Exception as e:
                    self.statusBar().showMessage(f"Error: {str(e)}")

    def select_folder_dest(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
        if folder:
            self.dest_path.setText(folder)

    def quality_current_value(self):
        if self.quality_combo.currentText() == "High":
            self.quality_path.setText(str(self.image_width))
        elif self.quality_combo.currentText() == "Medium":
            self.quality_path.setText(str(int(self.image_width * 0.65)))
        elif self.quality_combo.currentText() == "Low":
            self.quality_path.setText(str(int(self.image_width * 0.35)))

        if self.quality_dir_combo.currentText() == "High":
            self.quality_dir_path.setText(str(self.image_width))
        elif self.quality_dir_combo.currentText() == "Medium":
            self.quality_dir_path.setText(str(int(self.image_width * 0.65)))
        elif self.quality_dir_combo.currentText() == "Low":
            self.quality_dir_path.setText(str(int(self.image_width * 0.35)))

    def back_arrow_clicked(self, event):
        self.single_bubble.setVisible(True)
        self.dir_bubble.setVisible(True)
        self.single_bubble_expanded.setVisible(False)
        self.dir_bubble_expanded.setVisible(False)

    def single_bubble_clicked(self, event):
        self.single_bubble.setVisible(False)
        self.dir_bubble.setVisible(False)
        self.single_bubble_expanded.setVisible(True)
        self.dir_bubble_expanded.setVisible(False)

    def dir_bubble_clicked(self, event):
        self.single_bubble.setVisible(False)
        self.dir_bubble.setVisible(False)
        self.single_bubble_expanded.setVisible(False)
        self.dir_bubble_expanded.setVisible(True)

    def resize_pic(self):
        old_pic = self.image_path.text()
        if not old_pic:
            self.statusBar().showMessage("Please select an image first!")
            return

        base_name = os.path.splitext(os.path.basename(old_pic))[0]
        new_pic_name, ok = QInputDialog.getText(
            self, "Save As", "File name:", 
            QLineEdit.Normal, f"{base_name}_compressed"
        )
        
        if not ok or not new_pic_name:
            return

        original_ext = os.path.splitext(old_pic)[1]
        new_name, new_ext = os.path.splitext(new_pic_name)
        final_name = new_name + (new_ext or original_ext)
        save_dir = os.path.dirname(old_pic)
        new_pic = os.path.join(save_dir, final_name)

        try:
            self.compress_image(old_pic, new_pic, int(self.quality_path.text()))
            self.statusBar().showMessage(f"Saved to: {new_pic}")
        except Exception as e:
            self.statusBar().showMessage(f"Error: {str(e)}")

    def resize_folder(self):
        source_dir = self.source_path.text()
        dest_dir = self.dest_path.text()
        
        if not source_dir or not dest_dir:
            self.statusBar().showMessage("Select both directories!")
            return

        try:
            files = [f for f in os.listdir(source_dir) 
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            total = len(files)
            for idx, filename in enumerate(files):
                old_path = os.path.join(source_dir, filename)
                new_path = os.path.join(dest_dir, filename)
                
                quality = self.quality_dir_combo.currentText()
                with Image.open(old_path) as img:
                    orig_width = img.width
                    
                    if quality == "High":
                        new_width = orig_width
                    elif quality == "Medium":
                        new_width = int(orig_width * 0.65)
                    else:
                        new_width = int(orig_width * 0.35)
                
                self.compress_image(old_path, new_path, new_width)
                
                progress = int((idx+1)/total*100)
                self.statusBar().showMessage(f"Progress: {progress}%")
                QApplication.processEvents()
            
            self.statusBar().showMessage(f"Completed! Processed {total} images")
            
        except Exception as e:
            self.statusBar().showMessage(f"Error: {str(e)}")

    def compress_image(self, input_path, output_path, target_width):
        try:
            with Image.open(input_path) as img:
                w_percent = target_width / float(img.width)
                target_height = int(float(img.height) * w_percent)
                
                resized = img.resize(
                    (target_width, target_height),
                    resample=PIL.Image.LANCZOS
                )
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                if output_path.lower().endswith('.png'):
                    resized.save(output_path, optimize=True)
                else:
                    resized.save(output_path, 
                                quality=85,
                                optimize=True,
                                progressive=True)
                                
        except Exception as e:
            raise RuntimeError(f"Processing failed: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())