import cv2
import easyocr
import re
import time
import datetime
import imutils
import os
import sqlite3
from db_manager import *
import requests
import webbrowser
import socketio as sio_client
import logging
import threading
from queue import Queue
from typing import cast

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Setup
try:
    connect_db()
    logger.info("Database connected successfully")
except Exception as e:
    logger.error(f"Database connection failed: {e}")

reader = easyocr.Reader(['en'], gpu=False)
plate_pattern = r"[A-Z]{2}[0-9]{1,2}[A-Z]{0,2}[0-9]{3,4}"

# Setup SocketIO client for real-time updates (optional)
sio = None
try:
    sio = sio_client.Client()
    sio.connect('http://localhost:5000', wait_timeout=1)
    logger.info("[SOCKET] Connected to server")
except Exception as e:
    logger.warning(f"[SOCKET] Could not connect to server: {e}")
    logger.info("[SOCKET] Running in offline mode")

def _on_sio_connect():
    logger.info("[SOCKET] Connected to server")


def _on_sio_disconnect():
    logger.info("[SOCKET] Disconnected from server")


def _on_sio_connect_error(data):
    logger.error(f"[SOCKET] Connection error: {data}")


if sio:
    # Register handlers only if `on` is available and callable. Some SocketIO client
    # implementations may not expose a callable `on` attribute, so we guard calls.
    try:
        on_callable = getattr(sio, 'on', None)
        if callable(on_callable):
            try:
                # Preferred signature: on(event, handler)
                on_callable('connect', _on_sio_connect)
                on_callable('disconnect', _on_sio_disconnect)
                on_callable('connect_error', _on_sio_connect_error)
            except TypeError:
                # Some clients may use a different registration API; fall back
                # to decorator-based registration or skip registering.
                try:
                    @sio.event
                    def connect():
                        _on_sio_connect()

                    @sio.event
                    def disconnect():
                        _on_sio_disconnect()

                    @sio.event
                    def connect_error(data):
                        _on_sio_connect_error(data)
                except Exception:
                    logger.debug("SocketIO registration fallback failed; continuing offline")
        else:
            # Fall back to decorator-based registration if supported
            try:
                @sio.event
                def connect():
                    _on_sio_connect()

                @sio.event
                def disconnect():
                    _on_sio_disconnect()

                @sio.event
                def connect_error(data):
                    _on_sio_connect_error(data)
            except Exception:
                logger.debug("SocketIO event registration skipped (offline mode)")
    except Exception:
        logger.debug("SocketIO event registration failed; continuing in offline mode")

def clean_text(text):
    text = text.strip().upper().replace(" ", "")
    match = re.findall(plate_pattern, text)
    return match[0] if match else None

def detect_plate_easyocr(frame, save_path="detections"):
    """Enhanced plate detection with better error handling"""
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        filtered = cv2.bilateralFilter(gray, 11, 17, 17)
        results = reader.readtext(filtered)

        for (bbox, text, prob) in results:
            if float(prob) < 0.6:
                continue
            plate = clean_text(text)
            if plate and len(bbox) == 4:
                try:
                    x_coords = [pt[0] for pt in bbox]
                    y_coords = [pt[1] for pt in bbox]
                    x = int(min(x_coords))
                    y = int(min(y_coords))
                    w = int(max(x_coords)) - x
                    h = int(max(y_coords)) - y
                    os.makedirs(save_path, exist_ok=True)
                    cropped = frame[y:y+h, x:x+w]
                    filename = os.path.join(save_path, f"{plate}_{int(time.time())}.jpg")
                    cv2.imwrite(filename, cropped)
                    logger.info(f"Plate detected: {plate} (confidence: {prob:.2f})")
                    return plate, (x, y, w, h)
                except Exception as e:
                    logger.warning(f"Error processing plate detection: {e}")
                    continue
        return None, None
    except Exception as e:
        logger.error(f"Plate detection error: {e}")
        return None, None

# Runtime variables
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    logger.error("Failed to open camera")
    exit(1)

logger.info("[INFO] Smart Parking Plate Detector Ready")

last_detected_plate = None
last_detection_time = 0
cooldown = 5
detection_mode = None
status_message = "🚗 Press 'c' to detect plate"

def send_api_request(endpoint, data):
    """Send API request with error handling"""
    try:
        response = requests.post(f"http://localhost:5000{endpoint}", json=data, timeout=5)
        if response.status_code == 200:
            logger.info(f"API request successful: {endpoint}")
            return True
        else:
            logger.warning(f"API request failed: {endpoint} - Status: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"API request error: {endpoint} - {e}")
        return False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = imutils.resize(frame, width=640)
    key = cv2.waitKey(1) & 0xFF
    now = time.time()

    if key == ord('c'):
        detection_mode = "detect"
        print("\n[MODE] Plate detection activated.")

    if detection_mode:
        plate_text, box = detect_plate_easyocr(frame)
        if plate_text and box and (plate_text != last_detected_plate or now - last_detection_time > cooldown):
            last_detected_plate = plate_text
            last_detection_time = now
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            logger.info(f"[DETECTED] Plate: {plate_text} | Mode: {detection_mode.upper()} | Time: {datetime.now().strftime('%H:%M:%S')}")

            if detection_mode == "detect":
                # Check if plate is already in the database
                try:
                    conn = sqlite3.connect(DB_NAME)
                    c = conn.cursor()
                    c.execute("SELECT * FROM parking_log WHERE plate=? AND status='IN'", (plate_text,))
                    existing_entry = c.fetchone()
                    conn.close()
                    
                    if existing_entry:
                        # Plate already exists - process as exit
                        status_message = f"\u26a0\ufe0f {plate_text} already parked. Processing exit."
                        logger.info(f"Already inside: {plate_text}")
                        
                        # Get exit information
                        result = log_exit(plate_text)
                        logger.info(f"Exit result: {result}")
                        
                        # Accept either a dict or the ExitResult dataclass from db_manager
                        info = None
                        if isinstance(result, dict):
                            info = cast(dict, result)
                        elif hasattr(result, 'amount'):
                            # Convert dataclass-like object to dict for downstream usage
                            info = {
                                'plate': getattr(result, 'plate', plate_text),
                                'amount': getattr(result, 'amount', None),
                                'duration_min': getattr(result, 'duration_min', None),
                                'entry_time': getattr(result, 'entry_time', None),
                                'exit_time': getattr(result, 'exit_time', None),
                            }

                        if info:
                            status_message = f"💵 ₹{info['amount']} for {info['duration_min']} min"
                            logger.info(f"Exit info: {plate_text} | ₹{info['amount']} | {info['duration_min']} min")

                            # Notify dashboard to show QR code
                            send_api_request(f"/api/set_pending_exit/{plate_text}", {})

                            # Send real-time update to server
                            send_api_request("/api/plate_detected", {
                                'plate': plate_text,
                                'status': 'exit_pending',
                                'amount': info['amount'],
                                'duration': info['duration_min'],
                                'entry_time': info['entry_time'],
                                'exit_time': info['exit_time']
                            })
                        elif result == "db_locked":
                            status_message = f"🔒 DB Locked. Try again."
                            logger.error(f"DB LOCKED during exit: {plate_text}")
                        elif result == "not_found":
                            status_message = f"❌ Entry not found for {plate_text}"
                            logger.error(f"Entry not found for plate: {plate_text}")
                        elif result == "db_error":
                            status_message = f"❌ Database error for {plate_text}"
                            logger.error(f"Database error for plate: {plate_text}")
                        else:
                            status_message = f"❌ Unknown error processing exit for {plate_text}: {result}"
                            logger.warning(f"Exit processing failed: {result}")
                    else:
                        # New plate - process as entry
                        result = log_entry(plate_text)
                        if result == "already_in":
                            status_message = f"\u26a0\ufe0f {plate_text} already parked but not found in initial check."
                            logger.info(f"Already inside (unexpected): {plate_text}")
                        elif result == "db_locked":
                            status_message = f"🔒 DB Locked. Try again."
                            logger.error(f"DB LOCKED while entry: {plate_text}")
                        elif result == "full":
                            status_message = f"🚫 Parking full for {plate_text}"
                            logger.warning(f"Parking full: {plate_text}")
                        else:
                            status_message = f"✅ Entry logged: {plate_text}"
                            logger.info(f"Entry added: {plate_text}")
                            
                            # Send real-time update to server
                            send_api_request("/api/plate_detected", {
                                'plate': plate_text,
                                'status': 'entry_logged',
                                'entry_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                except Exception as e:
                    status_message = f"❌ Database error for {plate_text}: {str(e)}"
                    logger.error(f"Database error: {e}")
                    import traceback
                    traceback.print_exc()

            detection_mode = None
            print("-" * 60)

    cv2.putText(frame, status_message, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    cv2.imshow("Smart Parking Plate Detector", frame)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
