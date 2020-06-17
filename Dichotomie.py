  #Test de Dichotomie
class D:



    def phi(self,x):
        f= 2*x+3
        return f

    def dichotomie(self,a,b,epsilon):
            while abs(b-a) > epsilon :
                milieu = (b+a)/2
                if self.phi(a)*self.phi(milieu) < 0:
                    b=milieu
                else :
                    a= milieu
            return a

d = D()
print(d.dichotomie(-10,10,0.00000000000000001))
