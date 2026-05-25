from fastapi import FastAPI

app = FastAPI()

camera = False

@app.post("/camera/on")
def camera_on():
    global camera
    camera = True
    return {
        "message": "Camera ON",
        "camera": camera
    }

@app.post("/camera/off")
def camera_off():
    global camera
    camera = False
    return {
        "message": "Camera OFF",
        "camera": camera
    }

@app.get("/status")
def status():
    return {
        "camera": camera
    }
