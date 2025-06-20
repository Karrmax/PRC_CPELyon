import random
from time import sleep

def capteur_temperature(temp, verrou, queue):
    while True:
        temperature_mesure = random.uniform(10.0, 50.0)
        verrou.acquire()
        temp.value = temperature_mesure
        verrou.release()
        sleep(2)


def capteur_pression(press, verrou, queue):
    while True:
        pression_mesure = random.uniform(0.9, 1.3)
        verrou.acquire()
        press.value = pression_mesure
        verrou.release()
        sleep(2)
