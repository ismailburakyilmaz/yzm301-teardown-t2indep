# HALLUCINATIONS — İnceleme oturumu (Oturum 1)
Gerçek yanlış çıkarım kayıtları. Sayıyı tutturmak için olay uydurulmadı; aşağıdaki iki olay gerçekten yaşandı ve belirli vektörlerle yakalandı.

## H-001 — "n2 = round(n1 × oran)" (grupları ayrı yuvarlama)
- **Oturum / tarih:** 1 / 2026-10-18.
- **Ajanın ilk yanlış iddiası:** Eşit olmayan oranlı a priori sonucunda grup 2, grup 1'in orana göre ölçeklenip ayrı yuvarlanmasıyla bulunur (n2 = round(n1·r)) veya her grup sürekli çözümden ayrı yuvarlanır (n2 = round(N·r/(1+r))).
- **Neden başta kabul edildi:** İlk eşit-olmayan örnek GP-AP-007 (oran 2) 48/96 verdi; 96 = 48·2 olduğundan "n1'i oranla çarp" hipotezi sayısal olarak uydu. Oranlı dağıtımın doğal beklentisiydi.
- **Çürüten somut gözlem:** GP-AP-012 (oran 1.5) → n1=50, **n2=74** (50·1.5 = 75 değil). Kesin çürütme GP-AP-023 (oran 3) → sürekli bölünme 42.5/127.5; gözlenen **43/127** (127.5'in yuvarlaması 128 **değil**). Yani n2 bağımsız yuvarlanmıyor; n2 = N − n1.
- **Yakalayan vektör:** GP-AP-012, GP-AP-022, GP-AP-023 (ayrıca PROBE-R3 sonda koşuları).
- **Düzeltme:** RULE-011 "n1 = round_half_up(N/(1+r)), n2 = N − n1" olarak yazıldı; ayrı-yuvarlama hipotezi LEDGER C-054'te "çürütüldü" durumuyla saklandı.
- **Tekrarı önleyen kontrol:** Her oran vektöründe hem n1 hem n2 ayrı kaydedildi ve n1+n2 = N ile n1·r ≠ n2 örnekleri arandı; yarım-sınır (42.5, 35.5, 52.5) özellikle test edildi.
- **Son durum:** Kapandı; RULE-011 ve karşı-kanıt saklı.

## H-002 — "A priori N = sürekli çözümün tavanı" (basit yukarı yuvarlama)
- **Oturum / tarih:** 1 / 2026-10-18.
- **Ajanın ilk yanlış iddiası:** G*Power sürekli (kesirli) örneklem çözümünü tek bir tam sayıya **yukarı yuvarlar** (ödev metni de "G*Power yukarı yuvarlar" der); dolayısıyla toplam N, hedef gücü sağlayan en küçük tamsayıdır (tek de olabilir).
- **Neden başta kabul edildi:** Ödev metnindeki doğrudan ifade ("Bu kütüphaneler N'yi kesirli verir, G*Power yukarı yuvarlar") güçlü bir ön-kabuldü; çoğu vektörde sonuç bununla çelişmiyordu.
- **Çürüten somut gözlem:** (a) Gözlenen 24 a priori vektörün **tamamında toplam N çift**. (b) GP-PH-020: n1=6280, n2=6281 (toplam **12561, tek**) güç 0.8000282 ≥ 0.8 — yani tek toplam 12561 hedefi zaten sağlıyor; buna rağmen a priori (GP-AP-014) **12562** döndürdü. (c) GP-PH-012 (87/87 → 0.9494829 < 0.95) ve GP-PH-021 (42/126 → 0.7967341 < 0.8) bir önceki çift adımın yetersiz olduğunu doğruladı. Demek ki arama "en küçük tamsayı" değil, **çift adımlı en küçük** davranıyor; basit tavan değil.
- **Yakalayan vektör/test:** GP-AP-014 ↔ GP-PH-020 (çapraz kontrol), GP-PH-012, GP-PH-021.
- **Düzeltme:** RULE-010 "toplam N çift ve bu çiftler arasında hedefi sağlayan en küçük" olarak yazıldı; "tavan" hipotezi LEDGER C-053'te "çürütüldü" olarak saklandı. **Bunun iç algoritma kanıtı olmadığı** (çözücü kodu REA'da bulunamadı) açıkça sınır olarak belirtildi.
- **Tekrarı önleyen kontrol:** Minimalite yalnız üç çiftte doğrudan sınandı (GP-AP-002/GP-PH-012, GP-AP-023/GP-PH-021, GP-AP-014/GP-PH-020); önceki 'her a priori N için' ifadesi abartıydı (bağımsız inceleme raporu, H-006); ayrıca ödev metninin ifadeleri "doğrulanmamış doküman iddiası [DOK]" sayıldı, gözlemle sınandı.
- **Son durum:** Kapandı; RULE-010 ve karşı-kanıt saklı. İç algoritma belirsizliği SPEC Bölüm 13'te sınır olarak duruyor.

---
Not: Oran sınır kontrolünün ([0.01, 100]) t2-indep kod yolundan statik çağrı kenarı bulunamadı; bu bir yanlış çıkarım değil, **bilinçli bırakılmış belirsizliktir** (LEDGER C-026 sınır sütunu). [REA] olarak değil, GUI + ilgili fonksiyon kanıtıyla yazıldı. Bu yüzden halüsinasyon sayılmadı.

## H-003 — "Kritik t'nin işareti d'nin işaretini izler"
SPEC 0.9.0 RULE-008, d>0 için kritik t'nin pozitif olduğunu genelledi. Bağımsız inceleme cebirsel çelişkiyi gösterdi; ölçüm doğruladı: tek yönlü α=0.75, d=+0.5 → kritik −0.6810009 (GP-PH-027). Düzeltme: kritik = s·Q_t(1−α/k). Yakalayan: GP-PH-024…031, GP-AP-025…027.

## H-004 — "r ve 1/r ayna sonuç verir" (genel kural olarak)
SPEC 0.9.0 RULE-011 üç gözlenen çifti genelledi. r=0.3333333, N=170 → 128/42 (GP-AP-032); r=3 → 43/127. Düzeltme: ayna yalnız gözlenen çiftlerle sınırlandı.

## H-005 — "α ve güç (1e-07, 1) açık aralık"
SPEC 0.9.0 tablosu mesajdaki parantezi açık aralık diye okudu. α=1e-7 ve güç=1e-7 kabul edildi (GP-PH-032, GP-AP-033). Düzeltme: 1e-7 ≤ x < 1.

## H-006 — Kayıt abartıları
(a) INV-GUI-001 "geçersiz" sayıldı ama G*Power sonuç üretmişti (yeniden sınıflandı). (b) Minimalitenin "her a priori N için" doğrulandığı yazıldı; yalnız 3 çift. Yakalayan: bağımsız inceleme raporu.

## H-007 — "API başına token ölçülemez"
AGENT_COST'un ilk iki sürümü, girdi/çıktı/önbellek token'larını "ölçülmedi; ürün bu oturuma ayrıştırılmış rapor vermedi" diye yazdı. Bu, kaynak kontrol edilmeden yapılmış bir varsayımdı: Claude Code'un yerel oturum dökümünde her yanıtın `usage` alanı bulunuyor. Kullanıcının "tokeni göremez miyiz" sorusu üzerine döküm okundu; 311 yanıt, 124 444 478 girdi ve 333 128 çıktı token'ı ölçüldü. Düzeltme: AGENT_COST'a ölçülmüş tablo eklendi; görüntü token payı ve parasal maliyet hâlâ ölçülmedi olarak kaldı.

## H-008 — Hata dizelerini kök aramasına özgü saymak
“tolerances may not be negative” ve “unreasonable accuracy requirement” mesajları kök aramaya özgü ipucu sayılmıştı. Yayımlanmış GSL cquad integral kaynağında da ikisi bulunuyor. Düzeltme: bu dizeler tek başına N çözücüsünü tanımlamaz; elenen integral yolu yeniden arama diye etiketlenmedi. Kaynak ve sınır PUBLIC_FEASIBILITY_REPORT kaydında; asıl arama daha sonra farklı bir çağrı yolundan bulundu.

## H-009 — Üç örneklik denemede iki yönü sabitlemek
2026-10-21 inceleme denemesinin ilk sürümünde üç örnek için kuantil α/2 ile alınmıştı; örneklerin tails girdisi One idi. Yaklaşık 0.70 güç çıkması yöntemin başarısızlığı olarak kabul edilmeden girdiler denetlendi. Tails alanı kullanıldığında üç örnek de gösterim toleransında eşleşti. Beklenenler ve üretim motoru değiştirilmedi.

## H-010 — Cebirsel eşdeğerliği sayısal eşdeğerlik sanmak
Beta normalizasyonu ve NCT başlangıç adımlarındaki toplama sırası ilk deneyde statik kayıttan farklıydı. Ghidra kayıtlarındaki parantez sırası korununca aynı genel yöntemin N eşleşmesi 41/51'den 48/51'e çıktı. Bu, örneğe özel katsayı ayarı değildir. Düzeltme SPEC 1.0.3 Bölüm 15'te açık işlem sırasıdır; tam MSVC/x87 bit eşitliği yine iddia edilmez.

## H-011 — Bilimsel gösterimli değeri "5e-8 sınırını aşar" örneği saymak
2026-10-21, Claude (inceleme). CONTRACT.md Bölüm 6'daki "en fazla 5e-8 fark" ifadesine karşı Classroom soru taslağında 3.05715e-05 örnek gösterildi. Yanlış varsayım: daha az basamak gösterilen her değerde yuvarlama hatası büyür. Bilimsel gösterimde son hanenin yarısı 5e-11'dir, yani 5e-8'in altındadır; örnek iddiayı desteklemiyor. Codex'in bağımsız incelemesi taslağı okurken yakaladı; örnek, kullanıcının Classroom'a gönderdiği son metinden önce 11585.24 ve 3162.277 (yarım birim 0.005 ve 0.0005) ile değiştirildi. Kullanıcının paylaştığı son metinde hatalı örnek yok.

## H-012 — Doğrulayıcının hata önceliğini "soldan sağa" sanmak
2026-10-22, Claude (inceleme). CONTRACT uyum talimatında "birden fazla hata varsa mevcut soldan sağa öncelik korunur" yazıldı; ardından evre içi sıranın CONTRACT tablosuna göre değiştirilmesi önerildi. Yanlış varsayım: mevcut doğrulayıcının davranışı kod veya test okunmadan tahmin edildi. Gerçekte doğrulayıcı evreli çalışıyor (yapı → sayı biçimi → aralık). Codex SPEC 1.1.0 taslağını hazırlarken sordu; ilk yanıtta evre içi sıranın CONTRACT tablosuna göre değiştirilmesi de önerilmişti. Bu, uygulama ve aktarım öncesinde düzeltildi: "mevcut evreleri ve evre içi sırayı koru, yalnız belgele, sözleşme testleriyle doğrula". Codex taslaktaki yeniden sıralamayı geri aldı; mevcut sözleşme testleri 139/139 geçti (Codex raporu, 2026-10-22). CONTRACT hata önceliği tanımlamadığı için davranış değişikliği gerekmiyor. Kod değiştirilmedi.

## H-013 — NaN çıktılarını "farklı sonuç" saymak
2026-10-23, Claude (inceleme). CLI süre incelemesinde `scipy.special.nctdtr`'nin 3000 rastgele girdinin 290'ında `scipy.stats.nct.cdf`'ten farklı sonuç verdiği ve bu yolun motoru değiştireceği kullanıcıya bildirildi. Yanlış varsayım: karşılaştırma `!=` ile yapıldı; iki taraf da NaN döndürdüğünde NaN ≠ NaN olduğu için eşleşmeler fark sayıldı. NaN'ları eşit sayan karşılaştırmayla 20 000 girdide `nct.cdf`/`nctdtr`, `nct.sf`/`_nct_sf` ve `t.ppf`/`stdtrit` için fark 0 çıktı; SciPy 1.16.3 kaynağında `nct._cdf` zaten `nctdtr`'yi çağırıyor. Kullanıcı aynı gün düzeltildi; yanlış iddia Codex'e verilen bir talimata girmedi. Kod ve SPEC değiştirilmedi.

## H-014 — "Başarısızları çıkar" ile "N eşiğinin altı"nı aynı sanmak
2026-10-23, Claude (inceleme). README talimatında "N ≤ 3·10⁷ (gerçekçi bölge): a priori 77/77; uç bölge: 0/11" satırı önerildi. Yanlış varsayım: bilinen 11 uyuşmazlığı çıkarınca kalan 77 vektörün hepsinin N ≤ 3·10⁷ olduğu varsayıldı; eşik bölmesi gerçekte hesaplanmadı. Codex taslağı hazırlarken kayıtlardan hesapladı: N ≤ 3·10⁷ bölgesi 75/75, N > 3·10⁷ bölgesi 2/13 (GP-AP-045 N = 30 531 150 ve GP-AP-046 N = 43 288 698 eşleşiyor). İnceleme tarafı `oracle/contract_expectations.csv` ve `gpower_vectors.csv` ile aynı sonucu bağımsız olarak yeniden hesapladı. Yanlış satır README'ye girmeden düzeltildi; toplam 77/88 değişmedi. Kod, SPEC ve tolerans değiştirilmedi.

## H-015 — Dosyanın bir kısmını okuyup tamamı hakkında hüküm vermek
2026-10-23, Claude (inceleme). Genel denetimde yazım reposunun `.gitignore` dosyası `head -30` ile okunup "`experiments/` ve `SPEC_QUESTIONS.md` dışlanmıyor" diye yüksek önemli bulgu yazıldı. Yanlış varsayım: kesilmiş çıktının dosyanın tamamı olduğu. Dosya 39 satır; 31–39. satırlar `experiments/spec_1_0_3/` ve diğer 1.0.3 deney dosyalarını zaten dışlıyor. Codex aynı bulguyu kendi kaydıyla karşılaştırırken yakaladı. Düzeltme: dosyanın tamamı okundu; bulgunun yalnız `SPEC_QUESTIONS.md` kısmı geçerli kaldı ve denetim raporunda düzeltildi. Kod ve SPEC değiştirilmedi.
