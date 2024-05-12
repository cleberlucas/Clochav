import cv2
import pyzbar.pyzbar as pyzbar
import requests
import json
import threading
import time

_spots_default = {
    "0A": True,
    "0B": True,
    "0C": True,
    "0D": True,
    "0E": True,
    "0F": True,
    "0G": True,
    "0H": True
}

_spots_used = _spots_default.copy()

_frame = None

_decoded_objects = None

def init_spot():
    global _spots_used

    for spot_used in _spots_used.keys():
        floor = spot_used[0]
        space = spot_used[1]
        used = _spots_used[spot_used]

        updateSpot(floor,space,used)

    print("init_spot: Successfully Initialized")

def updateSpot(floor, space, used):
    try:
        api_url = f"http://127.0.0.1:5000/api/parking/space/{floor}/{space}"
        print(api_url)
        payload = {
            "used": used
        }
        json_payload = json.dumps(payload)
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.request("PUT", api_url, data=json_payload, headers=headers)

        if response.status_code != 200:
            print("updateSpot: Error making request. Status code:", response.status_code)

        response.close()

    except Exception as e:
        print("updateSpot: Error making request:", e)

def capture_handler():
    global _frame
    esp32_ip = '192.168.15.101:81'
    video_url = f'http://{esp32_ip}/stream'
    cap = cv2.VideoCapture(video_url)

    if not cap.isOpened():
        print("capture_handler: Error opening video capture")
        return

    while True:
        ret, _frame = cap.read()
        if not ret:
            print("Error reading video frame")
            return

def video_handler():
    global _frame
    global _decoded_objects

    while True:
        if _frame is None or _frame.size == 0:
            print("video_handler: Frame not detected")
            return

        frame = _frame.copy()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        decoded_objects = pyzbar.decode(gray)

        _decoded_objects = decoded_objects

        for obj in decoded_objects:
            bbox = obj.rect
            x, y, w, h = bbox.left, bbox.top, bbox.width, bbox.height

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            qr_data = obj.data.decode('utf-8')
            cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.imshow("Video", frame)
        cv2.waitKey(1)

def monitor_handler():
    global _spots_used
    global _decoded_objects

    while True:
        if _decoded_objects is None:
            print("monitor_handler: Objects not detecteds")
            return

        for obj in _decoded_objects:
            data = obj.data.decode('utf-8')

            try:
                floor = data[0]
                space = data[1]

                spot_used_key = f"{floor}{space}"
                if _spots_used[spot_used_key]:
                    _spots_used[spot_used_key] = False

            except json.JSONDecodeError as e:
                print(f"monitor_handler: Error decoding QR data: {e}")

def integrate_handler():
    global _spots_used

    last_state_spots_used = _spots_used.copy()

    while True:
        spots_used = _spots_used.copy()

        for spot_used in spots_used.keys():
            used = spots_used[spot_used]

            if used != last_state_spots_used[spot_used]:
                floor = spot_used[0]
                space = spot_used[1]
                updateSpot(floor,space,used)
                print(f"monitor_handler: Floor {floor} Space {space} Updated to {'OCCUPIED' if used else 'VACANT'}")
        
        last_state_spots_used = spots_used
        _spots_used = _spots_default.copy()

        print("monitor_handler: Successfully Integrated")
        time.sleep(5)

def run_capture_handler():
    while True:
        try:
            capture_handler()
        except Exception as e:
            print(f"run_capture_handler: Error - {e}")
        time.sleep(5)

def run_monitor_handler():
    while True:
        try:
            monitor_handler()
        except Exception as e:
            print(f"run_monitor_handler: Error - {e}")
        time.sleep(5)

def run_video_handler():
    while True:
        try:
            video_handler()
        except Exception as e:
            print(f"run_video_handler: Error - {e}")
        time.sleep(5)

def run_integrate_handler():
    while True:
        try:
            integrate_handler()
        except Exception as e:
            print(f"run_integrate_handler: Error - {e}")
        time.sleep(5)

def handlers():
    thread_capture = threading.Thread(target=run_capture_handler)
    thread_capture.daemon = True
    thread_capture.start()

    thread_monitor = threading.Thread(target=run_monitor_handler)
    thread_monitor.daemon = True
    thread_monitor.start()

    thread_video = threading.Thread(target=run_video_handler)
    thread_video.daemon = True
    thread_video.start()

    thread_integrate_handler = threading.Thread(target=run_integrate_handler)
    thread_integrate_handler.daemon = True
    thread_integrate_handler.start()

    while True:
        pass

if __name__ == "__main__":
    init_spot()
    handlers()

    
