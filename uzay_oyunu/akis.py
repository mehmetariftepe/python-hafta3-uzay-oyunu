"""Hafta 4: tembel üreteçler ve önbellekli rota hesabı."""
from collections.abc import Iterator, Iterable, Mapping, Sequence, Callable
from pathlib import Path
from functools import lru_cache


def fibonacci() -> Iterator[int]:
    """Sıfırdan başlayan Fibonacci sayılarını sonsuza kadar üretir."""
    onceki, simdiki = 0, 1
    while True:
        yield onceki
        onceki, simdiki = simdiki, onceki + simdiki


def yakit_gostergesi(yakit: int, tuketim: int) -> Iterator[int]:
    """Her adımda tüketir; sıfırı bir kez üretir, sonra sonlanır."""
    if yakit < 0 or tuketim <= 0:
        raise ValueError("Yakıt negatif, tüketim sıfır veya negatif olamaz.")
    while yakit > 0:
        yakit = max(0, yakit - tuketim)
        yield yakit


def satirlari_oku(yol: str | Path) -> Iterator[str]:
    """UTF-8 dosyayı satır satır okur; boşlukları ve yorumları atlar."""
    with Path(yol).open(encoding="utf-8") as dosya:
        for satir in dosya:
            satir = satir.strip()
            if satir and not satir.startswith("#"):
                yield satir


def ayristir(satirlar: Iterable[str]) -> Iterator[tuple[str, str, int]]:
    """Her seyir satırını kaynak, hedef ve yakıt demetine dönüştürür."""
    for satir in satirlar:
        kaynak, kalan = satir.split("->")
        hedef, yakit = kalan.split()
        yield kaynak.strip(), hedef, int(yakit)


def uzun_yolculuklar(
    kayitlar: Iterable[tuple[str, str, int]], esik: int
) -> Iterator[tuple[str, str, int]]:
    """Yalnızca yakıtı eşikten kesin büyük kayıtları tembelce üretir."""
    for kayit in kayitlar:
        if kayit[2] > esik:
            yield kayit


def rota_sayaci(baglantilar: Mapping[str, Sequence[str]]) -> Callable[[str, int], int]:
    """Tam adım sayısındaki rotaları sayan, bağımsız önbellekli closure döndürür."""
    @lru_cache(maxsize=None)
    def rota_sayisi(gezegen: str, adim: int) -> int:
        """Sıfır adımda boş rota birdir; diğerlerinde komşu sonuçları toplanır."""
        if adim < 0:
            raise ValueError("Adım negatif olamaz.")
        if gezegen not in baglantilar:
            raise ValueError("Bilinmeyen gezegen.")
        if adim == 0:
            return 1
        return sum(rota_sayisi(hedef, adim - 1) for hedef in baglantilar[gezegen])
    return rota_sayisi


def rota_sayaci_onbelleksiz(
    baglantilar: Mapping[str, Sequence[str]]
) -> Callable[[str, int], int]:
    """Karşılaştırma için aynı hesabın önbelleksiz sürümünü döndürür."""
    def rota_sayisi(gezegen: str, adim: int) -> int:
        """Her çağrıda alt rotaları yeniden hesaplar."""
        if adim < 0:
            raise ValueError("Adım negatif olamaz.")
        if gezegen not in baglantilar:
            raise ValueError("Bilinmeyen gezegen.")
        if adim == 0:
            return 1
        return sum(rota_sayisi(hedef, adim - 1) for hedef in baglantilar[gezegen])
    return rota_sayisi
