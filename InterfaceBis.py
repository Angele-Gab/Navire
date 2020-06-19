import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from PySide2.QtWidgets import *
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from Calcul import *

class Interface(QWidget):     #Classe de la deuxième IHM ouverte
    def __init__(self,stl,masse,epsilon,g):
        QWidget.__init__(self)

        self.__stl = stl
        self.__iseq = False   #Création d'un argument pour ne pas bouger le bateau à l'infini


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


        self.__your_mesh = mesh.Mesh.from_file(self.__stl)
        self.__ax.add_collection3d(mplot3d.art3d.Poly3DCollection(self.__your_mesh.vectors))
        scale = self.__your_mesh.points.flatten("C")

        self.__ax.auto_scale_xyz(scale, scale, scale)
        plt.title("Représentation 3D",color = "darkcyan")
        self.canvas.draw()
        self.canvas.setFixedSize(500,500)

        self.setStyleSheet("background-color: rgb(17,69,93);") #Changement de la couleur de fond


        #Partie 2D

        self.fig2 = plt.figure()
        self.canvas2 = FigureCanvas(self.fig2)
        self.__ax2 = plt.axes()


        self.__ax2.plot()
        plt.title("Détermination de la position d'équilibre",color = "darkcyan")
        plt.xlabel("Nombre d'itérations")
        plt.ylabel("Profondeur")
        self.canvas2.draw()
        self.canvas2.setFixedSize(750,500)

        #Layout de l'IHM

        self.layout = QGridLayout()
        self.setWindowTitle("Boat Sinking Interface")
        self.setFixedSize(1380, 700)
        Icon = QIcon("Abeille_Bourbon.png")
        self.setWindowIcon(Icon)


        self.button1 = QPushButton("Lancer")
        self.button1.setStyleSheet("QPushButton { font : 18pt ;color : white }")
        #self.button1.setStyleSheet("QPushButton { color : blue }")
        self.button1.setFixedSize(200,100)


        self.layout.addWidget(self.button1,0,2,1,1)
        self.layout.addWidget(self.canvas,1,1,1,1)
        self.layout.addWidget(self.canvas2,1,2,1,1)



        self.button1.clicked.connect(self.buttonLoad3DClicked)

        self.setLayout(self.layout)



    def buttonLoad3DClicked(self):    #Fontionc appliquée au "clic" du bouton

        # 3D
        if self.__iseq == False :    #Permet de ne pas pouvoir retranslater le bateau une fois la position d'équilibre atteinte
            self.fig = plt.figure()       #Une fois lancer la simulation translate le bateau à sa position d'équilibre
            self.canvas = FigureCanvas(self.fig)
            self.__ax.remove()
            self.__ax = plt.axes(projection='3d')
            self.__your_mesh.translate([0, 0, self.__equilibre])
            self.__ax.add_collection3d(mplot3d.art3d.Poly3DCollection(self.__your_mesh.vectors))
            scale = self.__your_mesh.points.flatten("C")

            self.__ax.auto_scale_xyz(scale, scale, scale)
            #hfont = {'fontname':'Comic Sans MS'}
            plt.title("Représentation 3D",color = "darkcyan")
            self.layout.addWidget(self.canvas,1,1,1,1)
            self.__iseq = True

        #2D

        self.fig2 = plt.figure()
        self.canvas2 = FigureCanvas(self.fig2)
        self.__ax2 = plt.axes()
        plt.title("Détermination de la position d'équilibre",color = "darkcyan")
        plt.xlabel("Nombre d'itérations")
        plt.ylabel("Profondeur")
        self.__ax2.plot(self.__X, self.__Y, "b-x", color = "indianred")   #Tracé du graphique
        #self.canvas2.draw()
        self.layout.addWidget(self.canvas2,1,2,1,1)




class Parametres(QWidget) :    #Classe de la première IHM
    def __init__(self):
        QWidget.__init__(self)
        self.__isClosed = False      #Argument permettant de ne pas fermer l'IHM et de ne pas ouvrir la suivante avant que les valeurs rentrées ne soient complètes


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
        self.label.setStyleSheet("QLabel { font : 13pt ; }")   #Changement de la taille du texte
        self.label.setAlignment(Qt.AlignCenter)

        self.label1= QLabel("Fichier STL :")        #Création d'entrées de textes
        self.label2= QLabel("Masse :")
        self.label3= QLabel("Précision :")
        self.label4 = QLabel("Gravité :")
        self.button = QPushButton("Valider")

        self.deroulement = QComboBox()    #Utilisation d'un dérouleur pour sélectionner le bateau choisi
        self.deroulement.addItem("Abeille_Bourbon.stl")     #Ajout de tous les bateaux disponibles
        self.deroulement.addItem("Rectangle.stl")
        self.deroulement.addItem("Cylindre.stl")
        self.deroulement.addItem("BargeAlu.stl")
        self.deroulement.addItem("SousMarin.stl")
        self.deroulement.addItem("Wigley.stl")
        self.deroulement.addItem("TriEqui_INCLINE.stl")
        self.deroulement.addItem("TriEquiHoriz_Z=0.stl")
        self.deroulement.addItem("TriEquiHoriz_Z=-2.stl")
        self.deroulement.addItem("TriRectHoriz_Z=0.stl")
        self.deroulement.addItem("TriRectHoriz_Z=-1.stl")
        self.deroulement.addItem("TriRect_INCLINE.stl")


        self.edit2= QLineEdit()     #Permet à l'utilisateur d'entrer les valeurs désirées
        self.edit3= QLineEdit()
        self.edit4= QLineEdit()


        self.layout.addWidget(self.label,0,0,1,2)    #Positionnement des élèments dans le layout
        self.layout.addWidget(self.label1,1,0)

        self.layout.addWidget(self.label2,2,0)
        self.layout.addWidget(self.label3,3,0)
        self.layout.addWidget(self.label4,4,0)

        self.layout.addWidget(self.deroulement,1,1)
        self.layout.addWidget(self.edit2,2,1)
        self.layout.addWidget(self.edit3,3,1)
        self.layout.addWidget(self.edit4,4,1)
        self.layout.addWidget(self.button,6,0,1,2)

        self.button.clicked.connect(self.buttonClicked)    #Appel de la fonction qui connecte le bouton à sa fonctionnalité


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



    def buttonClicked(self):

        self.__stl =self.deroulement.currentText ()   #Récupération des informations rentrées par l'utilisateur
        self.__masse = self.edit2.text()
        self.__precision = self.edit3.text()
        self.__gravite = self.edit4.text()

        if self.isEmpty(self.__stl,self.__masse,self.__precision,self.__gravite)==True:   #Vérification que les informations sont présentes
            self.label = QLabel("Vérifiez vos informations !")
            self.label.setStyleSheet("color : #F24C04;")
            self.label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.label, 5, 0, 1, 2)
            self.setLayout(self.layout)                                                    #Sinon, envoie un message d'erreur
            return
        if self.__masse.isalpha()!=False or self.__precision.isalpha()!=False or self.__gravite.isalpha()!=False:   #Vérification que les informations sont au bon format
            self.label = QLabel("Vérifiez vos informations !")
            self.label.setStyleSheet("color : #F24C04;")
            self.label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(self.label, 5, 0, 1, 2)
            self.setLayout(self.layout)                                                                             #Sinon, envoie un message d'erreur
            return



        self.__masse = float(self.__masse)
        self.__precision = float(self.__precision)
        self.__gravite = float(self.__gravite)
        self.close()
        self.__isClosed = True                      #Permet de lancer la seconde IHM

    def isEmpty(self,stl,masse,precision,gravite):    #Vérification des informations entrées
        if stl=="" or masse=="" or precision=="" or gravite=="":
            return True
        else:
            return False





#Programme principal

if __name__ == "__main__":
    app = QApplication([])


    winP = Parametres()
    winP.show()
    app.exec_()
    while winP.getClosed() == False :    #Bloque l'avancement du programme tant que la fenêtre paramètres est ouverte
        None


    win =Interface(winP.getSTL(),winP.getMasse(),winP.getPrecision(),winP.getGravite())
    win.show()
    app.exec_()

