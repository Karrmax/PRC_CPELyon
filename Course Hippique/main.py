import multiprocessing as mp
import os, time,math, random, sys, ctypes, signal
from utils import *
# Une liste de couleurs à affecter aléatoirement aux chevaux
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]


# La tache d''un cheval
def un_cheval(ma_ligne : int, keep_running, realTimePosition) : # ma_ligne commence à 0
    col=1
    while keep_running.value :
        move_to(ma_ligne+1,col) # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print(f'({chr(ord("A")+ma_ligne)}>', end='', flush=True) # Affiche le cheval
        col+=1
        realTimePosition[ma_ligne] = col
        
        time.sleep(0.1 * random.randint(1,5))
    # désormais, c'est l'arbitre qui va geler la course en cas de finish
#−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−


def arbitre(keep_running, realTimePosition):
    while True:
        time.sleep(0.1) # temps minimum d'attente d'un cheval donc pas de problème 
        
        if not keep_running.value : # Si la course est finie
            break
        firstPlayer = max(range(len(realTimePosition)), key=lambda i: realTimePosition[i])
        lastPlayer = min(range(len(realTimePosition)), key=lambda i: realTimePosition[i])
        
        move_to(Nb_process + 2, 1)
        # print(firstPlayer)
        en_couleur(CL_WHITE)
        
        print(str(chr(ord('A') + firstPlayer)), "est en tête avec", realTimePosition[firstPlayer], "et", str(chr(ord('A') + lastPlayer)), "est en queue avec", realTimePosition[lastPlayer], flush=True)
#
        if realTimePosition[firstPlayer] >= LONGEUR_COURSE : # Si un cheval a fini
            winner = chr(ord('A') + firstPlayer)
            # print(f"\n\nLe gagnant est {winner} !")
            keep_running.value = False # On arrête la course
            # return winner # On retourne le gagnant
#−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
def detourner_signal(signum, stack_frame) :
    move_to(24, 1)
    erase_line()
    move_to(24, 1)
    curseur_visible()
    print("La course est interrompu ...")
    exit(0)
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−

def predict(Nb_process):
    """ 
    Fonction de prédiction qui retourne un dictionnaire avec les chevaux et leur position initiale.
    """
    pordictPossible = [chr(ord('A') + i) for i in range(Nb_process)]
    predict = input("Prédiction des chevaux misez sur le premier cheval (A, B, C, ...): ").strip().upper()
    while predict not in pordictPossible:
        print("Prédiction invalide. Veuillez entrer une lettre valide (A, B, C, ...).")
        predict = input("Prédiction des chevaux misez sur le premier cheval (A, B, C, ...): ").strip().upper()
    print(f"Votre prédiction est : {predict}")
    return predict

def getWinner(realTimePosition, LONGEUR_COURSE):
    """
    Fonction pour déterminer le gagnant de la course.
    """
    for i in range(len(realTimePosition)):
        if realTimePosition[i] >= LONGEUR_COURSE:
            return chr(ord('A') + i)  # Retourne le cheval gagnant
    return None  # Aucun gagnant si aucun cheval n'a atteint la longueur de course

# La partie principale :
if __name__ == "__main__" :
    import platform
    if platform.system() == "Darwin" :
        mp.set_start_method('fork') # Nécessaire sous macos, OK pour Linux (voir le fichier des sujets)
        
    winner = None # Le gagnant de la course
    
    LONGEUR_COURSE = 100 # Tout le monde aura la même copie (donc no need to have a ’value’)
    
    Nb_process=20
    
    keep_running=mp.Value(ctypes.c_bool, True)
    realTimePosition = mp.Array('i', Nb_process)
    
    mes_process = [0 for i in range(Nb_process)]

    processArbitre = mp.Process(target=arbitre, args=(keep_running, realTimePosition))
    
    prediction = predict(Nb_process)
    
    
    processArbitre.start()

    effacer_ecran()
    curseur_invisible()
    
    # Détournement d’interruption
    signal.signal(signal.SIGINT, detourner_signal) # CTRL_C_EVENT ?
    
    for i in range(Nb_process): # Lancer Nb_process processus
        mes_process[i] = mp.Process(target=un_cheval, args= (i,keep_running, realTimePosition))
        mes_process[i].start()
        
    move_to(Nb_process+4, 1)
    
    print("tous lancés, CTRL-C arrêtera la course ...")
    print(f"Votre prédiction est : {prediction}")
    
    for i in range(Nb_process): mes_process[i].join()
    winner = getWinner(realTimePosition, LONGEUR_COURSE)
    
    
    en_couleur(CL_WHITE)
    move_to(26, 1)
    curseur_visible()
    
    print("Fini ... ", flush=True)
    # print(winner)
    if winner is not None and winner != prediction:
        move_to(28, 1)
        erase_line()
        en_couleur(CL_RED)
        print(f"Vous avez perdu, le gagnant est {winner} !", flush=True)
    elif winner is not None and winner == prediction:
        move_to(28, 1)
        erase_line()
        en_couleur(CL_GREEN)
        print(f"Vous avez gagné, le gagnant est {winner} !", flush=True)
    

