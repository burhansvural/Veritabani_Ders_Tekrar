# 📘 Veritabanı Ders Tekrarı – Üretim Seviyesi Kitaplık Uygulaması

Bu proje, **SQLAlchemy 2.0 (Async)**, **FastAPI**, **PostgreSQL**, **Redis**, **Bunny Stream** ve **Flet** kullanılarak inşa edilmiş, **üretim seviyesinde** bir kitaplık yönetim sistemidir. Amacımız, öğrencilerin sadece “çalışan kod” değil, **gerçek dünya mühendisliği** yetenekleri kazanmasını sağlamaktır.

---

## 🎯 Özellikler

- ✅ **Asenkron FastAPI backend** ile yüksek eşzamanlılık
- ✅ **PostgreSQL** ile veri bütünlüğü ve ölçeklenebilirlik
- ✅ **Redis** ile performans artışı (önbellekleme)
- ✅ **Bunny Stream** ile güvenli ve ücretsiz video yönetimi (15–20 dakikalık ders videoları için ideal)
- ✅ **Flet** ile masaüstü istemci (çoklu ekran, kimlik doğrulama, ilişkisel veri gösterimi)
- ✅ **Alembic** ile canlıda şema güncellemesi (veri kaybı olmadan)
- ✅ **Pytest** ile asenkron API testleri
- ✅ **JWT** ile güvenlik ve yetkilendirme
- ✅ **Docker** ile altyapı soyutlaması

---

## 🛠️ Kurulum

### 1. Ön Gereksinimler

- [Python 3.9+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (Windows/macOS) veya `docker` + `docker-compose` (Linux)
- [Bunny.net hesabı](https://bunny.net) (ücretsiz 100 GB depolama + 1 TB/ay çıkış trafiği)

### 2. Bunny Stream Hazırlığı

1. [Bunny.net](https://bunny.net) → **Stream** → **Library** oluşturun.
2. **API Key**’inizi alın (Settings → API Access).
3. `.env` dosyasına aşağıdaki bilgileri ekleyin:
   ```env
   BUNNY_STREAM_LIBRARY_ID=your_library_id
   BUNNY_STREAM_API_KEY=your_api_key
   ```

### 3. Proje Kurulumu

```bash
# 1. Depoya gönderme
cd Veritabani_Ders_Tekrar
rm -rf .git
git init
git remote add origin https://github.com/burhansvural/Veritabani_Ders_Tekrar.git
git add .
git commit -m "Proje yapısını düzelterek kök dizini doğru ayarladım"
git branch -M main
git push --force origin main

# 1a. Varolan içinde veri bulunan depoya değişiklikleri göndeme

git status
git add .
git commit -m "Geliştir: Modül 1'i ileri düzey güvenlik konularıyla zenginleştir" -m "
- SQL Injection bölümü, UNION, Boolean-based ve Error-based saldırı örnekleriyle güncellendi.
- Ham SQL ve ORM karşılaştırmasına somut ve yıkıcı saldırı simülasyonları eklendi.
- Modern uygulamalardaki çok katmanlı savunma stratejisi (WAF, Input Validation, Veritabanı Yetkileri vb.) açıklandı.
- Pedagojik anlatımlar ve gerçek dünya benzetmeleri güçlendirildi."
git push origin main


# 2. Sanal ortam oluşturun (isteğe bağlı ama önerilir)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# veya
venv\Scripts\activate     # Windows

# 3. Bağımlılıkları kurun
pip install -r requirements.txt

# 4. Ortam dosyasını oluşturun
cp .env.example .env
# .env dosyasını düzenleyin (Bunny, DB bilgileri)

# 5. Altyapıyı başlatın
docker-compose up -d

# 6. Veritabanı tablolarını oluşturun
alembic upgrade head

# 7. Backend'i başlatın
uvicorn backend.main:app --reload

# 8. Flet istemcisini başlatın (yeni terminal)
python desktop_client/main.py
```

---

## 📁 Dizin Yapısı

```
Veritabani_Ders_Tekrar/
│
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1.py                 # Modül 3, 5, 8, 11: CRUD, N+1 çözümü, güvenli endpoint'ler
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py           # Modül 2: Async engine, session
│   │   ├── security.py           # Modül 8: JWT token yönetimi
│   │   └── storage.py            # (Opsiyonel) Cloudflare R2 entegrasyonu
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py               # Base = declarative_base()
│   │   ├── yazar.py              # Modül 4: YazarDB
│   │   ├── kitap.py              # Modül 4: KitapDB
│   │   ├── kullanici.py          # Modül 4, 8: KullaniciDB
│   │   └── okuma_kaydi.py        # Modül 4, 11: OkumaKaydiDB
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── kitap.py              # Pydantic modelleri
│   │   ├── kullanici.py
│   │   └── okuma_kaydi.py
│   ├── main.py                   # FastAPI uygulaması, router entegrasyonu
│   └── __init__.py
│
├── desktop_client/
│   └── main.py                   # Modül 3, 11, 12: Flet istemcisi (giriş, kitap listesi, okuma geçmişi)
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Modül 7: Pytest fixture'ları
│   └── test_api.py               # Modül 7: API testleri
│
├── alembic/
│   ├── versions/                 # Modül 6: Otomatik oluşturulan göç dosyaları
│   ├── env.py                    # Modül 6: Alembic yapılandırması
│   └── script.py.mako
│
├── docs/
│   └── modul_notlari/            # (Opsiyonel) Öğrenciye dağıtılan ders notları
│       ├── modul_01_orm_felsefesi.md
│       ├── modul_02_async_mimari.md
│       ├── modul_03_crud_flet_entegrasyonu.md
│       ├── modul_04_iliskiler.md
│       ├── modul_05_n_plus_1_ve_cozum.md
│       ├── modul_06_alembic_gocler.md
│       ├── modul_07_pytest_testler.md
│       ├── modul_08_guvenlik_jwt.md
│       ├── modul_09_filtreleme_sayfalama.md
│       ├── modul_10_transactionlar.md
│       ├── modul_11_capstone_entegrasyon.md
│       └── modul_12_uretim_hazirligi.md
│
├── .env                          # Modül 2, 6: DATABASE_URL_ASYNC, DATABASE_URL_SYNC, Redis ayarları
├── .gitignore                    # .env, __pycache__, venv gibi dosyaları hariç tutar
├── alembic.ini                   # Modül 6: Alembic yapılandırma dosyası
├── docker-compose.yml            # Modül 12: PostgreSQL + Redis
├── Dockerfile                    # (Opsiyonel) Üretim için
├── requirements.txt              # Tüm bağımlılıklar (FastAPI, SQLAlchemy[asyncio], asyncpg, redis[async], flet, pytest, vs.)
└── README.md                     # Proje açıklaması, kurulum adımları, komutlar
```

---

## 🎥 Bunny Stream Entegrasyonu

Videolar **asla veritabanında saklanmaz**. Bunun yerine:

1. Kullanıcı, Flet arayüzünden video yükler.
2. Backend, videoyu **Bunny Stream**’e yükler.
3. Bunny, videoya özel bir **URL** döner.
4. Bu URL, **PostgreSQL’de** (`kitap.video_url`) saklanır.
5. Flet, bu URL’yi doğrudan oynatır (akış desteğiyle).

> 💡 **Avantaj:**  
> - **100 GB depolama + 1 TB/ay çıkış trafiği → ÜCRETSİZ**  
> - Otomatik transkodlama (720p, 1080p, mobil)  
> - Hazır embed edilebilir player

---

## 🧪 Testler

```bash
pytest
```

Testler, **gerçek veritabanı yerine geçici bir SQLite** kullanır ve her testten sonra veriyi temizler.

---

## 🚀 Üretim İçin İpuçları

- `.env` dosyasını **asla versiyon kontrolüne eklemeyin**.
- `uvicorn` yerine **Gunicorn + Uvicorn worker** kullanın.
- Bunny Stream API anahtarınızı **güvenli bir şekilde saklayın**.
- Redis ve PostgreSQL için **backup stratejisi** oluşturun.

---

## 📚 Ders Modülleri

Bu proje, aşağıdaki 12 modülü kapsar:
1. ORM Felsefesi
2. Asenkron Veritabanı Mimarisi
3. CRUD + Flet Entegrasyonu
4. İlişkiler (`relationship`, `ForeignKey`)
5. N+1 Problemi ve Çözümü (`selectinload`)
6. Alembic ile Canlıda Şema Güncelleme
7. Pytest ile Asenkron Testler
8. JWT ile Güvenlik
9. Filtreleme, Sıralama, Sayfalama
10. Transaction’lar (“Ya Hep Ya Hiç”)
11. Capstone: Tam Entegrasyon
12. Üretim Hazırlığı (Docker, Logging)

---

## 🙌 Katkı ve Sorular

Sorularınız için:  
📧 [burhansvural@gmail.com]  
📚 [Ders Notları Klasörü]

---

> ✨ **“Bir yazılım mühendisi, sadece kod yazar değil; güvenli, hızlı ve sürdürülebilir sistemler inşa eder.”**

---
