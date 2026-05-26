from flask import Flask, request, Response
import threading
import time

app = Flask(__name__)

latest_frame = None
frame_lock = threading.Lock()

@app.route("/")
def home():
    return "Flask server running"

@app.route("/upload", methods=["POST"])
def upload():
    global latest_frame

    with frame_lock:
        latest_frame = request.data

    return "Frame received", 200

@app.route("/live")
def live():

    def generate():

        last_frame = None

        while True:

            with frame_lock:
                frame = latest_frame

            if frame is not None and frame != last_frame:

                last_frame = frame

                yield (
                    b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n'
                    + frame +
                    b'\r\n'
                )

            time.sleep(0.02)

    return Response(
        generate(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
