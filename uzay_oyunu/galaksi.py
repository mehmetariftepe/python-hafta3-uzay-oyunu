"""Galaksi verisini JSON dosyasından okur."""
import json
from pathlib import Path
from typing import Any

def galaksi_kur(gezegenler: list[str], baglantilar: dict[str, list[str]],
                baslangic: str, **kwargs: Any) -> dict[str, Any]:
    """Başlangıcı doğrular ve yakıt verilmezse 50 ile galaksi oluşturur."""
    if baslangic not in gezegenler:
        raise ValueError("Başlangıç gezegeni listede yok.")
    return {"gezegenler": gezegenler, "baglantilar": baglantilar,
            "konum": baslangic, "yakit": kwargs.get("yakit", 50)}

def galaksi_oku() -> dict[str, Any]:
    """Modülün yanındaki JSON dosyasını okuyup galaksi_kur ile açar."""
    dosya_yolu = Path(__file__).with_name("galaksi.json")
    with dosya_yolu.open(encoding="utf-8") as dosya:
        veri = json.load(dosya)
    return galaksi_kur(**veri)
