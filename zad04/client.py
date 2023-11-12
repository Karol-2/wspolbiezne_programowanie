import multiprocessing

def client(server_input_queue, client_id, response_queue):
    # Przygotuj zapytanie do serwera
    request = {'id': client_id, 'response_queue': response_queue}
    print(request)
    # Wyślij zapytanie do serwera
    server_input_queue.put(request)
    print("wyslano")
    # Oczekiwanie na odpowiedź od serwera
    response = response_queue.get()

    # Wyświetlenie odpowiedzi
    print("Odpowiedź od serwera:", response)

if __name__ == '__main__':
    # Utwórz menedżera
    manager = multiprocessing.Manager()

    # Kolejka wejściowa dla serwera (wspólna dla wszystkich klientów)
    server_input_queue = manager.Queue()

    # Kolejka odpowiedzi dla klienta
    response_queue = manager.Queue()

    # ID klienta
    client_id = 2

    # Uruchomienie klienta w osobnym procesie
    client_process = multiprocessing.Process(target=client, args=(server_input_queue, client_id, response_queue))
    client_process.start()

    # Oczekiwanie na zakończenie procesu klienta
    client_process.join()
