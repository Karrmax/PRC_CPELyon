import multiprocessing as mp
from demandeur_lambda import lambda_demandeur
from calculateur_lambda import lambda_calculateur

if __name__ == "__main__" :
    nb_demandeurs = 5  #On peut choisir ici m demandeurs
    nb_calculateurs = 3 #On peut choisir n calculateurs
    
    # Création des Queues
    queue_demande = mp.Queue()
    queue_retour = [mp.Queue() for i in range(nb_demandeurs)]   #Pour bien avoir une queue de retour par demandeur

    #Création des demandeurs
    demandeurs = []
    for i in range(nb_demandeurs):
        demandeur_process = mp.Process(target=lambda_demandeur, args=(i, queue_demande, queue_retour[i]))
        demandeurs.append(demandeur_process)
        
    #Création des calculateurs
    calculateurs = []
    for i in range(nb_calculateurs):
        calculateur_process = mp.Process(target=lambda_calculateur, args=(queue_demande,queue_retour))        
        calculateurs.append(calculateur_process)
    
    for i in demandeurs:
        i.start()
        
    for i in calculateurs:
        i.start()

    for i in demandeurs:
        i.join()
        
    for i in calculateurs:
        i.join()

    for i in range(nb_calculateurs):
        queue_demande.put("Fin de demande")

