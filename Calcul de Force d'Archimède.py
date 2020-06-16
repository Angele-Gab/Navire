# numpy.stl
import numpy as np


#fonctions

class Navire :
    def __init__(self,chemin):
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
        self.__normal = liste_des_vecteurs_normaux
        self._facette = liste_des_facettes
        print(self._facette)

    def getf(self):
        return self._facette

    def getn(self):
        return self.__normal

    def ProdVect(self, u,v):
        #retourne les coordonnées de w=(wx,wy,wz)=u ^v
        wx = u[1]*v[2]-u[2]*v[1] #les indices sont numérotés de 0 à 2
        wy = u[2]*v[0]-u[0]*v[2]
        wz = u[0]*v[1]-u[1]*v[0]
        w = np.array([wx, wy, wz])
        return(w)

    def Norme(self, u):
        return (u[0]**2+u[1]**2+u[2]**2)**(1/2)

    def Surface(self, facette): # ++ Calcul et renvoi la norme du vecteur surface d'une facette donnés en entrée
        AB = np.array([facette[1][0]-facette[0][0], facette[1][1]-facette[0][1], facette[1][2]-facette[0][2]])
        AC = np.array([facette[2][0]-facette[0][0], facette[2][1]-facette[0][1], facette[2][2]-facette[0][2]])
        DsFk = self.Norme(self.ProdVect(AB, AC))/2
        return DsFk


    def Calculfacette(self, vecteur_normal, facette):
        ro = 1000
        g = 9.81
        Fkx = ro*g*np.array([(facette[0][0]+facette[1][0]+facette[2][0])/3, (facette[0][1]+facette[1][1]+facette[2][1])/3, (facette[0][2]+facette[1][2]+facette[2][2])/3])[2]*self.Surface(facette)*vecteur_normal[0]
        Fky = ro*g*np.array([(facette[0][0]+facette[1][0]+facette[2][0])/3, (facette[0][1]+facette[1][1]+facette[2][1])/3, (facette[0][2]+facette[1][2]+facette[2][2])/3])[2]*self.Surface(facette)*vecteur_normal[1]
        Fkz = ro*g*np.array([(facette[0][0]+facette[1][0]+facette[2][0])/3, (facette[0][1]+facette[1][1]+facette[2][1])/3, (facette[0][2]+facette[1][2]+facette[2][2])/3])[2]*self.Surface(facette)*vecteur_normal[2]
        return [Fkx, Fky, Fkz]

    def Calculfacettes(self,facette):
        Kx = 0
        Ky = 0
        Kz = 0
        for i in range(0, len(self.__normal)):
            #if self.__facette[i][0][2] > 0 or self.__facette[i][1][2] > 0 or self.__facette[i][2][2]:
                Fk = self.Calculfacette(self.__normal[i], facette[i])
                #print(Fk)
                Kx += Fk[0]
                Ky += Fk[1]
                Kz += Fk[2]
        self._archimede = [Kx, Ky, Kz]

        return self._archimede


    def Translation(self,ecart):
        liste_facettes = self._facette
        for i in liste_facettes :
            for j in i :
                j[2] += ecart
        return liste_facettes

    def Dichotomie(self,masse,a,b, epsilon):   # a modifier
        Fp = masse * 9.81   #Norme de la force poids
        maxi = b
        mini = a
        while abs(maxi-mini) > epsilon :
            milieu = (maxi+mini)/2
            newA = self.Translation(mini)
            newB = self.Translation(milieu)
            FaA = self.Calculfacettes(newA)
            FaB = self.Calculfacettes(newB)
            norme_FaA = (FaA[0]**2+FaA[1]**2+FaA[2]**2)**(1/2)
            norme_FaB = (FaB[0]**2+FaB[1]**2+FaB[2]**2)**(1/2)
            phiA = norme_FaA-Fp
            phiM = norme_FaB-Fp

            if phiA*phiM < 0:
                maxi=milieu
            else :
                mini= milieu
        return mini




#programme principal
#print(CalculFfacette(np.array([0, 1, 0]), np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 0, 1])))
#Lire_Stl(r"V_HULL.stl")
Bateau = Navire("Rectangular_HULL - Copie (2).stl")
#print(Bateau.Calculfacettes())
print(Bateau.Dichotomie(15000,-100,100, 0.2))
#print(Bateau.Translation(2))
