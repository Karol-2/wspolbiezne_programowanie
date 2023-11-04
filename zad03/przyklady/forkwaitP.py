# przykład fork, exit, wait plus ilustracja przekazania
# jakiejś wartości do procesu potomnego
import os 
import time
import sys

parametr = 5
paramDlaSyna = 11
# rozgałęziamy proces
pid = os.fork()
  
# niezerowy pid oznacza, że jesteśmy w procesie macierzystym
if pid > 0 :
    print("ojciec: pid stworzonego syna: ",pid)      
    # czekanie na zakończenie (jakiegoś) syna 
    status = os.wait()

    print("ojciec: PID procesu zakończonego:", status[0])
    if os.WIFSIGNALED(status[1]):
       print("ojciec: Sygnał, który zabił proces syna", status[1])
    if os.WIFEXITED(status[1]):
       print("ojciec: zwrócony kod powrotu syna ", os.WEXITSTATUS(status[1]))
  
else :
    print("syn: zaczynam")
    parametr = paramDlaSyna
    print("syn: mój PID: ", os.getpid())
    time.sleep(1)
    print("syn: kończę")
    os._exit(parametr)
#   ewentualnie  sys.exit(parametr)
      
