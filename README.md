# Hafta 3 - Fonksiyonlar

Öğrenci bilgileri: Mehmet Arif Tepe / 20253006008
Hazırlanma tarihi: 11.10.2026

Bu proje bağımsız bir çalışma örneğidir.
Önceki haftanın uzay oyunu, eski testler ve dersteki üç kapsam örneği
paylaşılmadığından, onların devamı veya birebir karşılığı olduğu iddia edilmez.
Harita bu örnek için kurulmuştur; özgün oyunun bağlantı sırası doğrulanamaz.
Git geçmişi bu çalışma sırasında oluşturulmuştur; 2. hafta commit'i yoktur.

## Çalıştırma

Python 3.12 ve uv gerekir.

```sh
uv run pytest
uv run python -m uzay_oyunu.oyun
uv run python -m uzay_oyunu.kayit
uv run python -m uzay_oyunu.kapsam_ornekleri
uv run python -m uzay_oyunu.bonus
```

Her görevden sonra testler çalıştırılır. Test çıktıları kontroller klasöründedir.
Her görev ayrı commit olarak kaydedilir. İlk saf fonksiyon testlerinin ve
paylaşılan varsayılan liste testinin başarısız sonuçları da korunur.

## Fonksiyonlar

| Fonksiyon | Temel mantık |
| --- | --- |
| envanter_metni | True olan eşyaları listeye ekler; join ile metin yapar. Çıktı basmaz. |
| hedef_menusu | enumerate ile hedefleri 1'den başlayarak numaralandırır. |
| gorev_kaydi | *adimlar çok sayıda adım, **ekler adlı ek bilgiler alır. |
| galaksi_kur | Başlangıcı kontrol eder; kwargs.get ile varsayılan yakıtı seçer. |
| galaksi_oku | JSON dosyasını okur, **veri ile alanları argümanlara açar. |
| yakit_ekle | None gelirse yeni liste açar; verilen listeyi aynı nesne olarak kullanır. |
| hamle_sayaci | İç fonksiyon nonlocal ile kendi toplamını değiştirir. |
| en_bagli_gezegenler | Negatif bağlantı sayısıyla azalan; isimle eşitlik sıralaması yapar. |
| sure_olc | Çağrı öncesi ve sonrası zamanı ölçer, asıl sonucu geri döndürür. |

Bu bağımsız oyunda her geçerli yolculuk 10 yakıt harcar. Dünya başlangıcında
kredi vardır; centauri ziyaretinde motor, orion ziyaretinde pilot edinilir.
Menülerde sayı seçilir;
q ile çıkılır. 2 ve ardından 4 seçilirse kara deliğe iki hamlede ulaşılır.
