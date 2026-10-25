"""Dekoratörle kayıt edilen, oyun durumunu okuyan terminal komutları."""
from collections.abc import Callable
from typing import Any

Durum = dict[str, Any]
Komut = Callable[[Durum], str]
KOMUTLAR: dict[str, tuple[Komut, str]] = {}


def komut(ad: str, aciklama: str = "") -> Callable[[Komut], Komut]:
    """Tanım anında kayıt yapar; sarmalamadan aynı fonksiyonu döndürür."""
    def kaydet(fonksiyon: Komut) -> Komut:
        """İsim çakışmasını reddeder; özgün fonksiyonun kimliğini korur."""
        if ad in KOMUTLAR:
            raise ValueError(f"Komut zaten kayıtlı: {ad}")
        KOMUTLAR[ad] = (fonksiyon, aciklama)
        return fonksiyon
    return kaydet


@komut("yardim", "komutları listeler")
def yardim(durum: Durum) -> str:
    """Kayıtlı komutları ve açıklamalarını alfabetik sıralar."""
    return "\n".join(f"{ad:<8} {aciklama}" for ad, (_, aciklama) in sorted(KOMUTLAR.items()))


@komut("envanter", "eşyalarını gösterir")
def envanter(durum: Durum) -> str:
    """Mevcut kredi, motor ve pilot bilgisini var olan metinle gösterir."""
    # Yerel import, oyun -> komutlar -> oyun döngüsünü tanım anında önler.
    from uzay_oyunu.oyun import envanter_metni
    return envanter_metni(durum["credits"], durum["engines"], durum["copilot"]) or "Envanter boş."


@komut("harita", "gidebileceğin gezegenleri gösterir")
def harita(durum: Durum) -> str:
    """Geçerli konumdan gidilebilen gezegenleri bağlantı sırasıyla gösterir."""
    return ", ".join(durum["baglantilar"][durum["konum"]]) or "Gidilebilecek gezegen yok."
