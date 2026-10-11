"""Varsayılan liste hatasının önceki sürümü."""
def yakit_ekle(miktar: int, depo: list[int] = []) -> list[int]:
    """Verilen miktarı depoya ekler."""
    depo.append(miktar)
    return depo
