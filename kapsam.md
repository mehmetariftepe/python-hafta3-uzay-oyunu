# Kapsam örnekleri

Dersteki üç örnek paylaşılmadığından aşağıdakiler bağımsız öğrenme örnekleridir.
Tahmin sütunu örneklerin beklenen çıktısını belirtir; öğrencinin derste yaptığı
bir tahmin olarak sunulmaz. Kodlar uzay_oyunu/kapsam_ornekleri.py içindedir.

| Örnek | Beklenen çıktı (tahmin) | Çalıştırılan gerçek sonuç | Neden |
| --- | --- | --- | --- |
| dis_degeri_oku | 10 | 10 | Yerel atama yoktur; modül düzeyindeki sayi okunur. |
| yerel_deger ve ardından dış sayi | 20, ardından 10 | 20, ardından 10 | Yerel sayi dıştaki sayi değişkenini değiştirmez. |
| kapsayan_fonksiyon | 30 | 30 | İç fonksiyon en yakın kapsayan fonksiyondaki sayi değerini bulur. |
| hatali_yerel | UnboundLocalError | UnboundLocalError | Fonksiyonda atama olduğundan sayi yereldir, ama print çalıştığında henüz değer almamıştır. |

İsim arama sırası: yerel, kapsayan fonksiyon, modül, yerleşik isimler.
UnboundLocalError örneğinde dışarıda sayi bulunması hatayı önlemez.
Çözüm, değeri okumadan önce yerel atamayı yapmak veya değeri parametreyle almaktır.

Varsayılan depo=[] listesi fonksiyon tanımlanırken bir kez oluşturulur.
Bu yüzden sonraki çağrı öncekinin listesini değiştirebilir. None kalıbında ise
depo verilmediğinde fonksiyon gövdesinde yeni liste oluşturulur.
