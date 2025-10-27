# 📚 Modül 1: ORM Felsefesi – Neden Bir “Evrensel Tercüman”a İhtiyacımız Var?  
  
## 🎯 Bu Modülde Öğrenecekleriniz  
  
- ORM (Object-Relational Mapper) nedir ve neden kullanılır?  
- Ham SQL ile ORM arasında temel farklar nelerdir?  
- SQLAlchemy Core ile SQLAlchemy ORM arasındaki fark nedir, hangisi ne zaman tercih edilmelidir?  
- Gerçek dünya projelerinde ORM’in sunduğu güvenlik ve sürdürülebilirlik avantajları.  
  
---  
  
## 🌍 Gerçek Dünya Benzetmesi: **Evrensel Tercüman**  
  
Hayal edin:    
Dünyanın dört bir yanından gelen mühendislerle (PostgreSQL, MySQL, SQLite, Oracle) aynı projede çalışıyorsunuz. Her biri kendi dilini konuşuyor. Siz de her dilde akıcı olmak zorunda mısınız?  
  
**Hayır!**  Yanınızda **sihirli bir tercüman** olsun:    
> **Siz sadece kendi dilinizde (Python) konuşursunuz.**  > **Tercüman, herkese kendi dilinde (SQL lehçesi) anında ve hatasız çevirir.**  
  
İşte **SQLAlchemy**, tam da bu **evrensel tercümanımızdır**.  
  
---  
  
## 🔍 ORM Nedir?  
  
**ORM (Object-Relational Mapper)**, veritabanı tablolarını **Python nesnelerine** dönüştüren bir araçtır. Böylece:  
  
- Veritabanıyla doğrudan SQL yazmadan iletişim kurabilirsiniz.  
- Tablolar → Sınıflar (`class KitapDB`)  
- Kolonlar → Özellikler (`baslik = Column(String)`)  
- Kayıtlar → Nesneler (`kitap = KitapDB(baslik="Sefiller")`)  
  
### 📌 Örnek: Kitap Ekleme  
  
**Ham SQL ile:**  
```sql  
INSERT INTO kitaplar (baslik, yazar) VALUES ('Sefiller', 'Victor Hugo');  
```  
  
**SQLAlchemy ORM ile (Python):**  
```python  
kitap = KitapDB(baslik="Sefiller", yazar="Victor Hugo")  
session.add(kitap)  
await session.commit()  
```  
  
> 💡 Aynı Python kodu, PostgreSQL, MySQL veya SQLite  veritabanları ile **Biz kodları hiç değiştirmeden çalışır**!  
  
---  
  
## ⚖️ ORM mi, Ham SQL(Core) mi?  
  
| Özellik | ORM (SQLAlchemy) | Ham SQL / Core |  
|--------|------------------|----------------|  
| **Geliştirme Hızı** | ⚡ Çok hızlı | Orta |  
| **Okunabilirlik** | ✅ Yüksek | ❌ Düşük |  
| **Veritabanı Bağımsızlığı** | ✅ Evet | ❌ Hayır |  
| **Güvenlik (SQL Injection)** | ✅ Otomatik koruma | ⚠️ Manuel önlem gerekir |  
| **Performans** | İyi | 🚀 Mükemmel (kompleks sorgularda) |  
  
> 📌 **Kural:**  > - **%95 proje** → **ORM** (hızlı, güvenli, sürdürülebilir)    
> - **%5 analitik/raporlama** → **Core** (maksimum performans)  
  
---  
  
## 🛡️ Güvenlik Avantajı: SQL Injection’a Otomatik Koruma  
  
**SQL Injection**, bir saldırganın, uygulamanızdaki bir forma girdiği metinle veritabanı komutlarınızı manipüle etmesidir. Bu, en yaygın ve en tehlikeli siber saldırılardan biridir.  
  
**Ham SQL**’de tehlikeli bir örnek:  
```python  
# YANLIŞ ve TEHLİKELİ!  
cursor.execute(f"SELECT * FROM kitaplar WHERE yazar = '{user_input}'")  
```  
Eğer `user_input = "'; DROP TABLE kitaplar; --"` olursa → **tüm tablo silinir!**  
  
**SQLAlchemy** ORM ile:  
```python  
# GÜVENLİ!  
session.execute(select(KitapDB).where(KitapDB.yazar == user_input))  
```  
SQLAlchemy, sizin yerinize "tercümanlık" yaparken, gelen tüm verileri **"parametrelendirilmiş sorgular"** adı verilen güvenli bir yöntemle işler. Bu, SQL Injection saldırılarını **neredeyse imkânsız** hale getirir.**  
  
---  
  
## 🧩 SQLAlchemy Core vs ORM  
  
| Araç | Ne Zaman Kullanılır? | Örnek Senaryo |  
|------|----------------------|---------------|  
| **ORM** | CRUD işlemleri, ilişkisel veri, hızlı prototipleme | Kitap ekle/listele, kullanıcı profili |  
| **Core** | Kompleks JOIN’ler, analitik sorgular, büyük veri | “Son 30 günde en çok okunan 10 yazarın ortalama okunma süresi” |  
  
> 💡 Bu derste **ORM odaklı** ilerleyeceğiz. Core, ileri seviye bir konudur.  
  
---  
  
## 🎯 Güvenlik  
  
- SQL injection nedir ve neden **`cursor.execute()` bile sizi koruyamaz**?  
- **UNION**, **Boolean-based**, **Error-based** saldırılar nasıl çalışır?  
- **Ham SQL**, **SQLAlchemy Core** ve **ORM** arasındaki farklar.  
- **Gelişmiş savunma katmanları**: Giriş doğrulama, yetki sınırlandırma, WAF.  
- **SQLAlchemy ORM’in** neden **en güvenli ve üretken** seçim olduğu.  
  
---  
  
## ⚠️ Uyarı: Bu Dosyadaki Kodlar Eğitim Amaçlıdır!  
  
Aşağıdaki örnekler, **SQL injection saldırılarını öğretmek** içindir.    
**Hiçbiri üretimde KULLANILMAMALIDIR.**  
  
---  
  
## 🔥 Bölüm 1: Ham SQL ile Tehlikeli Yol  
  
### 📄 `1_ham_sql_ornek.py` – Basit SQL Injection  
  
```python  
import sqlite3  
import os  
  
DB = "kitaplik.db"  
  
def setup():  
    if os.path.exists(DB): os.remove(DB)    conn = sqlite3.connect(DB)    conn.execute("CREATE TABLE kitaplar (id INTEGER, baslik TEXT, yazar TEXT)")    conn.execute("INSERT INTO kitaplar VALUES (1, '1984', 'George Orwell')")    conn.commit()    conn.close()  
def guvenli_sorgu(yazar):  
    conn = sqlite3.connect(DB)    cur = conn.cursor()    cur.execute("SELECT * FROM kitaplar WHERE yazar = ?", (yazar,))  # ✅ PARAMETRELİ    print("Güvenli:", cur.fetchall())    conn.close()  
def tehlikeli_sorgu(yazar):  
    conn = sqlite3.connect(DB)    cur = conn.cursor()    query = f"SELECT * FROM kitaplar WHERE yazar = '{yazar}'"  # ❌ f-string    cur.execute(query)  # execute() bile koruyamaz!    print("Tehlikeli:", cur.fetchall())    conn.close()  
if __name__ == "__main__":  
    setup()    guvenli_sorgu("' OR '1'='1")      # → []    tehlikeli_sorgu("' OR '1'='1")    # → TÜM KAYITLAR!  
```  
  
> 💡 **Sonuç:** `execute()` **çoklu komutu** engeller, ama **tek komut içinde UNION** gibi saldırılar **çalışır**.  
  
---  
  
## 💥 Bölüm 2: Gerçek Dünya Saldırıları  
  
### 📄 `2_union_saldirisi.py` – Veri Çalma  
  
```python  
# ... (setup ve tablolar: kitaplar + GİZLİ kullanicilar)  
  
def saldiri_union():  
    payload = "' UNION SELECT id, email, parola_hash FROM kullanicilar; --"    tehlikeli_sorgu(payload)  # → E-posta ve şifre hash'leri ekrana dökülür!  
```  
  
### 📄 `3_boolean_saldirisi.py` – “Evet/Hayır” Oyunu  
  
```python  
def boolean_sorgu(payload):  
    return len(tehlikeli_sorgu(payload)) > 0  
# Admin şifresinin ilk harfi 'c' mi?  
if boolean_sorgu("George Orwell' AND (SELECT SUBSTR(parola_hash,1,1) FROM kullanicilar WHERE email='admin@site.com')='c'; --"):  
    print("Evet!")  
```  
  
### 📄 `4_error_saldirisi.py` – Hata Mesajlarından Bilgi Çıkarma  
  
```python  
# SQLite versiyonunu öğren  
tehlikeli_sorgu("George Orwell' AND 1=CAST(sqlite_version() AS INT); --")  
# Hata mesajında: "invalid literal for int() with base 10: '3.44.2'"  
```  
  
---  
  
## 🛡️ Bölüm 3: Gelişmiş Savunma Katmanları  
  
### 1. **Giriş Doğrulama (Beyaz Liste)**  
  
```python  
import re  
  
def yazar_gecerli_mi(yazar: str) -> bool:  
    return bool(re.fullmatch(r"[a-zA-Z0-9\s\.\-\u00C0-\u017F]{1,100}", yazar))  
```  
  
### 2. **Çıkış Kısıtlaması**  
  
```python  
# Sadece gerekli sütunları getir  
session.query(KitapDB.baslik, KitapDB.yazar).filter(...)  
```  
  
### 3. **Tehlikeli Kelime Filtresi (Ek Katman)**  
  
```python  
TEHLIKELI = {"UNION", "SELECT", "DROP", "--", ";"}  
def filtrele(inp):  
    return not any(kw in inp.upper() for kw in TEHLIKELI)  
```  
  
### 4. **Veritabanı Yetki Sınırlandırması (PostgreSQL Örneği)**  
  
```sql  
CREATE USER web_app WITH PASSWORD '...';  
GRANT SELECT ON kitaplar TO web_app;  
REVOKE ALL ON kullanicilar FROM web_app; -- Gizli tabloya erişim YOK!  
```  
  
### 5. **Web Application Firewall (WAF)**  
  
- **Cloudflare**, **AWS WAF** gibi servisler, otomatik olarak bilinen payload’ları engeller.  
- Geliştirme sırasında test edilemez, ama **üretimde kritik**.  
  
---  
  
## ✅ Bölüm 4: SQLAlchemy ORM – Güvenli ve Üretken Çözüm  
  
### 📄 `5_sqlalchemy_orm_ornek.py`  
  
```python  
from sqlalchemy import create_engine, Column, Integer, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker  
  
engine = create_engine("sqlite:///kitaplik_orm.db")  
Base = declarative_base()  
Session = sessionmaker(bind=engine)  
  
class KitapDB(Base):  
    __tablename__ = "kitaplar"    id = Column(Integer, primary_key=True)    baslik = Column(String)    yazar = Column(String)  
def guvenli_arama(yazar_adi):  
    session = Session()    # ✅ Otomatik olarak parametreli sorgu oluşturur    sonuc = session.query(KitapDB).filter(KitapDB.yazar == yazar_adi).all()    session.close()    return sonuc  
```  
  
> 💡 **Avantajlar:**  
> - SQL injection **otomatik engellenir**,  
> - Kod **okunabilir ve sürdürülebilir**,  
> - Veritabanı **bağımsızlığı** sağlanır.  
  
---  
  
## 🧠 Öğrenciye Kritik Mesajlar  
  
1. **`cursor.execute()` sizi SQL injection’dan KORUMAZ.**    
Sadece çoklu komut çalıştırmayı engeller.  
  
2. **Güvenlik, tek bir kapı değil, KATMANLI BİR KALE gibidir:**    
- Giriş doğrulama →    
   - Parametreli sorgu / ORM →    
   - Veritabanı yetkileri →    
   - WAF (üretimde).  
  
3. **ORM, sadece “kolaylık” değil, “güvenlik zorunluluğudur.”**  
  
4. **Asla kullanıcı girdisine güvenme.**    
Onu **her zaman güvenli değer** olarak işle, **asla kod veya string ek** olarak işleme.  
  
---  
  
> **“Kullanıcıdan gelen her veriyi, sadece bir *metin parçası* (değer) olarak değerlendirin.    
> Asla onu, veritabanına göndereceğiniz bir *SQL komutu* (kod) parçası gibi birleştirip çalıştırmayın.”**  
  
### 📌 Basit Açıklama:  
- **Değer (Value):** `"George Orwell"` → Bu, **sadece bir isim**. Güvenli.  
- **Kod (Code):** `"George Orwell'; DROP TABLE kitaplar; --"` → Bu, **gizli bir komut** içeriyor. Tehlikeli.  
  
### 💡 Örnek ile Anlatım:  
**Yanlış (Kodu birleştiriyor):**  ```python  
sorgu = "SELECT * FROM kitaplar WHERE yazar = '" + kullanıcı_girdisi + "'"  
# Eğer kullanıcı_girdisi = "'; DROP TABLE kitaplar; --" ise,  
# sorgu = "SELECT ... WHERE yazar = ''; DROP TABLE kitaplar; --'"  
# → Veritabanınız silinir!  
```  
  
**Doğru (Değeri parametre olarak geçiriyor):**  ```python  
cursor.execute("SELECT * FROM kitaplar WHERE yazar = ?", (kullanıcı_girdisi,))  
# Burada kullanıcı_girdisi, **her zaman metin** olarak işlenir.  
# SQL komutu olarak **asla yorumlanmaz**.  
```  
  
### ✅ Kural:  
> **Kullanıcı ne yazarsa yazsın, onu *veri* olarak kabul et.    
> Onunla *komut* oluşturmak, kapıyı saldırganlara açmak demektir.**  
  
  
---  
  
  
## 🚀 Sonraki Adım: Asenkron Veritabanı Mimarisi  
  
Bir sonraki modülde, bu güvenli yapıyı **FastAPI + async SQLAlchemy(evrensel tercüman)** ile nasıl entegre edeceğimizi öğreneceğiz.  
  
---  
  
> 📌 **Not:** Tüm örnek kodlar, **`modul_01_orm_felsefesi/`** dizininde ayrı dosyalar halinde mevcuttur.    
  
---  
  
## 🎓 Öğrenciye Mesaj  
  
> “Bir mühendis, sadece ‘çalışan kod’ yazmaz.    
> **Güvenli, sürdürülebilir ve takımla paylaşılabilir** kod yazar.    
> ORM, bu hedefe ulaşmanın en güçlü araçlarından biridir.”  
  