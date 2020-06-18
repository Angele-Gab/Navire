import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from PySide2.QtWidgets import *
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from Clair import *

class Interface(QWidget):
    def __init__(self,stl,masse,epsilon,g):
        QWidget.__init__(self)


        Fichier = Info_fichier_stl(stl)   #Récupération des données du fichier stl demandé
        liste_normales=Fichier.getn()
        liste_facettes=Fichier.getf()
        Calcul1 = Calcul(liste_normales,liste_facettes)
        self.__equilibre = Calcul1.Dichotomie(g,masse, epsilon)[0]   #Récupération de la profondeur d'équilibre déterminée avec la dichotomie
        self.__Y = Calcul1.Dichotomie(g,masse, epsilon)[1]   #Récupération de la liste des valeurs prises par la dichotomie
        self.__X = Calcul1.Dichotomie(g,masse, epsilon)[2]   #Récupération de la liste du nombre d'itérations de la dichotomie

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


        self.__ax2.plot()
        plt.title("Détermination de la position d'équilibre",color = "blue")
        plt.xlabel("Nombre d'itérations")
        plt.ylabel("Profondeur")
        self.canvas2.draw()
        self.canvas2.setFixedSize(750,500)



        self.layout = QGridLayout()
        self.setWindowTitle("Boat sinking interface")
        self.setFixedSize(1300, 800)
        Icon = QIcon("Abeille_Bourbon.png")
        self.setWindowIcon(Icon)


        self.button1 = QPushButton("Lancer")
        self.button1.setFixedSize(200,100)


        self.layout.addWidget(self.button1,0,2,1,1)
        self.layout.addWidget(self.canvas,1,1,1,1)
        self.layout.addWidget(self.canvas2,1,2,1,1)


        self.button1.clicked.connect(self.buttonLoad3DClicked)

        self.setLayout(self.layout)



    def buttonLoad3DClicked(self):

        # 3D
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.__ax.remove()
        self.__ax = plt.axes(projection='3d')
        self.__your_mesh.translate([0, 0, self.__equilibre])
        self.__ax.add_collection3d(mplot3d.art3d.Poly3DCollection(self.__your_mesh.vectors))
        scale = self.__your_mesh.points.flatten("C")

        self.__ax.auto_scale_xyz(scale, scale, scale)
        self.layout.addWidget(self.canvas,1,1,1,1)

        #2D

        self.fig2 = plt.figure()
        self.canvas2 = FigureCanvas(self.fig2)
        self.__ax2 = plt.axes()
        self.__ax2.plot(self.__X, self.__Y, "b-x", color = "red")   #Tracé du graphique
        #self.canvas2.draw()
        self.layout.addWidget(self.canvas2,1,2,1,1)




class Parametres(QWidget) :
    def __init__(self):
        QWidget.__init__(self)
        self.__isClosed =0
        self.__erreur =1

        self.setWindowTitle("Paramétrages")
        self.setFixedSize(400, 200)

        Icon = QIcon("Parametre.png")
        self.setWindowIcon(Icon)


        self.layout = QGridLayout()

        self.__stl=""
        self.__masse=""
        self.__precision=""
        self.__gravite=""

        self.label = QLabel("Entrez les paramètres")
        self.label.setStyleSheet("QLabel { font : 13pt ; }")
        self.label.setAlignment(Qt.AlignCenter)

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

    def getMasse(self):
        return self.__masse

    def getGravite(self):
        return self.__gravite

    def getPrecision(self):
        return self.__precision


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
            self.label = QLabel("Vérifiez vos informations !")
            self.label.setStyleSheet("color : #F24C04;")
            self.label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.label, 5, 0, 1, 2)
            self.setLayout(self.layout)
            return
        if self.__masse.isalpha()!=False or self.__precision.isalpha()!=False or self.__gravite.isalpha()!=False:
            self.label = QLabel("Vérifiez vos informations !")
            self.label.setStyleSheet("color : #F24C04;")
            self.label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.label, 5, 0, 1, 2)
            self.setLayout(self.layout)
            return







        self.__stl = self.formatstl(self.__stl)
        self.__masse = float(self.__masse)
        self.__precision = float(self.__precision)
        self.__gravite = float(self.__gravite)
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


    win =Interface(winP.getSTL(),winP.getMasse(),winP.getPrecision(),winP.getGravite())
    win.show()
    app.exec_()

