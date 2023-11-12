import signal, sys


def handler(signum, frame):
    print(' Obsługa sygnału ', signum)


def handler1(signum, frame):
    print(' Inna obsługa  sygnału ', signum)
    sys.exit(0)


# przypisanie obsługi sygnału do SIGINT
signal.signal(signal.SIGINT, handler)

# przypisanie obsługi sygnału do SIGUSR!
signal.signal(signal.SIGUSR1, handler1)

while True:
    pass
