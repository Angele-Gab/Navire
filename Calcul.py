import numpy as np
import copy
import matplotlib.pyplot as plt
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt

#fonctions

class Info_fichier_stl: # cette classe permet de manipuler les coordonnées des 3 points des facettes et des vecteurs normaux associés d'un objet stl donné en argument d'entrée

    def __init__(self, chemin): # créer deux arguments (sous forme de listes) à l'aide du chemin de l'objet stl
        liste_de_valeurs = []
        fichier = open(chemin, "r")
        lignes = fichier.readlines() #fourni le texte en chaines de caractères
        lignes = lignes[1:-1]
        for i in lignes:
            k = i.split()     #Séparation des lignes
            for j in k:
                if j.isalpha() == False:   #Stockage des valeurs numériques uniquement
                    liste_de_valeurs.append(j)
        liste_des_vecteurs = []
        while len(liste_de_valeurs) != 0:    #Séparation des valeurs par trois pour obtenir des coordonnées de vecteurs
            vecteur = [float(liste_de_valeurs[0]), float(liste_de_valeurs[1]), float(liste_de_valeurs[2])]
            liste_des_vecteurs.append(vecteur)
            liste_de_valeurs = liste_de_valeurs[3:]
        liste_des_facettes = []
        liste_des_vecteurs_normaux = []
        while len(liste_des_vecteurs) != 0:   #On sépare par la suite les coordonnées des points des vecteurs normaux de chaque facette
            facette = [liste_des_vecteurs[1], liste_des_vecteurs[2], liste_des_vecteurs[3]]
            liste_des_vecteurs_normaux.append(liste_des_vecteurs[0])
            liste_des_facettes.append(facette)
            liste_des_vecteurs = liste_des_vecteurs[4:]
        fichier.close()
        self._normal = liste_des_vecteurs_normaux #argument sous forme de liste des facettes. Une facette étant une liste des coordonnées des points qui la compose
        self._facette = liste_des_facettes

    def getf(self):
        return self._facette

    def getn(self):
        return self._normal

class Calcul :
    def __init__(self,normale,facettes):
         self._normale = normale
         self._facette = facettes


    #CALCUL D'ARCHIMEDE
    #Outils de calcul

    def ProdVect(self, u, v):   #Fonction qui calcule le produit vectoriel
        #retourne les coordonnées de w=(wx,wy,wz)=u ^v
        wx = u[1]*v[2]-u[2]*v[1] #les indices sont numérotés de 0 à 2
        wy = u[2]*v[0]-u[0]*v[2]
        wz = u[0]*v[1]-u[1]*v[0]
        w = np.array([wx, wy, wz])
        return (w)

    def Norme(self, u):    #Fonction qui calcule la norme
        return (u[0]**2+u[1]**2+u[2]**2)**(1/2)


    def Surface(self, facette): # Calcule et renvoie la norme du vecteur surface d'une facette donnés en entrée
        AB = np.array([facette[1][0]-facette[0][0], facette[1][1]-facette[0][1], facette[1][2]-facette[0][2]])
        AC = np.array([facette[2][0]-facette[0][0], facette[2][1]-facette[0][1], facette[2][2]-facette[0][2]])
        DsFk = self.Norme(self.ProdVect(AB, AC))/2
        return DsFk

    def Calculfacette(self,g, vecteur_normal,  facette):    #Fonction qui calcule la poussée d'Archimède pour chaque facette
        ro = 1000
        XG = (facette[0][0]+facette[1][0]+facette[2][0])/3
        YG = (facette[0][1]+facette[1][1]+facette[2][1])/3
        ZG = (facette[0][2]+facette[1][2]+facette[2][2])/3
        Fkx = -ro*g*np.array([XG,YG ,ZG ])[2]*self.Surface(facette)*(-vecteur_normal[0])  #Simplification possible en ne conservant que ZG
        Fky = -ro*g*np.array([XG, YG, ZG])[2]*self.Surface(facette)*(-vecteur_normal[1])   #négatif car normale sortante
        Fkz = -ro*g*np.array([XG,YG ,ZG ])[2]*self.Surface(facette)*(-vecteur_normal[2])
        return [Fkx, Fky, Fkz]    #Retourne les coordonnées de cette force

    def Calculfacettes(self,g, facettes):    #Fonction qui additionne toutes les forces pour avoir la résultante finale
        Kx = 0
        Ky = 0
        Kz = 0

        for i in range(0, len(self._normale)):
            a = facettes[i][0]
            b = facettes[i][1]
            c = facettes[i][2]
            za = a[2]
            zb = b[2]
            zc = c[2]

        # cas du calcul de la force sur une facette totalement immergée
            if za <= 0 and zb <= 0 and zc <= 0:
                Fk = self.Calculfacette(g,self._normale[i], facettes[i])
                Kx += Fk[0]
                Ky += Fk[1]
                Kz += Fk[2]

        #cas du calcul de la force sur une facette dont deux coins sont immergés (trois cas traités séparemment rendu possible parce que c'est un triangle. Point d'amélioration à traité avec plus de temps : automatisation du calcul)
            elif za <= 0 and zb <= 0:
                AzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][2])
                BzO = self.calcul_point_sur_eau(facettes[i][1], facettes[i][2])
                # triangle AzO A B
                Fk1 = self.Calculfacette(g,self._normale[i], [AzO, a, b])
                Kx += Fk1[0]
                Ky += Fk1[1]
                Kz += Fk1[2]
                # triangle AzO BzO B
                Fk2 = self.Calculfacette(g,self._normale[i], [AzO, BzO, b])
                Kx += Fk2[0]
                Ky += Fk2[1]
                Kz += Fk2[2]

            elif za <= 0 and zc <= 0:
                AzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][1])
                CzO = self.calcul_point_sur_eau(facettes[i][1], facettes[i][2])
                # triangle AzO A C
                Fk1 = self.Calculfacette(g,self._normale[i], [AzO, a, c])
                Kx += Fk1[0]
                Ky += Fk1[1]
                Kz += Fk1[2]
                # triangle AzO CzO C
                Fk2 = self.Calculfacette(g,self._normale[i], [AzO, CzO, c])
                Kx += Fk2[0]
                Ky += Fk2[1]
                Kz += Fk2[2]

            elif zb <= 0 and zc <= 0:
                CzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][2])
                BzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][1])
                # triangle CzO C B
                Fk1 = self.Calculfacette(g,self._normale[i], [CzO, c, b])
                Kx += Fk1[0]
                Ky += Fk1[1]
                Kz += Fk1[2]
                # triangle CzO BzO B
                Fk2 = self.Calculfacette(g,self._normale[i], [CzO, BzO, b])
                Kx += Fk2[0]
                Ky += Fk2[1]
                Kz += Fk2[2]

        # cas du calcul de la force sur une facette dont un coin est immergé (trois cas traités séparemment rendu possible parce que c'est un triangle. Point d'amélioration à traité avec plus de temps : automatisation du calcul)
            elif za <= 0:
                BzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][1])
                CzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][2])
                #triangle A BzO CzO
                Fk = self.Calculfacette(g,self._normale[i], [a, BzO, CzO])
                Kx += Fk[0]
                Ky += Fk[1]
                Kz += Fk[2]

            elif zb <= 0:
                AzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][1])
                CzO = self.calcul_point_sur_eau(facettes[i][1], facettes[i][2])
                #triangle B AzO CzO
                Fk = self.Calculfacette(g,self._normale[i], [b, AzO, CzO])
                Kx += Fk[0]
                Ky += Fk[1]
                Kz += Fk[2]

            elif zc <= 0:
                AzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][2])
                BzO = self.calcul_point_sur_eau(facettes[i][1], facettes[i][2])
                #triangle C AzO BzO
                Fk = self.Calculfacette(g,self._normale[i], [c, AzO, BzO])
                Kx += Fk[0]
                Ky += Fk[1]
                Kz += Fk[2]


        self._archimede = [Kx, Ky, Kz]
        return self._archimede    #Retourne les coordonnées de cette force


    def calcul_point_sur_eau(self, A, B):
        xD = ((B[0]-A[0])*(-A[2]))/(B[2]-A[2]) + A[0]
        yD = ((B[1]-A[1])*(-A[2]))/(B[2]-A[2]) + A[1]
        return [xD, yD, 0]

    #SIMULATION DE TRANSLATION SELON Z

    def Translation(self,ecart):    #Translation du bateau, modifie  les coordonnées de la liste de vecteurs et donc bouge le bateau
        liste_facettes = self._facette
        for i in liste_facettes :
            for j in i :
                j[2] += ecart
        return liste_facettes

    def TranslationListe(self,liste,ecart):   #Translation utile seulement pour la dichotomie, modifie une COPIE de la liste de coordonnées
        copie = copy.deepcopy(liste)
        for i in copie :
            for j in i :
                j[2] += ecart
        return copie

    #CALCUL DE LA DICHOTOMIE

    def Dichotomie(self,g,masse, epsilon):   #Calcul de la dichotomie, retourne la valeur mini qui correspond alors à la valeur du zéro
        X = []
        Y = []
        i = 0
        Fp = masse * 9.81   #Norme de la force poids
        #print("Fp ",Fp)
        maxi = 100
        mini = -100
        #print(self._facette[0])
        listeA = copy.deepcopy(self._facette)  #Cette fonction permet de faire des copies de listes de listes
        listeB = copy.deepcopy(self._facette)
        compteur = 0
        print("loading...")
        while abs(maxi-mini) > epsilon :    #Tant que la différence est supérieure à notre marge de précision
            compteur += 1
            #print(">> Iteration n° ",compteur)
            milieu = (maxi+mini)/2
            #print("     mini ",mini," maxi ",maxi," milieu ",milieu)

            newA = self.TranslationListe(listeA,mini)      #Création des listes translatées en fonction de l'indice de hauteur donnée par les deux indices
            newB = self.TranslationListe(listeB,milieu)
            #print("      Premier facette A",newA[0])
            #print("      Premier facette B",newB[0])
            FaA = self.Calculfacettes(g,newA)                #On calcule alors la poussé d'Archimède pour ces deux nouvelles positions
            FaB = self.Calculfacettes(g,newB)
            #print("   FA ", FaA, " FaB", FaB)
            norme_FaA = (FaA[0]**2+FaA[1]**2+FaA[2]**2)**(1/2)      #On calcule les normes des ces forces
            norme_FaB = (FaB[0]**2+FaB[1]**2+FaB[2]**2)**(1/2)
            #print("   Norme FaA ",norme_FaA," Norme FaB",norme_FaB)
            phiA = norme_FaA-Fp                                     #On calcule avec la fonction phi qui soustraie la norme de la force d'Archimède à celle du poids
            phiM = norme_FaB-Fp
            #print(phiM)

            if phiA*phiM < 0:                   #On regarde si la multiplication est négative (si on est bien toujours dans un intervalle comportant le zéro

                maxi=milieu                   #On interchange les indices en fonction du résultat pour aller dans la bonne intervalle
            else :

                mini= milieu
        #print(Y)
            #X.append(phiM)
            X.append(milieu)
            Y.append(i)
            i+=1
        X = X[1:]   #ON enlève le zéro d'initialisation
        Y = Y[1:]

        return mini,X,Y





#programme principal
#print(CalculFfacette(np.array([0, 1, 0]), np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 0, 1])))
#Lire_Stl(r"V_HULL.stl")
#Bateau = Info_fichier_stl("Rectangular_HULL_Normals_Outward.stl")
#Bateau2 = Info_fichier_stl("V_HULL_modif_toutes_coordonnees.stl")
#print(Bateau.Translation(-1))
#print(Bateau.Calculfacettes(Bateau.getf()))
#print(Bateau2.Calculfacettes())
#Calcul1 = Calcul(Bateau.getn(),Bateau.getf())
#print(Calcul1.Calculfacette(Bateau.getn()[0],Bateau.getf()[0]))
#print(Bateau.getn()[0]) #On a que le vecteur grace à l'indice
#print(Bateau.getf()[0][0])
#print(Calcul1.Dichotomie(9.81,4000, 0.002))

