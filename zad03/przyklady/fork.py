# przykład użycia fork() 
import os 
import time
import errno

# rozgałęziamy proces
pid = os.fork()
  
# niezerowy pid oznacza, że jesteśmy w procesie macierzystym
if pid>0 :
    print("ojciec: mój PID: ", os.getpid())
    print("ojciec: pid stworzonego syna: ",pid)      
    print("ojciec: kontynuuacja działania")
    time.sleep(1)  
    print("ojciec: kończę")
elif pid == 0:
    print("syn: zaczynam")
    print("syn: mój PID: ", os.getpid())
    time.sleep(1)
    print("syn: kończę")
else:
    print("ojciec: błąd przy tworzeniu procesu")
    # wykorzystując moduł errno można sprawdzić
    # co to za błąd
      
