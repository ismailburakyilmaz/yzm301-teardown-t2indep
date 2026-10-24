# oracle CSV güncellemesi — SPEC 1.1.0 (2026-10-23)
Hazırlayan: Claude Code inceleme oturumu. Yeni G*Power ölçümü yapılmadı; yalnız kayıtlı gözlemler CSV'ye taşındı.

## Ne değişti (TEARDOWN_BASLANGIC_PAKETI/oracle/)
| Dosya | Önce | Sonra | Not |
|---|---|---|---|
| gpower_vectors.csv | 87 satır, `17a73c2b…de21` | 142 satır, `1d478209…ddb7` | Tur 6 (20), Tur 7 (27), Tur 8 (8) eklendi; ilk 87 satır bayt bayt aynı (tam önek) |
| invalid_cases.csv | 22 satır, `c0886128…e528` | 25 satır, `ef31f626…e091` | R7-I01…I03 GUI retleri eklendi; ilk 22 satır bayt bayt aynı |
| holdout_vectors.csv | — | 12 satır, `a7ada50f…d0db` | HO-01…HO-12; SPEC 1.1.0 referans kümesinde değil, aynı sütunlar |
| contract_expectations.csv | — | 167 satır, `70a32b9e…bca` | 142 vektör + 25 geçersiz durum için CONTRACT 1.0.0 CLI beklentisi (120 sayısal başarı, 47 hata); SPEC 1.1.0 veri bloğundan |
| manifest.csv | `79f2ad08…fa70` | `37993f31…9041` | İki satırın SHA/notu güncellendi, iki satır eklendi; özgün karışık satır sonları korundu |

Eski satırlardaki tarihî ifade (ör. eski geçici sözleşme kategorileri) değiştirilmedi; güncel CLI beklentisi `contract_expectations.csv` içindedir.

## Denetimler (build_oracle_csv.py, 0 sorun)
- SPEC 1.1.0 veri bloğu (`spec_version` 1.1.0) ile eski 87 satırın inputs/expected/displayed/comparison alanları birebir aynı.
- 55 yeni vektör ve 12 holdout için üç kaynak eşleşti: SPEC (holdout hariç) = `raw/*_observations.jsonl` = ayrıştırılmış protokol (`gpower_protocol_session4…7_parsed.json`, sıra numarası ve saat dahil). Post hoc'ta n1/n2 protokolde girdi olarak denetlendi.
- Her ekran görüntüsünün SHA-256'sı gözlem kaydındaki değerle aynı.
- Holdout kimliklerinin hiçbiri SPEC vektörlerinde yok.

## Yedek ve yeniden üretim
- Önceki üç dosya: `before/` (SHA'lar yukarıda).
- Yeniden üretim: `python -I build_oracle_csv.py <TEARDOWN_BASLANGIC_PAKETI> <çıktı klasörü>`; `out/` bu çalıştırmanın çıktısıdır.
