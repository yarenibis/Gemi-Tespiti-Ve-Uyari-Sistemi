from PIL import Image
import numpy as np
import tensorflow as tf
import cv2
import tempfile
import os
from collections import Counter
from Api.utils.fcm_service import send_warship_alert


MODEL_PATH = "Api/model/gemi_model_max_acc.h5"
INPUT_SIZE = (128, 128)

CLASS_NAMES = ['cruise_ship', 'ferry_boat', 'freight_boat', 'sailboat', 'warship']

_model = None  # modeli önbelleğe almak için,her çağırdığımda tekrar yüklenmesin diye

def get_model():
    global _model
    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)
    return _model

def prepare_image(image: Image.Image):
    print("Image mode:", image.mode)
    print("Original size:", image.size)

    image = image.convert("RGB")
    image = image.resize((128, 128))
    img_array = np.array(image).astype(np.float32) / 255.0

    print("After resize:", img_array.shape, img_array.dtype)

    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_image(image: Image.Image):
    model = get_model() #model yüklenir
    img = prepare_image(image) #resim hazırlanır
    preds = model.predict(img) #tahmin yapılır
    class_index = int(np.argmax(preds))  #yüksek olasılıklı sınıfın indexi alınır.
    confidence = float(np.max(preds))
    result_class = CLASS_NAMES[class_index]

    if result_class == "warship": #tahmin sonucu warship ise
        send_warship_alert() #bildirim yolla firebase'e / fcm_Service'den geliyor.

    return {
        "type": "image",
        "class": result_class,
        "confidence": confidence
    }



def predict_video(file_bytes: bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp: #geçici diske alınır
        tmp.write(file_bytes)
        tmp_path = tmp.name

    cap = cv2.VideoCapture(tmp_path) #karelerine ayrılır
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Toplam kare: {frame_count}, FPS: {fps}")

    predictions = []
    frame_id = 0
    model = get_model()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Videodaki her bir kareyi işlemek
        img_resized = cv2.resize(frame, (128, 128))
        img_array = np.array(img_resized) / 255.0  # Normalizasyon
        img_array = np.expand_dims(img_array, axis=0)  # Modelin beklediği şekle getirme: (1, 128, 128, 3)

        # Modeli kullanarak tahmin yapma -her bir kare üzerinde
        predictions_raw = model.predict(img_array, verbose=0)
        predicted_class_idx = np.argmax(predictions_raw)
        print(f"Predicted class index: {predicted_class_idx}")

        #tahmin yapılırken sınıf ve güven değeri alınır predictions listesine eklenir.
        predicted_class = CLASS_NAMES[predicted_class_idx]
        confidence = float(np.max(predictions_raw))
        predictions.append(predicted_class)

        print(f"Kare {frame_id}: {predicted_class} ({confidence:.2f})")
        frame_id += 1

    cap.release()
    os.remove(tmp_path)

    if not predictions:
        return {"type": "video", "error": "Hiçbir kare işlenemedi."}

    counts = Counter(predictions)  #En çok hangi sınıf görüldüyse o sonuç olarak kabul edilir
    most_common = counts.most_common(1)[0]
    result_class = most_common[0]

    if result_class == "warship":
        send_warship_alert()


    return {
        "type": "video",
        "class": most_common[0],  # en çok görülen sınıf
        "confidence": most_common[1] / len(predictions)  # oranla güven
    }
