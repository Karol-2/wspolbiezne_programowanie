# liczenie sumy trzech składników
import os
import sys
import time


def f(x, y, z):
    return x * x + y + 5


def g(x, y, z):
    return 3 * x + y * y - 1


def h(x, y, z):
    return y * y + z * x + 3


def fgh(x, y, z):
    #  liczy f(x,y,z)+2*g(x,y,z)+x*h(x,y,z)
    return f(x, y, z) + 2 * g(x, y, z) + x * h(x, y, z)


def fghW(x, y, z):
    suma = 0
    # rozgałęziamy proces dla 2*g(x,y,z)
    pid = os.fork()
    if pid > 0:  # proces macierzysty
        print("PID pierwszego syna: ", pid)
        # rozgałęziamy proces dla x*h(x,y,z)
        pid = os.fork()
        if pid > 0:  # nadal proces macierzysty
            print("PID drugiego syna,składnik ojca: ", pid, f(x, y, z))
            suma = f(x, y, z)
            # czekanie na zakończenie (jakiegoś) syna
            status = os.wait()
            if os.WIFSIGNALED(status[1]):
                print("ojciec: Sygnał, który zabił syna", status[1])
            if os.WIFEXITED(status[1]):
                suma = suma + os.WEXITSTATUS(status[1])
                print("pierwszy wait: ", os.WEXITSTATUS(status[1]))
            # drugie czekanie na zakończenie (jakiegoś) syna
            status = os.wait()
            if os.WIFSIGNALED(status[1]):
                print("ojciec: Sygnał, który zabił syna", status[1])
            if os.WIFEXITED(status[1]):
                suma = suma + os.WEXITSTATUS(status[1])
                print("drugi wait: ", os.WEXITSTATUS(status[1]))
                return suma
        else:  # syn drugi
            #  time.sleep(1)
            print("syn drugi: mój PID: ", os.getpid(), x * h(x, y, z))
            sys.exit(x * h(x, y, z))
    else:  # syn pierwszy
        print("syn pierwszy: mój PID: ", os.getpid(), 2 * g(x, y, z))
        sys.exit(2 * g(x, y, z))


print(fgh(2, 3, 4))
print(fghW(2, 3, 4))
