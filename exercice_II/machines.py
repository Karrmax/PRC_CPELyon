from time import sleep

def chauffage(chauffage_on, queue):
    while True:
        if chauffage_on.value:  #Si le chauffage est activé 
            queue.put("Chauffage ON")
        else:   #Si le chauffage est OFF
            queue.put("Chauffage OFF")
        sleep(2)

def pompe(pompe_on, queue):
    while True:
        if pompe_on.value:  #Si la pompe est activée
            queue.put("Pompe ON")
        else:   #Si la pompe est OFF
            queue.put("Pompe OFF")
        sleep(2)


