# Hafta 5: dekoratör sırası

Mehmet Arif Tepe / 20253006008

`uv run python -m uzay_oyunu.dekorator_ornekleri` ile gerçek çalıştırma:

| Tanım (yukarıdan aşağıya) | fib(20) | Çağrı sayısı |
| --- | ---: | ---: |
| Yalnızca `@say` | 6765 | 21891 |
| `@say`, `@lru_cache(maxsize=None)` | 6765 | 39 |
| `@lru_cache(maxsize=None)`, `@say` | 6765 | 21 |

Her ölçüm sıfır sayaç ve boş önbellekle başlar. Kod aynı süreçte tekrar
çalıştırıldığında da bunları temizler; test bunu iki kez doğrular.

## Tanım anı ve çağrı anı

Dekoratörler fonksiyon tanımlanırken aşağıdan yukarı uygulanır:

```python
@say
@lru_cache(maxsize=None)
def fib(n): ...
# fib = say(lru_cache(maxsize=None)(özgün_fonksiyon))
```

Çağrıda önce dıştaki, yani üstte yazılan dekoratör çalışır.
Özyinelemeli çağrılar da global `fib` adına döndüğü için aynı katmanlardan geçer.

- **Yalnızca sayaç:** tekrar eden alt problemler yeniden hesaplanır;
  0 ve 1 taban çağrıları dahil toplam 21891 çağrı yapılır.
- **Sayaç dışta:** önbellek tekrar hesabı engeller; sayaç önbelleğe giden
  isabetli çağrıları da görür. 21 farklı girdi ve 18 cache isabeti: toplam 39.
- **Önbellek dışta:** cache isabetinde doğrudan kayıtlı sonuç döner;
  içteki sayaç yalnızca 0–20 arasındaki 21 farklı hesap için çalışır.

Üçüncü durumda canlı sayaç `fib_cache_ustte.__wrapped__.cagri` ile okunur.
Dış cache sarmalayıcısına kopyalanmış bir nitelik güncel sayacı göstermeyebilir.
`functools.wraps` fonksiyonun adını, docstring'ini ve `__wrapped__` bağını korur.

## Diğer dekoratörlerde iki aşama

- `sure_olc`, `say`, `log_cagri`: tanım anında sarmalayıcı oluşturur;
  süre ölçme, sayma veya loglama işi her çağrıda yapılır.
- `sinirla(0, 100)`: önce sınırları taşıyan dekoratörü, sonra fonksiyonun
  sarmalayıcısını oluşturur. Çağrıda ilk argümanı kontrol eder.
- `hafiza(maxsize=2)`: tanım anında ayrı bir closure sözlüğü oluşturur;
  çağrıda kaydı arar, yoksa hesaplayıp saklar.
- `komut(ad, aciklama)`: tanım anında kayıt yapar ve **aynı fonksiyonu**
  döndürür. PDF'nin kimlik koruma koşulu nedeniyle burada sarmalayıcı ve
  `wraps` yoktur; kendisini kendisine sarmalamak yanlış bir `__wrapped__`
  döngüsü oluştururdu. Diğer bütün sarmalayıcılar `wraps` kullanır.
