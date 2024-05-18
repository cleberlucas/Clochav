import asyncio
import aiohttp
import cv2
import pyzbar.pyzbar as pyzbar
import json

with open('config.json', 'r') as config_file:
    _config = json.load(config_file)

_space_default = {}
_space_used = {}

_frame = None
_decoded_objects = None

async def space_init_async():
    print("space_init_async: Initialized")

    global _space_default, _space_used

    try:
        await spots_default_init_async()

        _space_used = _space_default.copy()

        for space_key in _space_used.keys():
            floor = space_key[0]
            space = space_key[1]
            used = _space_used[space_key]

            await space_update_async(floor, space, used)

        print("space_init_async: Executed")

    except Exception as e:
        print(f"space_init_async: Error - {e}")

async def spots_default_init_async():
    print("spots_default_init_async: Initialized")

    global _space_default

    try:
        api_url = f"{_config['api_url']}/api/parking/space"
        

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    print("spots_default_init_async: Error making request. Status code:", response.status)
                    return

                spaces_data = await response.json()

                for space in spaces_data:
                    space_key = f"{space['floor']}{space['spot']}"
                    _space_default[space_key] = True

    except Exception as e:
        print("spots_default_init_async: Error making request:", e)

async def space_update_async(floor, space, used):
    print("space_update_async: Initialized")

    try:
        api_url = f"{_config['api_url']}/api/parking/space/{floor}/{space}"

        payload = {"used": used}
        headers = {"Content-Type": "application/json"}

        async with aiohttp.ClientSession() as session:
            async with session.put(api_url, json=payload, headers=headers) as response:
                if response.status != 200:
                    print("space_update_async: Error making request. Status code:", response.status)

    except Exception as e:
        print("space_update_async: Error making request:", e)

async def capture_handler_async():
    print("capture_handler_async: Initialized")

    global _frame

    cap = cv2.VideoCapture(_config["stream_url"])

    if not cap.isOpened():
        print("capture_handler_async: Error opening video capture")
        return

    while True:
        ret, _frame = cap.read()
        if not ret:
            print("capture_handler_async: Error reading frame")
            return
        
        print("capture_handler_async: Executed")
        await asyncio.sleep(0.1)

async def scream_video_handler_async():
    print("scream_video_handler_async: Initialized")

    global _frame, _decoded_objects

    while True:
        if _frame is None or _frame.size == 0:
            print("scream_video_handler_async: Frame not detected")
            await asyncio.sleep(0.2)
            continue

        frame = _frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        decoded_objects = pyzbar.decode(gray)

        _decoded_objects = decoded_objects

        for obj in decoded_objects:
            bbox = obj.rect
            x, y, w, h = bbox.left, bbox.top, bbox.width, bbox.height

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            qr_data = obj.data.decode("utf-8")
            cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.imshow("Video", frame)
        cv2.waitKey(1)

        print("scream_video_handler_async: Executed")
        await asyncio.sleep(0.1)

async def recognition_handler_async():
    print("recognition_handler_async: Initialized")

    global _space_used, _decoded_objects

    while True:
        if _decoded_objects is None:
            print("recognition_handler_async: Objects not detected")
            await asyncio.sleep(0.1)
            continue

        for obj in _decoded_objects:
            data = obj.data.decode("utf-8")

            try:
                floor = data[0]
                space = data[1]

                space_used_key = f"{floor}{space}"
                if _space_used.get(space_used_key):
                    _space_used[space_used_key] = False

            except Exception as e:
                print(f"recognition_handler_async: Error decoding QR data: {e}")

        print("recognition_handler_async: Executed")
        await asyncio.sleep(0.1)

async def integrate_handler_async():
    print("integrate_handler_async: Initialized")

    global _space_used, _space_default

    await space_init_async()

    last_state_space_used = _space_used.copy()

    while True:
        for space_used_key in _space_used.keys():
            used = _space_used[space_used_key]
        
            #if used != last_state_space_used[space_used_key]:
            floor = space_used_key[0]
            space = space_used_key[1]
            await space_update_async(floor, space, used)
            print(f"integrate_handler_async: Floor {floor} Space {space} Updated to {'OCCUPIED' if used else 'VACANT'}")
        
        last_state_space_used = _space_used.copy()
        _space_used = _space_default.copy()

        print("integrate_handler_async: Executed")
        await asyncio.sleep(2)

async def run_tasks_sync():
    await asyncio.gather(
        capture_handler_async(),
        scream_video_handler_async(),
        recognition_handler_async(),
        integrate_handler_async()
    )

def main():
    asyncio.run(run_tasks_sync())

if __name__ == "__main__":
    main()