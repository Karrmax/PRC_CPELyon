import multiprocessing as mp
import time
import random

def demander(k_billes):
    verrouDemande.acquire()
    while nbBilles.value < k_billes:
        verrouDemande.release()
        semBillesRendue.acquire()
        verrouDemande.acquire()
    nbBilles.value -= k_billes
    verrouDemande.release()

def rendre(k_billes):
    nbBilles.value += k_billes
    semBillesRendue.release()

def travailleur(id, nb_billes):
    for i in range(M):
        print(f"Travailleur {id} demande {nb_billes} billes.")
        demander(nb_billes)
        print(f"Travailleur {id} a reçu {nb_billes} billes et travaille avec.")
        time.sleep(nb_billes)
        print(f"Travailleur {id} a fini de travailler avec {nb_billes} billes et les rend.")
        rendre(nb_billes)

def controleur(nb_billes_max):
    while True:
        if not (0 <= nbBilles.value <= nb_billes_max):
            print(f"Erreur: Nombre de billes {nbBilles.value} en dehors des limites (0, {nb_billes_max})")

if __name__ == "__main__":
    NB_MAX_BILLES = 20
    DEMANDES = [4, 3, 5, 2]
    
    M = 2 # nb de répetitions
    N = len(DEMANDES)  # Nombre de travailleurs
    
    verrouDemande = mp.Lock()  # Verrou pour la demande de billes
    
    semBillesRendue = mp.Semaphore(0)  # Sémaphore pour gérer

    nbBilles = mp.Value('i', NB_MAX_BILLES)  # Nombre de billes actuellement en main

    # Création des processus
    processusTravailleurs = [mp.Process(target=travailleur, args=(i, DEMANDES[i],)) for i in range(N)]
    processusControleur = mp.Process(target=controleur, args=(NB_MAX_BILLES,))
    # Démarrage des processus
    for p in processusTravailleurs : p.start()
    processusControleur.start()

    # Attente de la fin des processus
    for p in processusTravailleurs : p.join()
    processusControleur.terminate()