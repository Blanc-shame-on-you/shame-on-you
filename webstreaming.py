from flask import Flask, render_template, Response, request
import requests
import cv2
import numpy as np
from threading import Thread
import sqlite3
from models.main import detect, original, cycleGan

app = Flask(__name__)


@app.route("/")
def index():
    global client_ip
    # 접속한 라즈베리파이의 IP 저장
    client_ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    return render_template("index.html")

def generate(tag_id):
    # General OpenCV Mode
    if tag_id == "general":
        while True:            
            res = requests.get("http://{}:5000/".format(client_ip)).content
            decoded = cv2.imdecode(np.frombuffer(res, np.uint8), -1)
            result = original(decoded)
            res = cv2.imencode('.jpg', result)[1].tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + res + b"\r\n")
    # Cycle GAN Mode
    elif tag_id == "GAN":
        while True:
           
            res = requests.get("http://{}:5000/".format(client_ip)).content
            decoded = cv2.imdecode(np.frombuffer(res, np.uint8), -1)
            result = cycleGan(decoded)
            res = cv2.imencode('.jpg', result)[1].tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + res + b"\r\n")
    # template mode
    elif tag_id == "template":
        while True:
            res = requests.get("http://{}:5000/".format(client_ip)).content
            decoded = cv2.imdecode(np.frombuffer(res, np.uint8), -1)
            result = detect(decoded)
            res = cv2.imencode('.jpg', result)[1].tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + res + b"\r\n")
           


@app.route("/video_feed/<string:tag_id>")
def video_feed(tag_id):
    # 요청을 보냈던 client의 Ip로 이미지 수신
    x=Thread(target=generate,args=(tag_id,)).start()
    return Response(generate(tag_id), mimetype="multipart/x-mixed-replace; boundary=frame")

# @app.route('/people'):
# def select_people():
#     conn = sqlite3.connect("people.db")

#     cur = conn.cursor():
#     cur.execute("SELECT * FROM people ORDER BY time")
#     rows = cur.fetchall()
#     cur.close()
#     data = []
#     for idx, row in enumerate(rows):
#         if idx > 3:
#             break
#         data.append(row)
        
#     return Response(people_data=data)



if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
