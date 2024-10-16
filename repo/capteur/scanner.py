import threading
import time
import queue

class scanner:

    def __init__(self):
        self.q = queue.Queue()
        self.running = True
        self.t = True

    def scanner(self):
        x = 0
        
        while self.running:
            self.q.put(x)
            x += 2
            
            time.sleep(1)

    def check(self):
        try:
            return self.q.get_nowait()
        except Exception as e:
            return None
        

    def activer(self):
        t = threading.Thread(target=self.scanner)
        t.start()

    def stop(self):
        self.running = False
