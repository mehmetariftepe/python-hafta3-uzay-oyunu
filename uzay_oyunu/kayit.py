"""Esnek parametrelerle görev kaydı metni oluşturur."""

def gorev_kaydi(baslik: str, *adimlar: str, oncelik: str = "normal", **ekler: str) -> str:
    """Başlık, adımlar ve ek bilgileri düzenler; öncelik yalnızca adıyla verilir."""
    satirlar = [f"[{oncelik.upper()}] {baslik}"]
    for sira, adim in enumerate(adimlar, start=1):
        satirlar.append(f"  {sira}. {adim}")
    for anahtar, deger in ekler.items():
        satirlar.append(f"  {anahtar}: {deger}")
    return "\n".join(satirlar)

if __name__ == "__main__":
    print(gorev_kaydi("Kara deliğe atla", "Kredi kazan", "Pilot bul", "Hiperdrive al",
                     oncelik="yüksek", sorumlu="Ayşe"))
    print()
    adim_listesi = ["Kredi kazan", "Pilot bul", "Hiperdrive al"]
    ek_bilgiler = {"oncelik": "yüksek", "sorumlu": "Ayşe"}
    print(gorev_kaydi("Kara deliğe atla", *adim_listesi, **ek_bilgiler))
