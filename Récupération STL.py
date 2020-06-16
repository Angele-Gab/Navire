# numpy.stl
import numpy as np


#fonctions

def ProdVect(u,v):
    #retourne les coordonnées de w=(wx,wy,wz)=u ^v
    wx = u[1]*v[2]-u[2]*v[1] #les indices sont numérotés de 0 à 2
    wy = u[2]*v[0]-u[0]*v[2]
    wz = u[0]*v[1]-u[1]*v[0]
    w = np.array([wx, wy, wz])
    return(w)

def Norme(u):
    return (u[0]**2+u[1]**2+u[2]**2)**(1/2)


def Lire_Stl(titre_doc):
    liste_de_valeurs = []
    fichier = open(titre_doc, "r")
    lignes = fichier.readlines() #fourni le texte en chaines de caractères
    for i in lignes:
        k = i.split()
        for j in k:
            if j.isalpha() == False:
                liste_de_valeurs.append(j)
    new = []
    while len(liste_de_valeurs) != 0:
        vecteur = [liste_de_valeurs[0], liste_de_valeurs[1], liste_de_valeurs[2]]
        new.append(vecteur)
        liste_de_valeurs = liste_de_valeurs[3:]
    print("new :",new)
    newnew = []
    vecteur_normal = []
    while len(new) != 0:
        facette = [ new[1], new[2], new[3]]
        #print(facette)
        vecteur_normal.append(new[0])
        newnew.append(facette)
        new = new[4:]
    fichier.close()
    print(newnew) # liste des valeurs des coordonnées des facettes
    print(vecteur_normal)

def Surface(A, B, C):
    AB = np.array([B[0]-A[0], B[1]-A[1], B[2]-A[2]])
    AC = np.array([C[0]-A[0], C[1]-A[1], C[2]-A[2]])
    DsFk = Norme(ProdVect(AB, AC))/2
    return DsFk

def CalculFfacette(vecteur_normal, A, B, C):
    ro = 1000
    g = 9.81
    Fk = ro*g*np.array([(A[0]+B[0]+C[0])/3, (A[1]+B[1]+C[1])/3, (A[2]+B[2]+C[2])/3])[2]*Surface(A, B, C)*vecteur_normal
    return Fk




#programme principal
print(CalculFfacette(np.array([0, 1, 0]), np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 0, 1])))
Lire_Stl(r"V_HULL - Copie (2).stl")



