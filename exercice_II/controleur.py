from time import sleep



def controleur(temp, press, verrou, chauffage_on, pompe_on, queue):
    SEUIL_T = 30.0
    SEUIL_P = 1.1
    while True:
        verrou.acquire()
        t = temp.value
        p = press.value
        verrou.release()

        if t < SEUIL_T:
            chauffage_on.value = 1
        else:
            chauffage_on.value = 0 #Il ne faut pas oublier le cas où on est à la témpérature idéale

        if p > SEUIL_P:
            pompe_on.value = 1
        else:
            pompe_on.value = 0


        # queue.put(f"Chauffage {'ON' if chauffage_on.value else 'OFF'}, Pompe {'ON' if pompe_on.value else 'OFF'}")
        sleep(2)
