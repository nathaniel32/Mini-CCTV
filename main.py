import cv2
import threading
from flask import Flask, Response, render_template, request

app = Flask(__name__)

PASSWORD = "Nat12"
camera = None
online_time_out = 0

def online_check():
    global camera
    global online_time_out
    if online_time_out != 0:
        online_time_out -= 1
    else:
        camera = None
    timer = threading.Timer(1.0, online_check)
    timer.start()

def start_camera():
    global camera
    camera = cv2.VideoCapture(0)

def gen_frames():
    global online_time_out
    while True:
        online_time_out = 5
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/cctv', methods=['GET'])
def cctv():
    password = request.args.get('p', None)
    if password == PASSWORD:
        if not camera:
            start_camera()
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response("Unauthorized", status=401)

if __name__ == '__main__':
    online_check_thread = threading.Thread(target=online_check)
    online_check_thread.start()
    app.run(host='0.0.0.0', port=8080)