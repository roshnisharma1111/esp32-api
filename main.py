from flask import Flask, request, Response
import threading
import time

app = Flask(__name__)

latest_frame = None
frame_lock = threading.Lock()

@app.route("/")
def home():
    return "Flask running"

@app.route("/upload", methods=["POST"])
def upload():

    global latest_frame

    frame = request.data

    if frame:

        with frame_lock:
            latest_frame = frame

    return "OK", 200

@app.route("/live")
def live():

    def generate():

        global latest_frame

        while True:

            with frame_lock:
                frame = latest_frame

            if frame is not None:

                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' +
                    frame +
                    b'\r\n'
                )

            time.sleep(0.03)

    return Response(
        generate(),
        mimetype='multipart/x-mixed-replace; boundary=frame',
        headers={
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Connection": "keep-alive"
        }
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True
    )
