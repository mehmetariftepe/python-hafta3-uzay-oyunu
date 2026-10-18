"""Aynı galakside soğuk önbellekle, 20 adımlık rota hesabını karşılaştırır."""
import platform
from time import perf_counter

from uzay_oyunu.akis import rota_sayaci, rota_sayaci_onbelleksiz
from uzay_oyunu.galaksi import galaksi_oku


def main() -> None:
    """Önce önbelleksiz, sonra boş önbellekli hesabı ölçer ve doğrular."""
    galaksi = galaksi_oku()
    yavas = rota_sayaci_onbelleksiz(galaksi["baglantilar"])
    hizli = rota_sayaci(galaksi["baglantilar"])
    baslangic = perf_counter()
    sonuc = yavas("dünya", 20)
    yavas_sure = perf_counter() - baslangic
    baslangic = perf_counter()
    hizli_sonuc = hizli("dünya", 20)
    hizli_sure = perf_counter() - baslangic
    assert sonuc == hizli_sonuc
    print(f"Python {platform.python_version()} / {platform.system()}")
    print(f"20 adım rota sayısı: {sonuc}")
    print(f"Önbelleksiz: {yavas_sure:.9f} saniye")
    print(f"Önbellekli (soğuk): {hizli_sure:.9f} saniye")
    print(hizli.cache_info())
    print("3, 10, 40 adım:", tuple(hizli("dünya", n) for n in (3, 10, 40)))


if __name__ == "__main__":
    main()
