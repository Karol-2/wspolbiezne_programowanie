# proces otwierający kolekę IPC i wysyłający 
# 3 komunikaty  o typie 2

import sysv_ipc

klucz=11
s='bb'
mq = sysv_ipc.MessageQueue(klucz)

for i in range(0, 3):
    mq.send(s.encode(),True,2)
    print('2 wysyła')

