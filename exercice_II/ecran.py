from time import sleep


def ecran(queue, temp, press, verrou):
    SEUIL_T = 30.0
    SEUIL_P = 1.1
    while True:
        verrou.acquire()
        t = temp.value
        p = press.value
        print(f"[Écran]\nLes seuils:\nTempérature idéale:{SEUIL_T}°C\nPression idéale:{SEUIL_P}Bar")    #Nous sautons des lignes entre l'affichage des variables pour rendre plus visible l'affichage
        print(f"Température:{temp.value:.2f}°C, Pression:{press.value:.2f}Bar")
        verrou.release()

        while not queue.empty():
            msg = queue.get()
            print(f"{msg}")
        sleep(10)   #Temps avant un nouvel affichage