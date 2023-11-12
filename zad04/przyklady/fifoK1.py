import os

FIFO = 'kolejka'

fifo_out = os.open(FIFO, os.O_WRONLY) 
os.write(fifo_out, 'abcde'.encode())


