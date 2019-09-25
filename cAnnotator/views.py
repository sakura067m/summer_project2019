import sys
from pathlib import Path
from itertools import chain
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QFileDialog, QMessageBox,
                             QWidget, QPushButton, QCheckBox,
                             QDialogButtonBox,
                             QLabel, QLineEdit, QProgressBar,
                             QScrollArea,
                             QVBoxLayout,QHBoxLayout,QLayout,
                             QSizePolicy,
                             QShortcut,
                             )
from PyQt5.QtCore import pyqtSignal, QThread, QObject, Qt
from PyQt5.QtGui import QPixmap, QKeySequence

import numpy as np

wd = Path(__file__).parent

class CommentAnnotator(QMainWindow):

    end = pyqtSignal()

    def __init__(self, src, mainapp, parent=None):
        super().__init__(parent)
        self.app = mainapp
        p = Path(src)
        self.root = p
        with open(wd/"labels.txt", "r") as f:
            buf = f.read()
        self.labels = buf.split()
##        print(self.labels)
        order = p.glob("*.txt")
        self._order = order
        self.data = []
        self.saved = True

        self.initUI()
        self.init_conf()

        self.step()
        
####        self.activate()

    def showThumnail(self, filename):
        with open(filename, "r") as f:
            buf = f.read()
        s = buf.replace("\n", "<br>")
        self.label.setText(s)

    def step(self):
        try:
            cue = next(self._order)
        except StopIteration:
            self.end.emit()
            return
        name = str(cue)
##        print(name)
        self.showThumnail(name)
        self.filename = name

    def process(self, btn):
        self.saved = False
##        print("******")
##        print(btn)
        filename = self.filename
        label = btn.text()
        print("filename:", self.filename)
        print("pushed:", label)
        self.data.append((filename,label))
        self.step()

    def exit(self):
        if self.saved:
            print("closing")
            self.close()

        pushed = QMessageBox.warning(None,
                                     "About to quit...",
                                     "保存しますか？",
                                     QMessageBox.Save | QMessageBox.Close
                                     )
        if QMessageBox.Save == pushed:
            self.saveone()
            
        self.close()

    def saveone(self):
        if not self.data:
            return
        while True:
            print("poo", QFileDialog.getSaveFileName)
            savename, fmt = QFileDialog.getSaveFileName(
                None,
                "Save...",
                str(self.root),
                "カンマ区切り (*.csv);;All files (*.*)"
                )
            if not fmt:
                break
            if not savename:
                continue

            with open(savename, "w") as f:
                for filename, label in self.data:
                    print("{},{}".format(filename, label),
                          file=f
                          )                      



    @classmethod
    def go(cls):
        app = QApplication(sys.argv)

        for k in range(5):
            src = QFileDialog.getExistingDirectory(None,
                                                   "Open Directory",
                                                   "./",
                                                   QFileDialog.ShowDirsOnly
                                                   )
            if not src:
                print("Canceled")
                return 1
            p = Path(src)
            break
        else:
            print("Check your directory and try again.")
            return 1

        me = cls(p, mainapp=app)
        me.show()
        exit_code = app.exec_()
        return exit_code

    def initUI(self):
        self.resize(400,300)
##        self.setSizePolicy(QSizePolicy.Fixed,
##                           QSizePolicy.Fixed
##        self.setSizePolicy(QSizePolicy.Maximum,
##                           QSizePolicy.Maximum
##                           )
##        
        ## const
        base = QWidget(self)
##        base.setSizePolicy(QSizePolicy.Maximum,
##                           QSizePolicy.Maximum
##                           )

        scrollarea = QScrollArea(base)
        label = QLabel()
        scrollarea.setWidget(label)
        scrollarea.setWidgetResizable(True)
        scrollarea.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        label.setSizePolicy(QSizePolicy.Maximum,
                           QSizePolicy.MinimumExpanding
                           )
        label.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        label.setWordWrap(True)
        self.scrollarea = scrollarea
        self.label = label

        label_buttons = QDialogButtonBox(parent=self)
        for i,s in enumerate(self.labels):
            btn = label_buttons.addButton(s, QDialogButtonBox.ActionRole)
            btn.setShortcut(QKeySequence(str(i+1)))
##            print(s)
##            dir(btn)
        label_buttons.clicked.connect(self.process)
##        print(label_buttons.buttons())
        
        cancelbutton = QPushButton("Cancel",parent=base)
####        startbutton = QPushButton("start", parent=base)
####        startbutton.setEnabled(False)
        self.cancelbutton = cancelbutton
####        startbutton.clicked.connect(self.step)
####        self.activate = lambda: startbutton.setEnabled(True)
        cancelbutton.clicked.connect(self.exit)
        self.end.connect(lambda: print("end"))

        ## arrange
        self.setCentralWidget(base)
        
        baseLO = QVBoxLayout(base)
        baseLO.setSizeConstraint(QLayout.SetMinimumSize)

        baseLO.addWidget(scrollarea)
        

        buttomLO = QHBoxLayout()
        buttomLO.addWidget(label_buttons)
        buttomLO.addStretch()
####        buttomLO.addWidget(startbutton)
        buttomLO.addWidget(cancelbutton)
        baseLO.addLayout(buttomLO)

    def init_conf(self):
        scCtrlS = QShortcut(QKeySequence("Ctrl+S"),self)
        scCtrlS.activated.connect(self.saveone)

if __name__ == "__main__":
    CommentAnnotator.go()
