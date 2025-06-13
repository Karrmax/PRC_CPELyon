import multiprocessing as mp
import time
import random


possible_commands = [chr(i) for i in range(65, 91)]

def client_process(client_id, info, tempsMin=3, tempsMax=10):
    print(f"Client {client_id} is starting.")
    while True:
        tempsAttente = random.randint(tempsMin, tempsMax)
        time.sleep(tempsAttente)
        
        commande = random.choice(possible_commands)
        # if info["clients"]["id" == client_id]["commande"] == []:
        info["clients"]["id" == client_id]["commande"] += [commande]
        # info["clients"]["id" == client_id]["etat"] = 1
        # print(f"Client {client_id} is placing an order: {commande}")
        commandesClients.put((client_id, commande))

def server_process(server_id, info):
    print(f"Server {server_id} is starting.")
    while True:
        if commandesCuisiniers.empty():
            client_id, commande = commandesClients.get()
            # print(f"Server {server_id} is processing order from Client {client_id}: {commande}")
            info["servers"]["id" == server_id]["commande"] = (client_id, commande)
            info["servers"]["id" == server_id]["etat"] = 1
            time.sleep(random.uniform(0.5, 1.5))  # Simulate processing time
            commandesServeurs.put((server_id, client_id, commande))
        else:
            client_id, commande = commandesCuisiniers.get()
            info["servers"]["id" == server_id]["commande"] = (client_id, commande)
            info["servers"]["id" == server_id]["etat"] = 0
            print(f"Server {server_id} sending to client dish {client_id}: {commande}")
            

def cuisinier_process(cuisinier_id, info):
    print(f"Cuisinier {cuisinier_id} is starting.")
    while True:
        server_id, client_id, commande = commandesServeurs.get()
        # print(f"Cuisinier {cuisinier_id} is preparing order for Client {client_id} from Server {server_id}: {commande}")
        info["cuisiniers"]["id" == cuisinier_id]["commande"] = (server_id, client_id, commande)
        time.sleep(random.uniform(1, 2))
        commandesCuisiniers.put((client_id, commande))


def majore_dHomme(infos):
    print("Majore d'Homme is starting.")
    while True:
        print(infos)
        pass
    
if __name__ == "__main__":
    
    nbServers = 2
    nbClients = 5
    nbCuisinier = 3
    
    commandesClients = mp.Queue() # commandes lorsque le client à choisis il ajoute sa commande dans cette queue
    commandesServeurs = mp.Queue() # le serveur prend en charge la commande du client et l'ajoute dans cette queue apres l'avoir traitée
    commandesCuisiniers = mp.Queue() # le cuisinier prend en charge la commande du serveur et l'ajoute dans cette queue apres l'avoir préparée


    allProcessInfo = {
        "clients": [{"id": i, "commande": []} for i in range(nbClients)], # etat 0:cherche sa commande, 1:attend la commande 
        "servers": [{"id": i, "commande": []} for i in range(nbServers)], # etat 0:attend une commande du client, 1: traite la commande
        "cuisiniers": [{"id": i, "etat": 0, "commande": []} for i in range(nbCuisinier)] # etat 0:attend une commande du serveur, 1: prepare la commande
    }
    
    allProcessInfo = mp.Manager().dict(allProcessInfo)

    majore_dHommeProcess = mp.Process(target=majore_dHomme, args=(allProcessInfo,))

    serverProcess = [mp.Process(target=server_process, args=(i, allProcessInfo)) for i in range(nbServers)]
    clientProcess = [mp.Process(target=client_process, args=(i, allProcessInfo)) for i in range(nbClients)]
    cuisinierProcess = [mp.Process(target=cuisinier_process, args=(i, allProcessInfo)) for i in range(nbCuisinier)]

    majore_dHommeProcess.start()
    for p in serverProcess + clientProcess + cuisinierProcess:
        p.start()

    for p in serverProcess + clientProcess + cuisinierProcess:
        p.join()
    majore_dHommeProcess.join()
