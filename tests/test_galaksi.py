"""Galaksi başlangıcı, varsayılan yakıt ve JSON verisi."""
import pytest
from uzay_oyunu.galaksi import galaksi_kur, galaksi_oku

def test_gecersiz_baslangic() -> None:
    """Listede olmayan başlangıç reddedilmelidir."""
    with pytest.raises(ValueError):
        galaksi_kur(["mars"], {"mars": []}, "dünya")

def test_varsayilan_yakit() -> None:
    """Yakıt verilmediğinde 50, sıfır verildiğinde sıfır korunmalıdır."""
    assert galaksi_kur(["mars"], {"mars": []}, "mars")["yakit"] == 50
    assert galaksi_kur(["mars"], {"mars": []}, "mars", yakit=0)["yakit"] == 0

def test_json_ve_sira() -> None:
    """Bu örneğin JSON bağlantı sırası değişmeden okunmalıdır."""
    g = galaksi_oku()
    assert (g["konum"], g["yakit"]) == ("dünya", 100)
    assert g["baglantilar"]["dünya"] == ["centauri", "sirius"]
