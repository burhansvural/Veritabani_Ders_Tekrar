"""
Modül 1 - Örnek 2b: SQLAlchemy Core ile Flet Arayüzü

Bu örnek, SQLAlchemy Core kullanarak temel veritabanı işlemlerini (CRUD)
gerçekleştiren interaktif bir Flet uygulamasıdır.

Amaç: Öğrencilerin, ORM olmadan, SQL benzeri ifadelerle bir arayüzü
nasıl yöneteceklerini görmelerini sağlamaktır.
"""

import flet as ft
import sqlalchemy as sa

# --- Adım 1: Temelleri Kurmak ---

# Veritabanı motoru (echo=True ile SQL logları terminalde görünecek)
engine = sa.create_engine("sqlite:///kitaplik_core_flet.db", echo=True)
metadata = sa.MetaData()

# Tablo tanımı
kitaplar_tablosu = sa.Table(
    'kitaplar',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('baslik', sa.String, nullable=False),
    sa.Column('yazar', sa.String, nullable=False)
)


# Flet uygulamasını çalıştırmadan önce veritabanını hazırla
def veritabani_kurulum():
    """Tabloyu oluşturur ve içine başlangıç verilerini ekler."""
    metadata.drop_all(engine)
    metadata.create_all(engine)
    with engine.connect() as conn:
        stmt = sa.insert(kitaplar_tablosu).values([
            {'baslik': 'Sefiller', 'yazar': 'Victor Hugo'},
            {'baslik': '1984', 'yazar': 'George Orwell'},
            {'baslik': 'Dune', 'yazar': 'Frank Herbert'},
        ])
        conn.execute(stmt)
        conn.commit()
    print("✅ Veritabanı Flet için kuruldu.")


# --- Flet Uygulaması ---

def main(page: ft.Page):
    page.title = "SQLAlchemy Core ile Kütüphane Yönetimi"
    page.scroll = ft.ScrollMode.ADAPTIVE

    # --- Arayüz Elemanları ---

    baslik_input = ft.TextField(label="Kitap Başlığı", width=250)
    yazar_input = ft.TextField(label="Yazar", width=250)
    kitaplar_listesi_view = ft.ListView(expand=True, spacing=5)

    # --- Veritabanı Operasyonları (Flet Butonlarına Bağlı) ---

    def tum_kitaplari_listele(e=None):
        """Tüm kitapları veritabanından çeker ve arayüzü günceller."""
        kitaplar_listesi_view.controls.clear()
        with engine.connect() as conn:
            stmt = sa.select(kitaplar_tablosu).order_by(kitaplar_tablosu.c.id)
            result = conn.execute(stmt)
            for row in result:
                kitaplar_listesi_view.controls.append(
                    ft.Text(f"ID: {row.id}, Başlık: {row.baslik}, Yazar: {row.yazar}")
                )
        page.update()

    def kitap_ekle(e):
        if not baslik_input.value or not yazar_input.value:
            return

        with engine.connect() as conn:
            stmt = sa.insert(kitaplar_tablosu).values(
                baslik=baslik_input.value,
                yazar=yazar_input.value
            )
            conn.execute(stmt)
            conn.commit()

        baslik_input.value = ""
        yazar_input.value = ""
        tum_kitaplari_listele()  # Listeyi tazele

    def kitap_guncelle(e):
        # Bu örnekte, basitlik için ilk kitabı güncelleyelim
        if not baslik_input.value:
            return

        with engine.connect() as conn:
            # ID'si 1 olan kitabın başlığını güncelle
            stmt = (
                sa.update(kitaplar_tablosu)
                .where(kitaplar_tablosu.c.id == 1)
                .values(baslik=baslik_input.value)
            )
            conn.execute(stmt)
            conn.commit()

        baslik_input.value = ""
        tum_kitaplari_listele()

    def en_son_kitabi_sil(e):
        with engine.connect() as conn:
            # En yüksek ID'li kitabı bulmak için bir alt sorgu
            # Bu, Core'un SQL'e ne kadar yakın olduğunu gösterir
            latest_id_stmt = sa.select(sa.func.max(kitaplar_tablosu.c.id))
            latest_id = conn.execute(latest_id_stmt).scalar_one_or_none()

            if latest_id:
                # Silme işlemini yap
                delete_stmt = sa.delete(kitaplar_tablosu).where(kitaplar_tablosu.c.id == latest_id)
                conn.execute(delete_stmt)
                conn.commit()

        tum_kitaplari_listele()

    # --- Sayfa Düzeni ---

    page.add(
        ft.Column([
            ft.Text("SQLAlchemy Core Deney Paneli", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Terminaldeki SQL loglarını izleyin!", italic=True, color=ft.Colors.BLUE_GREY),
            ft.Divider(),

            ft.Row([baslik_input, yazar_input]),
            ft.Row([
                ft.Button("Yeni Kitap Ekle", on_click=kitap_ekle, icon=ft.Icons.ADD),
                ft.Button("ID 1'deki Kitabın Başlığını Güncelle", on_click=kitap_guncelle, icon=ft.Icons.EDIT),
                ft.Button("En Son Kitabı Sil", on_click=en_son_kitabi_sil, icon=ft.Icons.DELETE,
                                  bgcolor=ft.Colors.RED_200),
            ]),

            ft.Divider(),

            ft.Row([
                ft.Text("Veritabanındaki Kitaplar", size=18, weight=ft.FontWeight.BOLD),
                ft.IconButton(icon=ft.Icons.REFRESH, on_click=tum_kitaplari_listele, tooltip="Listeyi Yenile"),
            ]),
            ft.Container(
                content=kitaplar_listesi_view,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                padding=10,
                border_radius=5,
                height=300
            ),
        ])
    )

    # Uygulama ilk açıldığında listeyi doldur
    tum_kitaplari_listele()


if __name__ == "__main__":
    # Flet uygulamasını çalıştırmadan önce veritabanını her seferinde temiz bir şekilde kur
    veritabani_kurulum()
    # Flet uygulamasını web tarayıcısında çalıştır
    ft.run(main=main, view=ft.AppView.WEB_BROWSER)