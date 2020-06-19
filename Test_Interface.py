from PySide2.QtWidgets import *

class deuxieme_fenetre(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("Test 2")
        self.setMinimumSize(600, 400)
        self.layout = QVBoxLayout()

        self.label = QLabel("fenêtre 2")
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

class premiere_fenetre(QWidget):

    def __init__(self):
        self.__test = 0

        QWidget.__init__(self)

        self.setWindowTitle("Test 1")
        self.setMinimumSize(600, 400)
        self.layout = QVBoxLayout()

        self.button = QPushButton("ici")
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.buttonClicked)

        self.setLayout(self.layout)

    def buttonClicked(self):
        self.close()
        self.__test = 1

    def gettest(self):
        return self.__test




# programme principal

if __name__ ==  "__main__":
    app = QApplication([])
    win1 = premiere_fenetre()
    win1.show()
    app.exec_()
    while win1.gettest() == 0:
        None
    win2 = deuxieme_fenetre()
    win2.show()
    app.exec_()
