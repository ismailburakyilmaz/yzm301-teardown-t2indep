# Tur 8 ölçümü — ön kayıt (karar sınırları)
Kayıt: 2026-10-21, ölçümden önce. İnceleme oturumu (Claude Code). Bu dosya ölçüm başladıktan sonra değiştirilmez; SHA-256 ölçüm notunda verilir.

## Kaynak ve kapsam
Noktalar Codex inceleme koordinatörünün `INCELEME_KONTROLU/ROUND7_KAPSAM/OZEL_TEST_ONERILERI.md` önerisinden alındı (11 nokta). Resmî CONTRACT.md 1.0.0 (2026-10-21) Bölüm 5 `d > 0` dediği için negatif d'li 3 post hoc noktası CLI açısından geçersiz girdidir; bu turda ölçülmedi. Kalan 8 nokta ölçülür. Varsayılan motorun bu noktalardaki sonucu ölçümden önce hesaplanmadı; oracle G*Power'dır.

| Kimlik | Mod | Tails | d | α | Güç | Oran / n1, n2 | Amaç |
|---|---|---|---|---|---|---|---|
| B01 | a priori | Two | 20 | 0.05 | 0.8 | oran 6.999999 | sıfır gruba geçiş sınırının altı |
| B02 | a priori | Two | 20 | 0.05 | 0.8 | oran 7 | sıfır gruba geçiş sınırı |
| B03 | a priori | Two | 20 | 0.05 | 0.8 | oran 7.000001 | sıfır gruba geçiş sınırının üstü |
| B04 | a priori | Two | 0.55 | 0.05 | 0.8 | oran 2.9999999 | yarım-yukarı tahsis sınırı (GP-AP-022 komşusu) |
| B05 | a priori | Two | 0.55 | 0.05 | 0.8 | oran 3.0000001 | yarım-yukarı tahsis sınırı (GP-AP-022 komşusu) |
| B06 | post hoc | One | 0.5 | 0.4999999 | — | n1 3, n2 7 | α = 0.5'in hemen altı, küçük dengesiz grup |
| B07 | post hoc | One | 0.5 | 0.5 | — | n1 3, n2 7 | α = 0.5 (medyan) |
| B08 | post hoc | One | 0.5 | 0.5000001 | — | n1 3, n2 7 | α = 0.5'in hemen üstü |

## Kayıt kuralları
G*Power 3.1.9.7 (SHA-256 `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812`). Ekranlar `oracle/screenshots/R8-<Kimlik>_01.png`; protokol `oracle/raw/gpower_protocol_session7.rtf` (önceki 47 koşu dahil); değerler protokolden ayrıştırılır. G*Power girdi metnini normalleştirirse protokoldeki metin kaydedilir; iki komşu aynı girdiye dönüşürse bağımsız sayılmaz. Hata olursa hata penceresi kaydedilir; yerine nokta konmaz. LEDGER.md ve manifest.csv'ye doğrudan yazılmaz; ekler `INCELEME_KONTROLU/ROUND8_SINIR/` altında tutulur.
