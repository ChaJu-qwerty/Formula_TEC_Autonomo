import socket

HOST = "0.0.0.0"   # escuchar en cualquier interfaz
PORT = 5001        # puerto para monitor

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print("Esperando conexión desde vision.py en", PORT)

conn, addr = sock.accept()
print("Conectado a vision.py:", addr)

try:
    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break
        print("Ángulo recibido:", data)

except KeyboardInterrupt:
    print("Cerrando servidor...")
finally:
    conn.close()
