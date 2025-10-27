"""
Modül 1 - Örnek 2: SQLAlchemy Core ile Tanışma

Bu örnek, ORM kullanmadan, doğrudan tablolar ve SQL benzeri ifadelerle
veritabanıyla nasıl konuşulacağını gösterir. Bu, ham SQL'den daha güvenli
ama ORM'den daha detaylı bir yaklaşımdır.

Tüm işlemler ve çıktılar bu konsol ekranında görünecektir.
"""

import sqlalchemy as sa

# --- Adım 1: Temelleri Kurmak ---

# 1.1: Veritabanı Motorunu (Engine) Oluşturma
# Basitlik için dosya tabanlı bir SQLite veritabanı kullanacağız.
# echo=True, SQLAlchemy'nin arka planda oluşturduğu TÜM SQL sorgularını
# konsola yazdırmasını sağlar. Bu, ne olup bittiğini görmek için harika bir yoldur!
# ⚠️ NOT: Ders dışı yazacağınız tüm kodlarda BUNU KAPATIN! Yani echo=False yapın. Güvenlik ve performans için.
engine = sa.create_engine("sqlite:///kitaplik_core.db", echo=True)

# 1.2: MetaData Objesini Oluşturma
# MetaData, veritabanımızdaki tüm tabloların bir kataloğu gibidir.
metadata = sa.MetaData()

# 1.3: Tablo Yapısını Python'da Tanımlama (ORM'deki `class` yerine)
# Burada bir Python sınıfı DEĞİL, doğrudan bir `Table` nesnesi tanımlıyoruz.
kitaplar_tablosu = sa.Table(
    'kitaplar',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('baslik', sa.String, nullable=False),
    sa.Column('yazar', sa.String, nullable=False)
)


# --- Adım 2: Veritabanı Operasyonları İçin Fonksiyonlar ---

def veritabani_kurulum(engine, metadata, kitaplar_tablosu):
    """Tabloyu oluşturur ve içine başlangıç verilerini ekler."""
    print("\n--- VERİTABANI KURULUMU BAŞLIYOR ---")
    # Önceki çalıştırmalardan kalan tabloyu temizle
    metadata.drop_all(engine)
    # Tanımladığımız tabloyu veritabanında oluştur
    metadata.create_all(engine)

    # Veritabanıyla konuşmak için bir bağlantı (connection) açıyoruz.
    with engine.connect() as conn:
        # Tek seferde birden çok kitap eklemek için bir ifade oluşturuyoruz.
        stmt = sa.insert(kitaplar_tablosu).values([
            {'baslik': 'Sefiller', 'yazar': 'Victor Hugo'},
            {'baslik': '1984', 'yazar': 'George Orwell'},
            {'baslik': 'Dune', 'yazar': 'Frank Herbert'},
        ])
        # İfadeyi çalıştır
        conn.execute(stmt)
        # Değişiklikleri kalıcı hale getir
        # ⚠️ SQLAlchemy Core'da (INSERT/UPDATE/DELETE) için commit() ZORUNLUDUR.
        conn.commit()
    print("--- VERİTABANI KURULUMU TAMAMLANDI ---\n")


def tum_kitaplari_goster(engine, kitaplar_tablosu):
    """Tablodaki tüm kitapları listeler."""
    print("\n--- Tüm Kitaplar Listeleniyor ---")
    with engine.connect() as conn:
        stmt = sa.select(kitaplar_tablosu)
        result = conn.execute(stmt)
        for row in result:
            print(f"ID: {row.id}, Başlık: {row.baslik}, Yazar: {row.yazar}")


def yazara_gore_kitap_bul(engine, kitaplar_tablosu, yazar_adi):
    """Belirli bir yazara ait kitapları GÜVENLİ bir şekilde bulur."""
    print(f"\n--- Yazar '{yazar_adi}' için Kitaplar Aranıyor (Güvenli Yöntem) ---")
    with engine.connect() as conn:
        # DİKKAT: Burada f-string KULLANMIYORUZ!
        # SQLAlchemy Core, bu ifadeyi parametreli bir sorguya çevirerek
        # SQL Injection'ı otomatik olarak engeller.
        stmt = sa.select(kitaplar_tablosu).where(kitaplar_tablosu.c.yazar == yazar_adi)
        result = conn.execute(stmt)
        rows = result.fetchall()
        if rows:
            for row in rows:
                print(f"Bulunan Kitap: {row.baslik}")
        else:
            print("Bu yazara ait kitap bulunamadı.")


def yeni_kitap_ekle(engine, kitaplar_tablosu, baslik, yazar):
    """Yeni bir kitap ekler."""
    print(f"\n--- Yeni Kitap Ekleniyor: '{baslik}' ---")
    with engine.connect() as conn:
        stmt = sa.insert(kitaplar_tablosu).values(baslik=baslik, yazar=yazar)
        conn.execute(stmt)
        # ⚠️ SQLAlchemy Core'da (INSERT/UPDATE/DELETE) için commit() ZORUNLUDUR.
        conn.commit()
    print("Ekleme başarılı.")


def kitap_guncelle(engine, kitaplar_tablosu, eski_baslik, yeni_baslik):
    """Bir kitabın başlığını günceller."""
    print(f"\n--- Kitap Güncelleniyor: '{eski_baslik}' -> '{yeni_baslik}' ---")
    with engine.connect() as conn:
        stmt = (
            sa.update(kitaplar_tablosu)
            .where(kitaplar_tablosu.c.baslik == eski_baslik)
            .values(baslik=yeni_baslik)
        )
        conn.execute(stmt)
        # ⚠️ SQLAlchemy Core'da (INSERT/UPDATE/DELETE) için commit() ZORUNLUDUR.
        conn.commit()
    print("Güncelleme başarılı.")


def kitap_sil(engine, kitaplar_tablosu, baslik):
    """Bir kitabı başlığına göre siler."""
    print(f"\n--- Kitap Siliniyor: '{baslik}' ---")
    with engine.connect() as conn:
        stmt = sa.delete(kitaplar_tablosu).where(kitaplar_tablosu.c.baslik == baslik)
        conn.execute(stmt)
        # ⚠️ SQLAlchemy Core'da (INSERT/UPDATE/DELETE) için commit() ZORUNLUDUR.
        conn.commit()
    print("Silme başarılı.")


# --- Adım 3: Operasyonları Sırayla Çalıştırma ---

if __name__ == "__main__":
    # 1. Her çalıştırmada veritabanını temiz bir şekilde kur
    veritabani_kurulum(engine, metadata, kitaplar_tablosu)

    # 2. Başlangıç durumunu gör
    tum_kitaplari_goster(engine, kitaplar_tablosu)

    # 3. Güvenli filtreleme (SELECT ... WHERE)
    yazara_gore_kitap_bul(engine, kitaplar_tablosu, "George Orwell")

    # 4. Yeni bir kayıt ekle (INSERT)
    yeni_kitap_ekle(engine, kitaplar_tablosu, "Suç ve Ceza", "Fyodor Dostoyevski")
    tum_kitaplari_goster(engine, kitaplar_tablosu)

    # 5. Mevcut bir kaydı güncelle (UPDATE)
    kitap_guncelle(engine, kitaplar_tablosu, "Sefiller", "Les Misérables")
    tum_kitaplari_goster(engine, kitaplar_tablosu)

    # 6. Bir kaydı sil (DELETE)
    kitap_sil(engine, kitaplar_tablosu, "1984")
    tum_kitaplari_goster(engine, kitaplar_tablosu)

    print("\n\n" + "=" * 50)
    print(" DERSİN ÖZETİ: SQLAlchemy Core")
    print("=" * 50)
    print("✅ Gördüğünüz gibi, SQL'e çok daha yakın ifadeler kullandık.")
    print("✅ `Table`, `select`, `insert`, `update`, `delete` gibi fonksiyonlarla çalıştık.")
    print("✅ `echo=True` sayesinde Python kodumuzun hangi SQL'e dönüştüğünü gördük.")
    print("✅ ORM'deki sihirli `kitap.yazar` gibi nesne erişimleri burada yok, her şey daha açık.")
    print("⚠️ Daha fazla kod yazdık. ORM, bu işlemlerin çoğunu bizim için basitleştirir.")
    print("➡️ Şimdi ORM'in bu işlemleri nasıl daha 'Pythonic' hale getirdiğini daha iyi anlayabiliriz.")