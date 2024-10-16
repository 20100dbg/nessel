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

l = lora()
l.activer()

s = scanner()
s.activer()


while recherche:

    frequence = s.check()

    if frequence:
        print(f"found frequence : {frequence}")
        l.send(frequence)

    time.sleep(1)


l.stop()
s.stop()