import dill

#Calculateur
def lambda_calculateur(queue_demandes, queue_retour):
    while True:
        element = queue_demandes.get()
        if element == "Fin de demande":
            break
        lambda_fonction, a, b, c, demandeur_id = element
        
        res = dill.loads(lambda_fonction)(a, b, c)

        queue_retour[demandeur_id].put(res)