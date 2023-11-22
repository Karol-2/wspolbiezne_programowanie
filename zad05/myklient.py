import sysv_ipc
import os

# Klucze kolejek komunikatów
input_queue_key = 1111
output_queue_key = 6666

# Kolejki komunikatów
input_queue = sysv_ipc.MessageQueue(input_queue_key)
output_queue = sysv_ipc.MessageQueue(output_queue_key)

# PID klienta
pid = os.getpid()


def send_request(word):
    # Wysyłanie zapytania do serwera
    request = f'{pid},{word}'
    input_queue.send(request, type=int(pid))


def receive_response():
    # Odbieranie odpowiedzi od serwera
    response, _ = output_queue.receive(type=pid)
    print(f'Odpowiedź serwera: {response.decode("utf-8")}')


if __name__ == "__main__":
    print("Pid procesu: ", pid)
    word_to_translate = input("Podaj słowo do przetłumaczenia: ")
    # Wysyłanie zapytania do serwera
    send_request(word_to_translate)

    # Odbieranie odpowiedzi od serwera
    receive_response()
