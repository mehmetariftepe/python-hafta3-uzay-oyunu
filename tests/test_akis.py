"""Hafta 4 görevlerinin örnek, sınır ve tembellik testleri."""
from itertools import islice, takewhile

import pytest

from uzay_oyunu.akis import fibonacci
from uzay_oyunu.akis import yakit_gostergesi
from uzay_oyunu.galaksi import galaksi_oku
from uzay_oyunu.oyun import travel


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


def test_yakit_ornek_ve_stopiteration() -> None:
    """Son değer sıfırdır; tekrar next StopIteration yükseltir."""
    g = yakit_gostergesi(100, 30)
    assert list(g) == [70, 40, 10, 0]
    with pytest.raises(StopIteration):
        next(g)
    assert list(yakit_gostergesi(0, 5)) == []
    assert list(yakit_gostergesi(5, 10)) == [0]


@pytest.mark.parametrize("yakit,tuketim", [(-1, 5), (10, 0), (10, -1)])
def test_gecersiz_yakit(yakit: int, tuketim: int) -> None:
    """Geçersiz tüketim sonsuz döngüye yol açmamalıdır."""
    with pytest.raises(ValueError):
        next(yakit_gostergesi(yakit, tuketim))


def test_oyun_yakit_bitince_kaybeder(monkeypatch, capsys) -> None:
    """Son sıfır değerinden sonra yeni hamle veya giriş alınmaz."""
    cevaplar = iter(["yanlış", "1"])
    monkeypatch.setattr("builtins.input", lambda mesaj: next(cevaplar))
    g = galaksi_oku()
    g["yakit"] = 10
    assert travel(g) == 1
    assert (g["konum"], g["yakit"]) == ("centauri", 0)
    assert "Yakıtın bitti, uzayda sürükleniyorsun…" in capsys.readouterr().out


def test_oyun_sifir_yakitla_giris_istemez(capsys) -> None:
    """Boş gösterge doğrudan kayıp mesajına yol açar."""
    g = galaksi_oku()
    g["yakit"] = 0
    assert travel(g) == 0
    assert "Yakıtın bitti" in capsys.readouterr().out
