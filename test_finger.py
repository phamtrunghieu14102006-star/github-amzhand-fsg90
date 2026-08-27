import time
import serial

BAUD_RATE = 9600
COM_PORT = 'COM3'

try:
    arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2)
    print(f"Da ket noi thanh cong voi Arduino qua {COM_PORT}!")
except Exception as e:
    print("Loi ket noi Serial:", e)
    arduino = None

# Chon index ngon tay muon test: 0 (Ngon cai), 1 (Ngon tro), 2 (Ngon giua), 3 (Ngon nhan)
TEST_FINGER_INDEX = 1  # Mac dinh test Ngon tro (Servo index 2 va 3)

MIDDLE_POS = [90] * 8
current_angles = list(MIDDLE_POS)

def send_finger_command(finger_idx, offset1, offset2):
    s1_idx = finger_idx * 2
    s2_idx = finger_idx * 2 + 1
    
    current_angles[s1_idx] = max(0, min(180, MIDDLE_POS[s1_idx] + offset1))
    current_angles[s2_idx] = max(0, min(180, MIDDLE_POS[s2_idx] + offset2))
    
    data_string = ",".join(map(str, current_angles)) + "\n"
    if arduino and arduino.is_open:
        arduino.write(data_string.encode('utf-8'))
        print(f"Test Ngon {finger_idx} Tay Trai -> Angles: [{current_angles[s1_idx]}, {current_angles[s2_idx]}]")

def main():
    if not arduino:
        print("Khong co ket noi Arduino. Dung chuong trinh!")
        return

    try:
        while True:
            print("Action: Gap ngon tay...")
            send_finger_command(TEST_FINGER_INDEX, 60, -60)
            time.sleep(2.5)

            print("Action: Xoe ngon tay...")
            send_finger_command(TEST_FINGER_INDEX, -35, 35)
            time.sleep(1.5)

    except KeyboardInterrupt:
        print("\nDung test. Dua tay ve goc 90 deg!")
        data_string = ",".join(map(str, [90] * 8)) + "\n"
        if arduino and arduino.is_open:
            arduino.write(data_string.encode('utf-8'))
            arduino.close()

if __name__ == '__main__':
    main()