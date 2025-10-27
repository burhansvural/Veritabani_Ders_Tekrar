# Veritabani_Ders_Tekrar/modul_01_orm_felsefesi/1_ham_sql_ornek_ileri_saldirilar.py
"""
Modül 1 - Örnek 1 (İleri Seviye): SQL Injection Saldırı Vektörleri

Bu örnek, `cursor.execute()`'nun bile sizi KORUYAMAYACAĞI,
gerçek dünyada kullanılan sofistike SQL Injection saldırılarını gösterir.
Üç ana saldırı türünü inceleyeceğiz:
1. UNION Injection: Veri sızdırma.
2. Boolean-based Injection: "Evet/Hayır" sorularıyla bilgi toplama.
3. Error-based Injection: Hata mesajlarından bilgi sızdırma.
"""

import sqlite3
import os

DB_DOSYASI = "kitaplik_ileri_tehlike.db"


# --- Yardımcı Fonksiyonlar ---
def duraklat(mesaj=""):
    input(f"\n--- {mesaj}Devam etmek için Enter tuşuna basın ---")


# --- Veritabanı Fonksiyonları ---
def tablo_olustur():
    if os.path.exists(DB_DOSYASI): os.remove(DB_DOSYASI)
    conn = sqlite3.connect(DB_DOSYASI)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE kitaplar (id INTEGER PRIMARY KEY, baslik TEXT, yazar TEXT)")
    kitaplar = [('Sefiller', 'Victor Hugo'), ('1984', 'George Orwell')]
    cursor.executemany("INSERT INTO kitaplar (baslik, yazar) VALUES (?, ?)", kitaplar)
    cursor.execute("CREATE TABLE kullanicilar (id INTEGER PRIMARY KEY, email TEXT, parola_hash TEXT)")
    kullanicilar = [('admin@site.com', 'cok_gizli_sifre_hash_123'), ('user@site.com', 'baska_gizli_sifre_456')]
    cursor.executemany("INSERT INTO kullanicilar (email, parola_hash) VALUES (?, ?)", kullanicilar)
    conn.commit()
    conn.close()
    print("✅ Veritabanı, 'kitaplar' ve GİZLİ 'kullanicilar' tablolarıyla oluşturuldu.")


# --- Sorgu Fonksiyonu ---

# ❌ TEHLİKELİ: SQL Injection açığı var!
def kitaplari_getir_tehlikeli(yazar_adi: str):
    conn = sqlite3.connect(DB_DOSYASI)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = f"SELECT id, baslik, yazar FROM kitaplar WHERE yazar = '{yazar_adi}'"
    print(f"\n executing DANGEROUS query: {query}\n")
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        print("--- Uygulamanın Kullanıcıya Gösterdiği Sonuç ---")
        if not rows:
            print("Hiçbir şey bulunamadı.")
        else:
            for row in rows:
                print(f"Başlık: {row['baslik']}, Yazar: {row['yazar']}")
        print("-------------------------------------------")
        return len(rows) > 0  # Sonuç döndü mü dönmedi mi bilgisini geri verelim
    except Exception as e:
        print(f"❌ Sorgu çalıştırılırken bir HATA MESAJI oluştu: {e}")
        return False  # Hata durumunda sonuç yok
    finally:
        conn.close()


if __name__ == "__main__":
    tablo_olustur()

    # === SALDIRI 1: UNION INJECTION (VERİ ÇALMA) ===
    print("\n\n" + "=" * 50)
    print("💥 SALDIRI 1: UNION INJECTION - Doğrudan Veri Çalma 💥")
    print("=" * 50)
    print("Amaç: Kitap arama formunu kullanarak, GİZLİ 'kullanicilar' tablosundaki e-posta ve şifreleri çalmak.")
    saldiri_payload_1 = "' UNION SELECT id, email, parola_hash FROM kullanicilar; --"
    duraklat("UNION saldırısını başlatmak için ")
    kitaplari_getir_tehlikeli(saldiri_payload_1)
    print("\nSONUÇ: Başarılı! Gizli 'kullanicilar' tablosundaki tüm veriler doğrudan ekrana yazdırıldı.")

    # === SALDIRI 2: BOOLEAN-BASED INJECTION (EVET/HAYIR OYUNU) ===
    print("\n\n" + "=" * 50)
    print("💥 SALDIRI 2: BOOLEAN-BASED - Kör Talih Oyunu 💥")
    print("=" * 50)
    print("Senaryo: Uygulama artık detaylı sonuç göstermiyor, sadece 'Sonuç Bulundu' veya 'Bulunamadı' diyor.")
    print("Amaç: Veritabanına 'Evet/Hayır' soruları sorarak gizli bilgileri harf harf tahmin etmek.")
    duraklat("Boolean tabanlı saldırıyı başlatmak için ")

    print("\n--- Soru 1: 'kullanicilar' adında bir tablo var mı? ---")
    # Sorgu: 'George Orwell' VE (kullanicilar tablosundan 1 satır seçebiliyor muyum?)
    saldiri_payload_2a = "George Orwell' AND (SELECT COUNT(*) FROM kullanicilar) >= 1; --"
    if kitaplari_getir_tehlikeli(saldiri_payload_2a):
        print("\nCEVAP: EVET! 'kullanicilar' tablosu var, çünkü sorgu sonuç döndürdü.")
    else:
        print("\nCEVAP: Hayır, böyle bir tablo yok.")

    duraklat()

    print("\n--- Soru 2: Admin kullanıcısının şifresinin ilk harfi 'c' mi? ---")
    # Sorgu: 'George Orwell' VE (admin kullanıcısının şifresinin ilk harfi 'c' mi?)
    saldiri_payload_2b = "George Orwell' AND (SELECT SUBSTR(parola_hash, 1, 1) FROM kullanicilar WHERE email = 'admin@site.com') = 'c'; --"
    if kitaplari_getir_tehlikeli(saldiri_payload_2b):
        print("\nCEVAP: EVET! Şifrenin ilk harfi 'c'. ('cok_gizli_sifre_hash_123')")
    else:
        print("\nCEVAP: Hayır, şifrenin ilk harfi 'c' değil.")

    print(
        "\nSONUÇ: Saldırgan, bu 'Evet/Hayır' oyununu yüzlerce kez otomatik olarak deneyerek tüm şifreyi harf harf bulabilir!")

    # === SALDIRI 3: ERROR-BASED INJECTION (HATA MESAJLARINI KONUŞTURMA) ===
    print("\n\n" + "=" * 50)
    print("💥 SALDIRI 3: ERROR-BASED - Hatalardan Beslenmek 💥")
    print("=" * 50)
    print("Senaryo: Geliştirici, hataları kullanıcıya doğrudan gösteriyor (büyük bir hata!).")
    print("Amaç: Veritabanına kasıtlı olarak hatalı bir komut verip, hata mesajının içinde gizli bilgileri sızdırmak.")
    duraklat("Hata tabanlı saldırıyı başlatmak için ")

    print("\n--- Soru: SQLite versiyonu nedir? ---")
    # Sorgu: 'George Orwell' VE (bir sayıyı metne çevirmeye çalışarak hata yarat, metin olarak da SQLite versiyonunu kullan)
    # Bu, belirli veritabanı fonksiyonlarını (örn: sqlite_version()) bilmeyi gerektirir.
    saldiri_payload_3 = "George Orwell' AND 1=CAST(sqlite_version() AS INT); --"
    kitaplari_getir_tehlikeli(saldiri_payload_3)

    print("\nSONUÇ: Başarılı! Uygulama çöktü, ama hata mesajının içinde")
    print("   'invalid literal for int() with base 10: '3.XX.X'' gibi bir ifadeyle veritabanı versiyonunu öğrendik.")
    print("   Aynı teknik, tablo isimlerini, kullanıcı adlarını vb. sızdırmak için de kullanılabilir.")

    print("\n\n" + "=" * 50)
    print("DERSİN ÖZETİ: SQL Injection sadece veri çalmak değildir.")
    print("Aynı zamanda, bir dedektif gibi sistem hakkında yavaş yavaş bilgi toplamak veya")
    print("sistemi konuşturarak sırlarını ifşa etmesini sağlamaktır.")
    print(
        "✅ TEK ÇÖZÜM: Parametreli sorgular veya SQLAlchemy ORM gibi sizi TÜM bu senaryolardan koruyan araçlar kullanmaktır.")
    print("=" * 50)