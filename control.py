from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Usar PiGPIO para PWM más estable
factory = PiGPIOFactory()
servoPin = 23

servo = AngularServo(servoPin, 
                    min_angle=0, 
                    max_angle=180,
                    min_pulse_width=0.0005,   # 0.5ms
                    max_pulse_width=0.0025,   # 2.5ms
                    frame_width=0.02,         # 20ms periodo
                    pin_factory=factory)

def set_angle(angle):
    # Limitar ángulo y redondear
    angle = max(0, min(180, angle))
    rounded_angle = round(angle)
    
    servo.angle = rounded_angle
    sleep(0.5)  # Tiempo suficiente para movimiento

try:
    while True:
        angle = int(input("Ingresa un ángulo de 0 a 180: "))
        set_angle(angle)
except KeyboardInterrupt:
    print("Programa interrumpido")
    servo.detach()  # Liberar el servo