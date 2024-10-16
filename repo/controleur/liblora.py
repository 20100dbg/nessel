import threading
import time
import queue

class lora:

    def __init__(self):
        self.q = queue.Queue()
        self.running = True
        self.t = True

    def receive(self):
        x = 0
        
        while self.running:
            self.q.put(x)
            x += 5
            
            time.sleep(1)

    def send(self, msg):
        print(f"SENDING {msg}")

    def check(self):
        try:
            return self.q.get_nowait()
        except Exception as e:
            return None    

    def activer(self):
        t = threading.Thread(target=self.receive)
        t.start()

    def stop(self):
        self.running = False
