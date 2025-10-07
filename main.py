from machine import Pin, PWM
import time
import sys

# Define servo pins
servo_pins = [15, 16, 17, 18]  # change as per wiring
servos = []

# Setup PWM for each servo
for pin in servo_pins:
    s = PWM(Pin(pin))
    s.freq(50)  # 50Hz for servo
    servos.append(s)

# Function to set servo angle
def set_angle(servo, angle):
    # Convert 0–180 to duty cycle (1000–9000 range approx)
    min_duty = 1000
    max_duty = 9000
    duty = int(min_duty + (angle/180) * (max_duty-min_duty))
    servos[servo].duty_u16(duty)

# Main loop: read serial input like "0:90,1:120,2:45"
while True:
    try:
        line = sys.stdin.readline().strip()
        if not line:
            continue
        commands = line.split(",")
        for cmd in commands:
            idx, angle = cmd.split(":")
            idx, angle = int(idx), int(angle)
            if 0 <= idx < len(servos):
                set_angle(idx, angle)
    except Exception as e:
        pass
