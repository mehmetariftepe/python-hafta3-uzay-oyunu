"""Hafta 4 görevlerinin örnek, sınır ve tembellik testleri."""
from itertools import islice, takewhile
from pathlib import Path
from collections.abc import Iterator

import pytest

from uzay_oyunu.akis import fibonacci
from uzay_oyunu.akis import yakit_gostergesi
from uzay_oyunu.galaksi import galaksi_oku
from uzay_oyunu.oyun import travel
from uzay_oyunu.akis import satirlari_oku, ayristir, uzun_yolculuklar
from uzay_oyunu.akis import rota_sayaci, rota_sayaci_onbelleksiz
from functools import partial
from uzay_oyunu import istatistik
from uzay_oyunu import akis


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


def test_rota_tam_adim_ve_onbellek() -> None:
    """Küçük döngülü haritada tam adım sayısı ve cache isabeti doğrulanır."""
    baglantilar = {"a": ["a", "b"], "b": []}
    say = rota_sayaci(baglantilar)
    assert say("a", 0) == 1
    assert say("b", 1) == 0
    assert say("a", 3) == 2
    once = say.cache_info()
    assert say("a", 3) == 2
    assert say.cache_info().hits == once.hits + 1
    assert say.cache_info().misses == once.misses


def test_rota_kendi_galaksimiz() -> None:
    """Bağımsız, ileri yönlü sayımla gerçek haritanın sonuçlarını doğrular."""
    baglantilar = galaksi_oku()["baglantilar"]
    say = rota_sayaci(baglantilar)
    dagilim = {g: int(g == "dünya") for g in baglantilar}
    for adim in range(41):
        assert say("dünya", adim) == sum(dagilim.values())
        sonraki = dict.fromkeys(baglantilar, 0)
        for kaynak, adet in dagilim.items():
            for hedef in baglantilar[kaynak]:
                sonraki[hedef] += adet
        dagilim = sonraki
    yavas = rota_sayaci_onbelleksiz(baglantilar)
    for adim in range(8):
        assert say("dünya", adim) == yavas("dünya", adim)


def test_rota_sinirlar_ve_bagimsiz_onbellek() -> None:
    """Bilinmeyen gezegen, negatif adım ve farklı haritalar sınanır."""
    for kur in (rota_sayaci, rota_sayaci_onbelleksiz):
        say = kur({"a": []})
        with pytest.raises(ValueError):
            say("a", -1)
        with pytest.raises(ValueError):
            say("yok", 0)
    ilk = rota_sayaci({"a": []})
    ikinci = rota_sayaci({"a": ["a"]})
    assert ilk("a", 2) == 0
    assert ikinci("a", 2) == 1


@pytest.mark.parametrize("yakit,tuketim", [(-1, 5), (10, 0), (10, -1)])
def test_gecersiz_yakit(yakit: int, tuketim: int) -> None:
    """Geçersiz tüketim sonsuz döngüye yol açmamalıdır."""
    with pytest.raises(ValueError):
        next(yakit_gostergesi(yakit, tuketim))


def test_oyun_yakit_bitince_kaybeder(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Son sıfır değerinden sonra yeni hamle veya giriş alınmaz."""
    cevaplar = iter(["yanlış", "1"])
    monkeypatch.setattr("builtins.input", lambda mesaj: next(cevaplar))
    g = galaksi_oku()
    g["yakit"] = 10
    assert travel(g) == 1
    assert (g["konum"], g["yakit"]) == ("centauri", 0)
    assert "Yakıtın bitti, uzayda sürükleniyorsun…" in capsys.readouterr().out


def test_oyun_sifir_yakitla_giris_istemez(capsys: pytest.CaptureFixture[str]) -> None:
    """Boş gösterge doğrudan kayıp mesajına yol açar."""
    g = galaksi_oku()
    g["yakit"] = 0
    assert travel(g) == 0
    assert "Yakıtın bitti" in capsys.readouterr().out


def test_seyir_dosyasi() -> None:
    """PDF örneklerinin toplamı ve hedef sırası korunur."""
    yol = Path(__file__).resolve().parents[1] / "veri" / "seyir.txt"
    assert sum(y for _, _, y in ayristir(satirlari_oku(yol))) == 88
    kayitlar = ayristir(satirlari_oku(yol))
    assert [h for _, h, _ in uzun_yolculuklar(kayitlar, 10)] == [
        "sirius", "centauri", "orion", "kara_delik"
    ]


def test_bos_satir_yorum_ve_esik(tmp_path: Path) -> None:
    """Girintili yorumlar atlanır; eşiğe eşit kayıt alınmaz."""
    yol = tmp_path / "seyir.txt"
    yol.write_text("\n  # yorum\n a -> b 10\n b -> c 11\n", encoding="utf-8")
    assert list(uzun_yolculuklar(ayristir(satirlari_oku(yol)), 10)) == [("b", "c", 11)]


def test_boru_hatti_tembeldir() -> None:
    """İlk sonuç istenirken kaynağın ikinci satırı okunmamalıdır."""
    def kaynak() -> Iterator[str]:
        """Erken okuma olursa hata veren tek geçişli kaynak."""
        yield "a -> b 12"
        raise AssertionError("Gereğinden erken okundu")
    hat = uzun_yolculuklar(ayristir(kaynak()), 10)
    assert next(hat) == ("a", "b", 12)
    with pytest.raises(AssertionError, match="erken"):
        next(hat)


def test_dosya_okuma_da_tembeldir(tmp_path: Path) -> None:
    """Dosya üreteç kurulurken değil ilk next çağrısında açılır."""
    g = satirlari_oku(tmp_path / "yok.txt")
    with pytest.raises(FileNotFoundError):
        next(g)


def test_istatistik_iki_yazim() -> None:
    """Her sorunun iki çözümü kendi haritamızdaki beklenen sonucu verir."""
    g = galaksi_oku()
    assert istatistik.buyuk_adlar_map(g) == istatistik.buyuk_adlar_liste(g) == [
        "DÜNYA", "CENTAURI", "SIRIUS", "ORION", "KARA_DELIK"
    ]
    assert istatistik.en_az_iki_filter(g) == istatistik.en_az_iki_liste(g) == [
        "dünya", "centauri", "sirius"
    ]
    assert istatistik.toplam_baglanti_reduce(g) == istatistik.toplam_baglanti_sum(g) == 10


def test_istatistik_bos_galaksi() -> None:
    """Başlangıç değeri sayesinde reduce boş haritada da sıfır verir."""
    g = {"gezegenler": [], "baglantilar": {}}
    assert istatistik.buyuk_adlar_map(g) == istatistik.buyuk_adlar_liste(g) == []
    assert istatistik.en_az_iki_filter(g) == istatistik.en_az_iki_liste(g) == []
    assert istatistik.toplam_baglanti_reduce(g) == istatistik.toplam_baglanti_sum(g) == 0


def test_partial_yolculuk() -> None:
    """partial özgün fonksiyonu değiştirmeden hız parametresini bağlar."""
    assert isinstance(istatistik.hizli_yolculuk, partial)
    assert istatistik.hizli_yolculuk.func is istatistik.yolculuk
    assert istatistik.hizli_yolculuk.keywords == {"hiz": 3}
    assert istatistik.hizli_yolculuk(12) == 4
    assert istatistik.yolculuk(12) == 12


def test_zamanlayici_sahte_saat(monkeypatch: pytest.MonkeyPatch) -> None:
    """Gerçekte beklemeden aralık sınırlarında sinyal üretilmesi sınanır."""
    saat = [0.0]
    monkeypatch.setattr(akis, "perf_counter", lambda: saat[0])
    g = akis.zamanlayici(2)
    assert next(g) is False
    saat[0] = 1.99
    assert next(g) is False
    saat[0] = 2.0
    assert next(g) is True
    assert next(g) is False
    saat[0] = 4.0
    assert next(g) is True
    with pytest.raises(ValueError):
        next(akis.zamanlayici(0))
