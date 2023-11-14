import os

DB_SIZE = 10
MAX_LINE = 70
DB_DATA_FILE = "baza"


class ClientData:
    def __init__(self, id, nazwisko):
        self.id = id
        self.nazwisko = nazwisko


class MessageData:
    def __init__(self, id, homepath):
        self.id = id
        self.homepath = homepath


def create_database():
    data = [ClientData(0, "") for _ in range(DB_SIZE)]

    try:
        with open(DB_DATA_FILE, "r") as fp:
            for i, line in enumerate(fp):
                if i >= DB_SIZE:
                    break
                id, nazwisko = line.strip().split(maxsplit=1)
                data[i].id = int(id)
                data[i].nazwisko = nazwisko
    except FileNotFoundError:
        print("Brak pliku z zawartością bazy danych!")
        return None

    return data


def get_nazwisko_by_id(data, id):
    for client in data:
        if client.id == id:
            return client.nazwisko
    return "Nie ma rekordu z takim podanym ID w bazie danych!"


def get_client_data(client, size):
    buffer = client.read(size)
    data = MessageData(0, "")
    data.id, data.homepath = int.from_bytes(buffer[:4], byteorder='big'), buffer[4:].decode()
    return data


def send_message(server, db, data):
    nazwisko = get_nazwisko_by_id(db, data.id)
    length = len(nazwisko)
    message = length.to_bytes(4, byteorder='big') + nazwisko.encode()
    server.write(message)


def main():
    dbdata = create_database()

    os.mkfifo("klientfifo", 0o666)
    os.mkfifo("serwerfifo", 0o666)

    with open("klientfifo", "rb") as klient, open("serwerfifo", "wb") as serwer:
        while True:
            message_length = int.from_bytes(klient.read(4), byteorder='big')
            if message_length > 0:
                data = get_client_data(klient, message_length)
                send_message(serwer, dbdata, data)

    os.unlink("klientfifo")
    os.unlink("serwerfifo")


if __name__ == "__main__":
    main()
