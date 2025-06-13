import multiprocessing as mp
import time
import random
import pickle


possible_commands = [chr(i) for i in range(65, 91)]

def client_process(client_id, tempsMin=3, tempsMax=10):
    print(f"Client {client_id} is starting.")
    while True:
        tempsAttente = random.randint(tempsMin, tempsMax)
        time.sleep(tempsAttente)
        
        commande = random.choice(possible_commands)
        print(f"Client {client_id} is placing an order: {commande}")
        commandesClients.put((client_id, commande))

def server_process(server_id):
    print(f"Server {server_id} is starting.")
    while True:
        if commandesCuisiniers.empty():
            client_id, commande = commandesClients.get()
            print(f"Server {server_id} is processing order from Client {client_id}: {commande}")
            time.sleep(random.uniform(0.5, 1.5))  # Simulate processing time
            commandesServeurs.put((server_id, client_id, commande))
        else:
            client_id, commande = commandesCuisiniers.get()
            print(f"Server {server_id} sending to client dish {client_id}: {commande}")
            

def cuisinier_process(cuisinier_id):
    print(f"Cuisinier {cuisinier_id} is starting.")
    while True:
        server_id, client_id, commande = commandesServeurs.get()
        print(f"Cuisinier {cuisinier_id} is preparing order for Client {client_id} from Server {server_id}: {commande}")
        time.sleep(random.uniform(1, 2))
        commandesCuisiniers.put((client_id, commande))


def majore_dHomme():
    print("Majore d'Homme is starting.")
    while True:
        pass
    
if __name__ == "__main__":
    
    nbServers = 2
    nbClients = 5
    nbCuisinier = 3
    
    commandesClients = mp.Queue() # commandes lorsque le client à choisis il ajoute sa commande dans cette queue
    commandesServeurs = mp.Queue() # le serveur prend en charge la commande du client et l'ajoute dans cette queue apres l'avoir traitée
    commandesCuisiniers = mp.Queue() # le cuisinier prend en charge la commande du serveur et l'ajoute dans cette queue apres l'avoir préparée


    allProcessInfo = {
        "servers": [{"id": i, "etat": 0, "commande": None} for i in range(nbServers)], # etat 0:cherche sa commande, 1:attend la commande
        "clients": [{"id": i, "etat": 0, "commande": None} for i in range(nbClients)], # etat 0:attend une commande du client, 1: traite la commande
        "cuisiniers": [{"id": i, "etat": 0, "commande": None} for i in range(nbCuisinier)] # etat 0:attend une commande du serveur, 1: prepare la commande
    }
    
    

    serverProcess = [mp.Process(target=server_process, args=(i,)) for i in range(nbServers)]
    clientProcess = [mp.Process(target=client_process, args=(i,)) for i in range(nbClients)]
    cuisinierProcess = [mp.Process(target=cuisinier_process, args=(i,)) for i in range(nbCuisinier)]
    
    for p in serverProcess + clientProcess + cuisinierProcess:
        p.start()
    
    for p in serverProcess + clientProcess + cuisinierProcess:
        p.join()
