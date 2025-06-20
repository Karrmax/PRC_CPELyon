from random import randint



#Demandeur
def demandeur(id_demandeur, queue_demande, queue_retour):
    print(f"[Demandeur {id_demandeur}] lancé")  #Permet de voir quand le processus est lancé
    L = ["+","-","*","/"]   #Différents opérateurs utiles au calcul
    n = 5
    for y in range(n):  #Chaque demandeur donne n calculs à faire pour le calculateur        
        value1 = randint(0,100) #Générer une valeur entre 0 et 100
        value2 = randint(1,100) #Générer une valeur entre 1 et 100, j'ai décidé de retirer le 0 car lorsqu'on fait un essai avec énormément de demandeur, il y a bcp de chance qu'on tombe sur une division par 0
        x = randint(0,3)    #Pour choisir aléatoirement l'opérateur de notre calcul
        operator = L[x]
        queue_demande.put((value1, value2, operator, id_demandeur)) #Ajout dans la queue de demande des valeurs, de l'opérateur et de l'id de notre calcul
        res = queue_retour.get()    #Permet de récupérer le résultat propre à chaque demande dans la queue de retour qui lui est dédiée.
        print(f"[Demandeur {id_demandeur}] {value1}{L[x]}{value2} = {res}") #Affichage du résultat
