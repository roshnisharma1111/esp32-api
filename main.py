from flask import Flask, Response
import requests

app = Flask(__name__)

ESP32_URL = "http://192.168.24.88:81/stream"

@app.route("/")
def home():
    return "Flask server running"

@app.route("/live")
def video_feed():
    r = requests.get(ESP32_URL, stream=True)

    return Response(
        r.iter_content(chunk_size=1024),
        content_type=r.headers["Content-Type"]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
