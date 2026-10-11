"""Süre sarmalayıcısının argümanları ve sonucu koruması."""
from uzay_oyunu.bonus import sure_olc

def test_sarmalayici(capsys) -> None:
    """Konumlu ve adlı argümanlar asıl fonksiyona aktarılmalıdır."""
    def hesapla(a: int, b: int = 0) -> int:
        """İki sayıyı toplar."""
        return a + b
    assert sure_olc(hesapla)(3, b=4) == 7
    assert "Çalışma süresi:" in capsys.readouterr().out
