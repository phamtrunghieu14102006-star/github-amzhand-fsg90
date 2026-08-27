import cv2
import mediapipe as mp
import time
import math
import numpy as np
import serial

BAUD_RATE = 9600
COM_PORT = 'COM3'

try:
    arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2)
    print(f"Da ket noi thanh cong voi Arduino qua {COM_PORT}!")
except Exception as e:
    print("Chua cam Arduino (Dang chay che do Test giao dien):", e)
    arduino = None

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

latest_result = None

def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global latest_result
    latest_result = result

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    result_callback=print_result
)

def get_distance(p1, p2, w, h):
    x1, y1 = int(p1.x * w), int(p1.y * h)
    x2, y2 = int(p2.x * w), int(p2.y * h)
    return math.hypot(x2 - x1, y2 - y1)

prev_angles = np.array([90.0] * 8)
ALPHA = 0.3  # Bo loc EMA triet de rung giat cho SG90

with HandLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        frame_timestamp_ms = int(time.time() * 1000)
        landmarker.detect_async(mp_image, frame_timestamp_ms)

        if latest_result and latest_result.hand_landmarks:
            landmarks = latest_result.hand_landmarks[0]
            wrist = landmarks[0]
            palm_base = landmarks[9]

            palm_size = get_distance(wrist, palm_base, w, h)
            if palm_size == 0:
                palm_size = 1.0

            finger_tips = [4, 8, 12, 16]
            raw_8_angles = []

            for tip_idx in finger_tips:
                dist = get_distance(landmarks[tip_idx], wrist, w, h)
                ratio = dist / palm_size
                
                # Tinh offset goc dao dong
                offset = int(np.interp(ratio, [0.6, 1.6], [-40, 50]))
                
                # Quyen doi cho 2 Servo / 1 ngon tay trai
                s1_angle = 90 + offset
                s2_angle = 90 - offset
                raw_8_angles.extend([s1_angle, s2_angle])

            # Bo loc muot goc EMA
            raw_8_angles = np.array(raw_8_angles, dtype=float)
            smooth_angles = ALPHA * raw_8_angles + (1 - ALPHA) * prev_angles
            prev_angles = smooth_angles
            final_angles = smooth_angles.astype(int)

            data_string = ",".join(map(str, final_angles)) + "\n"

            if arduino and arduino.is_open:
                arduino.write(data_string.encode('utf-8'))

            cv2.putText(frame, f"Left Hand 8 Servos: {list(final_angles)}", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            for lm in landmarks:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

        cv2.imshow("Amazing Hand Left - Webcam Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    if arduino and arduino.is_open:
        arduino.close()