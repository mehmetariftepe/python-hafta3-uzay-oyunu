"""Hafta 4: tembel üreteçler ve önbellekli rota hesabı."""
from collections.abc import Iterator


def fibonacci() -> Iterator[int]:
    """Sıfırdan başlayan Fibonacci sayılarını sonsuza kadar üretir."""
    onceki, simdiki = 0, 1
    while True:
        yield onceki
        onceki, simdiki = simdiki, onceki + simdiki
