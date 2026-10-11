"""Yakıt deposunda varsayılan liste tuzağını önler."""
def yakit_ekle(miktar: int, depo: list[int] | None = None) -> list[int]:
    """Depo verilmezse her çağrı için yeni liste oluşturup miktarı ekler."""
    if depo is None:
        depo = []
    depo.append(miktar)
    return depo
