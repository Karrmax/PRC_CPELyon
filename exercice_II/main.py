import multiprocessing as mp
from machines import chauffage, pompe
from controleur import controleur
from capteurs import capteur_temperature, capteur_pression
from ecran import ecran



if __name__ == "__main__":

    verrou = mp.Lock()  #Création de notre verrou

    #On utilise 'd' car on partage un nombre réel par forcément un entier
    temp = mp.Value('d', 0.0)   #Température partagée 
    press = mp.Value('d', 0.0)  #Pression partagée

    chauffage_on = mp.Value('i', 0) #Création de la variable partagée pour le chauffage
    pompe_on = mp.Value('i', 0) #Création de la variable partagée pour la pompe

    queue = mp.Queue()

    processus = [
    mp.Process(target=capteur_temperature, args=(temp, verrou, queue)),       
    mp.Process(target=capteur_pression, args=(press, verrou, queue)),
    mp.Process(target=controleur, args=(temp, press, verrou, chauffage_on, pompe_on, queue)),       
    mp.Process(target=chauffage, args=(chauffage_on, queue)),      
    mp.Process(target=pompe, args=(pompe_on, queue)),       
    mp.Process(target=ecran, args=(queue, temp, press, verrou))
    ]


    for i in processus:
        i.start()

    for i in processus:
        i.join()





