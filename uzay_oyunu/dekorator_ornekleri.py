"""Hafta 5 dekoratörlerini gerçek hesaplar üzerinde gösterir."""
from uzay_oyunu.akis import rota_sayaci_onbelleksiz
from uzay_oyunu.dekoratorler import sure_olc
from uzay_oyunu.galaksi import galaksi_oku


def rota_suresini_goster() -> int:
    """Hafta 4'ün önbelleksiz sayacını dekore edip 20 adımı ölçer."""
    sayac = rota_sayaci_onbelleksiz(galaksi_oku()["baglantilar"])
    olculen = sure_olc(sayac)
    sonuc = olculen("dünya", adim=20)
    print(f"20 adımlık rota sayısı: {sonuc}")
    return sonuc


if __name__ == "__main__":
    rota_suresini_goster()
