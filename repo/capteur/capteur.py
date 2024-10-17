from lora import *
from scanner import *
from signal import signal, SIGINT

def handler(signal_received, frame):
    global recherche
    print("\n\nCaught Ctrl+C, stopping...")
    recherche = False


signal(SIGINT, handler)

global recherche
recherche = True

canal = 18
adresse = 1

l = lora(canal, adresse)
l.activer()

frequence_debut = 400e6
frequence_fin = 440e6

s = scanner(frequence_debut, frequence_fin)
s.activer()


while recherche:

    frequence = s.check()

    if frequence:
        print(f"found frequence : {frequence}")
        l.send(frequence)

    time.sleep(1)


l.stop()
s.stop()