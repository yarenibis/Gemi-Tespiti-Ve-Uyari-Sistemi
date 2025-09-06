# 🚢 Gemi Tespiti ve Sınıflandırma Sistemi

# Detaylı bilgi için rapor klasörü içindeki makaleyi okuyabilirsiniz.

## 📌 Proje Özeti
Gemi tespiti, güvenlik, lojistik ve çevre koruma gibi kritik alanlarda büyük bir öneme sahiptir.  
Uluslararası sularda veya ülkelerin kara sularında seyreden gemilerin izlenmesi, olası kaçakçılık, terörizm ve diğer suç faaliyetlerinin önlenmesi açısından son derece önemlidir. Ayrıca savaş gemilerinin veya şüpheli gemilerin tespiti, bir ülkenin güvenliğini sağlamak için stratejik bir rol oynar.  

Bu bağlamda geliştirilen proje, **mobil uygulama üzerinden gemi görüntülerini yükleyerek sınıflandırma yapılmasını** sağlamaktadır. Yapay zeka destekli model:  
- Yüklenen gemi görüntüsünü analiz eder,  
- Gemiyi sınıflandırır,  
- Tehlikeli olup olmadığını belirler.  

📌 Eğer sistem yüklenen gemiyi **“savaş gemisi”** olarak sınıflandırırsa, anında yetkililere bildirim gönderilmektedir.  
Ayrıca geminin konumu harita üzerinde işaretlenip veri tabanına kaydedilmektedir.  

Elde edilen sonuçlar:  
- Eğitim doğruluk oranı: **%90**  
- Doğrulama doğruluk oranı: **%89**  
- Test doğruluk oranı: **%91**

---
## ⚙️ Backend Geliştirme (FastAPI)
Backend geliştirme sürecinde **FastAPI** framework’ü tercih edilmiştir.  
- Kullanıcıdan gelen gemi görüntüsü **TensorFlow modeli** ile sınıflandırılmaktadır.  
- Eğer gemi **savaş gemisi** olarak tespit edilirse, sistem **Firebase Cloud Messaging (FCM)** aracılığıyla yetkililere **anında bildirim** göndermektedir.  
- Kullanıcının **konumu Google Maps API** ile alınarak sınıflandırma sonucu ile birlikte **Firebase Firestore** veri tabanına kaydedilmektedir.  
- Böylece yalnızca sınıflandırma değil, gerçek zamanlı **konum takibi ve olay kaydı** da sağlanmıştır.  

---

## 📱 Mobil Uygulama (Flutter)
- Kullanıcı arayüzü **Flutter** ile geliştirilmiştir.  
- Kullanıcı, cihazındaki **kamera** veya **galeriden** görüntü/video seçebilir.  
- Uygulama, kullanıcının **anlık konumunu** alarak görüntüyle birlikte **backend sunucusuna** iletir.  
- Sunucudan gelen sınıflandırma sonucu kullanıcıya gösterilir.  
- Eğer tehdit algılanırsa ilgili birime **otomatik bildirim** gönderilir.  

Bu yapı sayesinde kullanıcılar, basit bir mobil arayüz üzerinden **etkin ve güvenli gemi tespiti** gerçekleştirebilmektedir.  

---

## 📊 Veri Seti
- Veri seti tarafımdan **manuel olarak internet üzerinden toplanmış ve sınıflandırılmıştır.**  
- **5 farklı gemi sınıfı** içermektedir.  
- Her sınıfta **800 gemi fotoğrafı** olmak üzere toplam **4000 etiketli görüntü** bulunmaktadır.  
- Görüntüler açık deniz, liman ve farklı açılardan seçilerek modelin **genelleme gücü** artırılmıştır.  

📌 **Kullanılan Sınıflar:**  
- 🛳 **Cruise_ship:** Büyük yolcu gemileri (çok katlı, beyaz gövde).  
- 🚢 **Warship:** Savaş gemileri (gri renkli, radar/silah sistemli).  
- 📦 **Freight_boat:** Konteyner gemileri (uzun ve geniş yapılı).  
- ⛴ **Ferry_boat:** Feribotlar (düz tabanlı, yolcu/araç kapasiteli).  
- ⛵ **Sail_boat:** Yelkenli tekneler (küçük, sivri yapılı).  

📌 **Veri Seti Dağılımı:**  
- %64 → Eğitim  
- %16 → Doğrulama  
- %20 → Test  

--- 

## 🔗 Kaynaklar
- 📊 **Veri Seti (Kaggle):** [(https://www.kaggle.com/datasets/yarenbi/ship-dataset)]  
- 🤖 **Eğitilmiş Model (Kaggle):** [(https://www.kaggle.com/models/yarenbi/gemi_model)]  

---




