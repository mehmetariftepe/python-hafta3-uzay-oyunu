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

## Teslimin tamamlanması

GitHub deposu: https://github.com/mehmetariftepe/python-hafta3-uzay-oyunu

PDF GitHub deposunun bağlantısını ister. Özgün 2. hafta projesi
sağlandığında değişiklikler o projenin üzerine aktarılıp eski testler de
çalıştırılmalıdır. kapsam.md içindeki örnekler ders örnekleri değildir.
Her fonksiyonu açıklayabilecek şekilde çalışılmalıdır.

## Fonksiyonları açıklamak için kısa rehber

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
Bu kurallar dersin özgün oyunu hakkında iddia değildir. Menülerde sayı seçilir;
q ile çıkılır. 2 ve ardından 4 seçilirse kara deliğe iki hamlede ulaşılır.
PDF'teki 13 hamle bir çıktı biçimi örneğidir; her oyunun 13 hamle sürmesi gerekmez.

## Yerel git geçmişini açma

ZIP'in içindeki bundle dosyası commit geçmişini taşır:

```sh
git clone hafta3_git_gecmisi.bundle hafta3_proje
cd hafta3_proje
uv run pytest
```

Commitler gerçek hazırlama sırasıyla, 11.10.2026 tarihinde oluşturulmuştur.
Geçmişte eski haftaya ait veya öğrenci tarafından yazıldığı iddia edilen
commit bulunmaz. Görev commitleri GitHub deposuna sırayla aktarılmıştır.
