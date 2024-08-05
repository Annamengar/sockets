import socket
import select

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 12346

# Crear el socket del servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen(5)

# Lista de sockets y diccionario de clientes
sockets_list = [servidor]
clientes = {}  # Almacena los sockets y nombres de usuario

print(f'Servidor escuchando en {HOST}:{PORT}...')

def broadcast(mensaje, socket_excepcion):
    # Enviar el mensaje a todos los clientes excepto al que lo envió
    for cliente_socket in clientes:
        if cliente_socket != socket_excepcion:
            try:
                cliente_socket.send(mensaje)
            except:
                cliente_socket.close()
                sockets_list.remove(cliente_socket)
                del clientes[cliente_socket]

def manejar_mensaje(mensaje, cliente_socket):
    # Enviar el mensaje a todos los clientes excepto al que lo envió
    broadcast(mensaje, cliente_socket)

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == servidor:
            cliente_socket, cliente_address = servidor.accept()
            sockets_list.append(cliente_socket)
            # Solicitar nombre de usuario
            cliente_socket.send('Introduce tu nombre de usuario: '.encode('utf-8'))
            username = cliente_socket.recv(1024).decode('utf-8')
            clientes[cliente_socket] = username
            print(f'Nueva conexión aceptada de {cliente_address} con nombre de usuario {username}')
            broadcast(f'{username} se ha unido al chat.'.encode('utf-8'), cliente_socket)
        else:
            try:
                mensaje = notified_socket.recv(1024)
                if not mensaje:
                    username = clientes[notified_socket]
                    print(f'Conexión cerrada de {username}')
                    broadcast(f'{username} ha salido del chat.'.encode('utf-8'), notified_socket)
                    sockets_list.remove(notified_socket)
                    del clientes[notified_socket]
                    continue
                manejar_mensaje(mensaje, notified_socket)
            except:
                username = clientes[notified_socket]
                print(f'Conexión cerrada de {username}')
                sockets_list.remove(notified_socket)
                del clientes[notified_socket]
                continue

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clientes[notified_socket]
