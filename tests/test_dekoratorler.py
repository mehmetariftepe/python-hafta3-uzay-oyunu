"""Hafta 5 dekoratörlerinin ve komutlarının davranış testleri."""
import pytest

from uzay_oyunu import dekoratorler
from uzay_oyunu.dekoratorler import sure_olc


def test_sure_olc_sonucu_ve_bicimi_korur(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Sahte saatle biçimi doğrular; sonuç aynı nesne olarak dönmelidir."""
    saat = iter([1.0, 1.0123])
    monkeypatch.setattr(dekoratorler, "perf_counter", lambda: next(saat))
    sonuc = []

    @sure_olc
    def hesapla() -> list[int]:
        """Özgün listeyi döndürür."""
        return sonuc

    assert hesapla() is sonuc
    assert capsys.readouterr().out == "hesapla: 0.0123 sn\n"


def test_sure_olc_adli_argumanlar() -> None:
    """Konumsal ve keyword-only argümanlar eksiksiz aktarılmalıdır."""
    @sure_olc
    def topla(a: int, *, b: int) -> int:
        """İki sayıyı toplar."""
        return a + b

    assert topla(3, b=4) == 7


def test_sure_olc_fonksiyon_bilgisi() -> None:
    """wraps ad, belge ve özgün fonksiyon bağlantısını korumalıdır."""
    def ornek() -> int:
        """Korunacak açıklama."""
        return 5

    dekore = sure_olc(ornek)
    assert dekore.__name__ == "ornek"
    assert dekore.__doc__ == "Korunacak açıklama."
    assert dekore.__wrapped__ is ornek
