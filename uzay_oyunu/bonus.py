"""Bir fonksiyonun başarılı çağrısının çalışma süresini ölçer."""
from time import perf_counter
from typing import Callable, Any
from uzay_oyunu.araclar import en_bagli_gezegenler
from uzay_oyunu.galaksi import galaksi_oku

def sure_olc(fonksiyon: Callable[..., Any]) -> Callable[..., Any]:
    """Argümanları aktaran ve sonucu koruyarak süreyi yazan sarmalayıcı döndürür."""
    def sarmalayici(*args: Any, **kwargs: Any) -> Any:
        """Fonksiyonu verilen argümanlarla çalıştırıp geçen süreyi yazdırır."""
        baslangic = perf_counter()
        sonuc = fonksiyon(*args, **kwargs)
        sure = perf_counter() - baslangic
        print(f"Çalışma süresi: {sure:.6f} saniye")
        return sonuc
    return sarmalayici

if __name__ == "__main__":
    en_bagli_gezegenler = sure_olc(en_bagli_gezegenler)
    print(en_bagli_gezegenler(galaksi_oku()))
