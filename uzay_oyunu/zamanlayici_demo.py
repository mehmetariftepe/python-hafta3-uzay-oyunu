"""10 saniye boyunca iki ayrı aralıkta çalışan meşgul bekleme örneği."""
from time import perf_counter

from uzay_oyunu.akis import zamanlayici


def main() -> None:
    """2,4,6,8,10'da tik; 5,10'da tak yazar (yaklaşık zamanlar)."""
    tik = zamanlayici(2)
    tak = zamanlayici(5)
    # İki üreteci başlat; 10. saniyedeki iki son olayı da tamamla.
    next(tik)
    next(tak)
    baslangic = perf_counter()
    tik_sayisi, tak_sayisi = 0, 0
    while tik_sayisi < 5 or tak_sayisi < 2:
        if tik_sayisi < 5 and next(tik):
            print("tik")
            tik_sayisi += 1
        if tak_sayisi < 2 and next(tak):
            print("tak")
            tak_sayisi += 1
    print(f"Geçen süre: {perf_counter() - baslangic:.3f} saniye")


if __name__ == "__main__":
    main()
