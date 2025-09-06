import firebase_admin
from firebase_admin import credentials, messaging, firestore

# Firebase Admin SDK ile başlat
cred = credentials.Certificate("C:\\Users\\yaren\\PycharmProjects\\ship_detection_api\\YOUR JSON FİLE")
firebase_admin.initialize_app(cred)

def send_warship_alert():
    db = firestore.client()

    # Firestore'dan tüm admin tokenlarını al
    tokens_ref = db.collection("admin_tokens").stream()
    tokens = [doc.to_dict().get("token") for doc in tokens_ref if doc.to_dict().get("token")]

    if not tokens:
        print("❌ Kayıtlı admin token bulunamadı.")
        return

    # Bildirimi her token'a tek tek gönder
    for token in tokens:
        message = messaging.Message(
            notification=messaging.Notification(
                title="🚢 Savaş Gemisi Tespit Edildi!",
                body="⚠️ Acil durum: Lütfen kontrol edin.",
            ),
            token=token,
        )

        try:
            response = messaging.send(message)
            print("✅ Bildirim gönderildi:", response)
        except Exception as e:
            print(f"⚠️ Bildirim gönderilemedi ({token}): {e}")
