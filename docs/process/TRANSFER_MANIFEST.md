# TRANSFER_MANIFEST — İnceleme oturumundan yazım oturumuna aktarım
Bu dosya SPEC'in dışında tutulur ve yazım oturumuna verilmez. SPEC kendi özetini içermez.

| spec_version | spec_file | sha256 | status | frozen_at | vector_count | valid_by_mode | critical_open_questions | clean_room_check |
|---|---|---|---|---|---|---|---|---|
| 1.1.0 | SPEC.md (505700 bayt) | `016233430d0f4337c8d1de36a51747654fea31da2448a0798e17c47217cccdbe` | READY_FOR_IMPLEMENTATION — resmî CONTRACT 1.0.0; geçici kararlar Bölüm 14 | 2026-10-22T03:28:55.172708+03:00 | 142 GUI + 25 girdi + 14 ajan; public 25 ayrı | GUI AP 97, PH 45; CLI sayısal 120, ret 47 | Geçici kod/kapsam kararları Bölüm 14; resmî yanıt bekleniyor | kullanıcı/Claude onayı 2026-10-22; yalnız SPEC aktarıldı; iki 1.0.4 yedeği aktarim_yedekleri altında |
| 1.0.4 | SPEC.md (218507 bayt) | `48f75233dfbdd19d4248d97fc24dd243d54f830ecd1ad50ec3a36fa4b644ad7d` | READY_FOR_IMPLEMENTATION — geçici sözleşme; Bölüm 15 inceleme bulgusu, yeni yöntem üretime alınmadı; varsayılan motor korunur | 2026-10-21T13:31:16+03:00 | 87 + 22 + 14; JSON/Gherkin baytları aynı | AP 51, PH 36 | Q-1/Q-2 resmî teyit bekliyor | kullanıcı temiz oda onayı 2026-10-21; yalnız SPEC aktarıldı; önceki sürüm yedeği: `aktarim_yedekleri/SPEC_1.0.3_GPOWER_YAZIM_yedek_2026-10-21.md` |
| 1.0.3 | SPEC.md (221550 bayt) | `156f669255c02ef99c425e7e751e44fdb2d4b20eb976a1e19228dcd396df5afa` | READY_FOR_IMPLEMENTATION — sayısal yöntem; bağımsız yazım doğrulaması gerekir | 2026-10-21 | 87 + 22 + 14; JSON/Gherkin aynı | AP 51, PH 36 | Q-1/Q-2; AP-025/028/049/050 inceleme farkları | adres/decompile/kanıt kimliği yok; yalnız SPEC aktarıldı 2026-10-21T00:56:00.337985+00:00 |
| 1.0.2 | SPEC.md (206597 bayt) | `2107d0f7469a9bdbe7939684ee76870b9f8fcbe2c572421c45a90aece86c34bf` | READY_FOR_IMPLEMENTATION — geçici sözleşme | 2026-10-20 | 87 geçerli + 22 girdi gözlemi + 14 ajan sorusu; 17 yeni küçük d vektörü (GP-AP-035…051), ilk 70 vektör değişmedi | a-priori 51, post-hoc 36 | Q-1/Q-2 resmî teyit bekliyor | adres/decompile/ev_ yok; **aktarıldı 2026-10-20T22:48:25+03:00** → `GPOWER_YAZIM/SPEC.md`, kopya SHA-256 eşit; önceki 1.0.1 kopyası (`aebcfdf0…9221`) `aktarim_yedekleri/SPEC_1.0.1_GPOWER_YAZIM_yedek_2026-10-20.md` olarak saklandı |
| 1.0.1 | SPEC.md (173104 bayt) | `aebcfdf0b0f220041237e812ea36a01756160a7bff779580d34c1d77c8b39221` | READY_FOR_IMPLEMENTATION — geçici sözleşme | 2026-10-18T19:53:23+03:00 | 70 geçerli + 22 girdi gözlemi + 14 ajan sorusu; oracle bloğu değişmedi | a-priori 34, post-hoc 36 | Q-1/Q-2 resmî teyit bekliyor; Y-7/Y-8 cevaplandı | adres/decompile/ev_ yok; yalnız SPEC güncellemesi GPOWER_YAZIM klasörüne aktarıldı |
| 1.0.0 | SPEC.md (166 857 bayt) | `d01a19bc9e30f03a207a9cc7aa31f63468e9a84d7fb5b867d4560260dc470012` | READY_FOR_IMPLEMENTATION — yalnız kullanıcı tarafından seçilen geçici proje sözleşmesiyle; resmî ders sözleşmesi değildir | 2026-10-18 ~18:15 (Europe/Istanbul) | 70 geçerli + 22 girdi gözlemi + 14 ajan sorusu | a-priori 34, post-hoc 36 | Q-1 (post hoc CLI) ve Q-2 (serileştirme) resmî teyit bekliyor; geçici kararla doldu | geçti (aşağıda) |

## Önceki sürümler (aktarılmadı)
| spec_version | sha256 | status | not |
|---|---|---|---|
| 0.9.0 | `b85bc03ee225c9ff5c40b5ff3e3850f6d536f53ab6e9d91850f248f05f86e11d` (bağımsız inceleme raporunun ölçtüğü) | DRAFT | bağımsız incelemede düzeltme gerekti |
| 0.10.0 | `531edbfb19a4449503ca8b4e602441d20848b35fcb2aea9192b4adc5283d7570` | DRAFT | sözleşme kararları bekleniyordu |

## Aktarım öncesi kontroller (1.0.0)
- [x] Hedef: G*Power 3.1.9.7, `GPowerNT.exe`, SHA-256 `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812` (SPEC'te ve gömülü JSON başlığında).
- [x] REA/Ghidra 12.1.4 hedef üzerinde çalıştı (ENVIRONMENT.md).
- [x] 70 geçerli vektör (≥ 30), iki mod ve sınır grupları temsil ediliyor; her vektörün ekranı var; CSV ve G*Power protokol dökümüyle 70/70 eşleşme; manifest 104/104 SHA-256.
- [x] Kural dizini (RULE-001…026), Gherkin AC-01…AC-17, AC↔RULE↔vektör eşlemesi; tanımsız RULE/AC yok.
- [x] Gömülü JSON referans dosyasıyla birebir aynı; `schema_version`, `template_only: false`, `target`, `cli_contract`, `vectors`, `invalid` (expected_cli dahil), `agent_cases` (10 esas + 4 zorlayıcı).
- [x] SPEC'te adres, decompile kodu, `FUN_`/`ev_` işareti yok; uygulama için başka yerel dosya okumayı gerektirmiyor (dosya adları yalnız teslim birleştirmesi ve doğrulama kökeni bağlamında geçiyor).
- [x] Geçici sözleşme kuralları RULE-023…026 "[GEÇİCİ SÖZLEŞME]" etiketli; kaynak ve tarih (kullanıcı, 2026-10-18) SPEC ve LEDGER Bölüm 8'de.
- [x] Gizli test uyumu garanti edilmiyor (SPEC başlığı ve Bölüm 14).
- [ ] Q-1 ve Q-2 resmî teyidi — bekleniyor; farklı çıkarsa yeni SPEC sürümü ve yeni manifest satırı.

## Aktarım adımları (kullanıcı)
1. Yeni ve boş bir yazım klasörü oluştur; inceleme klasörünün altında olmasın.
2. Yalnız `SPEC.md`'yi oraya kopyala; kopyanın SHA-256'sının yukarıdaki değerle aynı olduğunu doğrula.
3. Yeni, geçmişsiz bir oturum aç (bu oturumu devam ettirme veya çatallama); ilk mesaj olarak `prompts/02_YAZIM_ILK_PROMPT.md` metnini gönder.
4. LEDGER, oracle, ekranlar, inceleme raporu, bu manifest ve süreç günlükleri yazım klasörüne konmaz.

## 1.0.1 aktarım notu
Önceki 1.0.0 gerçekten yazım oturumunda kullanıldı. 1.0.1 aynı yazım klasöründeki SPEC.md üzerine kopyalandı; kod ve fixture dosyaları değiştirilmedi. Yazım oturumu yeni sürümü kabul edip provenance kaydını kendi günceller. İlk prompt tarihî kayıt olarak değiştirilmez; devam talimatı yeni SPEC Bölüm 11 hükümlerini esas alır. Oracle JSON ve önceki Gherkin bloğu bayt düzeyinde aynıdır.

## 1.0.2 aktarım notu
1.0.2 küçük d ölçümüyle (OLCUM_RAPORU_KUCUK_D.md) hazırlandı. Değişiklik yalnız yeni vektörler (GP-AP-035…051), AC-18, RULE-010 ölçülen geçerlilik alanı ve RULE-016 tekrar notudur; CLI sözleşmesi, toleranslar, önceki 70 vektör, girdi gözlemleri ve ajan soruları değişmedi. Gherkin bloğu AC-18 eklendiği için değişti; oracle JSON'un ilk 70 vektörü aynı.
Aktarım kullanıcıya aittir: yazım oturumu (Codex) mevcut tamamlama turunu bitirdikten sonra SPEC.md, GPOWER_YAZIM klasöründeki kopyanın üzerine konur ve SHA-256 yukarıdaki değerle doğrulanır. Yazım oturumu yeni vektörleri fixture'a ekleyip testleri yeniden çalıştırır; eşleşmeyen küçük d vektörleri açık uyumsuzluk olarak raporlanır, motor için özel eşik veya katsayı eklenmez.

### 1.0.2 aktarım kaydı (2026-10-20T22:48:25+03:00)
- Aktarımdan önce `GPOWER_YAZIM/SPEC.md`: 173104 bayt, SHA-256 `aebcfdf0b0f220041237e812ea36a01756160a7bff779580d34c1d77c8b39221` (1.0.1; beklenen değerle aynı). Yedek inceleme tarafında: `aktarim_yedekleri/SPEC_1.0.1_GPOWER_YAZIM_yedek_2026-10-20.md` (aynı SHA-256).
- Aktarımdan sonra `GPOWER_YAZIM/SPEC.md`: 206597 bayt, SHA-256 `2107d0f7469a9bdbe7939684ee76870b9f8fcbe2c572421c45a90aece86c34bf`; inceleme tarafındaki SPEC.md ile eşit.
- Yalnız SPEC.md aktarıldı. LEDGER, oracle, ekranlar, ölçüm raporu ve bu manifest yazım klasörüne konmadı. Motor, testler ve fixture dosyaları değiştirilmedi; yazım oturumu başlatılmadı. Yeni sürümü kabul etmek, fixture'a eklemek ve testleri yeniden çalıştırmak yazım oturumunun işidir.

## 1.0.3 aktarım kaydı
- 2026-10-21T00:56:00.337985+00:00: yazım oturumu boşta doğrulandı. Önceki SHA 2107d0f7469a9bdbe7939684ee76870b9f8fcbe2c572421c45a90aece86c34bf; yeni SHA 156f669255c02ef99c425e7e751e44fdb2d4b20eb976a1e19228dcd396df5afa. Yalnız SPEC.md aktarıldı.
- JSON/Gherkin baytları aynı; eski SPEC yedeği inceleme tarafında aktarim_yedekleri/SPEC_1.0.2_before_numerical_2026-10-21.md.
- Motor, fixture, bağımlılık ve özgün deney dosyaları koordinatörce değiştirilmedi. İnceleme adayı 48/51 N, 83/87 tüm alanlar; bunlar yazım üretim sonucu değildir.

## 1.0.4 aktarım kaydı — 2026-10-21T13:31:16+03:00
- Kullanıcı temiz oda kontrolünü uygun buldu ve aktarımı onayladı (2026-10-21). Yeni yöntem üretime alınmadı; varsayılan motor korunur. Q-1/Q-2 resmî teyit bekliyor.
- Aktarım öncesi yazım ve inceleme SPEC 1.0.3: SHA-256 `156f669255c02ef99c425e7e751e44fdb2d4b20eb976a1e19228dcd396df5afa`. Yazım yedeği `aktarim_yedekleri/SPEC_1.0.3_GPOWER_YAZIM_yedek_2026-10-21.md`; inceleme yedeği `aktarim_yedekleri/SPEC_1.0.3_INCELEME_yedek_2026-10-21.md`. İki yedeğin özeti önceki kopyalarla aynı.
- Son SPEC 1.0.4: 218507 bayt; SHA-256 `48f75233dfbdd19d4248d97fc24dd243d54f830ecd1ad50ec3a36fa4b644ad7d`. İnceleme `SPEC.md`, onaylı son belge ve `GPOWER_YAZIM/SPEC.md` bayt düzeyinde eşit.
- Yalnız SPEC aktarıldı. JSON ve Gherkin blokları önceki 1.0.3 ile bayt düzeyinde aynı; 87 vektör, 22 girdi gözlemi, 14 ajan sorusu, toleranslar ve RULE-023…026 değişmedi. Holdout 87'ye eklenmedi.
- Adres, Evidence kimliği, FUN_ veya decompile kodu bulunmadı. Bölüm 12'deki decompile yasağı sözcük olarak korunur. Eski 0.9.0 “İlk DRAFT” kaydı tarihçedir; güncel durum değildir.
- Motor, testler, fixture'lar, deneyler ve diğer yazım dosyaları değiştirilmedi; diğer teslim dosyalarının SHA-256 envanteri aynı. Yazım oturumuna mesaj gönderilmedi. Devam talimatı yalnız inceleme tarafında taslak olarak hazırlandı.

## SPEC 1.1.0 aktarımı — 2026-10-22T03:28:55.172708+03:00

- Onaylı taslak: `0053012af6762c072e523bf7784a9151958e980174e2851bb78784170296a1ac`. Yalnız durum satırı ve değişiklik kaydına onay tarihi eklendi; gömülü JSON/Gherkin baytları aynı.
- Son SPEC: 505700 bayt, SHA-256 `016233430d0f4337c8d1de36a51747654fea31da2448a0798e17c47217cccdbe`. İnceleme ve GPOWER_YAZIM kopyaları aynı.
- Önceki iki SPEC 1.0.4 SHA-256: `48f75233dfbdd19d4248d97fc24dd243d54f830ecd1ad50ec3a36fa4b644ad7d`.
- Yazım yedeği: `C:\Users\Burak\Documents\Codex\2026-10-18\bu-k\outputs\TEARDOWN_BASLANGIC_PAKETI\aktarim_yedekleri\SPEC_1.0.4_GPOWER_YAZIM_yedek_2026-10-22_032855.md`.
- İnceleme yedeği: `C:\Users\Burak\Documents\Codex\2026-10-18\bu-k\outputs\TEARDOWN_BASLANGIC_PAKETI\aktarim_yedekleri\SPEC_1.0.4_INCELEME_yedek_2026-10-22_032855.md`.
- Yalnız SPEC aktarıldı; docs/CONTRACT ve fixture gerekirse gömülü metinden yazım oturumunda üretilecek. Motor/testler/fixture aktarılmadı veya değiştirilmedi.
- Gömülü veri başlığındaki tarihî taslak durumu ve diğer taslak ifadeleri kullanıcı yalnız iki satır değişikliği istediği için aynen korundu; üst durum satırı ve bu onay kaydı geçerlidir.
