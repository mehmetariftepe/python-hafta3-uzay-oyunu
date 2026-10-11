"""Saf metin fonksiyonları ve basit uzay oyunu akışı."""
from typing import Any
from uzay_oyunu.araclar import hamle_sayaci

def envanter_metni(credits: bool, engines: bool, copilot: bool) -> str:
    """Mevcut eşyaları tek metinde döndürür; boş envanterde boş metin verir."""
    esyalar = []
    if credits:
        esyalar.append("bol kredi")
    if engines:
        esyalar.append("hiperdrive")
    if copilot:
        esyalar.append("yetenekli bir pilot")
    if not esyalar:
        return ""
    return "Sende: " + ", ".join(esyalar)

def hedef_menusu(hedefler: list[str]) -> str:
    """Hedeflerin sırasını değiştirmeden birden başlayan menü döndürür."""
    satirlar = ["Nereye gitmek istersin?"]
    for sira, hedef in enumerate(hedefler, start=1):
        satirlar.append(f"[{sira}] {hedef}")
    return "\n".join(satirlar)

def travel(galaksi: dict[str, Any]) -> int:
    """Veri dosyasındaki bağlantılarla yolculuk yapar ve hamle sayısını döndürür."""
    sayac = hamle_sayaci()
    hamle = 0
    credits, engines, copilot = True, False, False
    while galaksi["konum"] != "kara_delik" and galaksi["yakit"] >= 10:
        planet = galaksi["konum"]
        print("Konum:", planet)
        print(envanter_metni(credits, engines, copilot))
        hedefler = galaksi["baglantilar"][planet]
        if not hedefler:
            break
        print(hedef_menusu(hedefler))
        secim = input("Seçim (çıkış: q): ")
        if secim == "q":
            break
        if not secim.isdigit() or not 1 <= int(secim) <= len(hedefler):
            print("Geçersiz seçim.")
            continue
        galaksi["konum"] = hedefler[int(secim) - 1]
        galaksi["yakit"] -= 10
        hamle = sayac()
        if galaksi["konum"] == "centauri":
            engines = True
        if galaksi["konum"] == "orion":
            copilot = True
    if galaksi["konum"] == "kara_delik":
        print("Kara deliğe ulaştın!")
    print(f"Oyunu {hamle} hamlede bitirdin!")
    return hamle

if __name__ == "__main__":
    from uzay_oyunu.galaksi import galaksi_oku
    travel(galaksi_oku())
