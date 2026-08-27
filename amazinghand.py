import time
import serial
import numpy as np

BAUD_RATE = 9600
COM_PORT = 'COM3'

try:
    arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2)
    print(f"Da ket noi thanh cong voi Arduino qua {COM_PORT}!")
except Exception as e:
    print("Loi ket noi Serial:", e)
    arduino = None

# Thiet lap rieng cho Tay Trai (Side = 2)
Side = 2
MIDDLE_POS = [90] * 8
current_angles = list(MIDDLE_POS)

def send_8_servos(angles):
    bounded_angles = [int(np.clip(a, 0, 180)) for a in angles]
    data_string = ",".join(map(str, bounded_angles)) + "\n"
    if arduino and arduino.is_open:
        arduino.write(data_string.encode('utf-8'))
        print(f"Sent 8 Servos (Left Hand): {bounded_angles}")

def move_finger(finger_idx, a1, a2):
    s1_idx = finger_idx * 2
    s2_idx = finger_idx * 2 + 1
    current_angles[s1_idx] = MIDDLE_POS[s1_idx] + a1
    current_angles[s2_idx] = MIDDLE_POS[s2_idx] + a2
    send_8_servos(current_angles)

def Move_Thumb(a1, a2):  move_finger(0, a1, a2)
def Move_Index(a1, a2):  move_finger(1, a1, a2)
def Move_Middle(a1, a2): move_finger(2, a1, a2)
def Move_Ring(a1, a2):   move_finger(3, a1, a2)

# --- DINH NGHIA CAC CU CHI TAY TRAI ---
def OpenHand():
    Move_Thumb(-35, 35)
    Move_Index(-35, 35)
    Move_Middle(-35, 35)
    Move_Ring(-35, 35)

def CloseHand():
    Move_Thumb(60, -60)
    Move_Index(60, -60)
    Move_Middle(60, -60)
    Move_Ring(60, -60)

def OpenHand_Progressive():
    Move_Thumb(-35, 35)
    time.sleep(0.15)
    Move_Index(-35, 35)
    time.sleep(0.15)
    Move_Middle(-35, 35)
    time.sleep(0.15)
    Move_Ring(-35, 35)

def SpreadHand():
    # Toa do dang ngon Tay Trai
    Move_Thumb(-4, 45)
    Move_Index(-45, 0)
    Move_Middle(-20, 20)
    Move_Ring(-4, 45)

def ClenchHand():
    # Toa do khep ngon Tay Trai
    Move_Thumb(-45, -4)
    Move_Index(0, 30)
    Move_Middle(-20, 20)
    Move_Ring(-35, 0)

def Index_Pointing():
    Move_Index(-40, 40)
    Move_Middle(60, -60)
    Move_Ring(60, -60)
    Move_Thumb(60, -60)

def Nonono():
    Index_Pointing()
    for _ in range(3):
        time.sleep(0.2)
        Move_Index(-10, 40)
        time.sleep(0.2)
        Move_Index(-40, 10)
    Move_Index(-35, 35)

def Perfect():
    # Chu OK Tay Trai
    Move_Thumb(-10, -30)
    Move_Index(25, -25)
    Move_Middle(0, 0)
    Move_Ring(-10, 10)

def Victory():
    Move_Thumb(60, -60)
    Move_Index(-15, 35)
    Move_Middle(-35, 15)
    Move_Ring(60, -60)

def Scissors():
    Victory()
    for _ in range(3):
        time.sleep(0.2)
        Move_Index(-25, 10)
        Move_Middle(-10, 25)
        time.sleep(0.2)
        Move_Index(-15, 35)
        Move_Middle(-35, 15)

def Pinched():
    Move_Thumb(0, -40)
    Move_Index(50, -50)
    Move_Middle(50, -50)
    Move_Ring(50, -50)

def Fuck():
    Move_Thumb(60, -60)
    Move_Index(60, -60)
    Move_Middle(-35, 35)
    Move_Ring(60, -60)

def main():
    if not arduino:
        print("Khong co ket noi Arduino. Dung chuong trinh!")
        return

    try:
        while True:
            OpenHand()
            time.sleep(1.0)

            CloseHand()
            time.sleep(2.0)

            OpenHand_Progressive()
            time.sleep(0.8)

            SpreadHand()
            time.sleep(0.8)

            ClenchHand()
            time.sleep(0.8)

            Index_Pointing()
            time.sleep(1.0)

            Nonono()
            time.sleep(0.8)

            Perfect()
            time.sleep(1.5)

            Victory()
            time.sleep(1.0)

            Scissors()
            time.sleep(1.0)

            Pinched()
            time.sleep(1.5)

            Fuck()
            time.sleep(1.5)

    except KeyboardInterrupt:
        print("\nDung chuong trinh. Dua tay ve vi tri xoe!")
        OpenHand()
        if arduino and arduino.is_open:
            arduino.close()

if __name__ == '__main__':
    main()