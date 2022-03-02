from PyQt5 import QtWidgets, QtGui
from ui1 import Ui_MainWindow
import sys
import inpaint
import cv2
from PyQt5.QtGui import QImage, QPixmap
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.setFont(QtGui.QFont('Arial', 15))
        self.ui.label.setText('picture path:')
        self.ui.label_2.setFont(QtGui.QFont('Arial', 15))
        self.ui.label_2.setText('save path:')        
        self.ui.label_3.setText('') 
        self.ui.label_4.setFont(QtGui.QFont('Arial', 15))
        self.ui.label_4.setText('text path:') 
        self.ui.pushButton.setText('select')
        self.ui.pushButton_2.setText('inpaint')
        self.ui.pushButton_3.setText('select')
        self.ui.pushButton_4.setText('save')
        self.ui.pushButton_5.setText('select')
        self.ui.textEdit.clear()
        self.ui.textEdit_2.clear()
        self.ui.textEdit_3.clear()
        self.ui.pushButton.clicked.connect(self.buttonClicked)
        self.ui.pushButton_2.clicked.connect(self.buttonClicked_2)
        self.ui.pushButton_3.clicked.connect(self.buttonClicked_3)
        self.ui.pushButton_4.clicked.connect(self.buttonClicked_4)
        self.ui.pushButton_5.clicked.connect(self.buttonClicked_5)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QColor(17, 77, 125))
        self.setPalette(palette)
        #self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        
    def buttonClicked(self):
            text = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.')[0]
            #print(text)
            self.ui.textEdit.setText(text)
    def buttonClicked_2(self):
            global savepath,path,img,tp
            path = self.ui.textEdit.toPlainText()
            tp = self.ui.textEdit_3.toPlainText()
            img = inpaint.inpaint(path,tp)
            self.showImage()
    def buttonClicked_3(self):
            text = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open File', '.')
            #print(text)
            self.ui.textEdit_2.setText(text)
    def buttonClicked_4(self):
        savepath = self.ui.textEdit_2.toPlainText()
        sp = savepath + "//final.jpg"
        cv2.imwrite(sp, img)
        print(sp)
        print('saved')
    def buttonClicked_5(self):
            text = QtWidgets.QFileDialog.getExistingDirectory(self, 'Open File', '.')
            self.ui.textEdit_3.setText(text)

    def showImage(self):
        
        self.img2 = img.copy()
        self.img2 = cv2.resize(self.img2,(400, 400),interpolation=cv2.INTER_AREA)

        if self.img2.size == 1:
            return

        height, width, channel = self.img2.shape
        bytesPerline = 3 * width
        self.qImg = QImage(self.img2.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.ui.label_3.setPixmap(QPixmap.fromImage(self.qImg))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
 
