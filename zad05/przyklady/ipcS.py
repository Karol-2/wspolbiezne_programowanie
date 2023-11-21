# proces tworzący kolekę IPC i odbierający 
# 6 komunikatów, naprzemian typu 1 i typu 2

import sysv_ipc

klucz=11

mq = sysv_ipc.MessageQueue(klucz, sysv_ipc.IPC_CREAT)

for i in range(0, 3):
    s, t = mq.receive(True,1)
    s = s.decode()
    print("Serwer: odebrałem %s  " % s)
    s, t = mq.receive(True,2)
    s = s.decode()
    print("Serwer: odebrałem %s  " % s)

mq.remove()
