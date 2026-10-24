# Bağımsız doğrulama — ön kayıt (Tur 5)
Kayıt: 2026-10-21, ölçümden önce. İnceleme oturumu (Claude Code). Bu dosya ölçüm başladıktan sonra değiştirilmez; SHA-256 değeri ölçüm raporunda verilir.

## Amaç
SPEC 1.0.3/1.0.4 aday sayısal yönteminin, geliştirilirken kullanılmamış girdilerde G*Power'ın a priori N'ini üretip üretmediğini sınamak. Oracle G*Power'dır. Bu noktalar yöntemi ayarlamak için kullanılmaz; yalnız karşılaştırma içindir.

## Seçim ilkesi
- Hiçbiri mevcut 87 vektörün girdileriyle aynı değildir (makine kontrolü yapıldı).
- Ağırlık, sapma gözlenen büyük N bölgesindedir (yaklaşık 3·10⁷ – 3·10¹⁰); farklı d, yön, α, güç, oran ve negatif d içerir.
- İki kontrol noktası uyumlu bölgededir (HO-10, HO-11).
- Seçim, aday yöntemin bu noktalardaki tahmini hesaplanmadan yapıldı. Ölçüm sırasında aday yöntem çalıştırılmayacak.

| Kimlik | Tails | d | α | Güç | Oran N2/N1 | Not |
|---|---|---|---|---|---|---|
| HO-01 | One | 0.0003 | 0.05 | 0.8 | 1 | büyük N |
| HO-02 | One | 0.0007 | 0.05 | 0.8 | 1 | geçiş bölgesi |
| HO-03 | One | 0.00008 | 0.05 | 0.8 | 1 | çok büyük N |
| HO-04 | Two | 0.0006 | 0.05 | 0.8 | 1 | iki yön |
| HO-05 | One | 0.0004 | 0.05 | 0.9 | 1 | farklı güç |
| HO-06 | One | 0.001 | 0.01 | 0.8 | 1 | farklı α |
| HO-07 | One | 0.0005 | 0.05 | 0.8 | 3 | eşit olmayan oran |
| HO-08 | Two | -0.0003 | 0.05 | 0.8 | 1 | negatif d |
| HO-09 | Two | 0.0002 | 0.1 | 0.95 | 0.5 | birleşik değişiklik |
| HO-10 | Two | 0.003 | 0.05 | 0.8 | 1 | kontrol (uyumlu bölge beklenir) |
| HO-11 | Two | 0.3 | 0.05 | 0.9 | 2 | kontrol (normal N) |
| HO-12 | One | 0.00003 | 0.05 | 0.8 | 1 | en büyük N |

## Kayıt kuralları
G*Power 3.1.9.7 (SHA-256 `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812`), Means: Difference between two independent means (two groups), A priori. Her koşu için ekran (`oracle/screenshots/HO-xx_01.png`) ve protokol satırı; protokol `oracle/raw/gpower_protocol_session4.rtf` olarak kaydedilir ve değerler oradan ayrıştırılır. İstemsiz koşu olursa kayda geçer, silinmez. Ölçülemeyen nokta (ör. G*Power hata verirse) olduğu gibi raporlanır, yerine başka nokta konmaz.
