from lora import *
from signal import signal, SIGINT

def handler(signal_received, frame):
    global recherche
    print("\n\nCaught Ctrl+C, stopping...")
    recherche = False

def pretty_frq(frq):
    strfrq = str(frq/1000000)
    strfrq = strfrq.ljust(7, '0')
    return strfrq + 'M'

def encoder(frequence):
    return frequence.to_bytes(4, 'big')

def decoder(frequence):
    return int.from_bytes(frequence)


signal(SIGINT, handler)

global recherche
recherche = True

l = lora()
l.activer()


while recherche:

    message = l.check()


    if message:
        print(f"RECEIVED : {message}")

    time.sleep(1)


l.stop()
s.stop()