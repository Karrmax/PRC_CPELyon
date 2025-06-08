import multiprocessing as mp
from demandeur import demandeur
from calculateur import calculateur
from demandeur_lambda import lambda_demandeur
from calculateur_lambda import lambda_calculateur

if __name__ == "__main__" :
    nb_demandeurs = 5  #On peut choisir ici m demandeurs
    nb_calculateurs = 3 #On peut choisir n calculateurs
    
    # Création de la Queue
    queue_demande = mp.Queue()
    queue_retour = [mp.Queue() for _ in range(nb_demandeurs)]

    #Création des demandeurs
    demandeurs = []
    for i in range(nb_demandeurs):
        demandeur_process = mp.Process(target=lambda_demandeur, args=(i, queue_demande, queue_retour[i]))  #Création des demandeurs
        demandeur_process.start()
        demandeurs.append(demandeur_process)
        
    #Création des calculateurs
    calculateurs = []
    for i in range(nb_calculateurs):
        calculateur_process = mp.Process(target=lambda_calculateur, args=(queue_demande,queue_retour))        
        calculateur_process.start()
        calculateurs.append(calculateur_process)
    
    # Attendre la fin des processus
    for p in demandeurs:
        p.join()
        
    for p in calculateurs:
        p.join()

    for i in range(nb_calculateurs):
        queue_demande.put("Fin de demande")

