import socket
import threading
import sys

# Configuración del cliente
HOST = '127.0.0.1'
PORT = 12346

# Solicitar nombre de usuario
username = input('Introduce tu nombre de usuario: ')

# Crear el socket del cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

# Enviar nombre de usuario al servidor
cliente.send(username.encode('utf-8'))

def recibir_mensajes():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            if mensaje:
                print(mensaje)
            else:
                break
        except:
            print("Ocurrió un error al recibir el mensaje.")
            cliente.close()
            break

def enviar_mensajes():
    while True:
        mensaje = f"{username}: {input('')}"
        cliente.send(mensaje.encode('utf-8'))

# Iniciar hilos para recibir y enviar mensajes
hilo_recibir = threading.Thread(target=recibir_mensajes)
hilo_recibir.start()

hilo_enviar = threading.Thread(target=enviar_mensajes)
hilo_enviar.start()
