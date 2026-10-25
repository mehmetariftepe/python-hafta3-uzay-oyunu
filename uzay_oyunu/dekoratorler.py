"""Hafta 5: sonuçları ve fonksiyon bilgisini koruyan dekoratörler."""
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar
import sys

P = ParamSpec("P")
R = TypeVar("R")


def sure_olc(fonksiyon: Callable[P, R]) -> Callable[P, R]:
    """Çağrı süresini saniye olarak yazdırır; sonucu veya hatayı korur."""
    @wraps(fonksiyon)
    def sarmalayici(*args: P.args, **kwargs: P.kwargs) -> R:
        """Argümanları aktarır ve hata oluşsa bile geçen süreyi bildirir."""
        baslangic = perf_counter()
        try:
            return fonksiyon(*args, **kwargs)
        finally:
            print(f"{fonksiyon.__name__}: {perf_counter() - baslangic:.4f} sn")
    return sarmalayici


def say(fonksiyon: Callable[P, R]) -> Callable[P, R]:
    """Sarmalayıcının cagri niteliğinde kendisine gelen çağrıları sayar."""
    @wraps(fonksiyon)
    def sarmalayici(*args: P.args, **kwargs: P.kwargs) -> R:
        """Önbellek dahil iç katmana geçmeden önce sayacı artırır."""
        sarmalayici.cagri += 1
        return fonksiyon(*args, **kwargs)
    sarmalayici.cagri = 0
    return sarmalayici


def log_cagri(fonksiyon: Callable[P, R]) -> Callable[P, R]:
    """Adı, argümanları ve sonucu stderr'e yazar; normal çıktıyı korur."""
    @wraps(fonksiyon)
    def sarmalayici(*args: P.args, **kwargs: P.kwargs) -> R:
        """Çağrı öncesi ve başarılı dönüş sonrası repr biçiminde kayıt basar."""
        argumanlar = [repr(arg) for arg in args]
        argumanlar.extend(f"{ad}={deger!r}" for ad, deger in kwargs.items())
        print(f"-> {fonksiyon.__name__}({', '.join(argumanlar)})", file=sys.stderr)
        sonuc = fonksiyon(*args, **kwargs)
        print(f"<- {fonksiyon.__name__} = {sonuc!r}", file=sys.stderr)
        return sonuc
    return sarmalayici
