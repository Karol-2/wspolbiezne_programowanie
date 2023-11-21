import sysv_ipc
import os
import time

# Klucze kolejek komunikatów
input_queue_key = 1111
output_queue_key = 6666

# Tworzenie kolejek komunikatów
input_queue = sysv_ipc.MessageQueue(input_queue_key, sysv_ipc.IPC_CREAT)
output_queue = sysv_ipc.MessageQueue(output_queue_key, sysv_ipc.IPC_CREAT)


def polish_to_english(word):
    dictionary = {
        'kot': 'cat',
        'pies': 'dog',
        'dom': 'house',
    }

    return dictionary.get(word, 'Nie znam takiego słowa')


def handle_client_request(request):
    # Odbierz zapytanie od klienta
    pid, word = request.split(',')

    # Przetwórz zapytanie
    translation = polish_to_english(word.strip())

    # Przygotuj odpowiedź
    response = f'{pid},{translation}'

    # Umieść odpowiedź w kolejce wyjściowej
    output_queue.send(response, type=int(pid))


if __name__ == "__main__":
    while True:
        # Odbierz zapytanie od klienta
        request, _ = input_queue.receive(type=0)

        # Symulacja opóźnienia w przetwarzaniu
        time.sleep(2)

        # Obsłuż zapytanie klienta
        handle_client_request(request.decode('utf-8'))
