import numpy as np
import copy
import matplotlib.pyplot as plt

#fonctions

class Info_fichier_stl: # cette classe permet de manipuler les coordonnées des 3 points des facettes et des vecteurs normaux associés d'un objet stl donné en argument d'entrée

    def __init__(self, chemin): # créer deux arguments (sous forme de listes) à l'aide du chemin de l'objet stl
        liste_de_valeurs = []
        fichier = open(chemin, "r")
        lignes = fichier.readlines() #fourni le texte en chaines de caractères
        lignes = lignes[1:-1]
        for i in lignes:
            k = i.split()
            for j in k:
                if j.isalpha() == False:
                    liste_de_valeurs.append(j)
        liste_des_vecteurs = []
        while len(liste_de_valeurs) != 0:
            vecteur = [float(liste_de_valeurs[0]), float(liste_de_valeurs[1]), float(liste_de_valeurs[2])]
            liste_des_vecteurs.append(vecteur)
            liste_de_valeurs = liste_de_valeurs[3:]
        liste_des_facettes = []
        liste_des_vecteurs_normaux = []
        while len(liste_des_vecteurs) != 0:
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

    def getfacette(self):
        return self._facette


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

    def Calculfacette(self, vecteur_normal, facette):    #Fonction qui calcule la poussée d'Archimède pour chaque facette
        ro = 1000
        g = 9.81
        XG = (facette[0][0]+facette[1][0]+facette[2][0])/3
        YG = (facette[0][1]+facette[1][1]+facette[2][1])/3
        ZG = (facette[0][2]+facette[1][2]+facette[2][2])/3
        Fkx = -ro*g*np.array([XG,YG ,ZG ])[2]*self.Surface(facette)*(-vecteur_normal[0])  #Simplification possible en ne conservant que ZG
        Fky = -ro*g*np.array([XG, YG, ZG])[2]*self.Surface(facette)*(-vecteur_normal[1])   #négatif car normale sortante
        Fkz = -ro*g*np.array([XG,YG ,ZG ])[2]*self.Surface(facette)*(-vecteur_normal[2])
        return [Fkx, Fky, Fkz]    #Retourne les coordonnées de cette force

    def Calculfacettes(self, facettes):    #Fonction qui additionne toutes les forces pour avoir la résultante finale
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
            print (za, zb, zc)

        # cas du calcul de la force sur une facette totalement immergée
            if za <= 0 and zb <= 0 and zc <= 0:
                Fk = self.Calculfacette(self._normale[i], facettes[i])
                Kx += Fk[0]
                Ky += Fk[1]
                Kz += Fk[2]
                #print(Kx, Ky, Kz)

        #cas du calcul de la force sur une facette dont deux coins sont immergés (trois cas traités séparemment rendu possible parce que c'est un triangle. Point d'amélioration à traité avec plusde temps : automatisation du calcul)
            elif za <= 0 and zb <= 0:
                AzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][2])
                BzO = self.calcul_point_sur_eau(facettes[i][1], facettes[i][2])
                # triangle AzO A B
                Fk1 = self.Calculfacette(self._normale[i], [AzO, a, b])
                Kx += Fk1[0]
                Ky += Fk1[1]
                Kz += Fk1[2]
                # triangle AzO BzO B
                Fk2 = self.Calculfacette(self._normale[i], [AzO, BzO, b])
                Kx += Fk2[0]
                Ky += Fk2[1]
                Kz += Fk2[2]
                #print(Kx, Ky, Kz)

            elif za <= 0 and zc <= 0:
                AzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][1])
                CzO = self.calcul_point_sur_eau(facettes[i][1], facettes[i][2])
                # triangle AzO A C
                Fk1 = self.Calculfacette(self._normale[i], [AzO, a, c])
                Kx += Fk1[0]
                Ky += Fk1[1]
                Kz += Fk1[2]
                #print(Kx, Ky, Kz)
                # triangle AzO CzO C
                Fk2 = self.Calculfacette(self._normale[i], [AzO, CzO, c])
                Kx += Fk2[0]
                Ky += Fk2[1]
                Kz += Fk2[2]
                #print(Kx, Ky, Kz)

            elif zb <= 0 and zc <= 0:
                CzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][2])
                BzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][1])
                # triangle CzO C B
                Fk1 = self.Calculfacette(self._normale[i], [CzO, c, b])
                Kx += Fk1[0]
                Ky += Fk1[1]
                Kz += Fk1[2]
                #print(Kx, Ky, Kz)
                # triangle CzO BzO B
                Fk2 = self.Calculfacette(self._normale[i], [CzO, BzO, b])
                Kx += Fk2[0]
                Ky += Fk2[1]
                Kz += Fk2[2]
                #print(Kx, Ky, Kz)

        # cas du calcul de la force sur une facette dont un coin est immergé (trois cas traités séparemment rendu possible parce que c'est un triangle. Point d'amélioration à traité avec plus de temps : automatisation du calcul)
            elif za <= 0:
                BzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][1])
                CzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][2])
                #triangle A BzO CzO
                Fk = self.Calculfacette(self._normale[i], [a, BzO, CzO])
                Kx += Fk[0]
                Ky += Fk[1]
                Kz += Fk[2]
                #print(Kx, Ky, Kz)

            elif zb <= 0:
                AzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][1])
                CzO = self.calcul_point_sur_eau(facettes[i][1], facettes[i][2])
                #triangle B AzO CzO
                Fk = self.Calculfacette(self._normale[i], [b, AzO, CzO])
                Kx += Fk[0]
                Ky += Fk[1]
                Kz += Fk[2]
                #print(Kx, Ky, Kz)

            elif zc <= 0:
                AzO = self.calcul_point_sur_eau(facettes[i][0], facettes[i][2])
                BzO = self.calcul_point_sur_eau(facettes[i][1], facettes[i][2])
                #triangle C AzO BzO
                Fk = self.Calculfacette(self._normale[i], [c, AzO, BzO])
                Kx += Fk[0]
                Ky += Fk[1]
                Kz += Fk[2]
                #print(Kx, Ky, Kz)

        #print([Kx, Ky, Kz])
        self._archimede = [Kx, Ky, Kz]
        #print(self._archimede)
        return self._archimede    #Retourne les coordonnées de cette force


    def calcul_point_sur_eau(self, A, B):
        xD = ((B[0]-A[0])*(-A[2]))/(B[2]-A[2]) + A[0]
        yD = ((B[1]-A[1])*(-A[2]))/(B[2]-A[2]) + A[1]
        return [xD, yD, 0]



Bateau = Info_fichier_stl("V_HULL_Normals_Outward - translation -1demi.stl")
Calcul1 = Calcul(Bateau.getn(), Bateau.getf())
print(Calcul1.Calculfacettes(Calcul1.getfacette()))
