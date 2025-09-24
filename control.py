from gpiozero import AngularServo
from time import sleep
servoPin = 14

servo = AngularServo(servoPin, min_angle = 0, max_angle = 180, min_pulse_width = 0.5/1000, max_pulse_width = 2.5/1000)

def set_angle(angle):
    servo.angle = angle
    sleep(1)

try:
    while True:
        angle = int(input("Ingresa un angulo de 0 a 180: "))
        set_angle(angle)
except KeyboardInterrupt:
    print("programa interrumpido")