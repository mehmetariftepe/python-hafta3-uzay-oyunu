# Hafta 3 - Fonksiyonlar

Öğrenci bilgileri: Mehmet Arif Tepe / 20253006008
Hazırlanma tarihi: 11.10.2026

Bu proje yapay zekâ desteğiyle hazırlanmış bağımsız bir çalışma örneğidir.
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

PDF GitHub deposunun bağlantısını ister. Bu ZIP ve yerel git geçmişi,
GitHub'da yayımlanmış depo bağlantısının yerini tutmaz. Özgün 2. hafta projesi
sağlandığında değişiklikler o projenin üzerine aktarılıp eski testler de
çalıştırılmalıdır. kapsam.md içindeki örnekler ders örnekleri değildir.
Her fonksiyonu açıklayabilecek şekilde çalışılmalıdır.
