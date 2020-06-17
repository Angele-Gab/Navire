import numpy as np
import copy

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
            if facettes[i][0][2] <= 0 or facettes[i][1][2] <= 0 or facettes[i][2][2] <= 0:

                Fk = self.Calculfacette(self._normale[i], facettes[i])
                Kx += Fk[0]
                Ky += Fk[1]
                Kz += Fk[2]
        self._archimede = [Kx, Ky, Kz]
        return self._archimede    #Retourne les coordonnées de cette force

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

    def Dichotomie(self,masse,a,b, epsilon):   #Calcul de la dichotomie, retourne la valeur mini qui correspond alors à la valeur du zéro
        Fp = masse * 9.81   #Norme de la force poids
        print("Fp ",Fp)
        maxi = b
        mini = a
        print(self._facette[0])
        listeA = copy.deepcopy(self._facette)
        listeB = copy.deepcopy(self._facette)
        compteur = 0
        while abs(maxi-mini) > epsilon :
            compteur += 1
            print(">> Iteration n° ",compteur)
            milieu = (maxi+mini)/2
            print("     mini ",mini," maxi ",maxi," milieu ",milieu)

            newA = self.TranslationListe(listeA,mini)
            newB = self.TranslationListe(listeB,milieu)
            #print("      Premier facette A",newA[0])
            #print("      Premier facette B",newB[0])
            FaA = self.Calculfacettes(newA)
            FaB = self.Calculfacettes(newB)
            print("   FA ", FaA, " FaB", FaB)
            norme_FaA = (FaA[0]**2+FaA[1]**2+FaA[2]**2)**(1/2)
            norme_FaB = (FaB[0]**2+FaB[1]**2+FaB[2]**2)**(1/2)
            #print("   Norme FaA ",norme_FaA," Norme FaB",norme_FaB)
            phiA = norme_FaA-Fp
            phiM = norme_FaB-Fp

            if phiA*phiM < 0:
                maxi= milieu
            else :
                mini= milieu
        return mini


#programme principal
#print(CalculFfacette(np.array([0, 1, 0]), np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 0, 1])))
#Lire_Stl(r"V_HULL.stl")
Bateau = Info_fichier_stl("Rectangular_HULL_Normals_Outward.stl")
#Bateau2 = Info_fichier_stl("V_HULL_modif_toutes_coordonnees.stl")
#print(Bateau.Translation(-1))
#print(Bateau.Calculfacettes(Bateau.getf()))
#print(Bateau2.Calculfacettes())
Calcul1 = Calcul(Bateau.getn(),Bateau.getf())
print(Calcul1.Calculfacette(Bateau.getn()[0],Bateau.getf()[0]))
#print(Bateau.getn()[0]) #On a que le vecteur grace à l'indice
#print(Bateau.getf()[0][0])
print(Calcul1.Dichotomie(4000,-10,50, 0.2))
