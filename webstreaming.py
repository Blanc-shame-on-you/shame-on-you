from flask import Flask, render_template, Response, request
import requests
import cv2
import numpy as np
from threading import Thread
import sqlite3


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
            try:
                res = requests.get("http://{}:5000/".format(client_ip)).content
                # OpenCV Bbox
                yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + res + b"\r\n")
            except Exception as err:
                print("ERROR MSG:[{}]".format(err))
    # Cycle GAN Mode
    elif tag_id == "GAN":
        while True:
            try:
                res = requests.get("http://{}:5000/".format(client_ip)).content
                # Adapt Cycle GAN
                yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + res + b"\r\n")
            except Exception as err:
                print("ERROR MSG:[{}]".format(err))
    # template mode
    elif tag_id == "template":
        while True:
            try:
                res = requests.get("http://{}:5000/".format(client_ip)).content
                # Adapt template Mode
                yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + res + b"\r\n")
            except Exception as err:
                print("ERROR MSG:[{}]".format(err))


@app.route("/video_feed/<string:tag_id>")
def video_feed(tag_id):
    # 요청을 보냈던 client의 Ip로 이미지 수신
    x=Thread(target=generate,args=(tag_id)).start()
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
