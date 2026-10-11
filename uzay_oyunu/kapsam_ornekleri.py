"""Ders örnekleri yerine hazırlanmış bağımsız kapsam örnekleri."""
sayi = 10

def dis_degeri_oku() -> None:
    """Yerel atama olmadığında modül düzeyindeki değeri okur."""
    print(sayi)

def yerel_deger() -> None:
    """Aynı isimde yerel değişken oluşturur; dış değeri değiştirmez."""
    sayi = 20
    print(sayi)

def kapsayan_fonksiyon() -> None:
    """İç fonksiyonun kapsayan fonksiyondaki değeri okuyuşunu gösterir."""
    sayi = 30
    def ic_fonksiyon() -> None:
        """En yakın kapsamdaki sayi değerini yazdırır."""
        print(sayi)
    ic_fonksiyon()

def hatali_yerel() -> None:
    """Yerel değişkene atamadan önce erişip UnboundLocalError üretir."""
    print(sayi)
    sayi = 40

if __name__ == "__main__":
    dis_degeri_oku()
    yerel_deger()
    print(sayi)
    kapsayan_fonksiyon()
    try:
        hatali_yerel()
    except UnboundLocalError:
        print("UnboundLocalError")
