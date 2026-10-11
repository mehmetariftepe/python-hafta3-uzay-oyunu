"""Saf metin fonksiyonlarının beklenen davranışları."""
import pytest
from uzay_oyunu.oyun import envanter_metni, hedef_menusu

@pytest.mark.parametrize("durum, beklenen", [
    ((False, False, False), ""),
    ((True, False, True), "Sende: bol kredi, yetenekli bir pilot"),
    ((False, True, False), "Sende: hiperdrive"),
    ((True, True, True), "Sende: bol kredi, hiperdrive, yetenekli bir pilot"),
])
def test_envanter(durum: tuple[bool, bool, bool], beklenen: str, capsys) -> None:
    """Envanter sırası korunmalı ve fonksiyon çıktı basmamalıdır."""
    assert envanter_metni(*durum) == beklenen
    assert capsys.readouterr().out == ""

def test_hedef_menusu(capsys) -> None:
    """Menü sırası, numaraları ve saf oluşu korunmalıdır."""
    hedefler = ["centauri", "sirius"]
    assert hedef_menusu(hedefler) == "Nereye gitmek istersin?\n[1] centauri\n[2] sirius"
    assert hedefler == ["centauri", "sirius"]
    assert capsys.readouterr().out == ""

def test_bos_menu() -> None:
    """Boş listede yalnızca menü başlığı döndürülür."""
    assert hedef_menusu([]) == "Nereye gitmek istersin?"
