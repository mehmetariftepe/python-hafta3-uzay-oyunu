"""Hafta 5 dekoratörlerini gerçek hesaplar üzerinde gösterir."""
from uzay_oyunu.akis import rota_sayaci_onbelleksiz
from functools import lru_cache
from uzay_oyunu.dekoratorler import sure_olc, say
from uzay_oyunu.galaksi import galaksi_oku


def rota_suresini_goster() -> int:
    """Hafta 4'ün önbelleksiz sayacını dekore edip 20 adımı ölçer."""
    sayac = rota_sayaci_onbelleksiz(galaksi_oku()["baglantilar"])
    olculen = sure_olc(sayac)
    sonuc = olculen("dünya", adim=20)
    print(f"20 adımlık rota sayısı: {sonuc}")
    return sonuc


@say
def fib_yalniz_say(n: int) -> int:
    """Önbelleksiz özyinelemeli Fibonacci; bütün çağrılar sayılır."""
    if n < 0:
        raise ValueError("n negatif olamaz.")
    if n < 2:
        return n
    return fib_yalniz_say(n - 1) + fib_yalniz_say(n - 2)


@say
@lru_cache(maxsize=None)
def fib_say_ustte(n: int) -> int:
    """Dış sayaç, önbelleğe isabet eden çağrıları da sayar."""
    if n < 0:
        raise ValueError("n negatif olamaz.")
    if n < 2:
        return n
    return fib_say_ustte(n - 1) + fib_say_ustte(n - 2)


@lru_cache(maxsize=None)
@say
def fib_cache_ustte(n: int) -> int:
    """Dış önbellek isabetlerinde içteki sayaç çalışmaz."""
    if n < 0:
        raise ValueError("n negatif olamaz.")
    if n < 2:
        return n
    return fib_cache_ustte(n - 1) + fib_cache_ustte(n - 2)


def fibonacci_cagrilarini_goster() -> tuple[int, int, int]:
    """Temiz önbellek ve sıfır sayaçlarla üç fib(20) hesabını karşılaştırır."""
    fib_yalniz_say.cagri = 0
    fib_say_ustte.cagri = 0
    fib_say_ustte.__wrapped__.cache_clear()
    fib_cache_ustte.cache_clear()
    fib_cache_ustte.__wrapped__.cagri = 0
    sonuclar = (fib_yalniz_say(20), fib_say_ustte(20), fib_cache_ustte(20))
    assert sonuclar == (6765, 6765, 6765)
    cagrilar = (fib_yalniz_say.cagri, fib_say_ustte.cagri,
                fib_cache_ustte.__wrapped__.cagri)
    for ad, adet in zip(("Yalnızca @say", "@say üstte", "@lru_cache üstte"), cagrilar):
        print(f"{ad}: {adet}")
    return cagrilar


if __name__ == "__main__":
    rota_suresini_goster()
    fibonacci_cagrilarini_goster()
