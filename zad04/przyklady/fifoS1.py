import os
import errno
import time
import multiprocessing

FIFO = 'kolejka'

# Utworzenie kolejki
try:
    os.mkfifo(FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

# Kolejka komunikatów do komunikacji między procesami
fifo_queue = multiprocessing.Queue()


def server():
    # Kolejka otwarta do odczytu
    fifo_in = os.open(FIFO, os.O_RDONLY)

    while True:
        r = os.read(fifo_in, 2)  # Czytanie 2 bajtów
        if len(r) > 0:
            print("Serwer: %s" % r.decode())
            # Przesłanie komunikatu do kolejki komunikatów
            fifo_queue.put(r.decode())
        else:
            print("Klient skończył")
            break
        time.sleep(5)  # Spowolnienie do testowania


# Uruchomienie serwera w osobnym procesie
server_process = multiprocessing.Process(target=server)
server_process.start()

while True:
    try:
        # Odczytanie komunikatu z kolejki komunikatów
        message = fifo_queue.get_nowait()
        print(f"Odczytano z kolejki komunikatów: {message}")
    except queue.Empty:
        pass

    time.sleep(1)  # Odczekanie 1 sekundy
