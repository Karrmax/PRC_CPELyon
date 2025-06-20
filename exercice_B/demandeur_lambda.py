from random import randint
import dill

#Demandeur
def lambda_demandeur(id_demandeur, queue_demande, queue_retour):
    print(f"[Demandeur {id_demandeur}] lancé")
    n = 5
    func = lambda a, b, c : 3*a**2 + 2*b + 5*c
    for y in range(n):  #Chaque demandeur donne n calculs à faire pour le calculateur        
        a = randint(0,20)
        b = randint(0,50)
        c = randint(0,100)
        queue_demande.put((dill.dumps(func), a, b, c, id_demandeur))
        res = queue_retour.get()
        print(f"[Demandeur {id_demandeur}] avec a={a}, b={b} et c={c}, on a  f(x)={res}")
