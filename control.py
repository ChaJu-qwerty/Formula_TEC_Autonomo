"""
Control básico de motor con TB6612FNG en Raspberry Pi 4 usando RPi.GPIO.

Conexión (ejemplo):
- TB6612 VM (motor power) -> batería/externa (según motor)
- TB6612 VCC (logic) -> 3.3V de la Raspberry Pi
- TB6612 GND -> GND comunes (Pi + fuente del motor)
- AIN1 -> GPIO 17  (dir A)
- AIN2 -> GPIO 27  (dir A)
- PWMA  -> GPIO 18  (PWM A)
- STBY  -> GPIO 22  (Standby, HIGH para habilitar)
(ajusta pines según tu cableado)

Ejecutar: sudo python3 this_file.py
"""

import RPi.GPIO as GPIO
import time

# --- Configuración de pines (BCM) ---
AIN1 = 23   # Pin de dirección A1
AIN2 = 24   # Pin de dirección A2
PWMA = 18   # Pin PWM para velocidad (canal A) -> usar pin que soporte PWM por software
STBY = 22   # Pin Standby del TB6612 (poner HIGH para habilitar)

PWM_FREQ = 1000  # Frecuencia PWM en Hz

# --- Inicialización ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(STBY, GPIO.OUT)

# Inicial: standby deshabilitado hasta configurar
GPIO.output(STBY, GPIO.LOW)

pwm_a = GPIO.PWM(PWMA, PWM_FREQ)
pwm_a.start(0)  # 0% duty cycle (parado)

def enable_driver():
    """Saca el TB6612 de standby (habilita salidas)."""
    GPIO.output(STBY, GPIO.HIGH)
    time.sleep(0.01)  # pequeño retardo

def disable_driver():
    """Pone el TB6612 en standby (deshabilita salidas)."""
    GPIO.output(STBY, GPIO.LOW)

def set_speed(percent):
    """
    Ajusta velocidad PWM.
    percent: 0..100
    """
    if percent < 0:
        percent = 0
    if percent > 100:
        percent = 100
    pwm_a.ChangeDutyCycle(percent)

def forward(percent=50):
    """Gira motor hacia adelante con velocidad percent%."""
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    set_speed(percent)

def backward(percent=50):
    """Gira motor hacia atrás con velocidad percent%."""
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    set_speed(percent)

def brake():
    """Freno (Both AIN1 y AIN2 HIGH) — para frenar activamente."""
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.HIGH)
    set_speed(0)

def coast():
    """Coast / stop (AIN1 = AIN2 = LOW) — motor libre."""
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    set_speed(0)

def cleanup():
    """Restablece pines y detiene PWM."""
    pwm_a.stop()
    GPIO.output(STBY, GPIO.LOW)
    GPIO.cleanup()

# --- Ejemplo de uso ---
if __name__ == "__main__":
    try:
        enable_driver()
        print("Driver habilitado. Probando motor...")

        print("Adelante al 60% por 3s")
        forward(60)
        time.sleep(3)

        print("Freno activo 1s")
        brake()
        time.sleep(1)

        print("Atrás al 40% por 3s")
        backward(40)
        time.sleep(3)

        print("Coast (parar libre)")
        coast()
        time.sleep(1)

        print("Ramped speed up 0->100")
        for s in range(0, 101, 5):
            forward(s)
            time.sleep(0.05)

        print("Ramped speed down 100->0")
        for s in range(100, -1, -5):
            forward(s)
            time.sleep(0.05)

        coast()
        print("Fin del demo. Deshabilitando driver.")
        disable_driver()

    except KeyboardInterrupt:
        print("Interrumpido por el usuario")

    finally:
        cleanup()
        print("Limpieza completa.")
