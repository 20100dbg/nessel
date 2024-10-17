import threading
import time
import queue
from rtlsdr import RtlSdr

class scanner:

    def __init__(self, frequence_debut, frequence_fin):
        self.queue = queue.Queue()
        self.running = True
        self.thread = True
        self.frequence_debut = frequence_debut
        self.frequence_fin = frequence_fin


    def check(self):
        try:
            return self.queue.get_nowait()
        except Exception as e:
            return None

    def activer(self):
        self.sdr = RtlSdr()
        self.thread = threading.Thread(target=self.scanner)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def arr_abs(self, arr):
        return [abs(x) for x in arr]

    def arr_mean(self, arr):
        return sum(arr) / len(arr)

    def arr_pow(self, arr, p):
        return [x ** p for x in arr]

    def get_frq_power(self, sdr, frq, nb_samples):    
        self.sdr.center_freq = frq # Hz
        x = self.sdr.read_samples(nb_samples)
        return self.arr_mean(self.arr_pow(self.arr_abs(x),2))

    def scanner(self):
        x = 0
        
        while self.running:

            nb_samples = 1024 * 4
            self.sdr.bandwith = 12.5e3 #0 = auto
            self.sdr.sample_rate = 2.048e6 # Hz
            self.sdr.freq_correction = 60  # PPM
            self.sdr.gain = 49

            threshold = 0.9
            frq = self.frequence_debut
            frq_start_detection = 0
            hop_width = 250000

            while True:
                if not self.running:
                    break

                avg_pwr = self.get_frq_power(self.sdr, frq, nb_samples)
                #print(f"\rScanning {pretty_frq(self.sdr.center_freq)} {avg_pwr}", end='')
                
                if avg_pwr >= threshold:
                
                    if frq_start_detection == 0:
                        frq -= 100000
                        frq_start_detection = self.sdr.center_freq
                        old_hop_width = hop_width
                        hop_width = 50000
                        max_pwr = 0
                        max_frq = 0
                    
                    if avg_pwr > max_pwr:
                        max_pwr = avg_pwr
                        max_frq = self.sdr.center_freq
                
                elif frq_start_detection != 0:
                    #print(f"\nFound activity on {pretty_frq(max_frq)} / start {frq_start_detection}")
                    self.queue.put(max_frq)

                    frq_start_detection = 0
                    hop_width = old_hop_width
                
                frq += hop_width

                if frq > self.frequence_fin:
                    frq = self.frequence_debut

            self.sdr.close()


