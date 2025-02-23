import socket
import threading
import mcrcon

clients = {}
clients_ron = {}
clients_skills = {}
is_game_started = False

def data_checker():
    data = list(map(lambda x: x.split(), list(clients.values())))
    if len(data) == 3 and all([len(data[0])==2, len(data[1])==2, len(data[2])==2]):
        d=[]
        for e in data:
            for i in e:
                d.append(i)
        if d.count('Runner') == 1 and d.count('TimeConverter18') == 1 and d.count('Remix008') == 1 and d.count('AlexUgar') == 1:
            return 'ready!'
    return 'hmm'

def start_game():
    global clients_skills
    host = "26.11.111.77"
    port = 25575
    password = "leshagay"
    mcr = mcrcon.MCRcon(host, password, port)
    mcr.connect()
    mcr.command('weather clear')
    mcr.command('time set day')
    mcr.command('gamemode survival @a')
    res = str(clients_skills) + '†' + str(dict(e.split() for e in clients.values()))
    for client in clients:
        client.send(res.encode('utf-8'))
    for client in clients:
        cl = clients[client].split()
        print()
        print(mcr.command(f'sudoop TimeConverter18 {cl[1].lower()} add {cl[0]}'))
    mcr.command('sudoop TimeConverter18 huntplus start 0')
    mcr.command('gamerule sendCommandFeedback false')
    print('ВСЁ')

def handle_client(client_socket, client_address):
    global clients_skills
    global is_game_started
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Сообщение от {client_address}: {message}")
                if '@' in message:
                    message.split('@')
                    clients_skills[message[0]] = message[1]
                elif message.count(' ') == 1:
                    clients[client_socket] = message
                    print(clients)
                    response = data_checker()
                    for client in list(clients.keys()):
                        client.send(response.encode('utf-8'))
                elif message.count(' ') == 0:
                    clients_ron[client_socket] = message
                    s = list(clients_ron.values())
                    print(s)
                    if len(s) == 3 and s[0] == 'y' and s[1] == 'y' and s[2] == 'y':
                        for client in list(clients_ron.keys()):
                            client.send('readytostart'.encode('utf-8'))

                    while len(clients_skills) != 3:
                        message2 = client_socket.recv(1024).decode('utf-8')
                        if message2:
                            if '@' in message2:
                                message2 = message2.split('@')
                                clients_skills[message2[0]] = message2[1]
                    if not is_game_started:
                        is_game_started = True
                        start_game()
        except:
            print(f"Клиент {client_address} отключился")
            clients.pop(client_socket)
            clients_ron.pop(client_socket)
            client_socket.close()
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('26.11.111.77', 12345))
server.listen(3)
print("Сервер запущен и ожидает подключения клиентов...")

while True:
    if len(clients) <= 3:
        client_socket, client_address = server.accept()
        print(f"Клиент {client_address} подключился")
        clients[client_socket] = 'nodata'

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()