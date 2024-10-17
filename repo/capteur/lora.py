import sx126x
import threading
import time
import queue

class lora:

    def __init__(self, canal, adresse):
        self.queue = queue.Queue()
        self.running = True
        self.thread = True
        self.canal = canal
        self.adresse = adresse

    def receive(self):
        while self.running:
            data = self.lora.receive()
            if data:
                self.queue.put(data)

            time.sleep(0.01)

    def send(self, msg):
        print(f"SENDING {msg}")
        self.lora.sendraw(msg)

    def check(self):
        try:
            return self.queue.get_nowait()
        except Exception as e:
            return None    

    def activer(self):
        #initialize lora
        self.lora = sx126x.sx126x(channel=self.canal,address=self.adresse,network=0)

        self.thread = threading.Thread(target=self.receive)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

