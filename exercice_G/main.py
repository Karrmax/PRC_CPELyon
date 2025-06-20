import multiprocessing as mp
from time import sleep
from lecteur import lecteur
from redacteur import redacteur

if __name__ == "__main__":
    nb_redacteur_en_attente = mp.Value('i',0)
    nb_lecteur = mp.Value('i',0)
    
    nb_redacteurs = 2
    nb_lecteurs = 3

    verrou = mp.Lock()
    lecture = mp.Semaphore(1)
    redaction = mp.Semaphore(1)
    
    processus_global = []

    for i in range(nb_lecteurs):
        lecteur_process = mp.Process(target = lecteur, args=(i, nb_lecteur, nb_redacteur_en_attente, verrou, lecture, redaction))
        processus_global.append(lecteur_process)

    for i in range(nb_redacteurs):
        redacteur_process = mp.Process(target = redacteur, args=(i, nb_lecteur, nb_redacteur_en_attente, verrou, lecture, redaction))
        processus_global.append(redacteur_process)

    for j in processus_global:
        j.start()

    for j in processus_global:
        j.join()

