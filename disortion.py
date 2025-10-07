import cv2
import serial
import time

# Serial to Pico(COM port or /dev/ttyUSB0)
pico = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(2)

# Open webcam
cap = cv2.VideoCapture(0)

# Servo positions start mid-range
servo_angles = [90, 90, 90, 90]

def send_servos(angles):
    cmd = ",".join([f"{i}:{a}" for i,a in enumerate(angles)]) + "\n"
    pico.write(cmd.encode())

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find bright spot (simulate "distortion target")
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    M = cv2.moments(thresh)
    if M["m00"] != 0:
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])

        # crude feedback: shift servos depending on centroid
        if cx < frame.shape[1]//2 - 20:
            servo_angles[0] = min(180, servo_angles[0]+1)
        elif cx > frame.shape[1]//2 + 20:
            servo_angles[0] = max(0, servo_angles[0]-1)

        if cy < frame.shape[0]//2 - 20:
            servo_angles[1] = min(180, servo_angles[1]+1)
        elif cy > frame.shape[0]//2 + 20:
            servo_angles[1] = max(0, servo_angles[1]-1)

        send_servos(servo_angles)

    # Display debug
    cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)
    cv2.imshow("AO Demo", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
