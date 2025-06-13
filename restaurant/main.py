import multiprocessing as mp
import time
import random
from utils import *

possible_commands = [chr(i) for i in range(65, 91)]

def client_process(client_id, info, tempsMin=3, tempsMax=10):
    # print(f"Client {client_id} is starting.")
    while True:
        tempsAttente = random.randint(tempsMin, tempsMax)
        time.sleep(tempsAttente)
        
        commande = random.choice(possible_commands)
        # if info["clients"]["id" == client_id]["commande"] == []:
        info["clients"][client_id]["commande"] += manager.list((commande))
        # print(client_id,info["clients"][client_id]["commande"],commande)
        # info["clients"]["id" == client_id]["etat"] = 1
        # print(f"Client {client_id} is placing an order: {commande}")
        commandesClients.put((client_id, commande))

def server_process(server_id, info):
    # print(f"Server {server_id} is starting.")
    while True:
        if not commandesCuisiniers.empty():
            client_id, commande = commandesCuisiniers.get()
            info["servers"][server_id]["commande"] =  manager.list((client_id, commande))
            info["servers"][server_id]["etat"] = 0
            info["clients"][client_id]["commande"].remove(commande)  # Remove the command from the client's list
            # info["clients"][client_id] = manager.dict(info["clients"][client_id])  # Ensure the client's state is updated in the manager
            # print(f"Server {server_id} sending to client dish {client_id}: {commande}")
            
        elif not commandesClients.empty():
            client_id, commande = commandesClients.get()
            # print(f"Server {server_id} is processing order from Client {client_id}: {commande}")
            info["servers"][server_id]["commande"] = manager.list((client_id, commande))
            info["servers"][server_id]["etat"] = 1
            info["servers"][server_id] = manager.dict(info["servers"][server_id])  # Ensure the server's state is updated in the manager
            time.sleep(random.uniform(0.5, 1.5))  # Simulate processing time
            commandesServeurs.put((server_id, client_id, commande))

def cuisinier_process(cuisinier_id, info):
    # print(f"Cuisinier {cuisinier_id} is starting.")
    while True:
        effacer_ecran()
        
        
        server_id, client_id, commande = commandesServeurs.get()      # print(f"Cuisinier {cuisinier_id} is preparing order for Client {client_id} from Server {server_id}: {commande}")
        info["cuisiniers"][cuisinier_id]["commande"] = manager.list((server_id, client_id, commande))
        info["cuisiniers"][cuisinier_id] = manager.dict(info["cuisiniers"][cuisinier_id])
        # print(info["cuisiniers"]["id" == cuisinier_id])
        time.sleep(random.uniform(3, 5))
        commandesCuisiniers.put((client_id, commande))
        info["cuisiniers"][cuisinier_id]["commande"] = manager.list()


def majore_dHomme(infos):
    # print("Majore d'Homme is starting.")
    while True:
        commandesClientsList = [infos["clients"][i]["commande"] for i in range(len(infos["clients"]))]
        commandesServeursList = [infos["servers"][i]["commande"] for i in range(len(infos["servers"]))]
        commandesCuisiniersList = [infos["cuisiniers"][i]["commande"] for i in range(len(infos["cuisiniers"]))]
        move_to(1,0) # pour effacer toute ma ligne
        erase_line()
        for i in range(len(infos["clients"])):
            move_to(1+i,0) # pour effacer toute ma ligne
            erase_line()
            print(f"Client {i} - Commande: {infos['clients'][i]['commande']}")
        for i in range(len(infos["servers"])):
            move_to(len(infos["clients"]) +1+i,0) # pour effacer toute ma ligne
            erase_line()
            if infos["servers"][i]["etat"] == 0:
                print(f"Server {i} - Commande: {infos['servers'][i]['commande']}")
            else:
                print(f"Server {i} - Apporte la commande: {infos['servers'][i]['commande']}")
            # print(f"Server {i} - Commande: {infos['servers'][i]['commande']}, Etat: {infos['servers'][i]['etat']}")
        for i in range(len(infos["cuisiniers"])):
            move_to(len(infos["clients"]) + len(infos["servers"]) + 1+i, 0) # pour effacer toute ma ligne
            erase_line()
            print(f"Cuisinier {i} - Commande: {infos['cuisiniers'][i]['commande']}")
        time.sleep(0.05)  # Update every 2 seconds
        # print(infos)
        pass
    
if __name__ == "__main__":
    
    nbServers = 2
    nbClients = 5
    nbCuisinier = 3
    
    commandesClients = mp.Queue() # commandes lorsque le client à choisis il ajoute sa commande dans cette queue
    commandesServeurs = mp.Queue() # le serveur prend en charge la commande du client et l'ajoute dans cette queue apres l'avoir traitée
    commandesCuisiniers = mp.Queue() # le cuisinier prend en charge la commande du serveur et l'ajoute dans cette queue apres l'avoir préparée
    manager = mp.Manager()
    allProcessInfo = manager.dict()
    allProcessInfo["clients"] = manager.dict({i: {"commande": manager.list(), "etat": 0} for i in range(nbClients)})  # etat 0:cherche sa commande, 1:attend la commande
    allProcessInfo["servers"] = manager.dict({i: {"etat": 0, "commande": manager.list()} for i in range(nbServers)})  # etat 0:attend une commande du client, 1: traite la commande
    allProcessInfo["cuisiniers"] = manager.dict({i: {"etat": 0, "commande": manager.list()} for i in range(nbCuisinier)})  # etat 0:attend une commande du serveur, 1: prepare la commande

    effacer_ecran()
    curseur_invisible()
    #allProcessInfo["clients"][0]["commande"] = ["A", "B", "C"]  # Exemple de commande initiale pour le premier client
    

    majore_dHommeProcess = mp.Process(target=majore_dHomme, args=(allProcessInfo,))

    clientProcess = [mp.Process(target=client_process, args=(i, allProcessInfo)) for i in range(nbClients)]
    serverProcess = [mp.Process(target=server_process, args=(i, allProcessInfo)) for i in range(nbServers)]
    cuisinierProcess = [mp.Process(target=cuisinier_process, args=(i, allProcessInfo)) for i in range(nbCuisinier)]

    majore_dHommeProcess.start()
    for p in serverProcess + clientProcess + cuisinierProcess:
        p.start()

    for p in serverProcess + clientProcess + cuisinierProcess:
        p.join()
    majore_dHommeProcess.join()
