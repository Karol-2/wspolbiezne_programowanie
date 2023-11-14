import os


class MessageInfo:
    def __init__(self, length, id, homepath):
        self.length = length
        self.id = id
        self.homepath = homepath


def get_id(arg):
    id = -1
    if arg is not None:
        id = int(arg)
    else:
        print("Nie podano ID rekordu!")
    return id


def send_message(klient, data):
    buffer = bytearray()
    buffer.extend(data.length.to_bytes(4, byteorder='big'))
    buffer.extend(data.id.to_bytes(4, byteorder='big'))
    buffer.extend(data.homepath.encode())
    klient.write(buffer)


def get_server_data(serwer):
    length_bytes = serwer.read(4)
    length = int.from_bytes(length_bytes, byteorder='big')
    nazwisko = serwer.read(length).decode()
    print(nazwisko)


def main():
    data = MessageInfo(0, 0, "")

    data.id = get_id(os.sys.argv[1])
    data.homepath = os.getenv("HOME")
    data.length = 8 + len(data.homepath.encode())

    if data.id < 0:
        return 1

    klient = os.open("klientfifo", os.O_WRONLY)
    serwer = os.open("serwerfifo", os.O_RDONLY)

    send_message(klient, data)
    get_server_data(serwer)


if __name__ == "__main__":
    main()
