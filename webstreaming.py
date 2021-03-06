from flask import Flask, Response, request, jsonify
import json
import requests
import cv2
import numpy as np
from threading import Thread
import sqlite3
from models.main import mask_detection, detect, original, cycleGan, db

CAM_IP = "10.120.73.197"  # raspberrypi IP
rtsp_url = "rtsp://{}:8554/live/stream".format(CAM_IP)
frame = None
app = Flask(__name__)


def get_frame():
    global frame
    cap = cv2.VideoCapture(rtsp_url)
    while cap.isOpened():
        _, frame = cap.read()


def generate(tag_id):

    # General OpenCV Mode
    # global frame

    if tag_id == "general":
        while True:
            try:
                # decoded = cv2.imdecode(np.frombuffer(frame, np.uint8), -1)
                result = original(frame.copy())
                res = cv2.imencode(".jpg", result)[1].tobytes()
                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + res + b"\r\n"
                )
            except Exception as err:
                print("ERROR MSG = [{}]".format(err))
    # Cycle GAN Mode
    elif tag_id == "GAN":
        while True:
            try:
                # ecoded = cv2.imdecode(np.frombuffer(frame, np.uint8), -1)
                result = cycleGan(frame.copy())
                res = cv2.imencode(".jpg", result)[1].tobytes()
                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + res + b"\r\n"
                )

            except Exception as err:
                print("ERROR MSG = [{}]".format(err))
    # template mode
    elif tag_id == "template":
        while True:
            try:
                # decoded = cv2.imdecode(np.frombuffer(frame, np.uint8), -1)
                result = detect(frame.copy())
                res = cv2.imencode(".jpg", result)[1].tobytes()
                yield (
                    b"--frame\r\ n" b"Content-Type: image/jpeg\r\n\r\n" + res + b"\r\n"
                )
            except Exception as err:
                print("ERROR MSG = [{}]".format(err))


@app.route("/video_feed/<string:tag_id>")
def video_feed(tag_id):
    # 요청을 보냈던 client의 Ip로 이미지 수신
    # global cap
    # cap = cv2.VideoCapture(rtsp_url)
    y = Thread(target=get_frame, args=()).start()
    x = Thread(target=generate, args=(tag_id,)).start()
    return Response(
        generate(tag_id), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/getData")
def get_people_data():
    conn = sqlite3.connect("people.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM people ORDER BY time")
    rows = cur.fetchall()
    cur.close()
    data = []
    for idx, row in enumerate(rows):
        if idx > 5:
            break
        data.append(row)
    data = {"data": data}

    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)