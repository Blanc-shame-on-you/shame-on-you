from flask import Flask, render_template, Response, request
import requests
import cv2
import numpy as np


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
    elif tag_id == "Gan":
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


@app.route("/video_feed/<string:id>")
def video_feed(id):
    # 요청을 보냈던 client의 Ip로 이미지 수신
    return Response(generate(id), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
