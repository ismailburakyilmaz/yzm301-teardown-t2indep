# SPEC 1.1.0 diferansiyel raporu

Motor SHA-256: `439e43df7464de82d192c69d87d5e3b0c1230ca953bf0645346675f91d20838c`; motor değişmedi.
Sıkı GUI karşılaştırması ve CONTRACT mutlak/bağıl 1e-6 ayrı sonuçlardır. Tam sayı alanları tam eşitlik ister.

| Küme | Sıkı tüm alan | Sıkı AP tahsis | Resmî tüm alan | Resmî AP tahsis |
|---|---:|---:|---:|---:|
| legacy87 | 74/87 | 39/51 | 61/72 | 36/47 |
| round6 | 20/20 | 20/20 | 19/19 | 19/19 |
| round7 | 27/27 | 21/21 | 21/21 | 17/17 |
| round8 | 8/8 | 5/5 | 8/8 | 5/5 |
| new55 | 55/55 | 46/46 | 48/48 | 41/41 |
| all142 | 129/142 | 85/97 | 109/120 | 77/88 |

Resmî retler 47/47: GUI hesap üretmiş 22 alan-dışı girdi + 25 girdi gözlemi. Public25 bu paydaya eklenmez.
PH güç, AP güç, yardımcı alanlar ve her alanın farkı JSON/CSV içinde. Açıklanmamış motor farkları düzeltilmiş sayılmadı.
Gizli AP %90 kapısı bilinmiyor. Tarihî sıkı ölçüt başarısızlıkları xfail/skip yapılmadı.
Yeni55 kaydın SPEC içindeki null/eksik ekran ve protocol bilgileri doldurulmadı; gerçek oracle ekranlarını kullanıcı ekleyecek.
