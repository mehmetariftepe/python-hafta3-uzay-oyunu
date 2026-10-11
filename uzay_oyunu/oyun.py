"""Envanter ve menü metinleri; oyun akışı sonraki görevlerde eklenir."""

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
