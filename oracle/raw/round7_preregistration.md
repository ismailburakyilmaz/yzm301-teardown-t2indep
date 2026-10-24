# Tur 7 ölçümü — ön kayıt (kapsam boşlukları, 2. bölüm)
Kayıt: 2026-10-21, ölçümden önce. İnceleme oturumu (Claude Code). Bu dosya ölçüm başladıktan sonra değiştirilmez; SHA-256 ölçüm notunda verilir.

## Amaç
Tur 6'da ölçülmemiş bölgeleri sınamak: tipik bölgeden ikinci rastgele örnek, tam sayı olmayan oranlarda grup yuvarlaması, negatif d birleşimleri, post hoc uçları, geçersiz ve sınır girdiler. Oracle G*Power'dır. Varsayılan motorun bu noktalardaki sonucu ölçümden önce hesaplanmadı.

## Seçim
- **T01–T10 (tipik, ikinci örnek):** Python `random.Random(20261022)`; mevcut 87 vektör, HO-01…12 ve R6-* ile aynı olanlar atlandı. Tails {One, Two}; d {0.2, 0.25, …, 0.8 (0.05 adım)}; α {0.05, 0.01, 0.1, 0.025}; güç {0.8, 0.85, 0.9, 0.95, 0.99}; oran {1, 2, 0.5, 1.5, 3, 0.75}.
- **Q, N, P, I:** elle seçildi.

### A priori
| Kimlik | Tails | d | α | Güç | Oran | Grup |
|---|---|---|---|---|---|---|
| T01 | Two | 0.65 | 0.1 | 0.85 | 1 | tipik |
| T02 | One | 0.35 | 0.01 | 0.8 | 0.75 | tipik |
| T03 | One | 0.2 | 0.01 | 0.85 | 0.5 | tipik |
| T04 | One | 0.75 | 0.01 | 0.85 | 3 | tipik |
| T05 | One | 0.35 | 0.025 | 0.8 | 3 | tipik |
| T06 | One | 0.45 | 0.01 | 0.99 | 0.5 | tipik |
| T07 | Two | 0.2 | 0.05 | 0.85 | 2 | tipik |
| T08 | Two | 0.25 | 0.05 | 0.99 | 2 | tipik |
| T09 | Two | 0.25 | 0.01 | 0.95 | 3 | tipik |
| T10 | Two | 0.25 | 0.025 | 0.95 | 0.75 | tipik |
| Q01 | Two | 0.5 | 0.05 | 0.8 | 1.3 | tam sayı olmayan oran |
| Q02 | One | 0.4 | 0.05 | 0.9 | 2.7 | tam sayı olmayan oran |
| Q03 | Two | 0.6 | 0.01 | 0.9 | 0.37 | tam sayı olmayan oran |
| Q04 | One | 0.3 | 0.1 | 0.8 | 1.7 | tam sayı olmayan oran |
| Q05 | Two | 0.8 | 0.05 | 0.95 | 0.6 | tam sayı olmayan oran |
| N01 | Two | -0.5 | 0.05 | 0.8 | 2 | negatif d + oran |
| N02 | One | -0.3 | 0.05 | 0.8 | 0.5 | negatif d + oran |
| N03 | Two | -0.8 | 0.01 | 0.9 | 1.5 | negatif d + oran |
| N04 | One | -1 | 0.1 | 0.95 | 3 | negatif d + oran |
| I04 | Two | 0.5 | 0.9999999 | 0.9999999 | 1 | sınır: α ve güç üst sınırda |
| I05 | Two | 20 | 0.0000001 | 0.9999999 | 1 | sınır: en küçük α, en büyük güç, en büyük d |

### Post hoc
| Kimlik | Tails | d | α | n1 | n2 | Grup |
|---|---|---|---|---|---|---|
| P01 | Two | 0.5 | 0.05 | 2 | 5000 | aşırı dengesiz |
| P02 | One | 1 | 0.05 | 1 | 1000 | aşırı dengesiz, n1 = 1 |
| P03 | Two | 2 | 0.0000001 | 3 | 3 | küçük df + en küçük α |
| P04 | Two | 0.004 | 0.05 | 500000 | 500000 | büyük N |
| P05 | One | 0.0004 | 0.05 | 50000000 | 50000000 | çok büyük N |
| P06 | Two | -0.3 | 0.01 | 40 | 120 | negatif d + dengesiz |

### Geçersiz girdi beklenen (a priori; G*Power davranışı kaydedilecek)
| Kimlik | Tails | d | α | Güç | Oran | Sınanan |
|---|---|---|---|---|---|---|
| I01 | Two | 0.5 | 0.05 | 0.8 | -1 | negatif oran |
| I02 | Two | 20.01 | 0.05 | 0.8 | 1 | d üst sınır üstü (a priori) |
| I03 | Two | -20.01 | 0.05 | 0.8 | 1 | d alt sınır altı (a priori) |

## Kayıt kuralları
G*Power 3.1.9.7 (SHA-256 `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812`), Means: Difference between two independent means (two groups). Ekranlar `oracle/screenshots/R7-<Kimlik>_01.png`; protokol `oracle/raw/gpower_protocol_session6.rtf`; değerler protokolden ayrıştırılır. Hata veren girdilerde hata penceresinin ekranı kaydedilir ve mesaj metni yazılır. Bir nokta reddedilirse yerine başka nokta konmaz. LEDGER.md ve manifest.csv'ye doğrudan yazılmaz; ekler `INCELEME_KONTROLU/ROUND7_KAPSAM/` altında tutulur.
