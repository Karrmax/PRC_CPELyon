#Calculateur
def lambda_calculateur(queue_demandes, queue_retour):
    while True:
        item = queue_demandes.get()
        if item == "Fin de demande":
            break
        lambda_fonction, x, demandeur_id = item
            
        res = lambda_fonction(x)

        queue_retour[demandeur_id].put(res)