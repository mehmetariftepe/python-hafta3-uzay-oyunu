"""Görev kaydının açılım ve öncelik davranışları."""
import inspect
from uzay_oyunu.kayit import gorev_kaydi

def test_liste_ve_sozluk_acilimi() -> None:
    """Doğrudan çağrı ile liste/sözlük açılımları aynı sonucu vermelidir."""
    adimlar = ["Kredi kazan", "Pilot bul", "Hiperdrive al"]
    ekler = {"oncelik": "yüksek", "sorumlu": "Ayşe"}
    beklenen = "[YÜKSEK] Kara deliğe atla\n  1. Kredi kazan\n  2. Pilot bul\n  3. Hiperdrive al\n  sorumlu: Ayşe"
    assert gorev_kaydi("Kara deliğe atla", *adimlar, **ekler) == beklenen
    assert gorev_kaydi("Kara deliğe atla", "Kredi kazan", "Pilot bul", "Hiperdrive al", oncelik="yüksek", sorumlu="Ayşe") == beklenen

def test_oncelik_yalnizca_adli() -> None:
    """Öncelik parametresi keyword-only olmalıdır."""
    assert inspect.signature(gorev_kaydi).parameters["oncelik"].kind == inspect.Parameter.KEYWORD_ONLY
    assert gorev_kaydi("Keşfet") == "[NORMAL] Keşfet"
