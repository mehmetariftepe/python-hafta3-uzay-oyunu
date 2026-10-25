"""Hafta 5 dekoratörlerinin ve komutlarının davranış testleri."""
import pytest

from uzay_oyunu import dekoratorler
from uzay_oyunu.dekoratorler import sure_olc
from uzay_oyunu.dekoratorler import say
from uzay_oyunu.dekoratorler import log_cagri
from uzay_oyunu.dekoratorler import sinirla, yakit_harca
from uzay_oyunu.dekoratorler import hafiza
from functools import lru_cache
from uzay_oyunu.dekorator_ornekleri import fibonacci_cagrilarini_goster
from uzay_oyunu import komutlar


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
    # Aynı süreçte ikinci çalıştırma da temiz önbellekle ölçülür.
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


def test_yardim_komutu() -> None:
    """Yardım kayıtlı üç komutu açıklamalarıyla alfabetik listeler."""
    assert komutlar.yardim({}).splitlines() == [
        "envanter eşyalarını gösterir",
        "harita   gidebileceğin gezegenleri gösterir",
        "yardim   komutları listeler",
    ]


def test_envanter_komutu() -> None:
    """Komut durumdaki güncel eşyaları okur; boş envanteri de açıklar."""
    durum = {"credits": True, "engines": True, "copilot": False}
    assert komutlar.envanter(durum) == "Sende: bol kredi, hiperdrive"
    assert durum == {"credits": True, "engines": True, "copilot": False}
    assert komutlar.envanter(dict.fromkeys(durum, False)) == "Envanter boş."


def test_harita_komutu() -> None:
    """Harita yalnızca mevcut konumun çıkışlarını özgün sırayla döndürür."""
    durum = {"konum": "a", "baglantilar": {"a": ["c", "b"], "b": []}}
    assert komutlar.harita(durum) == "c, b"
    durum["konum"] = "b"
    assert komutlar.harita(durum) == "Gidilebilecek gezegen yok."


def test_komut_kaydi_kimligi_ve_cakisma(monkeypatch: pytest.MonkeyPatch) -> None:
    """Dekoratör aynı fonksiyonu döndürür; ikinci kayıt ilki üzerine yazamaz."""
    monkeypatch.setattr(komutlar, "KOMUTLAR", {})

    def ornek(durum: komutlar.Durum) -> str:
        """Özgün komut açıklaması."""
        return "örnek"

    assert komutlar.komut("ornek", "açıklama")(ornek) is ornek
    assert komutlar.KOMUTLAR["ornek"] == (ornek, "açıklama")
    assert ornek.__doc__ == "Özgün komut açıklaması."
    with pytest.raises(ValueError, match="zaten kayıtlı"):
        @komutlar.komut("ornek")
        def ikinci(durum: komutlar.Durum) -> str:
            """Tanım tamamlanmadan reddedilecek komut."""
            return "ikinci"
    assert komutlar.KOMUTLAR["ornek"][0] is ornek


def test_travel_komutlari_hamle_ve_yakit_tuketmez(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Komutlar aynı menüye döner; güncel envanterle dört yolculuk yapılır."""
    from uzay_oyunu.galaksi import galaksi_oku
    from uzay_oyunu.oyun import travel
    cevaplar = iter(["harita", "envanter", "yardim", "1", "envanter",
                     "3", "envanter", "1", "4"])
    monkeypatch.setattr("builtins.input", lambda mesaj: next(cevaplar))
    galaksi = galaksi_oku()
    assert travel(galaksi) == 4
    assert (galaksi["konum"], galaksi["yakit"]) == ("kara_delik", 60)
    cikti = capsys.readouterr().out
    assert "centauri, sirius" in cikti
    assert "envanter eşyalarını gösterir" in cikti
    assert "Sende: bol kredi, hiperdrive, yetenekli bir pilot" in cikti
    assert cikti.count("Nereye gitmek istersin?") == 9


@pytest.mark.parametrize("miktar,beklenen", [(0, 100), (30, 70), (100, 0)])
def test_yakit_harca_sinirlar(miktar: int, beklenen: int) -> None:
    """Her iki sınır dahildir; normal bir ara değer de kabul edilir."""
    assert yakit_harca(miktar) == beklenen
    assert yakit_harca(miktar=miktar) == beklenen


@pytest.mark.parametrize("miktar", [-1, 101, 150])
def test_yakit_harca_aralik_disi(miktar: int) -> None:
    """Alt ve üst sınır dışındaki değerler anlamlı hata üretir."""
    with pytest.raises(ValueError) as hata:
        yakit_harca(miktar)
    assert str(hata.value) == f"yakit_harca: {miktar} değeri 0-100 aralığında değil"


def test_sinirla_arguman_aktarimi_ve_bilgi() -> None:
    """Öteki argümanlar ve fonksiyon bilgisi sarmalayıcıdan korunarak geçer."""
    @sinirla(0, 100)
    def hesapla(miktar: int = 30, *, carpan: int = 1) -> int:
        """Sınır örneği."""
        return miktar * carpan

    assert hesapla(miktar=20, carpan=3) == 60
    assert hesapla() == 30
    assert (hesapla.__name__, hesapla.__doc__) == ("hesapla", "Sınır örneği.")
    with pytest.raises(ValueError, match="Alt sınır"):
        sinirla(100, 0)
    with pytest.raises(TypeError):
        yakit_harca()


def test_hafiza_lru_cache_ile_ayni_sonuclar() -> None:
    """Sınırsız iki önbellekte Fibonacci sonuçları ve hesap sayısı aynıdır."""
    @hafiza()
    @say
    def fib(n: int) -> int:
        """Closure önbellekli Fibonacci."""
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    @lru_cache(maxsize=None)
    @say
    def diger(n: int) -> int:
        """Standart önbellekli Fibonacci."""
        return n if n < 2 else diger(n - 1) + diger(n - 2)

    assert fib(20) == diger(20) == 6765
    assert fib.__wrapped__.cagri == diger.__wrapped__.cagri == 21
    assert fib(20) == diger(20)
    assert fib.__wrapped__.cagri == diger.__wrapped__.cagri == 21
    assert (fib.__name__, fib.__doc__) == ("fib", "Closure önbellekli Fibonacci.")


def test_hafiza_fifo_lru_farki() -> None:
    """İsabet eski kaydı yenilemez; FIFO ile LRU atılma farkını gösterir."""
    @hafiza(maxsize=2)
    @say
    def fifo(n: int) -> int:
        """FIFO örneği."""
        return n * n

    @lru_cache(maxsize=2)
    @say
    def lru(n: int) -> int:
        """LRU örneği."""
        return n * n

    for n in (1, 2, 1, 3, 1):
        assert fifo(n) == lru(n) == n * n
    assert fifo.__wrapped__.cagri == 4  # 3 eklenince en eski eklenen 1 silinir.
    assert lru.__wrapped__.cagri == 3  # 1 isabetle güncellendiği için 2 silinir.


def test_hafiza_adli_argumanlar_ve_sifir() -> None:
    """Adlı argümanlar anahtara dahildir; maxsize=0 saklamayı kapatır."""
    @hafiza()
    @say
    def carp(a: int, *, b: int) -> int:
        """Adlı argüman örneği."""
        return a * b

    assert carp(2, b=3) == carp(2, b=3) == 6
    assert carp(2, b=4) == 8
    assert carp.__wrapped__.cagri == 2

    @hafiza(maxsize=0)
    @say
    def kapali(n: int) -> int:
        """Önbelleksiz çağrı."""
        return n

    assert kapali(2) == kapali(2) == 2
    assert kapali.__wrapped__.cagri == 2
    with pytest.raises(ValueError):
        hafiza(-1)


def test_hafiza_hatalari_saklamaz() -> None:
    """İstisna veren çağrı bir sonuç olarak önbelleğe yazılmamalıdır."""
    @hafiza(maxsize=1)
    @say
    def hata(n: int) -> int:
        """Her çağrıda hata verir."""
        raise ValueError("örnek hata")

    for _ in range(2):
        with pytest.raises(ValueError, match="örnek hata"):
            hata(1)
    assert hata.__wrapped__.cagri == 2
