from time import sleep

def redacteur (id_redacteur, nb_lecteur, nb_redacteur_en_attente, verrou, lecture, redaction):
    while True:
        
        print(f"Le rédacteur {id_redacteur} souhaite rédiger :") 
        verrou.acquire()
        nb_redacteur_en_attente.value += 1  #Un rédacteur veut écrire

        if nb_redacteur_en_attente == 1: 
            lecture.acquire()   #On veut empêcher l'arrivée d'un nouveau lecteur, on attend la fin de la lecture
        verrou.release()

        redaction.acquire()
        verrou.acquire()
        nb_redacteur_en_attente.value -= 1 
        print(f"Le rédacteur {id_redacteur} écrit :")
        sleep(4)    #Temps de rédaction de l'auteur
        print(f"Le rédacteur {id_redacteur} a terminé d'écrire :")
        redaction.release()

        if nb_redacteur_en_attente.value == 0:
            lecture.release()
        verrou.release()
        
        sleep(5)


        