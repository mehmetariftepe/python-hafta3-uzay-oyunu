"""Hafta 4 görevlerinin örnek, sınır ve tembellik testleri."""
from itertools import islice, takewhile

import pytest

from uzay_oyunu.akis import fibonacci


def test_fibonacci_next() -> None:
    """next ile ilk üç değer okunur."""
    g = fibonacci()
    assert (next(g), next(g), next(g)) == (0, 1, 1)


def test_fibonacci_islice_takewhile() -> None:
    """Sonsuz üreteç sınırlı sayıda veya koşula kadar okunur."""
    beklenen = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    assert list(islice(fibonacci(), 12)) == beklenen
    assert list(takewhile(lambda sayi: sayi < 100, fibonacci())) == beklenen


def test_fibonacci_tek_kullanimlik() -> None:
    """Aynı üreteç başa dönmez; kaldığı yerden devam eder."""
    g = fibonacci()
    assert list(islice(g, 3)) == [0, 1, 1]
    assert list(islice(g, 3)) == [2, 3, 5]
