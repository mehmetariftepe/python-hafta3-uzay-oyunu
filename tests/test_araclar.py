"""Closure sayacı ve lambda sıralaması."""
from uzay_oyunu.araclar import hamle_sayaci, en_bagli_gezegenler
from uzay_oyunu.galaksi import galaksi_oku
from uzay_oyunu.oyun import travel

def test_bagimsiz_sayaclar() -> None:
    """Sayaçlar kendi durumlarını tutmalı ve birbirini etkilememelidir."""
    birinci, ikinci = hamle_sayaci(), hamle_sayaci()
    assert [birinci(), birinci(), birinci()] == [1, 2, 3]
    assert ikinci() == 1
    assert birinci() == 4

def test_siralama() -> None:
    """Bu örneğin haritası PDF'teki sıralama sonucunu vermelidir."""
    assert en_bagli_gezegenler(galaksi_oku()) == ["sirius", "centauri", "dünya", "orion", "kara_delik"]

def test_esitlik_alfabetik() -> None:
    """Eşit bağlantı sayısında isim sırası kullanılmalıdır."""
    g = {"gezegenler": ["z", "a", "b"], "baglantilar": {"z": [], "a": [], "b": []}}
    assert en_bagli_gezegenler(g) == ["a", "b", "z"]
    assert g["gezegenler"] == ["z", "a", "b"]

def test_yolculuk_ve_gecersiz_secim(monkeypatch, capsys) -> None:
    """Geçersiz giriş hamle tüketmez; hedefe iki yolculukla gidilir."""
    cevaplar = iter(["yanlış", "2", "4"])
    monkeypatch.setattr("builtins.input", lambda mesaj: next(cevaplar))
    g = galaksi_oku()
    assert travel(g) == 2
    assert g["konum"] == "kara_delik" and g["yakit"] == 80
    assert "Oyunu 2 hamlede bitirdin!" in capsys.readouterr().out

def test_cikis_ve_yakitsizlik(monkeypatch) -> None:
    """Çıkışta veya yakıt yetmediğinde sayaç artırılmamalıdır."""
    monkeypatch.setattr("builtins.input", lambda mesaj: "q")
    assert travel(galaksi_oku()) == 0
    g = galaksi_oku()
    g["yakit"] = 0
    assert travel(g) == 0
