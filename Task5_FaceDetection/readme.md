# Task 5 — Face Detection & Recognition (Python)

Detects and recognizes faces in both static images and real-time webcam feed using OpenCV and face_recognition.

## Features
- 📸 Static image — upload any photo and detect all faces
- 📹 Webcam — real-time face detection and recognition
- 👤 Register known faces — add people by name so the app recognizes them
- 🗑️ Remove known faces from the database
- Confidence percentage shown for each recognized face
- Dark themed Tkinter GUI

## Setup

### Step 1 — Install dependencies

```bash
pip install opencv-python face_recognition Pillow numpy
```

> ⚠️ `face_recognition` requires `dlib`. If installation fails, run:
> ```bash
> pip install cmake
> pip install dlib
> pip install face_recognition
> ```
> On Windows you may need Visual Studio Build Tools installed.

### Step 2 — Run
```bash
python app.py
```

## How to Use

### Detect faces in an image
1. Click **Image** mode button
2. Click **Upload Image**
3. Click **Detect Faces**

### Real-time webcam
1. Click **Webcam** mode button
2. Click **Start Webcam**

### Register a known face
1. Click **Add Known Face**
2. Select a clear photo of the person
3. Enter their name
4. The app will now recognize them in future images/webcam

## Files
- `app.py` — main application
- `known_faces.pkl` — saved face database (auto-created)