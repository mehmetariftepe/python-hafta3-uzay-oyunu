"""Hamle sayacı ve bağlantı sayısına göre sıralama."""
from typing import Callable, Any

def hamle_sayaci() -> Callable[[], int]:
    """Her çağrıda bir artan, bağımsız bir sayaç fonksiyonu döndürür."""
    toplam = 0
    def arttir() -> int:
        """Kapsayan fonksiyondaki toplamı bir artırıp döndürür."""
        nonlocal toplam
        toplam += 1
        return toplam
    return arttir

def en_bagli_gezegenler(galaksi: dict[str, Any]) -> list[str]:
    """Bağlantı sayısı azalan, eşitlikte alfabetik sırada gezegenleri döndürür."""
    return sorted(galaksi["gezegenler"],
                  key=lambda gezegen: (-len(galaksi["baglantilar"][gezegen]), gezegen))
