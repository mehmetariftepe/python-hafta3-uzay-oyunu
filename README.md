# Hafta 5 - Dekoratörler ve komut sistemi

Mehmet Arif Tepe / 20253006008
Hazırlanma tarihi: 25.10.2026

Hafta 4'ün sonunda bulunan committen devam edilmiştir. Önceki harita ve test dosyaları korunmuştur.
Her görev ve bonus ayrı commit olarak kaydedilmiştir.

## Çalıştırma

Depo kökünde Python 3.12+ ile:

```sh
python -m uzay_oyunu.oyun
python -m uzay_oyunu.dekorator_ornekleri
```

`uv` kuruluysa aynı komutların başına `uv run` eklenebilir.
Testler için `uv run pytest -v` kullanılır; GitHub Actions da bu komutu çalıştırır.

Oyun menüsünde gezegen numarası yerine `yardim`, `envanter` veya `harita`
yazılabilir. Bu komutlar hamle ve yakıt tüketmez; aynı menü yeniden gösterilir.
`q` oyundan çıkar. Örnek: `yardim` → `harita` → `1` → `envanter`.

## Görevler ve dosyalar

| Görev | Uygulama | Kontrol |
| --- | --- | --- |
| 1: süre | `dekoratorler.sure_olc` | Sonuç, adlı argüman, ad/docstring ve çıktı biçimi |
| 2: sayaç ve sıra | `say`, `dekorator_ornekleri` | fib(20): 21891 / 39 / 21 çağrı |
| 3: log | `log_cagri` | `galaksi_kur` ve `hedef_menusu` gerçekten dekore edilir |
| 4: kayıt deseni | `komutlar.py`, `oyun.travel` | Üç komut, kimlik koruma, yinelenen ad ve oyun akışı |
| 5: sınır | `sinirla(0, 100)`, `yakit_harca` | 0 ve 100 dahil; -1, 101, 150 reddedilir |
| Bonus: önbellek | `hafiza(maxsize=None)` | Sınırsız cache, FIFO sınırı, adlı argümanlar ve lru_cache karşılaştırması |

Yeni testler `tests/test_dekoratorler.py` dosyasındadır.
Dekoratörlerin tanım/çağrı anındaki davranışı ve sıra açıklaması
[dekorator_sirasi.md](dekorator_sirasi.md) içindedir.

## Süre dekoratörünün gerçek ölçümü

25.10.2026, Python 3.12.14 / Linux ortamında
`python -m uzay_oyunu.dekorator_ornekleri` komutunun rota kısmı:

```text
rota_sayisi: 7.0232 sn
20 adımlık rota sayısı: 20617703
```

Bu, Hafta 4'ün önbelleksiz sayacının **dışarıdan** `sure_olc` ile
sarılmış halidir; her özyinelemeli çağrı için ayrı süre basılmaz.
Ölçüm `time.perf_counter()` ile yapılır ve dönen sonuç korunur.
Süre cihaza/yüke göre değişir; buradaki değer çalıştırılmış tek koşudur.

## Tasarım tercihleri

- Bütün sarmalayıcı dekoratörler `functools.wraps` ile adı, açıklamayı
  ve özgün fonksiyona `__wrapped__` bağlantısını korur. `*args`, `**kwargs`
  ve dönüş değerleri aktarılır. Tip ipuçları `ParamSpec`/`TypeVar` ile korunur.
- **Kayıt dekoratörü özel durumdur:** PDF aynı fonksiyonun döndürülmesini
  istediği için `komut` sarmalayıcı üretmez. `wraps` gerektiren yeni bir
  fonksiyon yoktur; fonksiyon kimliği testte `is` ile doğrulanır.
- Loglar `stderr` akışına yazılır. Böylece eski saf metin testlerinin
  `stdout` beklentisi değişmez; terminalde hem çağrı hem sonuç görünür.
  Ekranı sade tutmak için Bash'te `2>/dev/null`, PowerShell'de `2>$null`
  ile loglar gizlenebilir. İstisna halinde çağrı kaydı vardır ama dönüş değeri yoktur.
- `sinirla` hem `yakit_harca(30)` hem `yakit_harca(miktar=30)` çağrısını
  denetler. Geçersiz değerlerde asıl fonksiyon çalışmaz. Bu fonksiyon 100'lük
  ayrı depo örneğidir; oyunun mevcut yakıt üreteci korunmuştur.
- Bonus cache, `lru_cache` kullanmadan closure içindeki bir `dict` ile çalışır.
  `None` sınırsız, `0` kapalı önbellektir. Pozitif kapasitede ilk eklenen
  kayıt silinir (**FIFO**); isabetler eklenme sırasını yenilemez.
  `lru_cache` ise en uzun süredir kullanılmayanı siler (**LRU**).
  İki yöntem aynı fonksiyon sonuçlarını verir, fakat hesap sayıları farklı olabilir.
  Anahtarlar hashlenebilir konumsal/adlı argümanlardan oluşur; istisnalar saklanmaz.
  Bu basit eğitim örneği `lru_cache`'in tüm tür/iş parçacığı özelliklerini taklit etmez.

## Doğrulama

Yerel `uv run pytest -q`: **62 test geçti** (39 eski, 23 yeni test durumu).
Her görevden sonra bütün testler çalıştırılmıştır. Oyun entegrasyon testi,
komutlar arasında dört yolculuk yapıp 60 yakıtla kara deliğe ulaşır.

---

# Hafta 4 - Üreteçler ve functools (önceki belgeleme)

Mehmet Arif Tepe / 20253006008
Hazırlanma tarihi: 18.10.2026

Bu çalışma, aynı deponun 3. hafta son commit'i üzerine eklenmiştir.
Önceki harita ve testler korunmuştur. Beş görev ve bonus ayrı commit'lerdedir.

## Çalıştırma ve test

Python 3.12+ ve uv ile depo kökünde:

```sh
uv run pytest -v
uv run python -m uzay_oyunu.oyun
uv run python -m uzay_oyunu.rota_olcum
uv run python -m uzay_oyunu.zamanlayici_demo
```

GitHub Actions aynı `uv run pytest -v` komutunu çalıştırır.
Zamanlayıcı örneği yaklaşık 10 saniye sürer ve meşgul bekler.

## Görevlerin mantığı

1. **Fibonacci:** `akis.fibonacci()` sonsuzdur. `next()` ilk üç değeri
   `(0, 1, 1)` verir. `islice(fibonacci(), 12)` ile ilk 12 değer;
   `takewhile(lambda n: n < 100, fibonacci())` ile 100'den küçükler alınır.
   İkisinin sonucu `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]` olur.
   Aynı üreteç tekrar kullanılırsa kaldığı yerden sürer; otomatik başa dönmez.
2. **Yakıt:** `yakit_gostergesi(100, 30)` sırayla `70, 40, 10, 0`
   üretir. Sonraki `next()` bir `StopIteration` yükseltir. `travel()`
   göstergesini oyun başında bir kez oluşturur. Geçersiz seçim yakıt harcamaz.
   Eski testte iki yolculuk sonrası 80 beklendiğinden tüketim 10 korunmuştur.
   Sıfırı üreten son yolculuk tamamlanır; hedef kara delik değilse gösterge
   tükenince kayıp mesajı yazılır. Sıfır yakıtla giriş dahi istenmez.
3. **Boru hattı:** `satirlari_oku` → `ayristir` → `uzun_yolculuklar`.
   Dosya `with` içinde satır satır okunur; hiçbir aşama tüm veriyi listelemez.
   Toplam yakıt **88**, 10'dan büyük kayıtların hedefleri
   `['sirius', 'centauri', 'orion', 'kara_delik']` olur. Eşiğe eşitler alınmaz.
4. **Rota:** sıfır adım için bir boş rota vardır. Pozitif adımda her komşunun
   bir eksik adımlı rota sayısı toplanır. Çıkışı olmayan gezegende pozitif
   adımın sonucu sıfırdır. `@lru_cache(maxsize=None)` içteki özyinelemeli
   fonksiyondadır; aynı `(gezegen, adim)` tekrar hesaplanmaz. Harita,
   oluşturulan sayacın ömrü boyunca değiştirilmemelidir; değişirse yeni sayaç kurulur.
5. **İstatistik:** `istatistik.py` her soruyu iki biçimde çözer:
   `map` / liste üreteci; `filter` / liste üreteci; `reduce` / `sum`.
   Liste üreteçleri koşulu daha doğrudan gösterir. Önceki projede hız
   parametreli `yolculuk` bulunmadığından süreyi hesaplayan fonksiyon eklenmiştir.
   `hizli_yolculuk = partial(yolculuk, hiz=3)`; örneğin `hizli_yolculuk(12) == 4`.
   `partial` hızı önceden bağlar; çağrıda açıkça başka hız verilerek değiştirilebilir.

## Kendi haritamızdaki sonuçlar

PDF'deki örnek haritayla önceki haftanın haritası aynı değildir.
Haritayı örnek sonuçlara uydurmak için değiştirmedim. Mars yoktur;
fark bağlantılardadır: centauri'nin 3, sirius'un 4, orion'un 1 çıkışı vardır.

| İşlem | Sonuç |
| --- | --- |
| Dünya'dan 3 adımlık rotalar | 13 |
| Dünya'dan 10 adımlık rotalar | 4931 |
| Dünya'dan 40 adımlık rotalar | 362466971805923 |
| En az iki bağlantısı olanlar | dünya, centauri, sirius |
| Toplam yönlü bağlantı | 10 |

## Gerçek süre ölçümü

18.10.2026, Python 3.12.14 / Windows; `time.perf_counter()` ile tek koşu.
Önce önbelleksiz sürüm, sonra yeni ve boş önbellekli sayaç çalıştırılmıştır.
Her ikisinin 20 adım sonucu **20617703** olarak doğrulanmıştır.

| Sürüm | Süre (saniye) |
| --- | ---: |
| Önbelleksiz | 5.542470100 |
| Önbellekli, soğuk önbellek | 0.000066100 |

```text
CacheInfo(hits=92, misses=98, maxsize=None, currsize=98)
```

Bu çıktı yalnızca 20 adımlık ölçüm sonrasındadır. Süreler cihaza ve yüke göre
değişir; çok kısa sürelerde tek koşu hassas bir performans kıyaslaması değildir.
`rota_olcum` komutu iki sürümü aynı haritada yeniden ölçer.

## Bonus: meşgul bekleme

`akis.zamanlayici(aralik)` her sorguda sürenin dolup dolmadığını üretir.
Kaynak kitaptaki kod paylaşılmadığından bu, aynı kavram için yazılan bir uygulamadır.
Örnek, yaklaşık 2/4/6/8/10. saniyelerde **tik**, 5/10. saniyelerde **tak** yazar;
10. saniyede iki olay da işlenir. İşletim sistemi nedeniyle kesin zaman garantisi yoktur.

Bu bir **meşgul bekleme** örneğidir: döngü durmadan saati kontrol eder,
beklerken de CPU tüketir. `time.sleep()` ise iş parçacığını belirtilen süre
boyunca bekletir ve CPU'yu serbest bırakır; uyanış biraz gecikebilir.
Üreteç kullanmak tek başına CPU kullanımını azaltmaz.

## Test kapsamı

`tests/test_akis.py` her görevi kapsar: Fibonacci'nin tek geçişliliği,
`StopIteration`, yakıt bittiğinde oyun, boru hattının erken okumaması,
eşik sınırı, cache isabetleri, bağımsız önbellekler, istatistiklerin eşitliği
ve gerçek bekleme olmadan sahte saatle zamanlayıcı kontrolü.
Rota sayacı ayrıca 0–40 adım arasında bağımsız ileri yönlü sayımla karşılaştırılır.
Önceki haftanın test dosyaları değiştirilmemiştir.

---

# Hafta 3 - Fonksiyonlar (önceki belgeleme)

Mehmet Arif Tepe / 20253006008
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

