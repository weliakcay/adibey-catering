# Menü Güncelleme Sistemi

## Klasör Yapısı

```
menuler_data/
├── tabldot_menuler.xlsx   ← Tabldot menüleri buraya
├── kokteyl_menuler.xlsx   ← Kokteyl menüleri buraya
├── vip_menuler.xlsx       ← VIP menüleri buraya
└── KULLANIM.md            ← Bu dosya
menuler_guncelle.py        ← Güncelleme scripti (ana klasörde)
```

---

## Excel Dosyaları Nasıl Doldurulur?

### 📋 tabldot_menuler.xlsx — Sütunlar

| Sütun | Açıklama | Örnek |
|---|---|---|
| Menü Adı | Kartın başlığı | Anadolu Esintisi |
| Etiket | Üstteki renkli rozet (boş bırakılabilir) | Haftalık Favori |
| Etiket Rengi | Rozetin renk sınıfı | bg-primary / bg-emerald-600 |
| Fiyat (₺/kişi) | Sadece rakam | 170 |
| Yemek 1 | Menüdeki 1. yemek | Tavuk Çorbası |
| Yemek 2 | 2. yemek | Makarna |
| Yemek 3–7 | Diğer yemekler (boş bırakılabilir) | ... |

> Satır ekleyerek yeni menü kartı oluşturabilirsiniz.

---

### 🥂 kokteyl_menuler.xlsx — Sütunlar

| Sütun | Açıklama |
|---|---|
| Menü Adı | Başlık |
| Alt Başlık | Kısa açıklama cümlesi |
| Ürün 1–7 | Menüdeki ürünler (rozet olarak görünür) |

---

### ⭐ vip_menuler.xlsx — Sütunlar

| Sütun | Açıklama |
|---|---|
| Menü Adı | Başlık |
| Alt Başlık | Kısa açıklama cümlesi |
| Ürün 1–7 | Menüdeki ürünler (rozet olarak görünür) |

---

## Güncelleme Adımları

1. Excel dosyalarını düzenle (Numbers, Excel veya LibreOffice ile açılır)
2. Terminali aç
3. Şu komutu çalıştır:

```bash
cd "/Users/veliakcay/Documents/projeler/adıgüzel catering"
/Users/veliakcay/opt/anaconda3/bin/python3 menuler_guncelle.py
```

4. Tarayıcıda `http://localhost:3000/menuler.html` sayfasını yenile

---

## Görsel Ekleme

Görsel eklemek istediğinizde `images/` klasörüne şu isimlerle ekleyin:

| Menü | Görsel Adı |
|---|---|
| 1. Tabldot kartı | `images/menu_1.jpg` |
| 2. Tabldot kartı | `images/menu_2.jpg` |
| 3. Tabldot kartı | `images/menu_3.jpg` |
| Kokteyl | `images/kokteyl_1.jpg` |
| VIP | `images/vip_1.jpg` |

Görseli ekledikten sonra `menuler_guncelle.py` scriptini tekrar çalıştırın — script `<!-- GÖRSEL -->` yorumunu gerçek `<img>` etiketiyle değiştirir.

---

## Önemli Notlar

- Script çalıştırılmadan önce `menuler.html` otomatik yedeklenir (`menuler_yedek_TARIH.html`)
- Yedek dosyaları ana klasörde saklanır, silebilirsiniz
- Etiket Rengi için kullanılabilecek değerler:
  - `bg-primary` (turuncu)
  - `bg-emerald-600` (yeşil)
  - `bg-blue-600` (mavi)
  - `bg-purple-600` (mor)
  - `bg-rose-600` (kırmızı)
