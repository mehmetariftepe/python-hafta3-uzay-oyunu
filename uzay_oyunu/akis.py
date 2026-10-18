"""Hafta 4: tembel üreteçler ve önbellekli rota hesabı."""
from collections.abc import Iterator


def fibonacci() -> Iterator[int]:
    """Sıfırdan başlayan Fibonacci sayılarını sonsuza kadar üretir."""
    onceki, simdiki = 0, 1
    while True:
        yield onceki
        onceki, simdiki = simdiki, onceki + simdiki


def yakit_gostergesi(yakit: int, tuketim: int) -> Iterator[int]:
    """Her adımda tüketir; sıfırı bir kez üretir, sonra sonlanır."""
    if yakit < 0 or tuketim <= 0:
        raise ValueError("Yakıt negatif, tüketim sıfır veya negatif olamaz.")
    while yakit > 0:
        yakit = max(0, yakit - tuketim)
        yield yakit
