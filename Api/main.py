from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from PIL import Image
import io
from Api.utils.predict import predict_image, predict_video  # en üstte olmalı
from Api.utils.fcm_service import send_warship_alert
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Ship Detection API is running."}

@app.get("/upload", response_class=HTMLResponse)
async def upload_form():
    html = """
    <html>
        <head><title>Upload File</title></head>
        <body>
            <h2>Upload an image or video</h2>
            <form action="/predict" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*,video/*">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename.lower()

    if filename.endswith((".jpg", ".jpeg", ".png")): #dosya resimse
        image = Image.open(io.BytesIO(contents)).convert("RGB") 
        result = predict_image(image)  #predict_image fonksiyonu 
    elif filename.endswith((".mp4", ".avi", ".mov")): #video ise
        result = predict_video(contents)  # video analiz
    else:
        return JSONResponse(content={"error": "Desteklenmeyen dosya türü"}, status_code=400)

    return result


