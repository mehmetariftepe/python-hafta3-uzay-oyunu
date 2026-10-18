"""Galaksi sorularının fonksiyonel ve liste üreteçli karşılıkları."""
from functools import partial, reduce
from typing import Any


def buyuk_adlar_map(galaksi: dict[str, Any]) -> list[str]:
    """Gezegen adlarını map ile büyük harfe dönüştürür."""
    return list(map(str.upper, galaksi["gezegenler"]))


def buyuk_adlar_liste(galaksi: dict[str, Any]) -> list[str]:
    """Gezegen adlarını liste üreteci ile büyük harfe dönüştürür."""
    return [ad.upper() for ad in galaksi["gezegenler"]]


def en_az_iki_filter(galaksi: dict[str, Any]) -> list[str]:
    """En az iki çıkış bağlantısı olan gezegenleri filter ile seçer."""
    return list(filter(lambda ad: len(galaksi["baglantilar"][ad]) >= 2,
                       galaksi["gezegenler"]))


def en_az_iki_liste(galaksi: dict[str, Any]) -> list[str]:
    """Aynı seçimi liste üreteciyle, kaynak sırasını koruyarak yapar."""
    return [ad for ad in galaksi["gezegenler"] if len(galaksi["baglantilar"][ad]) >= 2]


def toplam_baglanti_reduce(galaksi: dict[str, Any]) -> int:
    """Bağlantı uzunluklarını reduce ile sıfırdan başlayarak toplar."""
    return reduce(lambda toplam, hedefler: toplam + len(hedefler),
                  galaksi["baglantilar"].values(), 0)


def toplam_baglanti_sum(galaksi: dict[str, Any]) -> int:
    """Bağlantı uzunluklarını sum ile toplar."""
    return sum(len(hedefler) for hedefler in galaksi["baglantilar"].values())


# Koşul ve işlem bir arada görüldüğü için liste üreteci ve sum daha okunaklı.
# str.upper gibi hazır bir fonksiyon varsa map de kısa ve anlaşılır.
def yolculuk(mesafe: float, hiz: float = 1) -> float:
    """Sabit hızla yolculuğun süresini mesafe / hız olarak döndürür."""
    if mesafe < 0 or hiz <= 0:
        raise ValueError("Mesafe negatif, hız sıfır veya negatif olamaz.")
    return mesafe / hiz


# Hafta 3'te hız parametreli yolculuk yoktu; travel oyun döngüsüdür.
hizli_yolculuk = partial(yolculuk, hiz=3)
hizli_yolculuk.__doc__ = "Hızı 3 olarak önceden bağlanmış yolculuk süresi hesabı."
