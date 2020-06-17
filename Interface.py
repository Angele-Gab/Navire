import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from PySide2.QtWidgets import *
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
#from erreur import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon

class Interface(QWidget):
    def __init__(self,stl):
        QWidget.__init__(self)

        #Partie 3D

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.__ax = plt.axes(projection='3d')
        self.__your_mesh = mesh.Mesh.from_file(stl)
        self.__ax.add_collection3d(mplot3d.art3d.Poly3DCollection(self.__your_mesh.vectors))
        scale = self.__your_mesh.points.flatten("C")
        self.__ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        self.canvas.setFixedSize(500,500)

        #Partie 2D

        self.fig2 = plt.figure()
        self.canvas2 = FigureCanvas(self.fig2)
        self.__ax2 = plt.axes()

        X=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
        Y=[39240.0, -39240.0, 39240.0, -39240.0, 39240.0, 39240.0, 39240.0, -39240.0, 39240.0, 9810.0, 9810.0, -39240.0, 9810.0, -26977.5, 9810.0, -8583.75, 9810.0, 613.125, 613.125, -3985.3125, 613.125, -1686.09375, 613.125, -536.484375, 613.125, 38.3203125, 38.3203125, -249.08203125, 38.3203125, -105.380859375, 38.3203125, -33.5302734375, 38.3203125, 2.39501953125, 2.39501953125, -15.567626953125, 2.39501953125, -6.5863037109375]

        self.__ax2.plot(X,Y, color = "red")
        plt.title("Titre")
        plt.xlabel("Abscisse")
        plt.ylabel("Ordonnée")
        self.canvas2.draw()
        self.canvas2.setFixedSize(750,500)



        self.layout = QGridLayout()
        self.setWindowTitle("Boat sinking interface")
        self.setFixedSize(1300, 800)
        Icon = QIcon("Abeille_Bourbon-6455_xlarge.png")
        self.setWindowIcon(Icon)


        self.button1 = QPushButton("Lancer")
        self.button1.setFixedSize(200,100)


        self.layout.addWidget(self.button1,0,2,1,1)
        self.layout.addWidget(self.canvas,1,1,1,1)
        self.layout.addWidget(self.canvas2,1,2,1,1)


        self.button1.clicked.connect(self.buttonLoad3DClicked)

        self.setLayout(self.layout)



    def buttonLoad3DClicked(self):
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.__ax.remove()
        self.__ax = plt.axes(projection='3d')
        self.__your_mesh.translate([0, 0,-1])
        self.__ax.add_collection3d(mplot3d.art3d.Poly3DCollection(self.__your_mesh.vectors))
        scale = self.__your_mesh.points.flatten("C")

        self.__ax.auto_scale_xyz(scale, scale, scale)
        self.layout.addWidget(self.canvas,1,1,1,1)







class Parametres(QWidget) :
    def __init__(self):
        QWidget.__init__(self)
        self.__isClosed =0
        self.__erreur =1

        self.setWindowTitle("Paramétrages")
        self.setFixedSize(400, 200)

        self.layout = QGridLayout()

        self.__stl=""
        self.__masse=""
        self.__precision=""
        self.__gravite=""

        self.label = QLabel("Entrez les paramètres :")
        self.label1= QLabel("Fichier STL :")
        self.label2= QLabel("Masse :")
        self.label3= QLabel("Précision :")
        self.label4 = QLabel("Gravité :")
        self.button = QPushButton("Valider")
        self.edit1= QLineEdit()
        self.edit2= QLineEdit()
        self.edit3= QLineEdit()
        self.edit4= QLineEdit()


        self.layout.addWidget(self.label,0,0,1,2)
        self.layout.addWidget(self.label1,1,0)

        self.layout.addWidget(self.label2,2,0)
        self.layout.addWidget(self.label3,3,0)
        self.layout.addWidget(self.label4,4,0)

        self.layout.addWidget(self.edit1,1,1)
        self.layout.addWidget(self.edit2,2,1)
        self.layout.addWidget(self.edit3,3,1)
        self.layout.addWidget(self.edit4,4,1)
        self.layout.addWidget(self.button,6,0,1,2)

        self.button.clicked.connect(self.buttonClicked)


        self.setLayout(self.layout)

    def getClosed(self):
        return self.__isClosed

    def getSTL(self):
        return self.__stl
    def getEr(self):
        return self.__erreur


    def formatstl(self,stl):
        if stl[-4:]==".stl":
            return stl
        else:
            stl =stl+".stl"
            return stl

    def buttonClicked(self):
        self.__stl =self.edit1.text()
        self.__masse = self.edit2.text()
        self.__precision = self.edit3.text()
        self.__gravite = self.edit4.text()

        if self.isEmpty(self.__stl,self.__masse,self.__precision,self.__gravite)==True:
            self.label = QLabel("Vérifiez vos informations")
            self.layout.addWidget(self.label, 5, 0, 1, 2)
            self.setLayout(self.layout)
            return
        if self.__masse.isalpha()!=False or self.__precision.isalpha()!=False or self.__gravite.isalpha()!=False:
            self.label = QLabel("Vérifiez vos informations")
            self.layout.addWidget(self.label, 5, 0, 1, 2)
            self.setLayout(self.layout)
            return





        self.__stl=self.formatstl(self.__stl)
        self.__masse=float(self.__masse)
        self.__precision=float(self.__precision)
        self.close()
        self.__isClosed = 1

    def isEmpty(self,stl,masse,precision,gravite):
        if stl=="" or masse=="" or precision=="" or gravite=="":
            return True
        else:
            return False










if __name__ == "__main__":
    app = QApplication([])


    winP = Parametres()
    winP.show()
    app.exec_()
    while winP.getClosed() == 0:
        None


    win =Interface(winP.getSTL())
    win.show()
    app.exec_()
