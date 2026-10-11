"""Varsayılan değiştirilebilir argüman tuzağı."""
from uzay_oyunu.yakit import yakit_ekle

def test_cagrilar_bagimsiz() -> None:
    """Depo verilmeden yapılan çağrılar aynı listeyi paylaşmamalıdır."""
    ilk = yakit_ekle(10)
    ikinci = yakit_ekle(20)
    assert ilk == [10]
    assert ikinci == [20]
    assert ilk is not ikinci

def test_verilen_depo_kullanilir() -> None:
    """Kullanıcının verdiği boş depo da aynı nesne olarak kullanılmalıdır."""
    depo = []
    assert yakit_ekle(5, depo) is depo
    assert depo == [5]
