"""Hafta 5 dekoratörlerinin ve komutlarının davranış testleri."""
import pytest

from uzay_oyunu import dekoratorler
from uzay_oyunu.dekoratorler import sure_olc
from uzay_oyunu.dekoratorler import say
from uzay_oyunu.dekoratorler import log_cagri
from uzay_oyunu.dekorator_ornekleri import fibonacci_cagrilarini_goster


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


def test_say_arguman_sonuc_ve_bilgi() -> None:
    """Sayaç fonksiyonları birbirinden bağımsız saymalı ve wraps kullanmalıdır."""
    @say
    def topla(a: int, *, b: int = 0) -> int:
        """Sayaç örneği."""
        return a + b

    @say
    def diger() -> None:
        """Ayrı sayaç."""

    assert topla.cagri == 0
    assert topla(2, b=3) == 5
    assert topla(1) == 1
    assert (topla.cagri, diger.cagri) == (2, 0)
    assert (topla.__name__, topla.__doc__) == ("topla", "Sayaç örneği.")


def test_fibonacci_dekorator_sirasi() -> None:
    """Üç katman sırası gerçek çağrılarla beklenen sayıları vermelidir."""
    assert fibonacci_cagrilarini_goster() == (21891, 39, 21)


def test_log_argumanlar_sonuc_ve_bilgi(capsys: pytest.CaptureFixture[str]) -> None:
    """Log iki aşamada doğru biçimde yazılır; normal stdout boş kalır."""
    @log_cagri
    def yolculuk(hedef: str, *, hiz: int) -> str:
        """Log örneği."""
        return f"{hedef} hiz={hiz}"

    assert yolculuk("orion", hiz=3) == "orion hiz=3"
    cikti = capsys.readouterr()
    assert cikti.out == ""
    assert cikti.err == "-> yolculuk('orion', hiz=3)\n<- yolculuk = 'orion hiz=3'\n"
    assert (yolculuk.__name__, yolculuk.__doc__) == ("yolculuk", "Log örneği.")


def test_log_hedef_fonksiyonlarda(capsys: pytest.CaptureFixture[str]) -> None:
    """İstenen iki mevcut fonksiyon gerçekten dekore edilmiş olmalıdır."""
    from uzay_oyunu.galaksi import galaksi_kur
    from uzay_oyunu.oyun import hedef_menusu

    assert galaksi_kur(["a"], {"a": []}, "a")["konum"] == "a"
    assert hedef_menusu(["a"]) == "Nereye gitmek istersin?\n[1] a"
    cikti = capsys.readouterr()
    assert cikti.out == ""
    for ad in ("galaksi_kur", "hedef_menusu"):
        assert f"-> {ad}(" in cikti.err
        assert f"<- {ad} = " in cikti.err
    # Aynı süreçte ikinci çalıştırma da temiz önbellekle ölçülür.
    assert fibonacci_cagrilarini_goster() == (21891, 39, 21)
