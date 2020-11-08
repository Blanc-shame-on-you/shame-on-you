from flask import Flask, render_template, Response, request
import requests
import cv2
import numpy as np
from .models.detect import detect
#from .models.MaskDetection.detect import detection


app = Flask(__name__)


@app.route("/")
def index():
    global client_ip
    # 접속한 라즈베리파이의 IP 저장
    client_ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    return render_template("index.html")


def gen():
    while True:
        try:
            res = requests.get("http://{}:5000/".format(client_ip)).content
            # Mask detection & convention
            result = detect(res)
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + res + b"\r\n")
        except Exception as err:
            print("ERROR MSG:[{}]".format(err))


@app.route("/video_feed")
def video_feed():
    # 요청을 보냈던 client의 Ip로 이미지 수신
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)