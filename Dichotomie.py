import numpy as np
import copy
import matplotlib.pyplot as plt

  #Test de Dichotomie
class D:

    def phi(self,x):
        f= 2*x+3
        return f

    def dichotomie(self,a,b,epsilon):
        X = []

        Y = []
        i = 0

        while abs(b-a) > epsilon :
            milieu = (b+a)/2
            if self.phi(a)*self.phi(milieu) < 0:
                X.append(self.phi(a))

                i+=1
                Y.append(i)
                b=milieu
            else :

                X.append(self.phi(a))

                i+=1
                Y.append(i)
                a= milieu
        plt.plot(Y,X)

        plt.show()
        return a

d = D()
print(d.dichotomie(-5,5,0.00001))
