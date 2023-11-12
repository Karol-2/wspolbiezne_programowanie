import multiprocessing
import time


def server(database, server_input_queue):
    while True:
        print("czekam...")

        # Odbierz zapytanie od klienta
        request = server_input_queue.get()
        print(request)
        # Sprawdź, czy zapytanie jest poprawne
        if 'id' in request and 'response_queue' in request:
            client_id = request['id']
            response_queue = request['response_queue']

            # Sprawdź bazę danych i przygotuj odpowiedź
            response = database.get(client_id, "Nie ma")
            print(response)
            # Odpowiedź klientowi
            response_queue.put(response)
        else:
            print("Nieprawidłowe zapytanie")


if __name__ == '__main__':
    # Przykładowa baza danych
    database = {1: 'Taylor', 2: 'Dua', 3: 'Britney'}

    # Utwórz menedżera
    manager = multiprocessing.Manager()

    # Kolejka wejściowa dla serwera (wspólna dla wszystkich klientów)
    server_input_queue = manager.Queue()

    server(database, server_input_queue)

    # Uruchomienie serwera w osobnym procesie
    # server_process = multiprocessing.Process(target=server, args=(database, server_input_queue))
    # server_process.start()
    #
    # # Przykładowe zapytanie od klienta
    # client_request = {'id': 2, 'response_queue': manager.Queue()}
    #
    # # Wysłanie zapytania do serwera
    # server_input_queue.put(client_request)
    #
    # # Oczekiwanie na odpowiedź od serwera
    # response = client_request['response_queue'].get()
    #
    # # Wyświetlenie odpowiedzi
    # print("Odpowiedź od serwera:", response)
    #
    # # Zakończenie procesu serwera
    # server_process.terminate()
