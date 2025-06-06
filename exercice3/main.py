import multiprocessing as mp
from utils import *


def acquireN(N):
    pass

def control():
    pass

# définition d'un travailleur
def travailleur(demande):
    for i in range(nbSequences):
        acquireN(demande)
        time.sleep(demande)
        releaseN(demande)







if __name__ == "__main__":
    
    nbBilles = 9
    billes = mp.Semaphore(nbBilles)
    
    
    nbProcess = 4
    my_procs = [None for i in range(nbProcess)]
    
    demande = [4, 3, 5, 2]
    
    nbSequences = 7
    proc_control = mp.Process(target=control, args=("",))
    
    for i in len(nbProcess) : my_procs[i] = mp.Process(target=travailleur, args=(demande,))
    
    for i in my_procs : i.start()
    
    for i in my_procs: i.join()
    
    proc_control.join()