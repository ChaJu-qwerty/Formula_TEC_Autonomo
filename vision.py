import socket
import time
import random

# Servidores: control en la Pi y monitor en la laptop
servers = [
    ("127.0.0.1", 5000),   # control.py (mismo Raspberry Pi)
    ("192.168.1.60", 5001) # monitor.py (otra laptop en la red)
]

# Conectar sockets TCP
sockets = []
for ip, port in servers:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    sockets.append(s)

try:
    while True:
        # Generar ángulo aleatorio
        angle = random.randint(0, 180)
        message = str(angle).encode("utf-8")

        # Enviar a todos los servidores
        for s in sockets:
            s.sendall(message)

        print("Ángulo enviado:", angle)
        time.sleep(1)

except KeyboardInterrupt:
    print("Cerrando conexiones...")
    for s in sockets:
        s.close()