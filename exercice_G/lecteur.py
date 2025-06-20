from time import sleep

def lecteur(id_lecteur, nb_lecteur, nb_redacteur_en_attente, verrou, lecture, redaction):
    
    while True:
        print(f"Le lecteur {id_lecteur} souhaite lire :")

        while True:
            lecture.acquire()   #Si un rédacteur est en attente, le rédacteur prend le jeton du sémaphore lecture  et le processus est donc bloqué ici
            verrou.acquire()
            if nb_redacteur_en_attente.value == 0:  #Personne ne peut rédiger, on peut donc donner le feu vert aux lecteurs
                nb_lecteur.value += 1  
                if nb_lecteur.value == 1: #Le premier lecteur prend le jeton de rédaction pour éviter que la rédaction ne se manifeste après qu'on est vérifié qu'il n'y ait pas de rédacteur en attente
                    redaction.acquire()
                verrou.release()
                lecture.release()
                break 
            else:
                verrou.release()
                lecture.release()
                sleep(1)       

        print(f"Le lecteur {id_lecteur} lit")
        sleep(4)    #Temps de lecture
        print(f"Le lecteur {id_lecteur} a terminé de lire")

        verrou.acquire()
        nb_lecteur.value -= 1
        if nb_lecteur.value == 0:
            redaction.release()
        verrou.release()

        sleep(8)


