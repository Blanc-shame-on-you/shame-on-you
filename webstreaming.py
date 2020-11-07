from flask import Flask, render_template, Response, request
import requests
import cv2


app = Flask(__name__)


@app.route("/")
def index():
    global client_ip
    # 접속한 라즈베리파이의 IP 저장
    client_ip = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)
    return render_template("index.html")


def gen(image):
    while True:
        # byte문자열인 image를 0.jpg로 저장후
        cv2.imwrite("./0.jpg", image)
        # 0.jpg를 capture
        cap = cv2.VideoCapture("./0.jpg")
        # capture한 이미지를 읽기
        success, cap = image.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    # 요청을 보냈던 client의 Ip로 이미지 수신
    video = requests.get(client_ip)
    return Response(gen(video), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)