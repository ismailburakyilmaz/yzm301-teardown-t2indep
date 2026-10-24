# Tur 6 ölçümü — ön kayıt (kapsam boşlukları)
Kayıt: 2026-10-21, ölçümden önce. İnceleme oturumu (Claude Code). Bu dosya ölçüm başladıktan sonra değiştirilmez; SHA-256 ölçüm notunda verilir.

## Amaç
Kâhin setinde ölçülmemiş a priori bölgeleri sınamak: tipik klinik bölgeden rastgele örnek, çok büyük d (yönergenin sınır listesinde), küçük df + uç α, büyük d + uç oran. Oracle G*Power'dır. Noktalar motoru ayarlamak için değil, sınamak için seçildi; varsayılan motorun bu noktalardaki sonucu ölçümden önce hesaplanmadı.

## Seçim
- **T01–T10 (tipik bölge):** Python `random.Random(20261021)` ile şu kümelerden eşit olasılıkla seçildi; mevcut 87 vektör ve HO-01…12 ile aynı olanlar atlandı. Tails {One, Two}; d {0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8}; α {0.05, 0.01, 0.1}; güç {0.8, 0.85, 0.9, 0.95}; oran {1, 2, 0.5, 1.5, 3}.
- **B01–B05 (büyük d), S01–S03 (küçük df + uç α), R01–R02 (büyük d + uç oran):** elle seçildi; hiçbiri mevcut kayıtlarla aynı değil.

| Kimlik | Tails | d | α | Güç | Oran N2/N1 | Grup |
|---|---|---|---|---|---|---|
| T01 | Two | 0.2 | 0.01 | 0.95 | 0.5 | tipik |
| T02 | One | 0.7 | 0.01 | 0.95 | 1 | tipik |
| T03 | Two | 0.6 | 0.05 | 0.8 | 0.5 | tipik |
| T04 | Two | 0.35 | 0.05 | 0.85 | 1 | tipik |
| T05 | One | 0.3 | 0.1 | 0.8 | 0.5 | tipik |
| T06 | One | 0.5 | 0.1 | 0.8 | 3 | tipik |
| T07 | Two | 0.45 | 0.1 | 0.8 | 2 | tipik |
| T08 | One | 0.45 | 0.01 | 0.8 | 1 | tipik |
| T09 | One | 0.6 | 0.1 | 0.8 | 1.5 | tipik |
| T10 | Two | 0.4 | 0.1 | 0.8 | 2 | tipik |
| B01 | Two | 1 | 0.05 | 0.8 | 1 | büyük d |
| B02 | One | 2 | 0.05 | 0.9 | 1 | büyük d |
| B03 | Two | 5 | 0.05 | 0.95 | 1 | büyük d |
| B04 | Two | 20 | 0.05 | 0.8 | 1 | büyük d (üst sınır) |
| B05 | One | -20 | 0.05 | 0.8 | 1 | büyük negatif d |
| S01 | Two | 10 | 0.0000001 | 0.95 | 1 | küçük df + en küçük α |
| S02 | One | 20 | 0.0000001 | 0.8 | 1 | küçük df + en küçük α |
| S03 | One | 2 | 0.9 | 0.95 | 1 | büyük α |
| R01 | Two | 20 | 0.05 | 0.8 | 100 | büyük d + uç oran |
| R02 | One | 5 | 0.05 | 0.9 | 0.01 | büyük d + uç oran |

## Kayıt kuralları
G*Power 3.1.9.7 (SHA-256 `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812`), Means: Difference between two independent means (two groups), A priori. Her koşu için ekran `oracle/screenshots/R6-<Kimlik>_01.png` ve protokol satırı; protokol `oracle/raw/gpower_protocol_session5.rtf` olarak kaydedilir ve değerler oradan ayrıştırılır. G*Power bir noktayı reddederse hata mesajı ekranıyla kaydedilir; yerine başka nokta konmaz. İstemsiz koşu olursa kayda geçer. Bu turda LEDGER.md ve manifest.csv'ye doğrudan yazılmaz (eşzamanlı çalışma); ekler ayrı dosyada tutulur.
