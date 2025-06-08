from random import randint

def lambda_fonction(x):
    return x**2 + 3*x + 5

#Demandeur
def lambda_demandeur(id_demandeur, queue_demande, queue_retour):
    print(f"[Demandeur {id_demandeur}] lancé")
    n = 5
    for y in range(n):  #Chaque demandeur donne n calculs à faire pour le calculateur        
        x = randint(0,20)
        queue_demande.put((lambda_fonction, x, id_demandeur))
        res = queue_retour.get()
        print(f"[Demandeur {id_demandeur}] avec x={x}, on a  f(x)={res}")
    queue_demande.put("Fin de demande")