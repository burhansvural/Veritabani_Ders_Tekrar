"""
Modül 1 - Örnek 2: Flet ile SQL Injection Deney Laboratuvarı

Bu uygulama, ham SQL kullanımının risklerini interaktif bir arayüzde gösterir.
Öğrenciler, farklı "saldırı payload'ları" deneyerek SQL Injection'ın
ne kadar yıkıcı olabileceğini kendi gözleriyle görecekler.
"""

import flet as ft
import sqlite3
import os

DB_DOSYASI = "kitaplik_flet_deney.db"


# --- Veritabanı Fonksiyonları ---

def tablo_olustur_ve_sifirla():
    """Veritabanını sıfırlar ve test verileriyle doldurur."""
    if os.path.exists(DB_DOSYASI):
        os.remove(DB_DOSYASI)

    conn = sqlite3.connect(DB_DOSYASI)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE kitaplar (
            id INTEGER PRIMARY KEY,
            baslik TEXT NOT NULL,
            yazar TEXT NOT NULL
        )
    """)
    kitaplar = [
        ('Sefiller', 'Victor Hugo'),
        ('Savaş ve Barış', 'Leo Tolstoy'),
        ('Suç ve Ceza', 'Fyodor Dostoyevski'),
        ('1984', 'George Orwell')
    ]
    cursor.executemany("INSERT INTO kitaplar (baslik, yazar) VALUES (?, ?)", kitaplar)
    conn.commit()
    conn.close()


def tum_kitaplari_getir():
    """Veritabanındaki tüm kitapları bir Flet kontrolleri listesi olarak döndürür."""
    controls = []
    try:
        conn = sqlite3.connect(DB_DOSYASI)
        cursor = conn.cursor()
        cursor.execute("SELECT id, baslik, yazar FROM kitaplar ORDER BY id")
        rows = cursor.fetchall()

        if not rows:
            controls.append(ft.Text("Tabloda hiç kitap yok. Muhtemelen silindi!", color=ft.Colors.RED))
        else:
            for row in rows:
                controls.append(ft.Text(f"ID: {row[0]}, Başlık: {row[1]}, Yazar: {row[2]}"))
        conn.close()
    except sqlite3.OperationalError:
        controls.append(
            ft.Text("❌ HATA: 'kitaplar' tablosu bulunamadı!", color=ft.Colors.RED, weight=ft.FontWeight.BOLD))

    return controls


# --- Flet Uygulaması ---

def main(page: ft.Page):
    page.title = "SQL Injection Deney Laboratuvarı"
    page.scroll = ft.ScrollMode.ADAPTIVE

    # --- Arayüz Elemanları ---

    arama_input = ft.TextField(label="Aranacak Yazar Adı veya Saldırı Metni", width=500)
    sonuc_text = ft.Text("Sorgu sonucu burada görünecek...", italic=True,color=ft.Colors.GREEN_900)
    mevcut_durum_listesi = ft.Column(controls=tum_kitaplari_getir())

    # --- Sorgu Fonksiyonları ---

    def arama_yap_tehlikeli(e):
        yazar_adi = arama_input.value
        if not yazar_adi:
            return

        conn = sqlite3.connect(DB_DOSYASI)
        cursor = conn.cursor()
        query = f"SELECT * FROM kitaplar WHERE yazar = '{yazar_adi}'"

        try:
            # `executescript` birden çok komuta izin verdiği için saldırılar için idealdir.
            cursor.executescript(query)
            # Eğer sorgu bir SELECT ise, fetchall ile sonuç alınır (sınırlı senaryo)
            # Genellikle saldırgan SELECT sonucunu umursamaz.
            sonuc_text.value = "Tehlikeli sorgu çalıştırıldı. Veritabanı durumu aşağıda."
        except Exception as err:
            sonuc_text.value = f"Tehlikeli sorguda hata: {err}"

        conn.commit()
        conn.close()

        # Her işlemden sonra veritabanının son durumunu göster
        mevcut_durum_listesi.controls = tum_kitaplari_getir()
        page.update()

    def arama_yap_guvenli(e):
        yazar_adi = arama_input.value
        if not yazar_adi:
            return

        conn = sqlite3.connect(DB_DOSYASI)
        cursor = conn.cursor()
        query = "SELECT * FROM kitaplar WHERE yazar = ?"

        try:
            cursor.execute(query, (yazar_adi,))
            rows = cursor.fetchall()
            if not rows:
                sonuc_text.value = "Güvenli sorgu sonuç bulamadı."
            else:
                sonuclar = "\n".join([f"{row[1]} by {row[2]}" for row in rows])
                sonuc_text.value = f"Güvenli sorgu sonucu:\n{sonuclar}"
        except Exception as err:
            sonuc_text.value = f"Güvenli sorguda hata: {err}"

        conn.close()

        # Güvenli sorgu veritabanını DEĞİŞTİREMEZ, bu yüzden
        # durumu yenilemeye gerek yok, ama tutarlılık için yapabiliriz.
        mevcut_durum_listesi.controls = tum_kitaplari_getir()
        page.update()

    def veritabani_sifirla(e):
        tablo_olustur_ve_sifirla()
        mevcut_durum_listesi.controls = tum_kitaplari_getir()
        sonuc_text.value = "Veritabanı başlangıç durumuna sıfırlandı."
        page.update()

    # --- Saldırı Senaryoları İçin Hızlı Butonlar ---

    def payload_yerlestir(payload):
        arama_input.value = payload
        page.update()

    payload_1 = "' OR '1'='1"
    payload_2 = "George Orwell'; UPDATE kitaplar SET yazar = 'SALDIRGAN' WHERE yazar = 'George Orwell'; --"
    payload_3 = "'; DROP TABLE kitaplar; --"

    # --- Sayfa Düzeni ---

    page.add(
        ft.Column([
            ft.Text("Deney Laboratuvarı", size=32, weight=ft.FontWeight.BOLD),
            ft.Text("Aşağıdaki metin kutusuna normal bir yazar adı veya bir saldırı metni girin."),
            arama_input,
            ft.Row([
                ft.Button("✅ Güvenli Sorgu Çalıştır", on_click=arama_yap_guvenli, icon=ft.Icons.SHIELD,
                                  bgcolor=ft.Colors.GREEN_100),
                ft.Button("❌ Tehlikeli Sorgu Çalıştır", on_click=arama_yap_tehlikeli, icon=ft.Icons.WARNING,
                                  bgcolor=ft.Colors.RED_100),
            ]),
            ft.Divider(),
            ft.Text("Hızlı Saldırı Senaryoları:", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.OutlinedButton("1. Bilgi Sızdır", on_click=lambda e: payload_yerlestir(payload_1)),
                ft.OutlinedButton("2. Veri Değiştir", on_click=lambda e: payload_yerlestir(payload_2)),
                ft.OutlinedButton("3. Tabloyu Yok Et", on_click=lambda e: payload_yerlestir(payload_3)),
            ]),
            ft.Divider(),
            ft.Text("Sorgu Sonucu:", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=sonuc_text,
                bgcolor=ft.Colors.BLUE_GREY_50,
                padding=10,
                border_radius=5
            ),
            ft.Divider(),
            ft.Row([
                ft.Text("Veritabanının Mevcut Durumu:", size=18, weight=ft.FontWeight.BOLD),
                ft.IconButton(icon=ft.Icons.REFRESH, on_click=veritabani_sifirla, tooltip="Veritabanını Sıfırla")
            ]),
            ft.Container(
                content=mevcut_durum_listesi,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                padding=10,
                border_radius=5
            ),
        ])
    )

    # Uygulama ilk açıldığında veritabanını hazırla
    veritabani_sifirla(None)


if __name__ == "__main__":
    ft.run(main=main,view=ft.AppView.WEB_BROWSER)