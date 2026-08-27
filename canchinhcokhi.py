import time
import serial

BAUD_RATE = 9600
COM_PORT = 'COM3'  # Thay cong COM tuong ung tren may tinh

try:
    arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2)
    print(f"Da ket noi thanh cong voi Arduino qua {COM_PORT}!")
except Exception as e:
    print("Loi ket noi Serial:", e)
    arduino = None

# Set tat ca 8 Servo tay trai ve goc Home 90 do
HOME_ANGLES = [90] * 8

def main():
    if not arduino:
        print("Khong co ket noi Arduino. Dung chuong trinh!")
        return

    print("Dang giu 8 Servo Tay Trai o goc trung tinh 90 deg de lap rap co khi...")
    try:
        while True:
            data_string = ",".join(map(str, HOME_ANGLES)) + "\n"
            if arduino and arduino.is_open:
                arduino.write(data_string.encode('utf-8'))
            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\nDung chuong trinh Home!")
        if arduino and arduino.is_open:
            arduino.close()

if __name__ == '__main__':
    main()