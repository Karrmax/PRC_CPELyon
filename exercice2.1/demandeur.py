from random import randint



#Demandeur
def demandeur(id_demandeur, queue_demande, queue_retour):
    print(f"[Demandeur {id_demandeur}] lancé")
    L = ["+","-","*","/"]   #Différents opérateurs utiles au calcul
    n = 5
    for y in range(n):  #Chaque demandeur donne n calculs à faire pour le calculateur        
        value1 = randint(0,100) #Générer une valeur entre 0 et 100
        value2 = randint(1,100) #Générer une valeur entre 1 et 100, j'ai décidé de retirer le 0 car lorsqu'on fait un essai avec énormément de demandeur, il y a bcp de chance qu'on tombe sur une division par 0
        x = randint(0,3)
        operator = L[x]
        queue_demande.put((value1, value2, operator, id_demandeur))
        res = queue_retour.get()
        print(f"[Demandeur {id_demandeur}] {value1}{L[x]}{value2} = {res}")
    queue_demande.put("Fin de demande")