import multiprocessing as mp
from demandeur import demandeur
from calculateur import calculateur


if __name__ == "__main__" :
    nb_demandeurs = 5  #On peut choisir ici m demandeurs
    nb_calculateurs = 3 #On peut choisir n calculateurs
    
    #Création des Queues
    queue_demande = mp.Queue()
    queue_retour = [mp.Queue() for i in range(nb_demandeurs)]

    #Création des demandeurs
    demandeur_process = [0 for i in range(nb_demandeurs)]
    for i in range(nb_demandeurs):
        demandeur_process[i] = mp.Process(target=demandeur, args=(i, queue_demande, queue_retour[i]))
        
    #Création des calculateurs
    calculateur_process = [0 for i in range(nb_calculateurs)]
    for i in range(nb_calculateurs):
        calculateur_process[i] = mp.Process(target=calculateur, args=(queue_demande,queue_retour))       
    
    for i in range (nb_demandeurs): #Nous nous appuyons sur la syntaxe du cours 1
        demandeur_process[i].start()
        
    for i in range (nb_calculateurs):
        calculateur_process[i].start()

    for i in range (nb_demandeurs):
        demandeur_process[i].join()
        
    for i in range (nb_calculateurs):
        calculateur_process[i].join()

    for i in range(nb_calculateurs):
        queue_demande.put("Fin de demande")


