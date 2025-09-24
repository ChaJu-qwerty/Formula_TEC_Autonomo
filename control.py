import socket
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Servo setup
factory = PiGPIOFactory()
servoPin = 23
servo = AngularServo(servoPin, min_angle=0, max_angle=180,
                     min_pulse_width=0.0005, max_pulse_width=0.0025,
                     frame_width=0.02, pin_factory=factory)

def set_angle(angle):
    angle = max(0, min(180, angle))
    servo.angle = round(angle)
    sleep(0.2)

# Servidor TCP (solo escucha a vision.py)
HOST = "127.0.0.1"   # mismo Raspberry
PORT = 5000          # puerto para control

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print("Esperando conexión de vision.py en", PORT)

conn, addr = sock.accept()
print("Conectado a vision.py:", addr)

try:
    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break
        angle = int(data)
        print("Ángulo recibido:", angle)
        set_angle(angle)

except KeyboardInterrupt:
    print("Interrumpido por usuario")
finally:
    conn.close()
    servo.detach()

