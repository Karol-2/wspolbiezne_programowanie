# proces otwierający kolekę IPC i wysyłający 
# 3 komunikaty  o typie 1

import sysv_ipc

klucz=11
s='aaa'
mq = sysv_ipc.MessageQueue(klucz)

for i in range(0, 3):
    mq.send(s.encode(),True,1)
    print('1 wysyła')
