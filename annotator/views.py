import sys
from pathlib import Path
from itertools import chain
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QFileDialog,
                             QWidget, QPushButton, QCheckBox,
                             QLabel, QLineEdit, QProgressBar,
                             QScrollArea,
                             QVBoxLayout,QHBoxLayout,QLayout,
                             QSizePolicy
                             )
from PyQt5.QtCore import pyqtSignal, QThread, QObject, Qt
from PyQt5.QtGui import QPixmap


class ImgAnnotator(QMainWindow):

    end = pyqtSignal()

    def __init__(self, src, mainapp, parent=None):
        super().__init__(parent)
        p = Path(src)
        self.root = p
        order = chain(p.glob("*.jpg"), p.glob("*.png"), p.glob("*.bmp"))
        self._order = order

        self.initUI()

        self.step()
        
        self.activate()

        print(self.size())

    def showThumnail(self, filename):
        label = self.thumnail
        pxmap = QPixmap(filename)
        label.setPixmap(pxmap)
##        label.setPixmap(
##            pxmap.scaled(
##                self.scrollarea.viewportSizeHint(),
##                Qt.KeepAspectRatio,
##                Qt.SmoothTransformation
##                )
##            )

    def step(self):
        try:
            cue = next(self._order)
        except StopIteration:
            self.end.emit()
            return
        name = str(cue)
        self.showThumnail(name)
        self.filename = name


    @classmethod
    def go(cls):
        app = QApplication(sys.argv)

        for k in range(5):
            src = QFileDialog.getExistingDirectory(None,
                                                   "Open Directory",
                                                   "../Fuji",
                                                   QFileDialog.ShowDirsOnly
                                                   )
            if not src:
                print("Canceled")
                return 1
            p = Path(src)
            if (p/"labels.txt").exists(): break
            else: print("labels.txt does not found.")
        else:
            print("Check your directory and try again.")
            return 1

        me = cls(p, mainapp=app)
        me.show()
        app.exec_()

    def initUI(self):
        self.resize(400,300)
##        self.setSizePolicy(QSizePolicy.Fixed,
##                           QSizePolicy.Fixed
        self.setSizePolicy(QSizePolicy.Maximum,
                           QSizePolicy.Maximum
                           )
        
        ## const
        base = QWidget(self)
        base.setSizePolicy(QSizePolicy.Maximum,
                           QSizePolicy.Maximum
                           )

        scrollarea = QScrollArea(base)
        self.scrollarea = scrollarea
        scrollarea.setSizePolicy(QSizePolicy.MinimumExpanding,
                               QSizePolicy.MinimumExpanding
                               )
        scrollarea.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)

        thumnail = QLabel(scrollarea)
##        thumnail.setScaledContents(True)
##        thumnail.resize(300,400)
        self.thumnail = thumnail
        thumnail.setSizePolicy(QSizePolicy.Maximum,
                               QSizePolicy.Maximum
                               )
        print(thumnail.size())
        scrollarea.setWidget(thumnail)
        scrollarea.setWidgetResizable(True)
        
        cancelbutton = QPushButton("Cancel",parent=base)
        startbutton = QPushButton("start", parent=base)
        startbutton.setEnabled(False)
        self.cancelbutton = cancelbutton
        self.canceled = cancelbutton.clicked
        startbutton.clicked.connect(self.step)
        self.activate = lambda: startbutton.setEnabled(True)

        ## arrange
        self.setCentralWidget(base)
        
        baseLO = QVBoxLayout(base)
        baseLO.setSizeConstraint(QLayout.SetMinimumSize)

        baseLO.addWidget(scrollarea)
        

        buttomLO = QHBoxLayout()
        buttomLO.addStretch()
        buttomLO.addWidget(startbutton)
        buttomLO.addWidget(cancelbutton)
        baseLO.addLayout(buttomLO)

if __name__ == "__main__":
    ImgAnnotator.go()
