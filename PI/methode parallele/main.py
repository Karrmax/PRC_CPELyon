import multiprocessing as mp
import random
import time

# définition d'un travailleur
def processPI(nb_iteration, X):
    count = 0
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
    # si le point est dans l’unit circle
        if x *x + y *y <= 1: count += 1
    X.value += count


if __name__ == "__main__":    
    baseTime = time.time()
    nbProcess = 4
    my_procs = [None for i in range(nbProcess)]
    
    nbHits = mp.Value('i', 0)
    
    nbIterations = 1e7
    for i in range(nbProcess) : my_procs[i] = mp.Process(target=processPI, args=(int(nbIterations//nbProcess), nbHits))
    
    for i in my_procs : i.start()
    
    for i in my_procs: i.join()
    
    print(f"valeur trouvée : {4 *nbHits.value / nbIterations}")
    
    execTime = round(time.time() - baseTime, 3)
    print(f"opération réalisée en {execTime}s")