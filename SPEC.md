# SPEC — t2-indep, resmî CONTRACT arayüzüne geçiş
Durum: READY_FOR_IMPLEMENTATION (resmî CONTRACT 1.0.0 ile; geçici kararlar Bölüm 14'te)
SPEC sürümü: 1.1.0
Tarih: 2026-10-22
Önceki aktarılmış sürüm: 1.0.4, SHA-256 `48f75233dfbdd19d4248d97fc24dd243d54f830ecd1ad50ec3a36fa4b644ad7d`.

Bu belge yeni arayüz ve veri geçişi taslağıdır. Henüz motor/CLI/MCP değişikliği yapılmadı; bu SPEC'in uygulanmış olduğu veya gizli testlerden geçtiği iddia edilmez. Resmî sözleşme ile aşağıdaki açık kullanıcı kararları farklı etiketlenir. Bölüm 15 yalnız tarihî inceleme bulgusudur; oradaki aday yöntemi uygulama talebi yoktur.

## 1. Kimlik, kapsam ve kaynak önceliği

- Hedef: G*Power 3.1.9.7 Windows, `GPowerNT.exe`, PE32 x86; hedef SHA-256 `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812`.
- Test: t tests → Means: Difference between two independent means (two groups), eşit varyanslı Student t testi; Welch yok. `t2-indep`; yalnız `a-priori` ve `post-hoc` uygulanır.
- **[CONTRACT]** Ders belgesi CONTRACT.md **1.0.0**, tarih 2026-10-21, SHA-256 **`4cbcc105a31f4b202f3e9a8d2cc0e9d4a8b94933997e47e3e00965f1f67f999f`**. Tam metin Bölüm 9 JSON başlığındaki `contract_document.text` içinde, UTF-8 olarak gömülüdür. Bu metni aynı UTF-8 baytlarıyla `docs/CONTRACT.md` yazmak serbesttir; özet doğrulanır. Bu ders belgesi ham binary/inceleme çıktısı değildir. Ayrı inceleme klasörüne erişmek gerekmez.
- CONTRACT dış arayüzü belirler. G*Power gözlemleri matematiksel davranışı belirler. Resmî girdi alanının dışı, GUI hesap üretmiş olsa da CLI tarafından reddedilir. Alan içindeki daha dar GUI retlerinin hata kodu aşağıda **[GEÇİCİ KARAR]** olarak ayrıca seçilmiştir.
- **[KULLANICI KAPSAMI]** Diğer dört aile ve `compromise`, `criterion`, `sensitivity` uygulanmaz; bu çağrılar `UNSUPPORTED` döndürür. Resmî 25 vektörde bu 23 ret CLI–MCP eşdeğerliği için sınanır; bunların sayısal altın sonuçlarını hesapladık diye sunulmaz. Ders yürütücüsünün bu kapsam yorumu teyit bekler.
- Yazım oturumu proje/binary bilgisi olarak yalnız bu onaylanacak SPEC'i kullanır. Gömmeli veri, resmî ders belgesi ve Bölüm 15'teki yayımlanmış kaynaklar izinlidir. Ham oracle, ekran, LEDGER, REA, eski ayrıntılı 1.0.3 reçetesi veya inceleme betikleri okunmaz. Kendi yazım kaynaklarının tarihçesi/ölçümleri korunur.
- **[ÖNKOŞUL DOĞRULANDI]** Python turu tamam: Windows 3.12.15 ve 3.13.16 son kaynaklarla 2078/2169, aynı 91 başarısız kimlik, 501 alanda sıfır fark. Aralık `>=3.12,<3.15`, varsayılan 3.14.8. Bu tarihî sonuç yeni 1.1.0 test sonucu değildir.

Etiketler: [GUI] ölçülmüş davranış; [REA] önceki soyut inceleme bulgusu, adresler aktarılmaz; [ÖDEV] eski ders metni; [CONTRACT] resmî 1.0.0 kuralı; [ÇIKARIM] ölçümlerden genelleme; [REGRESYON] eski sıkı ölçüt; [GEÇİCİ KARAR] bu taslakta açık kullanıcı tercihi, öğretim elemanı cevabı değildir. RULE-023…026'nın eski geçici sözleşmesi yerini bu belgeye bırakır; tarihî kopyalar silinmez.

## 2. Terimler ve gözlem/arayüz ayrımı

`d` Cohen etkisi; `alpha` I. tip hata; `power` AP hedef gücü veya PH hesaplanan güç; `actual_power` AP tamsayı gruplarla gerçekleşen güç; `N=n1+n2`; `ratio=N2/N1`; `df=N−2`; `ncp=δ`.

**Alan eşlemesi:** Eski matematik, GUI ve tarihî veride `critical` adı korunur; resmî CLI/MCP alanı **`critical_t`** olur. Bu birebir anahtar eşlemesidir; sayı, işaret, hassasiyet veya güç hesabı değişmez. Ham `expected/displayed/comparison` gözlemleri sırf yeni alan adı için yeniden yazılmaz; resmî çıktı beklentisi `cli_expectation` içinde ayrıca bulunur.

Signed d ve d=0 için önceki matematik gözlemi geçerlidir, fakat yeni resmî CLI girdisi d>0 ister. Negatif/sıfır GUI gözleminin korunması, CLI'nin bunları kabul etmesi anlamına gelmez.

## 3. Resmî CLI sözleşmesi — RULE-023

### 3.1 Kapsam ve çağrılar [CONTRACT]

Komut `gpower-clone`. Her alan ayrı `--alan değer` çiftiyle verilir; varsayılan yoktur. Ondalık ayırıcı nokta. Hesap çağrısı çevrimdışı ve deterministiktir. Log/uyarı stderr'e, sonuç stdout'a tek satır JSON yazılır. **Kodlama kuralı:** --version, başarı ve hata JSON'ları ASCII güvenli Unicode kaçışlarıyla serileştirilir; stdout baytları açıkça ASCII (UTF-8 ile aynı), BOM'suz yazılır. Windows konsol kod sayfası veya PYTHONIOENCODING veri baytlarını değiştirmemeli. İnsan açıklamalarındaki Türkçe karakterler JSON çözümlendiğinde aynen korunur. MCP text JSON'u da aynı serileştirme ilkesini kullanır; dosya günlükleri açıkça UTF-8 açılır. Bu bir arayüz/serileştirme şartıdır; hesap motorunu değiştirmez.

| Mod | Gerekli alanlar (test/mode dahil) | Başarı alanları |
|---|---|---|
| a-priori | test, mode, tails, d, alpha, power, ratio | ncp, critical_t, df, n1, n2, n_total, actual_power |
| post-hoc | test, mode, tails, d, alpha, n1, n2 | ncp, critical_t, df, power |

Başarı exit=0. JSON anahtar sırası semantik değildir; ek alanlar CONTRACT tarafından serbesttir, fakat bu projede gereksiz değişken alan eklenmez. Tamsayılar JSON integer, ondalıklar tam double hassasiyetle yazılır; `critical` zorunlu `critical_t` alanının yerine kullanılamaz.

Örnekler:

```text
gpower-clone --test t2-indep --mode a-priori --tails 2 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1
gpower-clone --test t2-indep --mode post-hoc --tails 2 --d 0.5 --alpha 0.05 --n1 105 --n2 105
```

Bu girdilerde ncp≈3.6228442, critical_t≈1.9714347, df=208; AP 105/105/210 ve actual_power≈0.9501287, PH power≈0.9501287. Bu sayılar erken yuvarlanarak yazılmaz.

### 3.2 --version [CONTRACT; ayrıntılar proje kararı]

Yalnız `gpower-clone --version`: exit=0 ve tek satır JSON:

```json
{"contract_version":"1.0.0","name":"Takim 20 - Ismail Burak Yilmaz","engine":"Python <gerçek çalışma sürümü>"}
```

`name` tam olarak **`Takim 20 - Ismail Burak Yilmaz`** olur; kullanıcı bu adı kesinleştirmiştir. `engine` gerçek yorumlayıcıyı belirtir, sabit 3.14 yazılmaz. `--version` ile başka bayrak birlikte gelirse `UNKNOWN_PARAM`, field ilk ek bayrak adı (tire olmadan). Bu ayrıntı CONTRACT tarafından belirlenmediğinden [GEÇİCİ KARAR]dır.

### 3.3 Başarı JSON'u ve ham motor

CLI/MCP adaptörü ham motorun `critical` sonucunu `critical_t` anahtarına eşler. Engine hesap yordamları, N araması, yuvarlama, df, dağılım veya SciPy sürümü değiştirilmez. Özellikle mevcut engine `calculate` fonksiyonu eski `contract.validate_values` yordamını çağırdığı için, ortak iç doğrulayıcıya yeni d/n sınırları ekleyip eski matematik regresyonunu dolaylı biçimde kesmek yasaktır. Yeni resmî giriş denetimi CLI/MCP adaptör katmanında ortak bir yordam olarak uygulanabilir; eski iç motor alanı ve negatif/sıfır gözlem testleri korunur.

### 3.4 Resmî ve gözlenen girdi alanı [CONTRACT + açık geçici eşleme]

| Alan | Resmî girdi alanı | Ölçülen daha dar GUI kabulü / proje davranışı |
|---|---|---|
| tails | integer 1 veya 2 | 3 gibi başka integer → OUT_OF_RANGE; sözcük/ondalık → INVALID_VALUE |
| d | >0 | AP 1e-5≤d≤20; PH 0<d≤20. Negatif ve sıfır → OUT_OF_RANGE; pozitif GUI retleri de geçici OUT_OF_RANGE |
| alpha | 0<alpha<1 | 1e-7≤alpha<1; daha küçük pozitif değer geçici OUT_OF_RANGE |
| power | 0<power<1 | 1e-7≤power<1; power<alpha → INCONSISTENT; eşitlik kabul |
| ratio | >0 | 0.01≤ratio≤100; daha dar alan dışı geçici OUT_OF_RANGE |
| n1,n2 (PH girdisi) | integer ≥2 | toplam≤2147483646; aşılırsa geçici OUT_OF_RANGE, field=n_total |

Bu tablo aralık evresine ulaşmış girdiler içindir. PH grup alanında işaretli tam sayı metni biçim evresini geçer; `-1`, `0` ve `1` aralık evresinde OUT_OF_RANGE olur. `2.0`, `2e0` veya sayı olmayan metin INVALID_VALUE kalır. Bu, CONTRACT 2.4 ve 5 dayanaklı **arayüz davranış değişikliğidir** (Bölüm 6.5); yeni aralık sınırları biçim denetiminin önüne taşınmaz.

AP girdisi n1/n2 almaz. AP sonucunda n1 veya n2 **0 veya 1** olabilir; GUI'deki gibi başarı JSON'u korunur. `actual_power` hedefin altında veya alpha'ya eşit olabilir; NO_SOLUTION'a dönüştürülmez. Bu çıktıların sayıları için yeni fiziksel/klinik doğrulama eklenmez.

## 4. Matematiksel davranış — hesap motoru değişmez
N = n1 + n2. Formüller gözlenen davranışın soyut tanımıdır.

### 4.1 Kural dizini
| RULE | Kısa tanım | Destek |
|---|---|---|
| RULE-001 | Test kimliği ve GUI seçimi (Bölüm 1) | [REA][GUI] |
| RULE-002 | α ve güç aralıkları; güç ≥ α (Bölüm 6.2) | [REA][GUI] |
| RULE-003 | d aralığı ve a priori mutlak d alt sınırı (Bölüm 6.2) | [REA][GUI] |
| RULE-004 | Oran aralığı (Bölüm 6.2) | [REA][GUI] |
| RULE-005 | Post hoc grup ve toplam N sınırları; kesirli n (Bölüm 6) | [REA][GUI] |
| RULE-006 | df = N − 2 | [REA][GUI] |
| RULE-007 | δ = d·√(n1·n2/N) | [REA][GUI] |
| RULE-008 | Kritik değer ve işaret | [GUI][ÇIKARIM] |
| RULE-009 | Güç formülü | [GUI][ÇIKARIM] |
| RULE-010 | A priori toplam N seçimi | [GUI][ÇIKARIM] |
| RULE-011 | A priori grup dağıtımı | [GUI][ÇIKARIM] |
| RULE-012 | Çıktılar tamsayı n ile; actual_power hedef altı olabilir | [GUI] |
| RULE-013 | En küçük N ve dejenere sonuç | [GUI] |
| RULE-014 | G*Power gösterim biçimi | [GUI] |
| RULE-015 | G*Power varsayılanları | [REA][GUI] |
| RULE-016 | Çok küçük mutlak d'de G*Power'ın hedef altı sonucu | [GUI] |
| RULE-017 | Post hoc n1 ↔ n2 değişmezliği | [GUI] |
| RULE-018 | G*Power bozuk sayı metnini önek olarak okur (yalnız GUI gözlemi) | [GUI] |
| RULE-020 | Tarihî ödev örneği; resmî çıktı alanları Bölüm 3 ile üstün gelir | [ÖDEV][CONTRACT] |
| RULE-021 | Hata JSON'u error/code/field; exit 2 veya 1 (Bölüm 6.4) | [CONTRACT][GEÇİCİ KARAR] |
| RULE-022 | Karşılaştırma ölçütü: N/n1/n2 tam; diğerleri gösterilen basamağa kadar | [ÖDEV] |
| RULE-023 | Resmî AP/PH CLI; critical_t, --version, kapsam (Bölüm 3) | [CONTRACT] |
| RULE-024 | Tam double ve iki ayrı sayısal karşılaştırma (Bölüm 7) | [CONTRACT][REGRESYON] |
| RULE-025 | Hata code/field ve exit 2/1; açık geçici kod eşlemeleri (Bölüm 6.4) | [CONTRACT][GEÇİCİ KARAR] |
| RULE-026 | Resmî giriş alanı, biçim, sabit doğrulama evre/sırası (Bölüm 6.4) | [CONTRACT][GEÇİCİ KARAR] |
| RULE-027 | Yayımlanmış sayısal yöntem adayı ve kaynakları (Bölüm 15.1) | [DOK; proje adayı] |
| RULE-028 | Aralık, durma, yuvarlama gözlemleri ve aday parametreler (Bölüm 15.2) | [REA; proje adayı ayrı] |

### 4.2 Tanımlar
- **RULE-006** `df = N − 2`. 87 vektörün tamamında doğru.
- **RULE-007** `δ = d · √( n1·n2 / (n1 + n2) )`; işaret d'nin işaretidir. Tam sıfır d veya bir grubun 0 olduğu dejenere durumda δ = 0 (Bölüm 5).
- **RULE-008 — Kritik değer** (k = tails, s yön işareti):
  `critical = s · Q_t( 1 − α/k ; df )`.
  Sonuçlar: α < 0.5 tek yönlü ve tüm iki yönlü durumlarda |critical| pozitif bir eşik, işaret s'yi izler. **Tek yönlü α > 0.5'te Q_t(1−α) negatiftir; bu yüzden d > 0 iken critical negatif, d < 0 iken pozitif gösterilir** (GP-PH-027/028, GP-AP-026/027). Tek yönlü α = 0.5'te gerçek değer 0'dır; G*Power sayısal gürültüyü pozitif bilimsel gösterimle yazar (6.6818e-17, 6.805748e-17) ve d < 0'da da işaret değişmez (GP-PH-024/025/026, GP-AP-025). d = 0'da s = +1 (GP-PH-022/023/026/029).
- **RULE-009 — Güç**, T′ ~ merkezi olmayan t(df, δ), c = gösterilen işaretli critical:
  - Tek yönlü: s = +1 ise `power = 1 − F_nct(c; df, δ)`; s = −1 ise `power = F_nct(c; df, δ)`. (Ret bölgesi d yönünde, c'nin ötesi.)
  - İki yönlü: `power = 1 − F_nct(|c|; df, δ) + F_nct(−|c|; df, δ)`.
  - d = 0'da her iki yönde güç = α (GP-PH-022/023/026/029). d'nin işaretinin değişmesi gücü değiştirmez (GP-PH-017/018, 025, 028, 031; GP-AP-017/018, 027).
  - **Hassasiyet:** güç hesabında kullanılan c, kuantilin **tam hassasiyetli** değeridir (Q_t'nin double sonucu). Ekranda 7 ondalığa yuvarlanmış critical veya JSON'a yazılmış metin güç hesabına geri beslenmez. Çıktıdaki `critical` alanı da bu tam hassasiyetli değerdir.
  - Bu formüllerin iç sayısal yöntemi 1.0.3 Bölüm 15 ile genişletildi; toleranslar ve referanslar korunur.
- **RULE-017** Post hoc'ta n1 ↔ n2 yer değişimi çıktıları değiştirmez (GP-PH-007/008, 009/010).
- **RULE-014 — Gösterim** [GUI] (yalnız G*Power ekran/protokol biçimi; CLI serileştirmesi değildir):
  - Tipik büyüklükte değerler sabit 7 ondalık (0.9501287; 63.2455532).
  - Çok küçük büyüklükler en çok 7 anlamlı basamaklı bilimsel gösterim, sondaki sıfırlar atılmış (3.05715e-05, 1.261586e-07, 1.25e-07, 6.6818e-17).
  - Büyük değerler 7 anlamlı basamak (11585.24; 3162.277).
  - Tam sıfır "0".
  - Biçimlerin geçiş eşikleri belirlenmedi (açık sınır). Karşılaştırma kuralı her vektörde gösterilen metinden türetildiği için bu belirsizlik karşılaştırmayı etkilemez (Bölüm 7).

## 5. A priori örneklem seçimi
- **RULE-010 — Toplam N** [GUI][ÇIKARIM]: Gözlenen **34 a priori sonucun tamamında N çifttir.** Seçilen N, sürekli bölünmeyle (n1c = N/(1+r), n2c = N·r/(1+r)) hedef güce ulaşan **en küçük çift** tamsayı gibi davranır.
  - Destek: GP-PH-020'de tek toplam 12561 (6280/6281) güç 0.8000282 ile hedefi sağlıyor; G*Power a priori (GP-AP-014) yine 12562 döndürüyor.
  - Minimalite **yalnız üç çiftte** doğrudan sınandı: GP-AP-002/GP-PH-012 (87/87 → 0.9494829 < 0.95), GP-AP-023/GP-PH-021 (42/126 → 0.7967341 < 0.8), GP-AP-014/GP-PH-020 (yukarıdaki tek toplam). Kesirli tahsisli adayların sürekli gücü GUI'de doğrudan ölçülemez.
  - **SINIR:** Bu kural gözlem genellemesidir. 1.0.3 Bölüm 15.2 arama yolunu ve yuvarlamayı tanımlar; tam bit eşitliği ve denenmemiş girdilerde garanti yoktur.
  - **Ölçülen geçerlilik alanı (1.0.2, Tur 3)** [GUI]: Küçük d ölçümlerinde (GP-AP-035…051) toplam N ≤ 30 531 150 olan 6 durumun 6'sında G*Power'ın N'i bu kuralla aynıdır. Toplam N ≥ 31 395 446 olan 13 ölçümün 12'sinde (GP-AP-019 ve 028 dahil) G*Power'ın N'i bu kuralın verdiği N'den farklıdır; fark N < 2·10⁸'de ±2…+6, daha büyük N'de +16'dan ±2,5·10⁷'ye kadardır. İstisna GP-AP-046'dır (güç 0.95, N = 43 288 698, eşleşir); ölçülen veride kesin bir N eşiği yoktur. Sapmanın nedeni bilinmiyor; bu alanda G*Power'ın değerleri yine **tam eşleşme hedefidir** ve kural için özel eşik, katsayı veya tablo eklenmez (Bölüm 10).
- **RULE-011 — Grup dağıtımı** [GUI][ÇIKARIM]: `n1 = round_half_up( N/(1+r) )`, `n2 = N − n1`.
  - Destek: 49.6→50, 72.94→73, 31.74→32, 268.8→269, 67.2→67; yarımlarda 42.5→43, 35.5→36, 52.5→53 ve n2 kalan. GP-AP-023 (r = 3, N = 170) → 43/127.
  - **Ayna yalnız gözlenen çiftlerde geçerlidir:** 2↔0.5, 4↔0.25, 100↔0.01 (GP-AP-007/008, 010/011, 020/021). **Genel kural değildir:** r = 0.3333333 (GUI'ye yazılan metin; 1/3'ün yedi ondalığa kesilmişi) N = 170 için **128/42** verir, 127/43 değil (GP-AP-032). Bu, kuralın öngörüsüyle aynıdır (170/1.3333333 = 127.50000…→128). "1/3" metni kesir olarak değerlendirilmez (RULE-018), bu yüzden tam 1/3 GUI'de girilemez.
  - Grup simetrisi tüm a priori girdilere test özelliği olarak uygulanmaz.
- **RULE-012** δ, critical, df ve actual_power seçilen tamsayı n1, n2 ile hesaplanır; actual_power hedefin altında kalabilir: GP-AP-010/011 (269/67 → 0.8995119 < 0.9), GP-AP-032 (128/42 → 0.7983302 < 0.8). GP-PH-013 aynı gücü post hoc'ta üretir.
- **RULE-013** Toplam N alt sınırı 3'tür, fakat a priori'de gözlenen en küçük toplam 4'tür (GP-AP-016, GP-AP-029, GP-AP-033). Dejenere: güç = α ve r = 100 → n1 = round(4/101) = 0, n2 = 4, δ = 0, actual_power 0.0500000 (GP-AP-024). Bu G*Power'ın ürettiği, grup büyüklüğü 0 olan bir sonuçtur (aynı n1 = 0 post hoc'ta reddedilir). Beklenen değer budur ve CLI de 0/4 sonucunu (n1 = 0, n2 = 4) hata vermeden üretir **[GEÇİCİ SÖZLEŞME]**; motor farklı üretirse uyumsuzluk sayılır.
- **RULE-016** d = 0.00001'de G*Power'ın döndürdüğü N (123638443832/grup) için actual_power 0.7999212 < 0.8 (GP-AP-019). Nedeni olarak "aramanın sayısal duyarlığı" yalnız **teşhis hipotezidir**, kanıtlanmış iç mekanizma değildir. Komşu d = −0.0000101'de sonuç hedefin üstündedir (GP-AP-028, 0.8000690). GP-AP-019'un beklenen N/n1/n2 değerleri de **tam eşleşme hedefidir**; motor eşleşmezse açık uyumsuzluk olarak sayılır (Bölüm 7.3). 2026-10-20'de GP-AP-019 ve GP-AP-028 aynı girdilerle birebir yeniden üretildi; G*Power bu girdilerde deterministiktir. Gösterilen actual_power'ın aynı gruplarla bağımsız hesaplanan güçten farkı N ≤ ~10⁸'de gösterim yuvarlaması içinde kalır, daha büyük N'de büyür (GP-AP-019'da ~4·10⁻⁵).


## 6. GUI gözlemi ve resmî hata katmanı

### 6.1 Post hoc gözlemi

Ham hesap girdileri tails,d,alpha,n1,n2 ve çıktıları critical/ncp/df/power'dır. Eski GUI tek kişilik grup veya d=0/negatif ile hesap yapabilir; aşağıdaki gözlem tablosu bunu kaydeder. Yeni CLI alanı Bölüm 3.4'te daha dardır. Kesirli n'yi GUI'nin yuvarlaması CLI'ye taşınmaz; CLI integer biçimi ister. Input kısıtları çıktıya otomatik uygulanmaz.

### 6.2 Girdi sınırları (G*Power gözlemi)
Hata metinleri G*Power'ın modal "Input error" metinleridir. Mesajdaki parantez gösterimi matematiksel açık/kapalı aralık anlamı taşımaz; kabul/red **ölçülen** davranıştır.

| Girdi | Mod | Kabul edilen ölçüm | Reddedilen ölçüm | G*Power metni | Sonuç aralığı |
|---|---|---|---|---|---|
| α | post hoc | 0.0000001 (GP-PH-032), 0.9999999 (GP-PH-033) | 0.000000099 (INV-GUI-014), 0 ve 1 (INV-GUI-009/010) | "Alpha is outside the admissible range (1e-07, 1)." | 1e-7 ≤ α < 1 |
| güç | a priori | 0.0000001 (GP-AP-033), 0.9999999 (GP-AP-034) | 1 (INV-GUI-011) | "Power is outside the admissible range (1e-07, 1)." | 1e-7 ≤ güç < 1 |
| güç − α | a priori | güç = α (GP-AP-016), α + 1e-7 (GP-AP-029) | α − 1e-7 (INV-GUI-019), 0.03 < 0.05 (INV-GUI-002) | "Power must be greater than or equal to alpha." | güç ≥ α |
| mutlak d | a priori | 0.00001 (GP-AP-019), 0.0000101 (GP-AP-028) | 0 (INV-GUI-003), 0.0000099 (INV-GUI-018) | "In an a priori analysis, the absolute value of the effect size must be greater than 0.00001." | mutlak d ≥ 0.00001 |
| d | post hoc | 20 (GP-PH-034), −20 (GP-PH-035) | 20.01 (INV-GUI-015), −20.01 (INV-GUI-016), 21 (INV-GUI-008) | "Effect size d is outside the admissible range (-20, 20)." | −20 ≤ d ≤ 20 |
| r | a priori | 0.01, 0.0101, 99.99, 100 (GP-AP-021, 030, 031, 020) | 0, 0.0099, 100.01, 101 (INV-GUI-012, 020, 021, 013) | "The allocation ratio falls outside the admissible range (0.01, 100)." | 0.01 ≤ r ≤ 100 |
| n1, n2 | post hoc | 1 (GP-PH-019) | 0 (INV-GUI-005) | "Sample size must be greater than or equal to 1." | n ≥ 1 |
| N | post hoc | 3 (GP-PH-019), 2147483646 (GP-PH-036) | 2 (INV-GUI-004), 2147483647 (INV-GUI-017) | "Total sample size is outside the admissible range (3, 2147483646)" | 3 ≤ N ≤ 2147483646 |

**Denenmemiş / açık sınırlar:** α ve gücün 1'e 1e-7'den daha yakın değerleri (ör. 0.99999999); d aralığının a priori modda ±20'de ölçümü (yalnız post hoc ölçüldü); a priori'de N üst sınırına yaklaşan durumlar ve büyük hesaplarda süre; negatif oran (ölçülmedi). Ölçülemeyen uçlar belirsiz kalır.

### 6.3 Bozuk metin ve dönüşümler (yalnız GUI gözlemi)
- **RULE-018** [GUI]: G*Power alandaki baştaki geçerli sayısal öneki okur ve hata vermez: "0.050.05" → 0.05, "0.950.95" → 0.95 (INV-GUI-001); "1/3" → 1 (INV-GUI-022, ifade değerlendirilmez).
- Girdi gözlemlerinin sınıflaması (22): **18 GUI reddi**, **2 kesirli-n dönüşümü** (INV-GUI-006/007), **2 bozuk metnin kabulü** (INV-GUI-001, INV-GUI-022).
- Bu davranışlar CLI için örnek alınmaz. CLI bu dört girdinin tamamını reddeder (E_NOT_A_NUMBER veya E_NOT_INTEGER) **[GEÇİCİ SÖZLEŞME]**.



### 6.4 Hata JSON'u ve eşleme — RULE-025

Proje çıktısı her hatada `error`, `code`, `field` içerir. `error` boş olmayan Türkçe/İngilizce insan açıklamasıdır; eski sabit İngilizce metinleri resmî zorunluluk sayılmaz. `code` aşağıdaki sabit semboldür. `field` mümkünse tire olmadan alan adı, bir alan suçlanamıyorsa null olur. CLI ve MCP **aynı girdide aynı JSON nesnesini**, aynı insan açıklamasıyla üretir.

| Durum | code | exit | field | Dayanak |
|---|---|---:|---|---|
| Eksik alan veya eksik değer | MISSING_PARAM | 2 | eksik alan | CONTRACT; sıra ayrıntısı geçici |
| Tanınmayan, tekrar eden veya modla ilgisiz alan | UNKNOWN_PARAM | 2 | alan adı | CONTRACT + tekrar politikası geçici |
| Sayı değil, yanlış tür, integer yerine ondalık, NaN/Infinity/bozuk metin | INVALID_VALUE | 2 | alan adı | CONTRACT + sözdizimi proje kararı |
| CONTRACT dışı değer; tails=3 | OUT_OF_RANGE | 2 | ilk aralık hatalı alan | CONTRACT |
| CONTRACT alanı içinde ama GUI'nin daha dar retleri | OUT_OF_RANGE | 2 | ilgili alan; toplam için n_total | **GEÇİCİ KARAR; resmî tanımdan daha geniş kullanım** |
| AP power<alpha | INCONSISTENT | 2 | power | GUI + kullanıcı kararı |
| Bilinmeyen/desteklenmeyen aile | UNSUPPORTED | 2 | test | CONTRACT + proje kapsamı |
| Bilinmeyen/desteklenmeyen mod | UNSUPPORTED | 2 | mode | CONTRACT + proje kapsamı |
| Bizim hesabımız sonlu sonuç üretemedi / iç hata | NO_SOLUTION | 1 | null | **GEÇİCİ KARAR; K-07/K-08 yanıtı bekleniyor** |

Son satır resmî NO_SOLUTION tanımıyla aynı değildir: CONTRACT bu kodu G*Power'ın da sonuç üretemediği durum için tanımlar. Kullanıcı bu tur kendi sayısal başarısızlığımız için de exit=1/NO_SOLUTION seçmiştir. Bu uyarlama resmî teyit edilmiş diye sunulmaz; oracle başarısızlığı kanıtlanmış diye yazılmaz. Beklenmeyen programlama hataları başarıya veya uydurma sayıya çevrilmez; açıklama JSON'u ve stderr kaydıyla iç hata olarak görünür. Yeni hata kodu uydurulmaz.

### 6.5 Biçim ve doğrulama önceliği — RULE-026

**[KORU VE BELGELE]** Destekli `t2-indep` + `a-priori`/`post-hoc` çağrılarında mevcut evreler ve her evrenin iç sırası korunur. CONTRACT tablo sırası yeni bir öncelik kuralı değildir; önceki taslağın bu varsayımı geri alınmıştır. CONTRACT öncelik tanımlamıyor. Mevcut davranış aşağıdaki gibidir; README Varsayımlar'a da böyle yazılır.

**[DAVRANIŞ DEĞİŞİKLİĞİ — kullanıcı onayı 2026-10-22]** Destek denetimi ayrı bir erken geçit olur: önce test/mod kimliği değerlendirilir. `test!=t2-indep` ise code=UNSUPPORTED, field=test, exit=2; test destekli ama mod AP/PH dışında ise code=UNSUPPORTED, field=mode, exit=2. İkisi de destek dışıysa test seçilir. Destek dışı kimlik belirlendiğinde diğer bayrakların bilinmeyen, eksik veya sayısal olarak bozuk olması bu sonucu değiştirmez; motor çağrılmaz. Kimlik eksik/değeri yok/yinelenmiş olduğundan tekil belirlenemiyorsa mevcut yapısal hata davranışı korunur. Bu geçit eski doğrulayıcının davranışı diye sunulmaz. Dayanak CONTRACT 2.4 hata tablosu, Bölüm 7/9 eşdeğerliği ve kullanıcının 23 açık vektör için kapsam kararıdır. MCP şeması bu değerleri önce SDK hatasına çevirmez; aynı UNSUPPORTED JSON'unu üreten geçide ulaştırır.

Erken geçitten geçen destekli çağrıların **mevcut** sırası:

1. CLI bayrak/değer çiftleri argv sırasıyla taranır. Bilinmeyen/yinelenen ad, ardından o bayrağın eksik değeri denetlenir; ilk hata seçilir. `--alpha=0.05` desteklenmez. Tanınan adlar test,mode,tails,d,alpha,power,ratio,n1,n2 olarak kalır; sırf başka ailenin public girdisinde var diye destekli çağrının izinli adları genişletilmez.
2. Yapı denetiminde tanınmayan adlar girdi eklenme sırasıyla denetlenir; eksikler test,mode,tails,d,alpha, ardından bilinen modun power,ratio veya n1,n2 sırasıyla denetlenir. Bundan sonra modla ilgisiz bilinen alanlar **girdi eklenme sırasıyla** denetlenir; tablo/sözlük sırasıyla sıralanmaz. CLI'de bu sıra argv'dir; tipli MCP nesnesinde çözümlenen anahtarların eklenme sırasıdır, kanonikleştirilmez. Eski destek denetimi bu yapı kontrollerinden sonraydı; yalnız yukarıdaki onaylı destek dışı geçidi bunu değiştirir.
3. Sayı metni/türü denetimi mevcut tails,d,alpha,power,ratio,n1,n2 sırasıyla, bulunmayan alanlar atlanarak yapılır. Destekli AP'de etkili sıra tails,d,alpha,power,ratio; PH'de tails,d,alpha,n1,n2 olur. Bu **kodda bulunan sıranın kaydıdır**, CONTRACT'tan türetilmiş yeni sıra değildir. Tüm sayı biçimi/türü hataları aralık kontrollerinden önce seçilir. CLI metin dönüşümünden sonra tipli doğrulayıcının yapı/tür denetimini yeniden yapması da korunur.
4. Aralık ve çapraz kontrollerin mevcut sırası: önce tails, d, alpha. AP'de ardından power aralığı, ratio aralığı, power>=alpha, a priori küçük-d sınırı. PH'de ardından **birleşik grup alt sınırı denetimi**, sonra toplam N sınırı. PH grup denetimi bağımsız alanlara sıralanmış yeni bir evreye dönüştürülmez.

**[DEĞİŞİKLİK; resmî girdi alanı]** Bölüm 3.4'teki d>0 ve PH n>=2 sınırları ilgili mevcut denetim konumlarında uygulanır; eski motorun kendi alanı korunur. Eşik değiştiği için daha önce geçen bir alan artık erken hata verebilir: d=0 ve power<alpha için eski CLI power koşulunda dururken yeni resmî adaptör d aralığında durur. Bu fark bir sıra değişikliği veya eski davranışla tam eşitlik diye sunulmaz. Sıra doğrulamasında ortak kabul/ret alanındaki vakalar ve açıkça değişen sınırlar ayrı değerlendirilir.

**[DAVRANIŞ DEĞİŞİKLİĞİ — kullanıcı onayı 2026-10-22; CONTRACT 2.4 ve 5]** PH n1/n2 metni artık isteğe bağlı `+`/`-` işareti ve ardından rakamlarla integer kabul edilir. `-1`, `-0`, `0`, `+0`, `+1`, `1` biçim evresini geçer, grup alt sınırında OUT_OF_RANGE olur; `+2` geçerli grup girdisidir. Ondalık `2.0`, üs biçimi `2e0`, NaN/Infinity/boş veya sayı olmayan metin INVALID_VALUE kalır. Tipli MCP integer değerleri negatifken de biçim evresini geçer, aralıkta reddedilir; bool veya JSON float integer kabul edilmez. Eski iç motorun işaretsiz grameri/tür kontrolü değişmez; bu genişleme yalnız resmî arayüz adaptöründedir. Büyük işaretli integer metinlerinin güvenli dönüşümü, daha sonraki biçim hatalarının aralık hatalarından önce bulunmasını engellemez. Diğer biçim kuralları korunur: ondalıkta işaret/nokta/bilimsel üs serbest, tails işaretli integer olabilir. Evre ve evre içi kontrol sırası değişmez; yalnız integer kabulü değişir. Örneğin alpha aralık dışı ve n1=-1 birlikteyse artık önce alpha aralık hatası seçilir; n2 bozuk metinse onun biçim hatası bütün aralık hatalarından önce gelir. Bu ilk-hata farkı onaylı biçim değişikliğinin sonucudur.

**field yeni çıktı alanıdır:** Eski uygulama yalnız hata kategorisi/açıklaması üretiyordu; eski bir field çıktısı varmış gibi raporlanmaz. Tek alanlı ilk mevcut hata koşulundan alan adı türetilir. Birleşik PH alt sınırı koşulunda hangi grup sınırı ihlal ediyorsa o seçilir; ikisi de ihlal ediyorsa n1 seçimi **açık proje eşleme kararıdır**, yeni kontrol sırası değildir. Toplam hatasında türetilmiş n_total, iç hatada null kullanılır. Destek geçidinde test/mod seçimi yukarıdaki onaylı değişikliktir.

Örnekler: ratio eksik ve n1 ekli destekli AP → MISSING_PARAM/ratio; ikinci d → UNKNOWN_PARAM/d. Destekli AP'ye önce n2 sonra n1 eklendiyse UNKNOWN_PARAM/n2; eklenme sırası tersse UNKNOWN_PARAM/n1. Sayı biçiminde ters argv ile d=-0.5 ve alpha=NaN → INVALID_VALUE/alpha; tails=3 ile d=0 → OUT_OF_RANGE/tails. d=9e-6 ve power<alpha → INCONSISTENT/power. Hiç argüman yok → MISSING_PARAM/test. Dolayısıyla **bütün hata önceliği argv'den bağımsızdır denmez**; bu bağımsızlık yalnız sabit sıra kullanan değer denetimleri içindir.

**Mevcut davranışın doğrulaması (2026-10-22):** Mevcut tests/test_contract.py ve tests/test_spec_1_0_1.py dosyaları değiştirilmeden 139 test geçti; 0 başarısız/hata/atlanan. Ayrıca 19 salt okuma yoklamasıyla yapı sırası, sayı/aralık ayrımı, işaretsiz grup biçimi ve eski destek denetiminin yeri doğrulandı. Kaynak hash'leri aynı kaldı. Bunlar eski uygulama sırasının kanıtıdır; yeni code/field, resmî sınırlar ve erken destek geçidinin uygulanıp sınandığı anlamına gelmez. Destekli çağrılar için tarihî test girdileri/ilk hata kimliği korunmalı; onaylı sınır/JSON değişiklikleri aktif testlerde ayrı belgelenmeli. 23 destek dışı public vektörde CLI ve MCP'nin aynı UNSUPPORTED JSON'unu vermesi **yeni geçidin** kabul testidir.

## 7. Karşılaştırma ve serileştirme — RULE-024

### 7.1 Motor düzeyi uyum ölçütü (G*Power'a karşı)
**RULE-022** [ÖDEV]: N, n1, n2 tam eşleşir; diğer değerler G*Power'ın gösterdiği basamağa kadar eşleşir. Her vektörün `comparison` alanı, **G*Power'ın gösterdiği metinden** türetilen alan bazında kuralı taşır:

| Kural | Hangi gösterim | Ölçüt | Örnek |
|---|---|---|---|
| `exact_integer` | n1, n2, n_total, df | tam eşitlik | 105 |
| `exact_zero` | "0" gösterilen değer | değer tam 0 (tolerans yok) | GP-AP-024 ncp |
| `displayed_decimals` | sabit ondalıklı metin, k ondalık | mutlak fark ≤ 0.5·10^(−k) | 0.9501287 → 5e-8; 11585.24 → 0.005 |
| `displayed_significant_scientific` | m.mmm…e±x metni | mutlak fark ≤ 0.5·10^(x − mantissa ondalık sayısı) | 3.05715e-05 → 5e-11 |

- Sıfır gösterilen ncp için kesin sıfır gerekir; "0" yazımı yarım birimlik hatayı meşrulaştırmaz.
- Toleranslar genişletilmez; kural değişikliği yeni SPEC sürümü ve gerekçe ister.
- **Zor alanlar:** α = 0.5 tek yönlü vektörlerde (GP-PH-024/025/026, GP-AP-025) critical gerçekte 0'dır ve G*Power sayısal gürültü gösterir (6.6818e-17). **[TARİHÎ SIKI REGRESYON]** Mevcut sıkı karşılaştırma korunur: beklenen değer gösterilen metindir; motor 0 veya farklı bir gürültü üretirse alan **açık uyumsuzluk** olarak raporlanır, gizlenmez ve tolerans genişletilmez.



Bu sıkı gösterim testi **korunmuş motor/GUI regresyonudur**. Raw anahtar critical ve resmî anahtar critical_t aynı sayıya eşlenir; `comparison` değerleri değiştirilmez. 22 GUI hesabının CLI'den reddedilmesi, eski motor gözleminin silinmesini gerektirmez.

### 7.2 Resmî CONTRACT karşılaştırması [CONTRACT; göreli formül proje kararı]

Tamsayılar n1,n2,n_total,df tam eşit. Ondalıklar için **abs(actual-reference)≤1e-6 VEYA abs(actual-reference)≤1e-6·abs(reference)**. Göreli payda abs(reference) seçimi CONTRACT'ın yazmadığı ayrıntı için kullanıcı/proje kararıdır. Reference=0 durumunda mutlak dal yeterlidir. NaN/Infinity eşleşmez. Bu kurallar gömülü `contract_numeric_rule` içinde ayrı bulunur ve başarılı `cli_expectation` buna atıf yapar; eski sıkı `comparison` üzerine yazılmaz. Medyan critical'ında 0 ile GUI gürültüsü resmî toleransta eşleşebilir; sıkı ölçütte fark olarak kalır.

### 7.3 Serileştirme ve rapor paydaları

Ondalıklar en kısa geri okunabilir tam double gösterimiyle, erken yuvarlama olmadan yazılır; tamsayılar integer'dır. Eski dört ondalıklı ödev örneği tarihî karşılaştırmadır; yeni stdout'u dört ondalığa yuvarlama zorunluluğu yoktur. Q-1/Q-2 resmî AP/PH tablosu ve tam double kuralıyla cevaplanmıştır.

Raporlar **eski 87**, **Tur 6**, **Tur 7**, **Tur 8**, yeni 55 birleşimi ve bütün GUI 142 için ayrı tutulur. Her kümede AP tahsisi, PH güç, yardımcı alanlar, sıkı ve resmî tolerans ayrı sayılır. 142 GUI hesabının hepsi ham motor/regresyon paydasındadır; 22'si resmî giriş dışı olduğundan CLI sayısal paydasına değil ret testlerine girer. Alan içi CLI sayısal payda **120 (88 AP, 32 PH)**, CLI hata vakası **47 (22+25)**. 25 açık MCP/CLI vektörü ayrı eşdeğerlik paydasıdır; motor GUI sayısını artırmaz.

Hata beklenen vakada error/code/field ve exit proje beklentisine göre sınanır. 22 ret motorun eski N başarısızlıklarını silmek veya GUI başarısını yükseltmek için kullanılmaz. Hata beklenmeyen çağrıda parse hatası, timeout, eksik çıktı, iç hata başarısızdır; ayrı sayılır. CONTRACT %90 kapısı **gizli AP N alanlarında** geçerlidir; yerel oran kapının geçtiğini kanıtlamaz. Yerel vaka başarısı için N,n1,n2'nin tümünün eşleşmesi aranır; resmî payda yorumu henüz sorular arasındadır.

## 8. Gherkin ve test göçü

Aşağıdaki kabul kriterleri 1.1.0 hedefidir; yapılmış test sonucu değildir. Eski AC-01…018 ve fixture/ölçümler tarihî kopyada korunur. Resmî CLI beklentileri yeni şemaya güncellenirken eski numeric gözlemler değiştirilmez. Yeni API'yi geçirmek için engine testi, başarısız oracle, tolerans veya payda çıkarılmaz; skip/xfail uygulanmaz.

```gherkin
Feature: SPEC 1.1.0 official interface and preserved GUI observations

  # AC-101; RULE-023/024
  Scenario Outline: Mandatory K1 interfaces return official keys at full precision
    Given the complete CLI input of <vector>
    When the official CLI is called
    Then exit is 0 and stdout is one JSON object
    And critical_t is present and integer fields are JSON integers
    And strict and CONTRACT comparisons are reported separately
    Examples:
      | vector    |
      | GP-AP-001 |
      | GP-PH-001 |
      | GP-AP-002 |

  # AC-102; RULE-026
  Scenario: All 22 calculated GUI inputs outside the official domain are rejected
    Given each vector whose cli_expectation.outcome is error
    When CLI and MCP receive its recorded inputs
    Then exit is 2 with code OUT_OF_RANGE and the recorded field
    And the original GUI expected/displayed/comparison remains unchanged

  # AC-103; RULE-025/026
  Scenario: All 25 input observations have explicit new CLI expectations
    Given each invalid entry and its original GUI outcome
    When its cli_argv is run
    Then exit/code/field matches expected_cli
    And error is a nonempty explanation
    And accepted GUI malformed/fractional cases are not relabeled GUI rejections

  # AC-104; RULE-025/026
  Scenario: Supported validation preserves each existing phase and its internal order
    Given d is negative and alpha is NaN in an otherwise complete AP request
    When the flags are permuted without changing values
    Then code is INVALID_VALUE and field is alpha in every permutation
    And with tails 3 and d 0 code is OUT_OF_RANGE and field is tails
    And missing AP ratio precedes an extra n1
    And extra n2 then n1 selects UNKNOWN_PARAM field n2
    And extra n1 then n2 selects UNKNOWN_PARAM field n1
    And post hoc signed integer group text -1 or 0 passes format and fails range with OUT_OF_RANGE
    And post hoc group text +2 is accepted and 2.0 or 2e0 or nonnumeric text is INVALID_VALUE
    And a later group format error precedes an earlier negative group range error
    And historical t2-indep contract tests stay unchanged and pass on the preserved validator

  # AC-105; RULE-023
  Scenario: Version query is a special standalone command
    When gpower-clone --version is run
    Then exit is 0 and contract_version is 1.0.0
    And name is exactly Takim 20 - Ismail Burak Yilmaz and engine states the actual Python version
    And version, success and error JSON bytes are ASCII safe and independent of the Windows console encoding
    And non ASCII error text is preserved after JSON decoding

  # AC-106; RULE-011/012/013
  Scenario Outline: AP degenerate outputs remain success despite input bounds
    Given the recorded AP input of <vector>
    When the official CLI is called
    Then exit is 0 and the output groups match the GUI exactly
    And achieved power is not forced up to the target
    Examples:
      | vector    |
      | GP-AP-024 |
      | R6-R01    |
      | R6-R02    |
      | R8-B01    |
      | R8-B02    |
      | R8-B03    |
      | R7-T06    |
      | R7-T07    |

  # AC-107; RULE-006..014/022
  Scenario: All 142 raw GUI calculations remain motor regression cases
    Given the preserved numerical motor and all vectors
    When the raw motor is compared with each expected/displayed/comparison
    Then strict field outcomes and AP group outcomes are reported per cohort
    And mismatches are ordinary reported failures without skip/xfail or tuning
    And negative/zero d and n1=1 observations are not removed by CLI validation

  # AC-108; RULE-022/024
  Scenario: Scientific notation has separate strict and official comparisons
    Given R7-P03, R7-I04, and R8-B06/B07/B08
    When numeric fields are compared
    Then original strict tolerances are 5e-13, 5e-14, and 5e-14/5e-24/5e-14 respectively
    And CONTRACT absolute-or-relative 1e-6 is a separate result

  # AC-109; RULE-024
  Scenario: Serialization does not feed rounded critical values into power
    Given any CLI-success vector
    When the result is serialized and parsed again
    Then floating values preserve the full double result
    And integer fields remain integers and NaN/Infinity is never emitted
    And critical_t is the unrounded alias of the raw critical result

  # AC-110; RULE-023 and explicit scope decision
  Scenario: All 25 public vectors have CLI-MCP equivalence
    Given every public_vector_cli_mcp_cases entry
    When the same input is sent to CLI and power_analysis
    Then the parsed JSON objects are equal
    And the two mandatory K1 cases match numeric public expectations
    And the other 23 cases return matching UNSUPPORTED errors
    And unsupported test or mode is checked before the other flags without calling the motor
    And unsupported test selects field test and unsupported mode selects field mode with exit 2
    And MCP input validation does not replace these errors with an SDK schema error

  # AC-111; RULE-025, provisional K-07/K-08
  Scenario: Local numerical failure is an internal error, not fabricated output
    Given a supported valid input and a simulated NumericalError from the motor
    When CLI and MCP call the shared adapter
    Then CLI exit is 1 with code NO_SOLUTION and field null
    And MCP returns the same error JSON as text
    And no claim is made that GPower also failed

  # AC-112; CONTRACT 7
  Scenario: The MCP tool name and payload follow the official interface
    When tools are listed
    Then the only tool is power_analysis
    And its parameter names match CLI
    And a valid call result contains the CLI JSON as text

  # AC-113; CONTRACT 8 and historical log policy
  Scenario: Existing actual calls are migrated without fabricated measurements
    Given the preserved real model/MCP records
    When historical log envelopes are converted offline
    Then logs/agent_calls.jsonl contains one row per actually executed tool call
    And original tool_input/tool_output/timestamps and source hashes are preserved
    And unknown tokens are null with a note, not zero
    And old responses are not relabeled current CONTRACT measurements
    And no new provider request is made

  # AC-114; CONTRACT 2.1, provisional timer scope
  Scenario: Actual CLI timing is measured in separate processes
    Given GP-AP-001, GP-AP-019, GP-PH-036 and one invalid request
    When each is launched three times through gpower-clone
    Then every raw wall-clock duration and result is recorded
    And the 2-second target is reported per invocation without hiding overruns
    And no motor change is made to improve the measured score

  # AC-115; embedded document integrity
  Scenario: Official documents and fixtures are reconstructed from SPEC
    Given contract_document and public_vectors_document
    When docs/CONTRACT.md and tests/fixtures/public_vectors.jsonl are written
    Then their UTF-8 bytes match their embedded SHA-256 hashes
    And the public fixture has exactly 25 source records

  # AC-116; complete reporting and history
  Scenario: New contracts do not rewrite historical measurement provenance
    When full tests and summaries are generated
    Then legacy87, round6, round7, round8 and official CLI outcomes are separate
    And 142 raw calculations, 120 official numeric inputs and 47 error cases are distinguished
    And previous specs, fixtures, actual runs and failed attempts remain archived
    And the actual new test totals are reported instead of assuming 2169
```

Eski→yeni test izleği: AC-01/06/11/15→AC-101; AC-02/04/10/14/18→AC-107; AC-03/08→AC-106; AC-05/07/13→AC-102+107; AC-09/16→AC-103; AC-12→AC-107+108; AC-17→AC-109. Bu ilişki eski dosyaları silme yetkisi değildir. Tarihî motor gözlemi ile yeni CLI beklentisinin farkı raporda açıkça yazılır.

## 9. Gömülü referans veri — schema_version 3

Bu tek JSON bloğu, yeni arayüz için gereken verinin tamamını taşır. `vectors` ham GUI alanlarını korur; `cli_expectation` resmî arayüz beklentisidir. Başarıda sayıları ve toleransları ikinci kez çoğaltmak yerine `expected_from=vector.expected`, `strict_comparison_from=vector.comparison`, `field_mapping=cli_field_mapping` ve `contract_comparison=contract_numeric_rule` kullanılır: bunlar aynı JSON içindeki ilgili nesnelere atıftır, dosya yolu değildir. `critical` anahtarı `cli_field_mapping` ile `critical_t` olur; diğer anahtarlar aynı kalır. `required_keys` resmî alan listesidir. Böylece aynı sayının farklı kopyalarda ayrışması önlenir.

`invalid` içinde eski `expected_cli` tarihî anahtara taşınmış, yeni `expected_cli` resmî/geçici code/field eşlemesi olmuştur. Eski gözlem metinleri aynı kalır. `agent_cases` 14 öğesi tarihî sorular ve cevap beklentileridir; güncel gerçek model ölçümü sayılmaz. Tam CONTRACT metni ve açık fixture metni kendi SHA-256'larıyla gömülüdür; dış inceleme dosyası gerekmez.

Yeni 55 hesap vektöründen yalnız incelemeye ait screenshot, screenshot_sha256 ve protocol_run alanları çıkarılmıştır; eski 87 ile aynı aktarım sınırı uygulanır. Bu üç alan ham inceleme kayıtlarında korunur. Girdiler, gözlenen sayılar/metinler, karşılaştırma toleransları ve vaka kimlikleri değişmez.

`docs/CONTRACT.md` = `contract_document.text.encode('utf-8')`; `tests/fixtures/public_vectors.jsonl` = `public_vectors_document.text.encode('utf-8')`. Her iki dosya yazıldıktan sonra gömülü SHA-256 ile doğrulanır. `public_vectors` eğitmenin25 sayısal altın kaydını aynen tutar; `public_vector_cli_mcp_cases` 2 sayısal/23 UNSUPPORTED kapsam beklentisini ayrıca tanımlar.

```json
{
  "schema_version": 3,
  "template_only": false,
  "spec_version": "1.1.0",
  "status": "DRAFT_NOT_APPROVED_NOT_TRANSFERRED",
  "predecessor": {
    "version": "1.0.4",
    "sha256": "48f75233dfbdd19d4248d97fc24dd243d54f830ecd1ad50ec3a36fa4b644ad7d"
  },
  "target": {
    "program": "G*Power",
    "version": "3.1.9.7",
    "file": "GPowerNT.exe",
    "sha256": "c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812"
  },
  "contract_document": {
    "version": "1.0.0",
    "sha256": "4cbcc105a31f4b202f3e9a8d2cc0e9d4a8b94933997e47e3e00965f1f67f999f",
    "encoding": "utf-8",
    "repository_destination": "docs/CONTRACT.md",
    "text": "# CONTRACT.md — `gpower-clone` Arayüz Sözleşmesi\n\n**Sözleşme sürümü:** 1.0.0\n**Ders:** YZM301 · Teardown Sprint\n**Referans (kâhin):** G*Power 3.1.9.7 (Windows)\n\nBu belge, yeniden yazdığınız hesap motorunun dış dünyayla **nasıl konuştuğunu** tanımlar: komut, parametre adları, çıktı alanları, hata biçimi ve karşılaştırma kuralları. Gizli test vektörleri, bütün takımların uygulamalarında **aynı düzenekle, otomatik olarak** çalıştırılacak. Sözleşmeye uymayan bir uygulama, hesabı doğru olsa bile değerlendirilemez.\n\n## Etik niyet\n\nBu çalışma, G*Power'ın yazarlarının (Faul, Erdfelder, Lang ve Buchner) bilim dünyasına ücretsiz sunduğu emeğe saygıyla, yalnızca eğitim amacıyla yürütülen bir derstir; G*Power'ı değiştirmiyor, dağıtmıyor, satmıyor ve hiçbir çıktımızı G*Power olarak sunmuyoruz. G*Power'ı yalnızca davranışını gözlemlediğimiz bir referans olarak kullanıyoruz: kaynak kodu ya da kaynak koda dönüştürülmüş çıktısı yayımlanmıyor, hesap yayımlanmış yöntemlerden ve gözlenen davranıştan bağımsız olarak yeniden yazılıyor. Amacımız G*Power'la yarışmak değil, ona ajan çağı için bir katkı önermektir; en iyi çalışmaları yazarların değerlendirmesine sunacak, yazarların talebi hâlinde ilgili materyali derhal yayından kaldıracağız.\n\n*This is a non-commercial university course run solely for educational purposes, with respect for the work the authors of G\\*Power (Faul, Erdfelder, Lang and Buchner) have made freely available to the scientific community; we do not modify, redistribute or sell G\\*Power, and none of our outputs is presented as G\\*Power. G\\*Power serves only as a behavioural reference: no source code or decompiled output is published, and the calculations are reimplemented independently from published methods and observed behaviour. Our aim is not to compete with G\\*Power but to propose a contribution for the age of AI agents; we will offer the best results to the authors for their review and will promptly withdraw any material at their request.*\n\n---\n\n> Sözleşme **arayüzü** tanımlar, **davranışı** tanımlamaz. N'nin nasıl yuvarlandığı, eşit olmayan oranda n1/n2'nin nasıl dağıldığı, iterasyonun ne zaman durduğu ya da hangi girdilerin reddedildiği burada yazmıyor. Bunlar G*Power'ın davranışıdır ve bulmanız gereken şeylerdir (kanıt defterinde `[REA]`).\n\n---\n\n## 1. Kapsam\n\n| Kapsamda | Kapsam dışı |\n|---|---|\n| 5 test ailesi (Bölüm 4) | G*Power'daki diğer tüm testler |\n| 5 analiz modu (Bölüm 3) | Grafik (X-Y plot) ve protokol çıktısı |\n| Etki büyüklüğünün doğrudan girilmesi | Etki büyüklüğünü ortalama ve standart sapmadan hesaplama (\"Determine\" penceresi) |\n\n**Zorunlu modlar:** `a-priori` ve `post-hoc`.\n**Bonus modlar:** `compromise`, `criterion`, `sensitivity`.\n\n---\n\n## 2. Genel kurallar\n\n### 2.1 Komut\n\n```\ngpower-clone --test <TEST_ID> --mode <MODE_ID> [--<alan> <değer> ...]\n```\n\n- Çalıştırılabilir dosyanın adı `gpower-clone`. Dil serbest. README'de kurulumu ve çalıştırmayı tek komutla gösterin.\n- Her parametre `--<alan> <değer>` biçimindedir. Alan adları Bölüm 4'teki tablolarla **birebir** aynıdır.\n- **Varsayılan değer yoktur.** Bir mod için gerekli olan her alan açıkça verilmelidir. Eksik alan hatadır.\n- Tanınmayan bir alan hatadır. Modla ilgisiz bir alan (örneğin `post-hoc` modunda `--power`) da hatadır.\n- Ondalık ayırıcı her zaman noktadır (`0.05`). İşletim sisteminin dil ayarından etkilenmemelisiniz.\n- Ağ erişimi yoktur. Her çağrı 2 saniye içinde tamamlanmalıdır.\n- Aynı girdi her zaman aynı çıktıyı verir (deterministik).\n\n### 2.2 Sürüm sorgusu\n\n```\ngpower-clone --version\n```\n```json\n{\"contract_version\": \"1.0.0\", \"name\": \"<takım-adı>\", \"engine\": \"<dil ve sürüm>\"}\n```\n\n### 2.3 Başarılı çıktı\n\n- `stdout`'a **tek satır JSON** yazılır. Başka hiçbir şey yazılmaz (log, uyarı ve ilerleme bilgisi `stderr`'e).\n- Çıkış kodu `0`.\n- Sayılar JSON `number` olarak yazılır, **tam double hassasiyetle**. Yuvarlamayın; karşılaştırmayı düzenek yapar (Bölüm 6).\n- Tam sayı alanları (`n1`, `n2`, `n_total`, `df`, `df1`, `df2`) JSON tam sayısıdır (`88`, `88.0` değil).\n- Bölüm 4'te listelenen alanlar **zorunludur**. Fazladan alan yazabilirsiniz; düzenek onları yok sayar.\n\n### 2.4 Hata çıktısı\n\n```json\n{\"error\": \"Power, alpha değerinden büyük olmalı\", \"code\": \"INCONSISTENT\", \"field\": \"power\"}\n```\n\n- `stdout`'a tek satır JSON. `error` alanı insan için açıklamadır (Türkçe ya da İngilizce).\n- Çıkış kodları: `2` geçersiz girdi, `1` iç hata (hesap yapılamadı, beklenmeyen durum).\n\n| `code` | Anlamı |\n|---|---|\n| `MISSING_PARAM` | Mod için gerekli bir alan verilmedi |\n| `UNKNOWN_PARAM` | Tanınmayan ya da bu modla ilgisiz alan |\n| `INVALID_VALUE` | Sayı değil, tam sayı olması gereken yerde ondalık vb. |\n| `OUT_OF_RANGE` | Bölüm 5'teki aralığın dışında |\n| `INCONSISTENT` | Değerler tek tek geçerli ama birlikte anlamsız |\n| `UNSUPPORTED` | Bilinmeyen `--test` ya da `--mode` |\n| `NO_SOLUTION` | Girdiler geçerli ama G*Power da bir sonuç üretemiyor |\n\n> Ödev metnindeki `{\"error\":\"<açıklama>\"}` biçimi geçerliliğini korur. `code` ve `field` alanları bu sürümle eklendi; düzenek önce `error` alanının varlığına, sonra `code` değerine bakar.\n\n---\n\n## 3. Analiz modları\n\n| `MODE_ID` | G*Power'daki adı | Ne hesaplar | Durum |\n|---|---|---|---|\n| `a-priori` | A priori: Compute required sample size | Gerekli örneklem büyüklüğü | **Zorunlu** |\n| `post-hoc` | Post hoc: Compute achieved power | Ulaşılan güç | **Zorunlu** |\n| `compromise` | Compromise: Compute implied α & power | β/α oranına göre α ve güç | Bonus |\n| `criterion` | Criterion: Compute required α | Gerekli α | Bonus |\n| `sensitivity` | Sensitivity: Compute required effect size | Saptanabilir en küçük etki büyüklüğü | Bonus |\n\nG*Power'da dört büyüklükten (α, güç, N, etki büyüklüğü) üçünü verirsiniz, dördüncüsünü hesaplar. Mod, hangisinin hesaplanacağını seçer.\n\n---\n\n## 4. Test aileleri\n\n### 4.0 Ortak alanlar\n\n| Alan | G*Power etiketi | Tür | Not |\n|---|---|---|---|\n| `test` | — | metin | Test kimliği (aşağıda) |\n| `mode` | Type of power analysis | metin | Bölüm 3 |\n| `tails` | Tail(s) | tam sayı: `1` ya da `2` | Yalnızca t testlerinde |\n| `alpha` | α err prob | ondalık | |\n| `power` | Power (1-β err prob) | ondalık | |\n| `beta_alpha_ratio` | β/α ratio | ondalık | Yalnızca `compromise` |\n\nÇıktıda kullanılan ortak alanlar:\n\n| Alan | G*Power etiketi |\n|---|---|\n| `ncp` | Noncentrality parameter δ ya da λ |\n| `n_total` | Total sample size |\n| `actual_power` | Actual power (`a-priori` çıktısı) |\n| `power` | Power (1-β err prob) (`post-hoc` ve `compromise` çıktısı) |\n| `alpha` | α err prob (`criterion` ve `compromise` çıktısı) |\n| `beta` | β err prob (`compromise` çıktısı) |\n\n---\n\n### 4.1 `t2-indep` · K1\n\n**G*Power:** t tests – Means: Difference between two independent means (two groups)\n**Klinik örnek:** İlaç ve plasebo grubu\n\n| Mod | Girdi alanları | Çıktı alanları |\n|---|---|---|\n| `a-priori` | `tails`, `d`, `alpha`, `power`, `ratio` | `ncp`, `critical_t`, `df`, `n1`, `n2`, `n_total`, `actual_power` |\n| `post-hoc` | `tails`, `d`, `alpha`, `n1`, `n2` | `ncp`, `critical_t`, `df`, `power` |\n| `compromise` | `tails`, `d`, `beta_alpha_ratio`, `n1`, `n2` | `ncp`, `critical_t`, `df`, `alpha`, `beta`, `power` |\n| `criterion` | `tails`, `d`, `power`, `n1`, `n2` | `ncp`, `critical_t`, `df`, `alpha` |\n| `sensitivity` | `tails`, `alpha`, `power`, `n1`, `n2` | `ncp`, `critical_t`, `df`, `d` |\n\n| Alan | G*Power etiketi |\n|---|---|\n| `d` | Effect size d |\n| `ratio` | Allocation ratio N2/N1 |\n| `n1`, `n2` | Sample size group 1, Sample size group 2 |\n| `critical_t` | Critical t |\n| `df` | Df |\n\nÖrnek:\n```\ngpower-clone --test t2-indep --mode a-priori --tails 1 --d 0.5 --alpha 0.05 --power 0.95 --ratio 1\n```\n```json\n{\"ncp\": 3.3166248, \"critical_t\": 1.6536580, \"df\": 174, \"n1\": 88, \"n2\": 88, \"n_total\": 176, \"actual_power\": 0.9514254}\n```\n\n> Sensitivity modunda G*Power yalnızca d ≥ 0 yönünü hesaplar. Sözleşmede yön parametresi yoktur.\n\n---\n\n### 4.2 `t-paired` · K2\n\n**G*Power:** t tests – Means: Difference between two dependent means (matched pairs)\n**Klinik örnek:** Aynı hastalarda önce ve sonra tansiyon\n\n| Mod | Girdi alanları | Çıktı alanları |\n|---|---|---|\n| `a-priori` | `tails`, `dz`, `alpha`, `power` | `ncp`, `critical_t`, `df`, `n_total`, `actual_power` |\n| `post-hoc` | `tails`, `dz`, `alpha`, `n_total` | `ncp`, `critical_t`, `df`, `power` |\n| `compromise` | `tails`, `dz`, `beta_alpha_ratio`, `n_total` | `ncp`, `critical_t`, `df`, `alpha`, `beta`, `power` |\n| `criterion` | `tails`, `dz`, `power`, `n_total` | `ncp`, `critical_t`, `df`, `alpha` |\n| `sensitivity` | `tails`, `alpha`, `power`, `n_total` | `ncp`, `critical_t`, `df`, `dz` |\n\n| Alan | G*Power etiketi |\n|---|---|\n| `dz` | Effect size dz |\n| `n_total` | Total sample size (çift sayısı) |\n\nÖrnek:\n```\ngpower-clone --test t-paired --mode a-priori --tails 1 --dz 0.5 --alpha 0.05 --power 0.95\n```\n```json\n{\"ncp\": 3.3541020, \"critical_t\": 1.6802300, \"df\": 44, \"n_total\": 45, \"actual_power\": 0.9512400}\n```\n\n---\n\n### 4.3 `anova-oneway` · K3\n\n**G*Power:** F tests – ANOVA: Fixed effects, omnibus, one-way\n**Klinik örnek:** Üç tedavi kolu\n\n| Mod | Girdi alanları | Çıktı alanları |\n|---|---|---|\n| `a-priori` | `f`, `alpha`, `power`, `groups` | `ncp`, `critical_f`, `df1`, `df2`, `n_total`, `actual_power` |\n| `post-hoc` | `f`, `alpha`, `n_total`, `groups` | `ncp`, `critical_f`, `df1`, `df2`, `power` |\n| `compromise` | `f`, `beta_alpha_ratio`, `n_total`, `groups` | `ncp`, `critical_f`, `df1`, `df2`, `alpha`, `beta`, `power` |\n| `criterion` | `f`, `power`, `n_total`, `groups` | `ncp`, `critical_f`, `df1`, `df2`, `alpha` |\n| `sensitivity` | `alpha`, `power`, `n_total`, `groups` | `ncp`, `critical_f`, `df1`, `df2`, `f` |\n\n| Alan | G*Power etiketi |\n|---|---|\n| `f` | Effect size f |\n| `groups` | Number of groups |\n| `critical_f` | Critical F |\n| `df1`, `df2` | Numerator df, Denominator df |\n\nÖrnek:\n```\ngpower-clone --test anova-oneway --mode a-priori --f 0.25 --alpha 0.05 --power 0.95 --groups 5\n```\n```json\n{\"ncp\": 19.0625, \"critical_f\": 2.4017397, \"df1\": 4, \"df2\": 300, \"n_total\": 305, \"actual_power\": 0.9521313}\n```\n\n---\n\n### 4.4 `chi2-contingency` · K4\n\n**G*Power:** χ² tests – Goodness-of-fit tests: Contingency tables\n**Klinik örnek:** Tedaviye yanıt oranları\n\n| Mod | Girdi alanları | Çıktı alanları |\n|---|---|---|\n| `a-priori` | `w`, `alpha`, `power`, `df` | `ncp`, `critical_chi2`, `n_total`, `actual_power` |\n| `post-hoc` | `w`, `alpha`, `n_total`, `df` | `ncp`, `critical_chi2`, `power` |\n| `compromise` | `w`, `beta_alpha_ratio`, `n_total`, `df` | `ncp`, `critical_chi2`, `alpha`, `beta`, `power` |\n| `criterion` | `w`, `power`, `n_total`, `df` | `ncp`, `critical_chi2`, `alpha` |\n| `sensitivity` | `alpha`, `power`, `n_total`, `df` | `ncp`, `critical_chi2`, `w` |\n\n| Alan | G*Power etiketi |\n|---|---|\n| `w` | Effect size w |\n| `df` | Df (**girdi**; bu ailede çıktı değildir) |\n| `critical_chi2` | Critical χ² |\n\nÖrnek:\n```\ngpower-clone --test chi2-contingency --mode a-priori --w 0.3 --alpha 0.05 --power 0.95 --df 5\n```\n```json\n{\"ncp\": 19.8, \"critical_chi2\": 11.0704977, \"n_total\": 220, \"actual_power\": 0.9502155}\n```\n\n---\n\n### 4.5 `multireg-r2` · Bonus aile\n\n**G*Power:** F tests – Linear multiple regression: Fixed model, R² deviation from zero\n**Klinik örnek:** Risk faktörlerinin açıkladığı varyans\n\n| Mod | Girdi alanları | Çıktı alanları |\n|---|---|---|\n| `a-priori` | `f2`, `alpha`, `power`, `predictors` | `ncp`, `critical_f`, `df1`, `df2`, `n_total`, `actual_power` |\n| `post-hoc` | `f2`, `alpha`, `n_total`, `predictors` | `ncp`, `critical_f`, `df1`, `df2`, `power` |\n| `compromise` | `f2`, `beta_alpha_ratio`, `n_total`, `predictors` | `ncp`, `critical_f`, `df1`, `df2`, `alpha`, `beta`, `power` |\n| `criterion` | `f2`, `power`, `n_total`, `predictors` | `ncp`, `critical_f`, `df1`, `df2`, `alpha` |\n| `sensitivity` | `alpha`, `power`, `n_total`, `predictors` | `ncp`, `critical_f`, `df1`, `df2`, `f2` |\n\n| Alan | G*Power etiketi |\n|---|---|\n| `f2` | Effect size f² |\n| `predictors` | Number of predictors |\n\nÖrnek:\n```\ngpower-clone --test multireg-r2 --mode a-priori --f2 0.15 --alpha 0.05 --power 0.95 --predictors 2\n```\n```json\n{\"ncp\": 16.05, \"critical_f\": 3.0837059, \"df1\": 2, \"df2\": 104, \"n_total\": 107, \"actual_power\": 0.9518556}\n```\n\n---\n\n## 5. Girdi aralıkları\n\nBu aralıkların dışındaki bir değer `OUT_OF_RANGE` ile reddedilir. Aralığın **içindeki** bir değerin kabul edilip edilmeyeceğine G*Power'ın davranışı karar verir; bunu keşfetmek sizin işiniz.\n\n| Alan | Tür | Aralık |\n|---|---|---|\n| `tails` | tam sayı | `1` ya da `2` |\n| `alpha` | ondalık | 0 < alpha < 1 |\n| `power` | ondalık | 0 < power < 1 |\n| `beta_alpha_ratio` | ondalık | > 0 |\n| `d`, `dz`, `f`, `w`, `f2` | ondalık | > 0 |\n| `ratio` | ondalık | > 0 |\n| `n1`, `n2`, `n_total` | tam sayı | ≥ 2 |\n| `groups` | tam sayı | ≥ 2 |\n| `df` (χ² girdisi) | tam sayı | ≥ 1 |\n| `predictors` | tam sayı | ≥ 1 |\n\n---\n\n## 6. Karşılaştırma kuralları\n\nDüzenek, uygulamanızın çıktısını G*Power'ın protokolde gösterdiği değerle karşılaştırır.\n\n| Alan türü | Kural |\n|---|---|\n| Tam sayılar: `n1`, `n2`, `n_total`, `df`, `df1`, `df2` | **Tam eşleşme** |\n| Ondalıklar: `ncp`, `critical_*`, `actual_power`, `power`, `alpha`, `beta`, etki büyüklüğü | \\|sizin − G*Power\\| ≤ 1e-6 **ya da** göreli fark ≤ 1e-6 |\n| Hata beklenen vektör | `error` alanı var ve çıkış kodu `0` değil. `code` eşleşirse ek puan. |\n\nG*Power ondalıkları 7 basamakla gösterir (`0.9514254`). Bu basamakta yuvarlanmış değerle tam double değeriniz arasında en fazla 5e-8 fark olur, yani tolerans bunu rahatça karşılar. Toleransın içinde kalamıyorsanız sorun yuvarlamada değil, hesaptadır.\n\n### Kapı\n\nGizli `a-priori` vektörlerinde **N alanlarının** (`n_total`, varsa `n1` ve `n2`) en az **%90** oranında tam eşleşmesi gerekir. Bu oran tutmazsa MCP ve ajan bonusları puanlanmaz.\n\n---\n\n## 7. MCP sunucusu (bonus)\n\n- Tek bir araç: **`power_analysis`**\n- Girdi şeması, CLI ile **aynı alan adlarını** kullanır. `test` ve `mode` zorunludur; diğer alanlar Bölüm 4'teki tablolara göre zorunlu olur.\n- Çıktı, CLI'nin `stdout` JSON'u ile **aynıdır** ve metin içeriği olarak döner.\n- Hata durumunda aynı hata JSON'u döner.\n- Hesap mantığı MCP katmanına kopyalanmaz; MCP aynı motoru çağırır.\n- **Eşdeğerlik testi zorunlu:** Bölüm 8'deki 25 vektörün her biri için CLI çıktısı ile MCP çıktısı aynı olmalı.\n\n## 8. AI ajanı (bonus)\n\nAjan, MCP aracını çağırır; hesabı asla kendisi yapmaz. Araç çağrılarını `logs/agent_calls.jsonl` dosyasına, her çağrı bir satır olacak biçimde yazın:\n\n```json\n{\"ts\": \"2026-10-23T10:15:00+03:00\", \"question\": \"<kullanıcının sorusu>\", \"tool_input\": {...}, \"tool_output\": {...}, \"tokens_in\": 0, \"tokens_out\": 0}\n```\n\nDeğerlendirme sorularında ve loglarda yalnızca **kurgusal araştırma senaryoları** kullanılır. Gerçek hasta verisi, kimlik bilgisi ya da bir kişiyi tanımlayabilecek herhangi bir bilgi soruya, loga ya da repoya girmez.\n\n---\n\n## 9. Referans vektörleri (açık)\n\nAşağıdaki 25 vektör, eğitmenin G*Power protokol kayıtlarından **birebir** alınmıştır (5 aile × 5 mod). Değerler G*Power'ın gösterdiği 7 basamaklıdır. Her satır bir JSON nesnesidir; dosya olarak `public_vectors.jsonl` adıyla kaydedip test düzeneğinizde doğrudan kullanabilirsiniz.\n\nDikkat: Bu vektörlerin hepsi tek kuyruklu ve her modda tek bir parametre seti var. Gizli vektörler çift kuyruk, eşit olmayan oran, sınır değerler ve geçersiz girdiler içerir. Yalnızca bu 25 vektörü geçmek yetmez.\n\n```jsonl\n{\"id\":\"t2-indep/a-priori\",\"input\":{\"test\":\"t2-indep\",\"mode\":\"a-priori\",\"tails\":1,\"d\":0.5,\"alpha\":0.05,\"power\":0.95,\"ratio\":1},\"expected\":{\"ncp\":3.3166248,\"critical_t\":1.6536580,\"df\":174,\"n1\":88,\"n2\":88,\"n_total\":176,\"actual_power\":0.9514254}}\n{\"id\":\"t2-indep/post-hoc\",\"input\":{\"test\":\"t2-indep\",\"mode\":\"post-hoc\",\"tails\":1,\"d\":0.5,\"alpha\":0.05,\"n1\":88,\"n2\":88},\"expected\":{\"ncp\":3.3166248,\"critical_t\":1.6536580,\"df\":174,\"power\":0.9514254}}\n{\"id\":\"t2-indep/compromise\",\"input\":{\"test\":\"t2-indep\",\"mode\":\"compromise\",\"tails\":1,\"d\":0.5,\"beta_alpha_ratio\":1,\"n1\":88,\"n2\":88},\"expected\":{\"ncp\":3.3166248,\"critical_t\":1.6606859,\"df\":174,\"alpha\":0.0492887,\"beta\":0.0492887,\"power\":0.9507113}}\n{\"id\":\"t2-indep/criterion\",\"input\":{\"test\":\"t2-indep\",\"mode\":\"criterion\",\"tails\":1,\"d\":0.5,\"power\":0.95,\"n1\":88,\"n2\":88},\"expected\":{\"ncp\":3.3166248,\"critical_t\":1.6676050,\"df\":174,\"alpha\":0.0485965}}\n{\"id\":\"t2-indep/sensitivity\",\"input\":{\"test\":\"t2-indep\",\"mode\":\"sensitivity\",\"tails\":1,\"alpha\":0.05,\"power\":0.95,\"n1\":88,\"n2\":88},\"expected\":{\"ncp\":3.3025887,\"critical_t\":1.6536580,\"df\":174,\"d\":0.4978840}}\n{\"id\":\"t-paired/a-priori\",\"input\":{\"test\":\"t-paired\",\"mode\":\"a-priori\",\"tails\":1,\"dz\":0.5,\"alpha\":0.05,\"power\":0.95},\"expected\":{\"ncp\":3.3541020,\"critical_t\":1.6802300,\"df\":44,\"n_total\":45,\"actual_power\":0.9512400}}\n{\"id\":\"t-paired/post-hoc\",\"input\":{\"test\":\"t-paired\",\"mode\":\"post-hoc\",\"tails\":1,\"dz\":0.5,\"alpha\":0.05,\"n_total\":45},\"expected\":{\"ncp\":3.3541020,\"critical_t\":1.6802300,\"df\":44,\"power\":0.9512400}}\n{\"id\":\"t-paired/compromise\",\"input\":{\"test\":\"t-paired\",\"mode\":\"compromise\",\"tails\":1,\"dz\":0.5,\"beta_alpha_ratio\":1,\"n_total\":45},\"expected\":{\"ncp\":3.3541020,\"critical_t\":1.6864315,\"df\":44,\"alpha\":0.0493959,\"beta\":0.0493959,\"power\":0.9506041}}\n{\"id\":\"t-paired/criterion\",\"input\":{\"test\":\"t-paired\",\"mode\":\"criterion\",\"tails\":1,\"dz\":0.5,\"power\":0.95,\"n_total\":45},\"expected\":{\"ncp\":3.3541020,\"critical_t\":1.6922637,\"df\":44,\"alpha\":0.0488334}}\n{\"id\":\"t-paired/sensitivity\",\"input\":{\"test\":\"t-paired\",\"mode\":\"sensitivity\",\"tails\":1,\"alpha\":0.05,\"power\":0.95,\"n_total\":45},\"expected\":{\"ncp\":3.3417616,\"critical_t\":1.6802300,\"df\":44,\"dz\":0.4981604}}\n{\"id\":\"anova-oneway/a-priori\",\"input\":{\"test\":\"anova-oneway\",\"mode\":\"a-priori\",\"f\":0.25,\"alpha\":0.05,\"power\":0.95,\"groups\":5},\"expected\":{\"ncp\":19.0625000,\"critical_f\":2.4017397,\"df1\":4,\"df2\":300,\"n_total\":305,\"actual_power\":0.9521313}}\n{\"id\":\"anova-oneway/post-hoc\",\"input\":{\"test\":\"anova-oneway\",\"mode\":\"post-hoc\",\"f\":0.25,\"alpha\":0.05,\"n_total\":100,\"groups\":5},\"expected\":{\"ncp\":6.2500000,\"critical_f\":2.4674936,\"df1\":4,\"df2\":95,\"power\":0.4663312}}\n{\"id\":\"anova-oneway/compromise\",\"input\":{\"test\":\"anova-oneway\",\"mode\":\"compromise\",\"f\":0.25,\"beta_alpha_ratio\":1,\"n_total\":100,\"groups\":5},\"expected\":{\"ncp\":6.2500000,\"critical_f\":1.4272492,\"df1\":4,\"df2\":95,\"alpha\":0.2309247,\"beta\":0.2309247,\"power\":0.7690753}}\n{\"id\":\"anova-oneway/criterion\",\"input\":{\"test\":\"anova-oneway\",\"mode\":\"criterion\",\"f\":0.25,\"power\":0.95,\"n_total\":100,\"groups\":5},\"expected\":{\"ncp\":6.2500000,\"critical_f\":0.6552638,\"df1\":4,\"df2\":95,\"alpha\":0.6245994}}\n{\"id\":\"anova-oneway/sensitivity\",\"input\":{\"test\":\"anova-oneway\",\"mode\":\"sensitivity\",\"alpha\":0.05,\"power\":0.95,\"n_total\":100,\"groups\":5},\"expected\":{\"ncp\":19.5245874,\"critical_f\":2.4674936,\"df1\":4,\"df2\":95,\"f\":0.4418664}}\n{\"id\":\"chi2-contingency/a-priori\",\"input\":{\"test\":\"chi2-contingency\",\"mode\":\"a-priori\",\"w\":0.3,\"alpha\":0.05,\"power\":0.95,\"df\":5},\"expected\":{\"ncp\":19.8000000,\"critical_chi2\":11.0704977,\"n_total\":220,\"actual_power\":0.9502155}}\n{\"id\":\"chi2-contingency/post-hoc\",\"input\":{\"test\":\"chi2-contingency\",\"mode\":\"post-hoc\",\"w\":0.3,\"alpha\":0.05,\"n_total\":100,\"df\":5},\"expected\":{\"ncp\":9.0000000,\"critical_chi2\":11.0704977,\"power\":0.6235846}}\n{\"id\":\"chi2-contingency/compromise\",\"input\":{\"test\":\"chi2-contingency\",\"mode\":\"compromise\",\"w\":0.3,\"beta_alpha_ratio\":1,\"n_total\":100,\"df\":5},\"expected\":{\"ncp\":9.0000000,\"critical_chi2\":7.6804954,\"alpha\":0.1747455,\"beta\":0.1747455,\"power\":0.8252545}}\n{\"id\":\"chi2-contingency/criterion\",\"input\":{\"test\":\"chi2-contingency\",\"mode\":\"criterion\",\"w\":0.3,\"power\":0.95,\"n_total\":100,\"df\":5},\"expected\":{\"ncp\":9.0000000,\"critical_chi2\":4.6618452,\"alpha\":0.4585253}}\n{\"id\":\"chi2-contingency/sensitivity\",\"input\":{\"test\":\"chi2-contingency\",\"mode\":\"sensitivity\",\"alpha\":0.05,\"power\":0.95,\"n_total\":100,\"df\":5},\"expected\":{\"ncp\":19.7801344,\"critical_chi2\":11.0704977,\"w\":0.4447486}}\n{\"id\":\"multireg-r2/a-priori\",\"input\":{\"test\":\"multireg-r2\",\"mode\":\"a-priori\",\"f2\":0.15,\"alpha\":0.05,\"power\":0.95,\"predictors\":2},\"expected\":{\"ncp\":16.0500000,\"critical_f\":3.0837059,\"df1\":2,\"df2\":104,\"n_total\":107,\"actual_power\":0.9518556}}\n{\"id\":\"multireg-r2/post-hoc\",\"input\":{\"test\":\"multireg-r2\",\"mode\":\"post-hoc\",\"f2\":0.15,\"alpha\":0.05,\"n_total\":100,\"predictors\":2},\"expected\":{\"ncp\":15.0000000,\"critical_f\":3.0901867,\"df1\":2,\"df2\":97,\"power\":0.9371108}}\n{\"id\":\"multireg-r2/compromise\",\"input\":{\"test\":\"multireg-r2\",\"mode\":\"compromise\",\"f2\":0.15,\"beta_alpha_ratio\":1,\"n_total\":100,\"predictors\":2},\"expected\":{\"ncp\":15.0000000,\"critical_f\":2.9610326,\"df1\":2,\"df2\":97,\"alpha\":0.0564634,\"beta\":0.0564634,\"power\":0.9435366}}\n{\"id\":\"multireg-r2/criterion\",\"input\":{\"test\":\"multireg-r2\",\"mode\":\"criterion\",\"f2\":0.15,\"power\":0.95,\"n_total\":100,\"predictors\":2},\"expected\":{\"ncp\":15.0000000,\"critical_f\":2.8223021,\"df1\":2,\"df2\":97,\"alpha\":0.0643616}}\n{\"id\":\"multireg-r2/sensitivity\",\"input\":{\"test\":\"multireg-r2\",\"mode\":\"sensitivity\",\"alpha\":0.05,\"power\":0.95,\"n_total\":100,\"predictors\":2},\"expected\":{\"ncp\":15.9319908,\"critical_f\":3.0901867,\"df1\":2,\"df2\":97,\"f2\":0.1593199}}\n```\n\n---\n\n## 10. Alan sözlüğü (klinik anlamı)\n\nHekimin diliyle bu alanlar ne anlama geliyor? Ajan katmanı kuran takımlar için özellikle önemli.\n\n| Kavram | Alan | Anlamı |\n|---|---|---|\n| Hipotez yönü | `tails` | Araştırmacı yön iddia ediyorsa (\"yeni tedavi **daha iyi**\") tek kuyruk (`1`). Yalnızca fark iddia ediyorsa (\"**fark var**\") çift kuyruk (`2`). Bu karar veriden önce, etik kurula sunulan hipotezde verilir. |\n| I. tip hata | `alpha` | Gerçekte fark yokken fark var deme riski. Genellikle 0.05 ya da 0.01. Araştırmacı belirler. |\n| Test gücü | `power` | Gerçekte fark varken onu yakalama olasılığı (1 − β). Genellikle 0.80 ve üzeri. |\n| Etki büyüklüğü | `d`, `dz`, `f`, `w`, `f2` | Farkın standartlaştırılmış büyüklüğü. Literatürden alınır. Büyüdükçe gereken N küçülür. |\n\nCohen'in (1988) geleneksel eşikleri:\n\n| Alan | Küçük | Orta | Büyük |\n|---|---|---|---|\n| `d`, `dz` | 0.2 | 0.5 | 0.8 |\n| `f` | 0.10 | 0.25 | 0.40 |\n| `w` | 0.1 | 0.3 | 0.5 |\n| `f2` | 0.02 | 0.15 | 0.35 |\n\n> Ajan katmanı için uyarı: \"orta etki\" bir **kategoridir**, bir değer değildir. Kullanıcı yalnızca \"orta\" dediyse ajan 0.5 değerini sessizce varsaymamalı; varsayımı kullanıcıya açıkça söylemeli ya da onay istemelidir.\n\n---\n\n## 11. Değişiklik politikası\n\n- Sözleşme [anlamsal sürümleme](https://semver.org/lang/tr/) kullanır. Düzeltmeler `1.0.x`, geriye uyumlu eklemeler `1.x.0` olarak yayımlanır.\n- Her değişiklik Classroom'da duyurulur ve bu dosyanın sonundaki değişiklik kaydına eklenir.\n- Sözleşmede bir belirsizlik bulursanız ödev gönderisine yorum olarak yazın. Belirsizliği ilk bulan takım artı puan alır.\n\n### Değişiklik kaydı\n\n| Sürüm | Tarih | Değişiklik |\n|---|---|---|\n| 1.0.0 | 2026-10-21 | İlk yayın |"
  },
  "cli_contract": {
    "status": "official_contract_with_explicit_user_selected_provisional_decisions",
    "reviewed_on": "2026-10-22",
    "validation_order": {
      "basis": "existing implementation, not CONTRACT table order; user correction 2026-10-22",
      "scope": "supported t2-indep a-priori/post-hoc path",
      "phases": [
        "structure",
        "numeric_format",
        "ranges",
        "cross_checks"
      ],
      "structure_order": [
        "argv scan unknown_or_duplicate then missing_value",
        "unknown names in insertion order",
        "missing COMMON then recognized mode fields",
        "irrelevant mode fields in insertion order",
        "legacy support check"
      ],
      "missing_common_order": [
        "test",
        "mode",
        "tails",
        "d",
        "alpha"
      ],
      "irrelevant_fields_order": "input insertion order, argv order for CLI; no sorting",
      "numeric_format_order": [
        "tails",
        "d",
        "alpha",
        "power",
        "ratio",
        "n1",
        "n2"
      ],
      "a_priori_field_order": [
        "tails",
        "d",
        "alpha",
        "power",
        "ratio"
      ],
      "post_hoc_field_order": [
        "tails",
        "d",
        "alpha",
        "n1",
        "n2"
      ],
      "a_priori_checks": [
        "tails range",
        "d range",
        "alpha range",
        "power range",
        "ratio range",
        "power>=alpha",
        "small d limit"
      ],
      "post_hoc_checks": [
        "tails range",
        "d range",
        "alpha range",
        "combined group minimum",
        "total N bound"
      ],
      "argv_order_does_not_control_value_errors": true,
      "argv_order_can_control_structural_errors": true,
      "group_integer_text": "optional sign then digits; values below 2 pass format and fail range",
      "group_integer_change": {
        "status": "explicit user-approved interface behavior change 2026-10-22",
        "basis": "CONTRACT 2.4 and 5",
        "signed_integer_format": true,
        "negative_typed_integer_passes_format": true,
        "below_two_error": "OUT_OF_RANGE",
        "decimal_exponent_or_nonnumeric_error": "INVALID_VALUE",
        "phase_order_unchanged": true,
        "engine_unchanged": true
      },
      "field_mapping_is_new": true,
      "shared_group_field_projection": "n1 if it violates the bound, otherwise n2; explicit project mapping",
      "existing_validation_tests": {
        "tests": 139,
        "failures": 0,
        "errors": 0,
        "skipped": 0
      },
      "additional_read_only_probes": 19
    },
    "unsupported_gateway": {
      "status": "explicit user-approved behavior change 2026-10-22",
      "basis": "CONTRACT 2.4 and 7/9 plus user scope decision",
      "order": [
        "test",
        "mode"
      ],
      "ignore_other_flags_once_unsupported": true,
      "motor_called": false,
      "error_code": "UNSUPPORTED",
      "exit_code": 2,
      "field": "test for unsupported test; otherwise mode",
      "ambiguous_or_missing_identity": "preserve existing structural errors",
      "supported_path_validation_order_unchanged": true,
      "mcp_returns_same_error_json": true
    },
    "error_required_keys": [
      "error",
      "code",
      "field"
    ],
    "error_text": "nonempty human explanation; CLI and MCP must match",
    "version_name": "Takim 20 - Ismail Burak Yilmaz",
    "json_transport": {
      "ascii_safe_escapes": true,
      "stdout_encoding": "ascii bytes, identical to UTF-8 for this wire format",
      "bom": false,
      "console_encoding_independent": true,
      "mcp_text_same_policy": true,
      "log_files_encoding": "utf-8"
    },
    "invalid_input_exit_code": 2,
    "internal_error_exit_code": 1,
    "internal_error_provisional_code": "NO_SOLUTION",
    "internal_error_field": null
  },
  "cli_field_mapping": {
    "critical": "critical_t"
  },
  "contract_numeric_rule": {
    "integer_fields": [
      "n1",
      "n2",
      "n_total",
      "df"
    ],
    "integer_rule": "exact_integer",
    "float_rule": "absolute_or_relative",
    "abs_tol": 1e-06,
    "rel_tol": 1e-06,
    "relative_denominator": "abs(reference)"
  },
  "vectors": [
    {
      "id": "GP-AP-001",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP typical/equal ratio/one-two tails",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.95",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.95",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 3.6228442,
        "critical": 1.9714347,
        "df": 208,
        "n1": 105,
        "n2": 105,
        "n_total": 210,
        "actual_power": 0.9501287
      },
      "displayed": {
        "ncp": "3.6228442",
        "critical": "1.9714347",
        "df": "208",
        "n1": "105",
        "n2": "105",
        "n_total": "210",
        "actual_power": "0.9501287"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-002",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP typical/equal ratio/one-two tails",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.95",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.95",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 3.3166248,
        "critical": 1.653658,
        "df": 174,
        "n1": 88,
        "n2": 88,
        "n_total": 176,
        "actual_power": 0.9514254
      },
      "displayed": {
        "ncp": "3.3166248",
        "critical": "1.6536580",
        "df": "174",
        "n1": "88",
        "n2": "88",
        "n_total": "176",
        "actual_power": "0.9514254"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-003",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP typical/equal ratio/one-two tails",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.8",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.8",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.884441,
        "critical": 2.0085591,
        "df": 50,
        "n1": 26,
        "n2": 26,
        "n_total": 52,
        "actual_power": 0.8074866
      },
      "displayed": {
        "ncp": "2.8844410",
        "critical": "2.0085591",
        "df": "50",
        "n1": "26",
        "n2": "26",
        "n_total": "52",
        "actual_power": "0.8074866"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-004",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP typical/equal ratio/one-two tails",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.2",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.2",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.4899799,
        "critical": 1.647323,
        "df": 618,
        "n1": 310,
        "n2": 310,
        "n_total": 620,
        "actual_power": 0.8002178
      },
      "displayed": {
        "ncp": "2.4899799",
        "critical": "1.6473230",
        "df": "618",
        "n1": "310",
        "n2": "310",
        "n_total": "620",
        "actual_power": "0.8002178"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-005",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP typical/equal ratio/one-two tails",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.01",
        "power": "0.9",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.01",
        "--power",
        "0.9",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 3.8890873,
        "critical": 2.5964692,
        "df": 240,
        "n1": 121,
        "n2": 121,
        "n_total": 242,
        "actual_power": 0.9008344
      },
      "displayed": {
        "ncp": "3.8890873",
        "critical": "2.5964692",
        "df": "240",
        "n1": "121",
        "n2": "121",
        "n_total": "242",
        "actual_power": "0.9008344"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-006",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP typical/equal ratio/one-two tails",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.3",
        "alpha": "0.1",
        "power": "0.85",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.3",
        "--alpha",
        "0.1",
        "--power",
        "0.85",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.6916538,
        "critical": 1.6496293,
        "df": 320,
        "n1": 161,
        "n2": 161,
        "n_total": 322,
        "actual_power": 0.8510936
      },
      "displayed": {
        "ncp": "2.6916538",
        "critical": "1.6496293",
        "df": "320",
        "n1": "161",
        "n2": "161",
        "n_total": "322",
        "actual_power": "0.8510936"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "capture first written to misnamed path by helper bug, renamed; content verified",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-007",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP unequal and reciprocal ratios",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "2"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "2"
      ],
      "expected": {
        "ncp": 2.8284271,
        "critical": 1.976811,
        "df": 142,
        "n1": 48,
        "n2": 96,
        "n_total": 144,
        "actual_power": 0.8021395
      },
      "displayed": {
        "ncp": "2.8284271",
        "critical": "1.9768110",
        "df": "142",
        "n1": "48",
        "n2": "96",
        "n_total": "144",
        "actual_power": "0.8021395"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-008",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP unequal and reciprocal ratios",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "0.5"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "0.5"
      ],
      "expected": {
        "ncp": 2.8284271,
        "critical": 1.976811,
        "df": 142,
        "n1": 96,
        "n2": 48,
        "n_total": 144,
        "actual_power": 0.8021395
      },
      "displayed": {
        "ncp": "2.8284271",
        "critical": "1.9768110",
        "df": "142",
        "n1": "96",
        "n2": "48",
        "n_total": "144",
        "actual_power": "0.8021395"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-009",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP unequal and reciprocal ratios",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.4",
        "alpha": "0.05",
        "power": "0.9",
        "ratio": "3"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.4",
        "--alpha",
        "0.05",
        "--power",
        "0.9",
        "--ratio",
        "3"
      ],
      "expected": {
        "ncp": 2.9393877,
        "critical": 1.6501989,
        "df": 286,
        "n1": 72,
        "n2": 216,
        "n_total": 288,
        "actual_power": 0.9010523
      },
      "displayed": {
        "ncp": "2.9393877",
        "critical": "1.6501989",
        "df": "286",
        "n1": "72",
        "n2": "216",
        "n_total": "288",
        "actual_power": "0.9010523"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-010",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP unequal and reciprocal ratios",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.4",
        "alpha": "0.05",
        "power": "0.9",
        "ratio": "0.25"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.4",
        "--alpha",
        "0.05",
        "--power",
        "0.9",
        "--ratio",
        "0.25"
      ],
      "expected": {
        "ncp": 2.9295701,
        "critical": 1.6494286,
        "df": 334,
        "n1": 269,
        "n2": 67,
        "n_total": 336,
        "actual_power": 0.8995119
      },
      "displayed": {
        "ncp": "2.9295701",
        "critical": "1.6494286",
        "df": "334",
        "n1": "269",
        "n2": "67",
        "n_total": "336",
        "actual_power": "0.8995119"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "ACTUAL POWER BELOW TARGET 0.9; n1*ratio=67.25 -> n2 67",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-011",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP unequal and reciprocal ratios",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.4",
        "alpha": "0.05",
        "power": "0.9",
        "ratio": "4"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.4",
        "--alpha",
        "0.05",
        "--power",
        "0.9",
        "--ratio",
        "4"
      ],
      "expected": {
        "ncp": 2.9295701,
        "critical": 1.6494286,
        "df": 334,
        "n1": 67,
        "n2": 269,
        "n_total": 336,
        "actual_power": 0.8995119
      },
      "displayed": {
        "ncp": "2.9295701",
        "critical": "1.6494286",
        "df": "334",
        "n1": "67",
        "n2": "269",
        "n_total": "336",
        "actual_power": "0.8995119"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "mirror of AP-010; n2 != n1*ratio (268)",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-012",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP unequal and reciprocal ratios",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.6",
        "alpha": "0.05",
        "power": "0.9",
        "ratio": "1.5"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.6",
        "--alpha",
        "0.05",
        "--power",
        "0.9",
        "--ratio",
        "1.5"
      ],
      "expected": {
        "ncp": 3.2774892,
        "critical": 1.9795999,
        "df": 122,
        "n1": 50,
        "n2": 74,
        "n_total": 124,
        "actual_power": 0.9017553
      },
      "displayed": {
        "ncp": "3.2774892",
        "critical": "1.9795999",
        "df": "122",
        "n1": "50",
        "n2": "74",
        "n_total": "124",
        "actual_power": "0.9017553"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "n1*ratio=75 but n2=74",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-013",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP unequal and reciprocal ratios",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.6",
        "alpha": "0.05",
        "power": "0.9",
        "ratio": "0.7"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.6",
        "--alpha",
        "0.05",
        "--power",
        "0.9",
        "--ratio",
        "0.7"
      ],
      "expected": {
        "ncp": 3.2876602,
        "critical": 1.9795999,
        "df": 122,
        "n1": 73,
        "n2": 51,
        "n_total": 124,
        "actual_power": 0.9034919
      },
      "displayed": {
        "ncp": "3.2876602",
        "critical": "1.9795999",
        "df": "122",
        "n1": "73",
        "n2": "51",
        "n_total": "124",
        "actual_power": "0.9034919"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-014",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP boundaries (small/large/negative d, power=alpha, d=1e-5)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.05",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.05",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.8020082,
        "critical": 1.9601529,
        "df": 12560,
        "n1": 6281,
        "n2": 6281,
        "n_total": 12562,
        "actual_power": 0.8000594
      },
      "displayed": {
        "ncp": "2.8020082",
        "critical": "1.9601529",
        "df": "12560",
        "n1": "6281",
        "n2": "6281",
        "n_total": "12562",
        "actual_power": "0.8000594"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "very small d",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-015",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP boundaries (small/large/negative d, power=alpha, d=1e-5)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "3",
        "alpha": "0.05",
        "power": "0.95",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "3",
        "--alpha",
        "0.05",
        "--power",
        "0.95",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 4.7434165,
        "critical": 2.3060041,
        "df": 8,
        "n1": 5,
        "n2": 5,
        "n_total": 10,
        "actual_power": 0.9847017
      },
      "displayed": {
        "ncp": "4.7434165",
        "critical": "2.3060041",
        "df": "8",
        "n1": "5",
        "n2": "5",
        "n_total": "10",
        "actual_power": "0.9847017"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "large d",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-016",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP boundaries (small/large/negative d, power=alpha, d=1e-5)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.05",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.05",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 0.5,
        "critical": 4.3026527,
        "df": 2,
        "n1": 2,
        "n2": 2,
        "n_total": 4,
        "actual_power": 0.0615079
      },
      "displayed": {
        "ncp": "0.5000000",
        "critical": "4.3026527",
        "df": "2",
        "n1": "2",
        "n2": "2",
        "n_total": "4",
        "actual_power": "0.0615079"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "power == alpha accepted; minimum sample n1=n2=2 returned",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-017",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP boundaries (small/large/negative d, power=alpha, d=1e-5)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "-0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "-0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": -2.8284271,
        "critical": -1.9789706,
        "df": 126,
        "n1": 64,
        "n2": 64,
        "n_total": 128,
        "actual_power": 0.8014596
      },
      "displayed": {
        "ncp": "-2.8284271",
        "critical": "-1.9789706",
        "df": "126",
        "n1": "64",
        "n2": "64",
        "n_total": "128",
        "actual_power": "0.8014596"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "negative d two-tailed: same N as |d|; ncp and critical t shown negative",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-AP-018",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP boundaries (small/large/negative d, power=alpha, d=1e-5)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "-0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "-0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": -2.5248762,
        "critical": -1.6602343,
        "df": 100,
        "n1": 51,
        "n2": 51,
        "n_total": 102,
        "actual_power": 0.8058986
      },
      "displayed": {
        "ncp": "-2.5248762",
        "critical": "-1.6602343",
        "df": "100",
        "n1": "51",
        "n2": "51",
        "n_total": "102",
        "actual_power": "0.8058986"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "negative d one-tailed: test direction follows sign of d; critical t negative",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-AP-019",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP boundaries (small/large/negative d, power=alpha, d=1e-5)",
      "class": "hard_power_below_target",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.00001",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.00001",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.4863472,
        "critical": 1.6448536,
        "df": 247276887662,
        "n1": 123638443832,
        "n2": 123638443832,
        "n_total": 247276887664,
        "actual_power": 0.7999212
      },
      "displayed": {
        "ncp": "2.4863472",
        "critical": "1.6448536",
        "df": "247276887662",
        "n1": "123638443832",
        "n2": "123638443832",
        "n_total": "247276887664",
        "actual_power": "0.7999212"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "d exactly 0.00001 accepted; very large N; actual power 0.7999212 is BELOW target 0.8. Diagnostic hypothesis (not proven): finite precision/termination of the internal search. Expected N/n1/n2 remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-001",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH equal groups, one/two tails",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "105",
        "n2": "105"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "105",
        "--n2",
        "105"
      ],
      "expected": {
        "ncp": 3.6228442,
        "critical": 1.9714347,
        "df": 208,
        "power": 0.9501287
      },
      "displayed": {
        "ncp": "3.6228442",
        "critical": "1.9714347",
        "df": "208",
        "power": "0.9501287"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "matches GP-AP-001 outputs exactly",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-002",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH equal groups, one/two tails",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "64",
        "n2": "64"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "64",
        "--n2",
        "64"
      ],
      "expected": {
        "ncp": 2.8284271,
        "critical": 1.657037,
        "df": 126,
        "power": 0.8786642
      },
      "displayed": {
        "ncp": "2.8284271",
        "critical": "1.6570370",
        "df": "126",
        "power": "0.8786642"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-003",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH equal groups, one/two tails",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.8",
        "alpha": "0.05",
        "n1": "26",
        "n2": "26"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.8",
        "--alpha",
        "0.05",
        "--n1",
        "26",
        "--n2",
        "26"
      ],
      "expected": {
        "ncp": 2.884441,
        "critical": 2.0085591,
        "df": 50,
        "power": 0.8074866
      },
      "displayed": {
        "ncp": "2.8844410",
        "critical": "2.0085591",
        "df": "50",
        "power": "0.8074866"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "matches GP-AP-003",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-004",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH equal groups, one/two tails",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.2",
        "alpha": "0.01",
        "n1": "100",
        "n2": "100"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0.2",
        "--alpha",
        "0.01",
        "--n1",
        "100",
        "--n2",
        "100"
      ],
      "expected": {
        "ncp": 1.4142136,
        "critical": 2.3453283,
        "df": 198,
        "power": 0.1783213
      },
      "displayed": {
        "ncp": "1.4142136",
        "critical": "2.3453283",
        "df": "198",
        "power": "0.1783213"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-005",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH equal groups, one/two tails",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.3",
        "alpha": "0.1",
        "n1": "50",
        "n2": "50"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.3",
        "--alpha",
        "0.1",
        "--n1",
        "50",
        "--n2",
        "50"
      ],
      "expected": {
        "ncp": 1.5,
        "critical": 1.6605512,
        "df": 98,
        "power": 0.439186
      },
      "displayed": {
        "ncp": "1.5000000",
        "critical": "1.6605512",
        "df": "98",
        "power": "0.4391860"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-006",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH equal groups, one/two tails",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "1",
        "alpha": "0.05",
        "n1": "10",
        "n2": "10"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "1",
        "--alpha",
        "0.05",
        "--n1",
        "10",
        "--n2",
        "10"
      ],
      "expected": {
        "ncp": 2.236068,
        "critical": 2.100922,
        "df": 18,
        "power": 0.5620066
      },
      "displayed": {
        "ncp": "2.2360680",
        "critical": "2.1009220",
        "df": "18",
        "power": "0.5620066"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-007",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH unequal groups and swaps",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "40",
        "n2": "80"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "40",
        "--n2",
        "80"
      ],
      "expected": {
        "ncp": 2.5819889,
        "critical": 1.9802722,
        "df": 118,
        "power": 0.7260699
      },
      "displayed": {
        "ncp": "2.5819889",
        "critical": "1.9802722",
        "df": "118",
        "power": "0.7260699"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-008",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH unequal groups and swaps",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "80",
        "n2": "40"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "80",
        "--n2",
        "40"
      ],
      "expected": {
        "ncp": 2.5819889,
        "critical": 1.9802722,
        "df": 118,
        "power": 0.7260699
      },
      "displayed": {
        "ncp": "2.5819889",
        "critical": "1.9802722",
        "df": "118",
        "power": "0.7260699"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "swap of PH-007: identical outputs",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-009",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH unequal groups and swaps",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.4",
        "alpha": "0.05",
        "n1": "30",
        "n2": "90"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0.4",
        "--alpha",
        "0.05",
        "--n1",
        "30",
        "--n2",
        "90"
      ],
      "expected": {
        "ncp": 1.8973666,
        "critical": 1.6578695,
        "df": 118,
        "power": 0.5954621
      },
      "displayed": {
        "ncp": "1.8973666",
        "critical": "1.6578695",
        "df": "118",
        "power": "0.5954621"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-010",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH unequal groups and swaps",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.4",
        "alpha": "0.05",
        "n1": "90",
        "n2": "30"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0.4",
        "--alpha",
        "0.05",
        "--n1",
        "90",
        "--n2",
        "30"
      ],
      "expected": {
        "ncp": 1.8973666,
        "critical": 1.6578695,
        "df": 118,
        "power": 0.5954621
      },
      "displayed": {
        "ncp": "1.8973666",
        "critical": "1.6578695",
        "df": "118",
        "power": "0.5954621"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "swap of PH-009: identical",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-011",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH unequal groups and swaps",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.6",
        "alpha": "0.01",
        "n1": "25",
        "n2": "75"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.6",
        "--alpha",
        "0.01",
        "--n1",
        "25",
        "--n2",
        "75"
      ],
      "expected": {
        "ncp": 2.5980762,
        "critical": 2.6269311,
        "df": 98,
        "power": 0.4913405
      },
      "displayed": {
        "ncp": "2.5980762",
        "critical": "2.6269311",
        "df": "98",
        "power": "0.4913405"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": null,
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-012",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH thresholds/minimality, small n, small/large/negative/zero d",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "87",
        "n2": "87"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "87",
        "--n2",
        "87"
      ],
      "expected": {
        "ncp": 3.2977265,
        "critical": 1.6537609,
        "df": 172,
        "power": 0.9494829
      },
      "displayed": {
        "ncp": "3.2977265",
        "critical": "1.6537609",
        "df": "172",
        "power": "0.9494829"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "N-1 per group of GP-AP-002: power < 0.95 -> AP-002 minimal",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-013",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH thresholds/minimality, small n, small/large/negative/zero d",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.4",
        "alpha": "0.05",
        "n1": "269",
        "n2": "67"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0.4",
        "--alpha",
        "0.05",
        "--n1",
        "269",
        "--n2",
        "67"
      ],
      "expected": {
        "ncp": 2.9295701,
        "critical": 1.6494286,
        "df": 334,
        "power": 0.8995119
      },
      "displayed": {
        "ncp": "2.9295701",
        "critical": "1.6494286",
        "df": "334",
        "power": "0.8995119"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "reproduces GP-AP-010 actual power from its integer groups",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-014",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH thresholds/minimality, small n, small/large/negative/zero d",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "2",
        "n2": "2"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "2",
        "--n2",
        "2"
      ],
      "expected": {
        "ncp": 0.5,
        "critical": 4.3026527,
        "df": 2,
        "power": 0.0615079
      },
      "displayed": {
        "ncp": "0.5000000",
        "critical": "4.3026527",
        "df": "2",
        "power": "0.0615079"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "smallest group sizes; matches GP-AP-016",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-015",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH thresholds/minimality, small n, small/large/negative/zero d",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.01",
        "alpha": "0.05",
        "n1": "50",
        "n2": "50"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.01",
        "--alpha",
        "0.05",
        "--n1",
        "50",
        "--n2",
        "50"
      ],
      "expected": {
        "ncp": 0.05,
        "critical": 1.9844675,
        "df": 98,
        "power": 0.0502809
      },
      "displayed": {
        "ncp": "0.0500000",
        "critical": "1.9844675",
        "df": "98",
        "power": "0.0502809"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "tiny d: power approx alpha",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-016",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH thresholds/minimality, small n, small/large/negative/zero d",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "3",
        "alpha": "0.05",
        "n1": "5",
        "n2": "5"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "3",
        "--alpha",
        "0.05",
        "--n1",
        "5",
        "--n2",
        "5"
      ],
      "expected": {
        "ncp": 4.7434165,
        "critical": 2.3060041,
        "df": 8,
        "power": 0.9847017
      },
      "displayed": {
        "ncp": "4.7434165",
        "critical": "2.3060041",
        "df": "8",
        "power": "0.9847017"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "matches GP-AP-015",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-017",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH thresholds/minimality, small n, small/large/negative/zero d",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "-0.5",
        "alpha": "0.05",
        "n1": "50",
        "n2": "50"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "-0.5",
        "--alpha",
        "0.05",
        "--n1",
        "50",
        "--n2",
        "50"
      ],
      "expected": {
        "ncp": -2.5,
        "critical": -1.6605512,
        "df": 98,
        "power": 0.7989362
      },
      "displayed": {
        "ncp": "-2.5000000",
        "critical": "-1.6605512",
        "df": "98",
        "power": "0.7989362"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "negative d one-tailed post hoc: direction follows sign of d; power same as |d|",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-PH-018",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH thresholds/minimality, small n, small/large/negative/zero d",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "-0.5",
        "alpha": "0.05",
        "n1": "50",
        "n2": "50"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "-0.5",
        "--alpha",
        "0.05",
        "--n1",
        "50",
        "--n2",
        "50"
      ],
      "expected": {
        "ncp": -2.5,
        "critical": -1.9844675,
        "df": 98,
        "power": 0.6968934
      },
      "displayed": {
        "ncp": "-2.5000000",
        "critical": "-1.9844675",
        "df": "98",
        "power": "0.6968934"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "negative d two-tailed post hoc",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-PH-019",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH thresholds/minimality, small n, small/large/negative/zero d",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "1",
        "n2": "2"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "1",
        "--n2",
        "2"
      ],
      "expected": {
        "ncp": 0.4082483,
        "critical": 12.7062047,
        "df": 1,
        "power": 0.0540922
      },
      "displayed": {
        "ncp": "0.4082483",
        "critical": "12.7062047",
        "df": "1",
        "power": "0.0540922"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "smallest admissible total N=3 with a group of size 1",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "n1",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "approved n>=2 threshold at existing combined group check; field projection is a project decision"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-AP-020",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP ratio admissible bounds",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "100"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "100"
      ],
      "expected": {
        "ncp": 2.8142761,
        "critical": 1.9607047,
        "df": 3204,
        "n1": 32,
        "n2": 3174,
        "n_total": 3206,
        "actual_power": 0.8033011
      },
      "displayed": {
        "ncp": "2.8142761",
        "critical": "1.9607047",
        "df": "3204",
        "n1": "32",
        "n2": "3174",
        "n_total": "3206",
        "actual_power": "0.8033011"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "upper admissible ratio; n2 != n1*ratio (3200)",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-021",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP ratio admissible bounds",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "0.01"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "0.01"
      ],
      "expected": {
        "ncp": 2.8142761,
        "critical": 1.9607047,
        "df": 3204,
        "n1": 3174,
        "n2": 32,
        "n_total": 3206,
        "actual_power": 0.8033011
      },
      "displayed": {
        "ncp": "2.8142761",
        "critical": "1.9607047",
        "df": "3204",
        "n1": "3174",
        "n2": "32",
        "n_total": "3206",
        "actual_power": "0.8033011"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "lower admissible ratio; mirror of AP-020",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-022",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP half-rounding of n1",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.55",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "3"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.55",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "3"
      ],
      "expected": {
        "ncp": 2.8511673,
        "critical": 1.9770537,
        "df": 140,
        "n1": 36,
        "n2": 106,
        "n_total": 142,
        "actual_power": 0.8082856
      },
      "displayed": {
        "ncp": "2.8511673",
        "critical": "1.9770537",
        "df": "140",
        "n1": "36",
        "n2": "106",
        "n_total": "142",
        "actual_power": "0.8082856"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "N/(1+r)=35.5 -> n1=36 (half up), n2=N-n1=106",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-023",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP half-rounding of n1",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "3"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "3"
      ],
      "expected": {
        "ncp": 2.8338811,
        "critical": 1.9741852,
        "df": 168,
        "n1": 43,
        "n2": 127,
        "n_total": 170,
        "actual_power": 0.8044668
      },
      "displayed": {
        "ncp": "2.8338811",
        "critical": "1.9741852",
        "df": "168",
        "n1": "43",
        "n2": "127",
        "n_total": "170",
        "actual_power": "0.8044668"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "N/(1+r)=42.5 -> n1=43 half up; n2=127=N-n1 (not round(127.5)=128)",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-020",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH thresholds/minimality, small n, small/large/negative/zero d",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.05",
        "alpha": "0.05",
        "n1": "6280",
        "n2": "6281"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.05",
        "--alpha",
        "0.05",
        "--n1",
        "6280",
        "--n2",
        "6281"
      ],
      "expected": {
        "ncp": 2.8018967,
        "critical": 1.9601529,
        "df": 12559,
        "power": 0.8000282
      },
      "displayed": {
        "ncp": "2.8018967",
        "critical": "1.9601529",
        "df": "12559",
        "power": "0.8000282"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "odd total 12561 already reaches 0.8, yet GP-AP-014 returned 12562: a priori total is not the minimal integer total (even/per-group step)",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-021",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH thresholds/minimality, small n, small/large/negative/zero d",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "42",
        "n2": "126"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "42",
        "--n2",
        "126"
      ],
      "expected": {
        "ncp": 2.806243,
        "critical": 1.9743578,
        "df": 166,
        "power": 0.7967341
      },
      "displayed": {
        "ncp": "2.8062430",
        "critical": "1.9743578",
        "df": "166",
        "power": "0.7967341"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "previous even total (168, exact split for r=3) of GP-AP-023 is below 0.8",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-024",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP degenerate minimum with extreme ratio",
      "class": "degenerate_gui_output",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.05",
        "ratio": "100"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.05",
        "--ratio",
        "100"
      ],
      "expected": {
        "ncp": 0,
        "critical": 4.3026527,
        "df": 2,
        "n1": 0,
        "n2": 4,
        "n_total": 4,
        "actual_power": 0.05
      },
      "displayed": {
        "ncp": "0",
        "critical": "4.3026527",
        "df": "2",
        "n1": "0",
        "n2": "4",
        "n_total": "4",
        "actual_power": "0.0500000"
      },
      "comparison": {
        "ncp": {
          "rule": "exact_zero",
          "abs_tol": 0
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "degenerate: minimum total N=4, n1=round(4/101)=0, n2=4; ncp displayed '0'; G*Power reports a group of size 0 (post hoc would reject n1=0)",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-022",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH thresholds/minimality, small n, small/large/negative/zero d",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0",
        "alpha": "0.05",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0",
        "--alpha",
        "0.05",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": 0,
        "critical": 2.0243942,
        "df": 38,
        "power": 0.05
      },
      "displayed": {
        "ncp": "0",
        "critical": "2.0243942",
        "df": "38",
        "power": "0.0500000"
      },
      "comparison": {
        "ncp": {
          "rule": "exact_zero",
          "abs_tol": 0
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "d=0 accepted in post hoc; ncp displayed '0'; critical positive; power equals alpha",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-PH-023",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH thresholds/minimality, small n, small/large/negative/zero d",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0",
        "alpha": "0.05",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0",
        "--alpha",
        "0.05",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": 0,
        "critical": 1.6859545,
        "df": 38,
        "power": 0.05
      },
      "displayed": {
        "ncp": "0",
        "critical": "1.6859545",
        "df": "38",
        "power": "0.0500000"
      },
      "comparison": {
        "ncp": {
          "rule": "exact_zero",
          "abs_tol": 0
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "d=0 one-tailed post hoc; critical positive; power equals alpha",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-PH-024",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH alpha >= 0.5 critical sign",
      "class": "near_zero_critical_scientific",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.5",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.5",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": 1.5811388,
        "critical": 6.6818e-17,
        "df": 38,
        "power": 0.9430769
      },
      "displayed": {
        "ncp": "1.5811388",
        "critical": "6.6818e-17",
        "df": "38",
        "power": "0.9430769"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_significant_scientific",
          "significant_digits": 5,
          "abs_tol": 5e-22
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "one-tailed alpha=0.5: critical displayed 6.6818e-17 (numerically ~0, scientific display)",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-025",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH alpha >= 0.5 critical sign",
      "class": "near_zero_critical_scientific",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "-0.5",
        "alpha": "0.5",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "-0.5",
        "--alpha",
        "0.5",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": -1.5811388,
        "critical": 6.6818e-17,
        "df": 38,
        "power": 0.9430769
      },
      "displayed": {
        "ncp": "-1.5811388",
        "critical": "6.6818e-17",
        "df": "38",
        "power": "0.9430769"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_significant_scientific",
          "significant_digits": 5,
          "abs_tol": 5e-22
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "one-tailed alpha=0.5, d<0: critical stays +6.6818e-17 (not negated)",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-PH-026",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH alpha >= 0.5 critical sign",
      "class": "near_zero_critical_scientific",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0",
        "alpha": "0.5",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0",
        "--alpha",
        "0.5",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": 0,
        "critical": 6.6818e-17,
        "df": 38,
        "power": 0.5
      },
      "displayed": {
        "ncp": "0",
        "critical": "6.6818e-17",
        "df": "38",
        "power": "0.5000000"
      },
      "comparison": {
        "ncp": {
          "rule": "exact_zero",
          "abs_tol": 0
        },
        "critical": {
          "rule": "displayed_significant_scientific",
          "significant_digits": 5,
          "abs_tol": 5e-22
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "one-tailed alpha=0.5, d=0: power = alpha = 0.5",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-PH-027",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH alpha >= 0.5 critical sign",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.75",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.75",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": 1.5811388,
        "critical": -0.6810009,
        "df": 38,
        "power": 0.9878041
      },
      "displayed": {
        "ncp": "1.5811388",
        "critical": "-0.6810009",
        "df": "38",
        "power": "0.9878041"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "one-tailed alpha=0.75, d>0: critical NEGATIVE (-0.6810009)",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-028",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH alpha >= 0.5 critical sign",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "-0.5",
        "alpha": "0.75",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "-0.5",
        "--alpha",
        "0.75",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": -1.5811388,
        "critical": 0.6810009,
        "df": 38,
        "power": 0.9878041
      },
      "displayed": {
        "ncp": "-1.5811388",
        "critical": "0.6810009",
        "df": "38",
        "power": "0.9878041"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "one-tailed alpha=0.75, d<0: critical +0.6810009; same power as d>0",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-PH-029",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH alpha >= 0.5 critical sign",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0",
        "alpha": "0.75",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0",
        "--alpha",
        "0.75",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": 0,
        "critical": -0.6810009,
        "df": 38,
        "power": 0.75
      },
      "displayed": {
        "ncp": "0",
        "critical": "-0.6810009",
        "df": "38",
        "power": "0.7500000"
      },
      "comparison": {
        "ncp": {
          "rule": "exact_zero",
          "abs_tol": 0
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "one-tailed alpha=0.75, d=0: critical -0.6810009, power = alpha",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-PH-030",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH alpha >= 0.5 critical sign",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.75",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.75",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": 1.5811388,
        "critical": 0.3209591,
        "df": 38,
        "power": 0.9252246
      },
      "displayed": {
        "ncp": "1.5811388",
        "critical": "0.3209591",
        "df": "38",
        "power": "0.9252246"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "two-tailed alpha=0.75, d>0: critical +0.3209591",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-031",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH alpha >= 0.5 critical sign",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "-0.5",
        "alpha": "0.75",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "-0.5",
        "--alpha",
        "0.75",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": -1.5811388,
        "critical": -0.3209591,
        "df": 38,
        "power": 0.9252246
      },
      "displayed": {
        "ncp": "-1.5811388",
        "critical": "-0.3209591",
        "df": "38",
        "power": "0.9252246"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "two-tailed alpha=0.75, d<0: critical -0.3209591",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-PH-032",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH input bounds (alpha, d, total N)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.0000001",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.0000001",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": 1.5811388,
        "critical": 6.5517472,
        "df": 38,
        "power": 3.05715e-05
      },
      "displayed": {
        "ncp": "1.5811388",
        "critical": "6.5517472",
        "df": "38",
        "power": "3.05715e-05"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_significant_scientific",
          "significant_digits": 6,
          "abs_tol": 5e-11
        }
      },
      "observation_note": "alpha exactly 1e-7 ACCEPTED (lower bound closed); power displayed 3.05715e-05",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-033",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH input bounds (alpha, d, total N)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.9999999",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.9999999",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": 1.5811388,
        "critical": 1.261586e-07,
        "df": 38,
        "power": 1.0
      },
      "displayed": {
        "ncp": "1.5811388",
        "critical": "1.261586e-07",
        "df": "38",
        "power": "1.0000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_significant_scientific",
          "significant_digits": 7,
          "abs_tol": 5e-14
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "alpha 0.9999999 accepted; critical displayed 1.261586e-07",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-034",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH input bounds (alpha, d, total N)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "20",
        "alpha": "0.05",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "20",
        "--alpha",
        "0.05",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": 63.2455532,
        "critical": 2.0243942,
        "df": 38,
        "power": 1.0
      },
      "displayed": {
        "ncp": "63.2455532",
        "critical": "2.0243942",
        "df": "38",
        "power": "1.0000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "d = 20 accepted (upper bound closed)",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-PH-035",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH input bounds (alpha, d, total N)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "-20",
        "alpha": "0.05",
        "n1": "20",
        "n2": "20"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "-20",
        "--alpha",
        "0.05",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "expected": {
        "ncp": -63.2455532,
        "critical": -2.0243942,
        "df": 38,
        "power": 1.0
      },
      "displayed": {
        "ncp": "-63.2455532",
        "critical": "-2.0243942",
        "df": "38",
        "power": "1.0000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "d = -20 accepted (lower bound closed)",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-PH-036",
      "test": "t2-indep",
      "mode": "post-hoc",
      "source": "gpower_gui",
      "subgroup": "PH input bounds (alpha, d, total N)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "1073741823",
        "n2": "1073741823"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "1073741823",
        "--n2",
        "1073741823"
      ],
      "expected": {
        "ncp": 11585.24,
        "critical": 1.959964,
        "df": 2147483644,
        "power": 1.0
      },
      "displayed": {
        "ncp": "11585.24",
        "critical": "1.9599640",
        "df": "2147483644",
        "power": "1.0000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 2,
          "abs_tol": 0.005
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "total N = 2147483646 accepted (upper bound closed); ncp displayed 11585.24",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-025",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP alpha >= 0.5 critical sign",
      "class": "near_zero_critical_scientific",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.5",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.5",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 0.8660254,
        "critical": 6.805748e-17,
        "df": 10,
        "n1": 6,
        "n2": 6,
        "n_total": 12,
        "actual_power": 0.8067619
      },
      "displayed": {
        "ncp": "0.8660254",
        "critical": "6.805748e-17",
        "df": "10",
        "n1": "6",
        "n2": "6",
        "n_total": "12",
        "actual_power": "0.8067619"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_significant_scientific",
          "significant_digits": 7,
          "abs_tol": 5e-24
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "a priori one-tailed alpha=0.5: critical 6.805748e-17; total N 12",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-026",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP alpha >= 0.5 critical sign",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.75",
        "power": "0.9",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.75",
        "--power",
        "0.9",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 0.7071068,
        "critical": -0.7175582,
        "df": 6,
        "n1": 4,
        "n2": 4,
        "n_total": 8,
        "actual_power": 0.9143631
      },
      "displayed": {
        "ncp": "0.7071068",
        "critical": "-0.7175582",
        "df": "6",
        "n1": "4",
        "n2": "4",
        "n_total": "8",
        "actual_power": "0.9143631"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "a priori one-tailed alpha=0.75, d>0: critical negative -0.7175582",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-027",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP alpha >= 0.5 critical sign",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "-0.5",
        "alpha": "0.75",
        "power": "0.9",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "-0.5",
        "--alpha",
        "0.75",
        "--power",
        "0.9",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": -0.7071068,
        "critical": 0.7175582,
        "df": 6,
        "n1": 4,
        "n2": 4,
        "n_total": 8,
        "actual_power": 0.9143631
      },
      "displayed": {
        "ncp": "-0.7071068",
        "critical": "0.7175582",
        "df": "6",
        "n1": "4",
        "n2": "4",
        "n_total": "8",
        "actual_power": "0.9143631"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "a priori one-tailed alpha=0.75, d<0: critical +0.7175582; same N as d>0",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-AP-028",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP input-bound neighbours (|d|, power vs alpha, ratio)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "-0.0000101",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "-0.0000101",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": -2.4866106,
        "critical": -1.6448536,
        "df": 242455929076,
        "n1": 121227964539,
        "n2": 121227964539,
        "n_total": 242455929078,
        "actual_power": 0.800069
      },
      "displayed": {
        "ncp": "-2.4866106",
        "critical": "-1.6448536",
        "df": "242455929076",
        "n1": "121227964539",
        "n2": "121227964539",
        "n_total": "242455929078",
        "actual_power": "0.8000690"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "|d| = 0.0000101 accepted; huge N; actual power 0.8000690 >= target",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "GP-AP-029",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP input-bound neighbours (|d|, power vs alpha, ratio)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.0500001",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.0500001",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 0.5,
        "critical": 2.9199856,
        "df": 2,
        "n1": 2,
        "n2": 2,
        "n_total": 4,
        "actual_power": 0.0994117
      },
      "displayed": {
        "ncp": "0.5000000",
        "critical": "2.9199856",
        "df": "2",
        "n1": "2",
        "n2": "2",
        "n_total": "4",
        "actual_power": "0.0994117"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "power 0.0500001 just above alpha accepted; N=4",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-030",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP input-bound neighbours (|d|, power vs alpha, ratio)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "0.0101"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "0.0101"
      ],
      "expected": {
        "ncp": 2.4874686,
        "critical": 1.6454639,
        "df": 2498,
        "n1": 2475,
        "n2": 25,
        "n_total": 2500,
        "actual_power": 0.8000896
      },
      "displayed": {
        "ncp": "2.4874686",
        "critical": "1.6454639",
        "df": "2498",
        "n1": "2475",
        "n2": "25",
        "n_total": "2500",
        "actual_power": "0.8000896"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "ratio 0.0101 accepted",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-031",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP input-bound neighbours (|d|, power vs alpha, ratio)",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "99.99"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "99.99"
      ],
      "expected": {
        "ncp": 2.487588,
        "critical": 1.645458,
        "df": 2522,
        "n1": 25,
        "n2": 2499,
        "n_total": 2524,
        "actual_power": 0.8001248
      },
      "displayed": {
        "ncp": "2.4875880",
        "critical": "1.6454580",
        "df": "2522",
        "n1": "25",
        "n2": "2499",
        "n_total": "2524",
        "actual_power": "0.8001248"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "ratio 99.99 accepted",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-032",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP half-rounding of n1, inexact reciprocal ratio",
      "class": "half_tie_inexact_ratio",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "0.3333333"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "0.3333333"
      ],
      "expected": {
        "ncp": 2.8117401,
        "critical": 1.9741852,
        "df": 168,
        "n1": 128,
        "n2": 42,
        "n_total": 170,
        "actual_power": 0.7983302
      },
      "displayed": {
        "ncp": "2.8117401",
        "critical": "1.9741852",
        "df": "168",
        "n1": "128",
        "n2": "42",
        "n_total": "170",
        "actual_power": "0.7983302"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "ratio typed 0.3333333: N=170 as in GP-AP-023 (r=3) but split 128/42, NOT the mirror 127/43; actual power 0.7983302 < 0.8",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-033",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP power bounds",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.0000001",
        "power": "0.0000001",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.0000001",
        "--power",
        "0.0000001",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 0.5,
        "critical": 3162.277,
        "df": 2,
        "n1": 2,
        "n2": 2,
        "n_total": 4,
        "actual_power": 1.25e-07
      },
      "displayed": {
        "ncp": "0.5000000",
        "critical": "3162.277",
        "df": "2",
        "n1": "2",
        "n2": "2",
        "n_total": "4",
        "actual_power": "1.25e-07"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 3,
          "abs_tol": 0.0005
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_significant_scientific",
          "significant_digits": 3,
          "abs_tol": 5e-10
        }
      },
      "observation_note": "alpha = power = 1e-7 accepted (power lower bound closed); critical 3162.277, power 1.25e-07",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-034",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP power bounds",
      "class": "standard",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.9999999",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.9999999",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 7.17635,
        "critical": 1.9628541,
        "df": 822,
        "n1": 412,
        "n2": 412,
        "n_total": 824,
        "actual_power": 0.9999999
      },
      "displayed": {
        "ncp": "7.1763500",
        "critical": "1.9628541",
        "df": "822",
        "n1": "412",
        "n2": "412",
        "n_total": "824",
        "actual_power": "0.9999999"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "power 0.9999999 accepted; run [80] 13:53:30 is an unintended identical repeat (Return key)",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-035",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_agrees",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.01",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.01",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.4864835,
        "critical": 1.6448598,
        "df": 247302,
        "n1": 123652,
        "n2": 123652,
        "n_total": 247304,
        "actual_power": 0.8000005
      },
      "displayed": {
        "ncp": "2.4864835",
        "critical": "1.6448598",
        "df": "247302",
        "n1": "123652",
        "n2": "123652",
        "n_total": "247304",
        "actual_power": "0.8000005"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-01, protocol [2] 22:34:46. G*Power N equals the inspection-side SPEC-rule computation (delta +0); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-036",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_agrees",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.005",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.005",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.4864784,
        "critical": 1.6448552,
        "df": 989210,
        "n1": 494606,
        "n2": 494606,
        "n_total": 989212,
        "actual_power": 0.8000005
      },
      "displayed": {
        "ncp": "2.4864784",
        "critical": "1.6448552",
        "df": "989210",
        "n1": "494606",
        "n2": "494606",
        "n_total": "989212",
        "actual_power": "0.8000005"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-02, protocol [3] 22:34:58. G*Power N equals the inspection-side SPEC-rule computation (delta +0); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-037",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_agrees",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.002",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.002",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.4864754,
        "critical": 1.6448539,
        "df": 6182558,
        "n1": 3091280,
        "n2": 3091280,
        "n_total": 6182560,
        "actual_power": 0.8000001
      },
      "displayed": {
        "ncp": "2.4864754",
        "critical": "1.6448539",
        "df": "6182558",
        "n1": "3091280",
        "n2": "3091280",
        "n_total": "6182560",
        "actual_power": "0.8000001"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-03, protocol [4] 22:35:08. G*Power N equals the inspection-side SPEC-rule computation (delta +0); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-038",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_agrees",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.001",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.001",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.486475,
        "critical": 1.6448537,
        "df": 24730230,
        "n1": 12365116,
        "n2": 12365116,
        "n_total": 24730232,
        "actual_power": 0.8
      },
      "displayed": {
        "ncp": "2.4864750",
        "critical": "1.6448537",
        "df": "24730230",
        "n1": "12365116",
        "n2": "12365116",
        "n_total": "24730232",
        "actual_power": "0.8000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-04, protocol [5] 22:35:17. G*Power N equals the inspection-side SPEC-rule computation (delta +0); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-039",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_deviation",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.0005",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.0005",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.4864749,
        "critical": 1.6448536,
        "df": 98920914,
        "n1": 49460458,
        "n2": 49460458,
        "n_total": 98920916,
        "actual_power": 0.8
      },
      "displayed": {
        "ncp": "2.4864749",
        "critical": "1.6448536",
        "df": "98920914",
        "n1": "49460458",
        "n2": "49460458",
        "n_total": "98920916",
        "actual_power": "0.8000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-05, protocol [6] 22:35:28. G*Power N differs from the inspection-side SPEC-rule computation (delta -2); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-040",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_deviation",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.0002",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.0002",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.4864749,
        "critical": 1.6448536,
        "df": 618255740,
        "n1": 309127871,
        "n2": 309127871,
        "n_total": 618255742,
        "actual_power": 0.8
      },
      "displayed": {
        "ncp": "2.4864749",
        "critical": "1.6448536",
        "df": "618255740",
        "n1": "309127871",
        "n2": "309127871",
        "n_total": "618255742",
        "actual_power": "0.8000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-06, protocol [7] 22:35:40. G*Power N differs from the inspection-side SPEC-rule computation (delta +16); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-041",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_deviation",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.0001",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.0001",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.4864764,
        "critical": 1.6448536,
        "df": 2473025908,
        "n1": 1236512955,
        "n2": 1236512955,
        "n_total": 2473025910,
        "actual_power": 0.8000004
      },
      "displayed": {
        "ncp": "2.4864764",
        "critical": "1.6448536",
        "df": "2473025908",
        "n1": "1236512955",
        "n2": "1236512955",
        "n_total": "2473025910",
        "actual_power": "0.8000004"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-07, protocol [8] 22:35:50. G*Power N differs from the inspection-side SPEC-rule computation (delta +3014); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-042",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_deviation",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.00005",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.00005",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.4864755,
        "critical": 1.6448536,
        "df": 9892096270,
        "n1": 4946048136,
        "n2": 4946048136,
        "n_total": 9892096272,
        "actual_power": 0.8
      },
      "displayed": {
        "ncp": "2.4864755",
        "critical": "1.6448536",
        "df": "9892096270",
        "n1": "4946048136",
        "n2": "4946048136",
        "n_total": "9892096272",
        "actual_power": "0.8000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-08, protocol [9] 22:36:01. G*Power N differs from the inspection-side SPEC-rule computation (delta +4698); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-043",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_deviation",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.00002",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.00002",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.4864856,
        "critical": 1.6448536,
        "df": 61826107834,
        "n1": 30913053918,
        "n2": 30913053918,
        "n_total": 61826107836,
        "actual_power": 0.8000056
      },
      "displayed": {
        "ncp": "2.4864856",
        "critical": "1.6448536",
        "df": "61826107834",
        "n1": "30913053918",
        "n2": "30913053918",
        "n_total": "61826107836",
        "actual_power": "0.8000056"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-09, protocol [10] 22:36:11. G*Power N differs from the inspection-side SPEC-rule computation (delta +535514); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-044",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_deviation",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.0008",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.0008",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.4864749,
        "critical": 1.6448537,
        "df": 38640982,
        "n1": 19320492,
        "n2": 19320492,
        "n_total": 38640984,
        "actual_power": 0.8
      },
      "displayed": {
        "ncp": "2.4864749",
        "critical": "1.6448537",
        "df": "38640982",
        "n1": "19320492",
        "n2": "19320492",
        "n_total": "38640984",
        "actual_power": "0.8000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-12, protocol [13] 22:37:18. G*Power N differs from the inspection-side SPEC-rule computation (delta -2); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-045",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_agrees",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.0009",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.0009",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.486475,
        "critical": 1.6448537,
        "df": 30531148,
        "n1": 15265575,
        "n2": 15265575,
        "n_total": 30531150,
        "actual_power": 0.8
      },
      "displayed": {
        "ncp": "2.4864750",
        "critical": "1.6448537",
        "df": "30531148",
        "n1": "15265575",
        "n2": "15265575",
        "n_total": "30531150",
        "actual_power": "0.8000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-13, protocol [14] 22:37:33. G*Power N equals the inspection-side SPEC-rule computation (delta +0); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-046",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_agrees",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "One",
        "d": "0.001",
        "alpha": "0.05",
        "power": "0.95",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.001",
        "--alpha",
        "0.05",
        "--power",
        "0.95",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 3.2897074,
        "critical": 1.6448537,
        "df": 43288696,
        "n1": 21644349,
        "n2": 21644349,
        "n_total": 43288698,
        "actual_power": 0.95
      },
      "displayed": {
        "ncp": "3.2897074",
        "critical": "1.6448537",
        "df": "43288696",
        "n1": "21644349",
        "n2": "21644349",
        "n_total": "43288698",
        "actual_power": "0.9500000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-14, protocol [15] 22:37:52. G*Power N equals the inspection-side SPEC-rule computation (delta +0); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-047",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_deviation",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.001",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.001",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.801582,
        "critical": 1.9599641,
        "df": 31395444,
        "n1": 15697723,
        "n2": 15697723,
        "n_total": 31395446,
        "actual_power": 0.8
      },
      "displayed": {
        "ncp": "2.8015820",
        "critical": "1.9599641",
        "df": "31395444",
        "n1": "15697723",
        "n2": "15697723",
        "n_total": "31395446",
        "actual_power": "0.8000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-15, protocol [16] 22:38:25. G*Power N differs from the inspection-side SPEC-rule computation (delta +2); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-048",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_deviation",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.001",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "2"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.001",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "2"
      ],
      "expected": {
        "ncp": 2.8015818,
        "critical": 1.9599641,
        "df": 35319872,
        "n1": 11773291,
        "n2": 23546583,
        "n_total": 35319874,
        "actual_power": 0.8
      },
      "displayed": {
        "ncp": "2.8015818",
        "critical": "1.9599641",
        "df": "35319872",
        "n1": "11773291",
        "n2": "23546583",
        "n_total": "35319874",
        "actual_power": "0.8000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-16, protocol [17] 22:38:38. G*Power N differs from the inspection-side SPEC-rule computation (delta -2); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-049",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_deviation",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.0005",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.0005",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.8015819,
        "critical": 1.959964,
        "df": 125581776,
        "n1": 62790889,
        "n2": 62790889,
        "n_total": 125581778,
        "actual_power": 0.8000001
      },
      "displayed": {
        "ncp": "2.8015819",
        "critical": "1.9599640",
        "df": "125581776",
        "n1": "62790889",
        "n2": "62790889",
        "n_total": "125581778",
        "actual_power": "0.8000001"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-17, protocol [18] 22:38:55. G*Power N differs from the inspection-side SPEC-rule computation (delta +6); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-050",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_deviation",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.0005",
        "alpha": "0.01",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.0005",
        "--alpha",
        "0.01",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 3.4174505,
        "critical": 2.5758293,
        "df": 186863488,
        "n1": 93431745,
        "n2": 93431745,
        "n_total": 186863490,
        "actual_power": 0.8
      },
      "displayed": {
        "ncp": "3.4174505",
        "critical": "2.5758293",
        "df": "186863488",
        "n1": "93431745",
        "n2": "93431745",
        "n_total": "186863490",
        "actual_power": "0.8000000"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-18, protocol [19] 22:39:06. G*Power N differs from the inspection-side SPEC-rule computation (delta -4); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "GP-AP-051",
      "test": "t2-indep",
      "mode": "a-priori",
      "source": "gpower_gui",
      "subgroup": "AP small d (round 3)",
      "class": "small_d_rule_agrees",
      "counts_in_success_rate": true,
      "inputs": {
        "tails": "Two",
        "d": "0.002",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.002",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.8015824,
        "critical": 1.9599643,
        "df": 7848862,
        "n1": 3924432,
        "n2": 3924432,
        "n_total": 7848864,
        "actual_power": 0.8000001
      },
      "displayed": {
        "ncp": "2.8015824",
        "critical": "1.9599643",
        "df": "7848862",
        "n1": "3924432",
        "n2": "3924432",
        "n_total": "7848864",
        "actual_power": "0.8000001"
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "observation_note": "Round 3 small-d measurement SD-19, protocol [20] 22:39:23. G*Power N equals the inspection-side SPEC-rule computation (delta +0); expected values are G*Power's and remain exact-match targets.",
      "cohort": "legacy_87",
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-B01",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "Two",
        "d": "1",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "2.9154759",
        "critical": "2.0369333",
        "df": "32",
        "n1": "17",
        "n2": "17",
        "n_total": "34",
        "actual_power": "0.8070367"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "1",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.9154759,
        "critical": 2.0369333,
        "df": 32,
        "n1": 17,
        "n2": 17,
        "n_total": 34,
        "actual_power": 0.8070367
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-B02",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "One",
        "d": "2",
        "alpha": "0.05",
        "power": "0.9",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "3.4641016",
        "critical": "1.8124611",
        "df": "10",
        "n1": "6",
        "n2": "6",
        "n_total": "12",
        "actual_power": "0.9420286"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "2",
        "--alpha",
        "0.05",
        "--power",
        "0.9",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 3.4641016,
        "critical": 1.8124611,
        "df": 10,
        "n1": 6,
        "n2": 6,
        "n_total": 12,
        "actual_power": 0.9420286
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-B03",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "Two",
        "d": "5",
        "alpha": "0.05",
        "power": "0.95",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "6.1237244",
        "critical": "2.7764451",
        "df": "4",
        "n1": "3",
        "n2": "3",
        "n_total": "6",
        "actual_power": "0.9927759"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "5",
        "--alpha",
        "0.05",
        "--power",
        "0.95",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 6.1237244,
        "critical": 2.7764451,
        "df": 4,
        "n1": 3,
        "n2": 3,
        "n_total": 6,
        "actual_power": 0.9927759
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-B04",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "Two",
        "d": "20",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "20.0000000",
        "critical": "4.3026527",
        "df": "2",
        "n1": "2",
        "n2": "2",
        "n_total": "4",
        "actual_power": "1.0000000"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "20",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 20.0,
        "critical": 4.3026527,
        "df": 2,
        "n1": 2,
        "n2": 2,
        "n_total": 4,
        "actual_power": 1.0
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-B05",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "One",
        "d": "-20",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "-20.0000000",
        "critical": "-2.9199856",
        "df": "2",
        "n1": "2",
        "n2": "2",
        "n_total": "4",
        "actual_power": "1.0000000"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "-20",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": -20.0,
        "critical": -2.9199856,
        "df": 2,
        "n1": 2,
        "n2": 2,
        "n_total": 4,
        "actual_power": 1.0
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "R6-R01",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "Two",
        "d": "20",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "100"
      },
      "displayed": {
        "ncp": "0",
        "critical": "2.7764451",
        "df": "4",
        "n1": "0",
        "n2": "6",
        "n_total": "6",
        "actual_power": "0.0500000"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "20",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "100"
      ],
      "expected": {
        "ncp": 0.0,
        "critical": 2.7764451,
        "df": 4,
        "n1": 0,
        "n2": 6,
        "n_total": 6,
        "actual_power": 0.05
      },
      "comparison": {
        "ncp": {
          "rule": "exact_zero",
          "abs_tol": 0.0
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-R02",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "One",
        "d": "5",
        "alpha": "0.05",
        "power": "0.9",
        "ratio": "0.01"
      },
      "displayed": {
        "ncp": "0",
        "critical": "1.6882977",
        "df": "36",
        "n1": "38",
        "n2": "0",
        "n_total": "38",
        "actual_power": "0.0500000"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "5",
        "--alpha",
        "0.05",
        "--power",
        "0.9",
        "--ratio",
        "0.01"
      ],
      "expected": {
        "ncp": 0.0,
        "critical": 1.6882977,
        "df": 36,
        "n1": 38,
        "n2": 0,
        "n_total": 38,
        "actual_power": 0.05
      },
      "comparison": {
        "ncp": {
          "rule": "exact_zero",
          "abs_tol": 0.0
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-S01",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "Two",
        "d": "10",
        "alpha": "0.0000001",
        "power": "0.95",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "18.7082869",
        "critical": "11.2389604",
        "df": "12",
        "n1": "7",
        "n2": "7",
        "n_total": "14",
        "actual_power": "0.9982578"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "10",
        "--alpha",
        "0.0000001",
        "--power",
        "0.95",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 18.7082869,
        "critical": 11.2389604,
        "df": 12,
        "n1": 7,
        "n2": 7,
        "n_total": 14,
        "actual_power": 0.9982578
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-S02",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "One",
        "d": "20",
        "alpha": "0.0000001",
        "power": "0.8",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "31.6227766",
        "critical": "16.3207038",
        "df": "8",
        "n1": "5",
        "n2": "5",
        "n_total": "10",
        "actual_power": "0.9997264"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "20",
        "--alpha",
        "0.0000001",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 31.6227766,
        "critical": 16.3207038,
        "df": 8,
        "n1": 5,
        "n2": 5,
        "n_total": 10,
        "actual_power": 0.9997264
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-S03",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "One",
        "d": "2",
        "alpha": "0.9",
        "power": "0.95",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "2.0000000",
        "critical": "-1.8856181",
        "df": "2",
        "n1": "2",
        "n2": "2",
        "n_total": "4",
        "actual_power": "0.9985888"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "2",
        "--alpha",
        "0.9",
        "--power",
        "0.95",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.0,
        "critical": -1.8856181,
        "df": 2,
        "n1": 2,
        "n2": 2,
        "n_total": 4,
        "actual_power": 0.9985888
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-T01",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "Two",
        "d": "0.2",
        "alpha": "0.01",
        "power": "0.95",
        "ratio": "0.5"
      },
      "displayed": {
        "ncp": "4.2242682",
        "critical": "2.5782824",
        "df": "2006",
        "n1": "1339",
        "n2": "669",
        "n_total": "2008",
        "actual_power": "0.9500094"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.2",
        "--alpha",
        "0.01",
        "--power",
        "0.95",
        "--ratio",
        "0.5"
      ],
      "expected": {
        "ncp": 4.2242682,
        "critical": 2.5782824,
        "df": 2006,
        "n1": 1339,
        "n2": 669,
        "n_total": 2008,
        "actual_power": 0.9500094
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-T02",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "One",
        "d": "0.7",
        "alpha": "0.01",
        "power": "0.95",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "4.0211939",
        "critical": "2.3553746",
        "df": "130",
        "n1": "66",
        "n2": "66",
        "n_total": "132",
        "actual_power": "0.9508125"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.7",
        "--alpha",
        "0.01",
        "--power",
        "0.95",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 4.0211939,
        "critical": 2.3553746,
        "df": 130,
        "n1": 66,
        "n2": 66,
        "n_total": 132,
        "actual_power": 0.9508125
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-T03",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "Two",
        "d": "0.6",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "0.5"
      },
      "displayed": {
        "ncp": "2.8565714",
        "critical": "1.9839715",
        "df": "100",
        "n1": "68",
        "n2": "34",
        "n_total": "102",
        "actual_power": "0.8075970"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.6",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "0.5"
      ],
      "expected": {
        "ncp": 2.8565714,
        "critical": 1.9839715,
        "df": 100,
        "n1": 68,
        "n2": 34,
        "n_total": 102,
        "actual_power": 0.807597
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-T04",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "Two",
        "d": "0.35",
        "alpha": "0.05",
        "power": "0.85",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "3.0108138",
        "critical": "1.9680657",
        "df": "294",
        "n1": "148",
        "n2": "148",
        "n_total": "296",
        "actual_power": "0.8510627"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.35",
        "--alpha",
        "0.05",
        "--power",
        "0.85",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 3.0108138,
        "critical": 1.9680657,
        "df": 294,
        "n1": 148,
        "n2": 148,
        "n_total": 296,
        "actual_power": 0.8510627
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-T05",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "One",
        "d": "0.3",
        "alpha": "0.1",
        "power": "0.8",
        "ratio": "0.5"
      },
      "displayed": {
        "ncp": "2.1354157",
        "critical": "1.2853087",
        "df": "226",
        "n1": "152",
        "n2": "76",
        "n_total": "228",
        "actual_power": "0.8023314"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.3",
        "--alpha",
        "0.1",
        "--power",
        "0.8",
        "--ratio",
        "0.5"
      ],
      "expected": {
        "ncp": 2.1354157,
        "critical": 1.2853087,
        "df": 226,
        "n1": 152,
        "n2": 76,
        "n_total": 228,
        "actual_power": 0.8023314
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-T06",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.1",
        "power": "0.8",
        "ratio": "3"
      },
      "displayed": {
        "ncp": "2.1576868",
        "critical": "1.2904324",
        "df": "96",
        "n1": "25",
        "n2": "73",
        "n_total": "98",
        "actual_power": "0.8069938"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.1",
        "--power",
        "0.8",
        "--ratio",
        "3"
      ],
      "expected": {
        "ncp": 2.1576868,
        "critical": 1.2904324,
        "df": 96,
        "n1": 25,
        "n2": 73,
        "n_total": 98,
        "actual_power": 0.8069938
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-T07",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "Two",
        "d": "0.45",
        "alpha": "0.1",
        "power": "0.8",
        "ratio": "2"
      },
      "displayed": {
        "ncp": "2.5144262",
        "critical": "1.6559704",
        "df": "138",
        "n1": "47",
        "n2": "93",
        "n_total": "140",
        "actual_power": "0.8043539"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.45",
        "--alpha",
        "0.1",
        "--power",
        "0.8",
        "--ratio",
        "2"
      ],
      "expected": {
        "ncp": 2.5144262,
        "critical": 1.6559704,
        "df": 138,
        "n1": 47,
        "n2": 93,
        "n_total": 140,
        "actual_power": 0.8043539
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-T08",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "One",
        "d": "0.45",
        "alpha": "0.01",
        "power": "0.8",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "3.1978508",
        "critical": "2.3451371",
        "df": "200",
        "n1": "101",
        "n2": "101",
        "n_total": "202",
        "actual_power": "0.8022908"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.45",
        "--alpha",
        "0.01",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 3.1978508,
        "critical": 2.3451371,
        "df": 200,
        "n1": 101,
        "n2": 101,
        "n_total": 202,
        "actual_power": 0.8022908
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-T09",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "One",
        "d": "0.6",
        "alpha": "0.1",
        "power": "0.8",
        "ratio": "1.5"
      },
      "displayed": {
        "ncp": "2.1664102",
        "critical": "1.2980450",
        "df": "52",
        "n1": "22",
        "n2": "32",
        "n_total": "54",
        "actual_power": "0.8072022"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.6",
        "--alpha",
        "0.1",
        "--power",
        "0.8",
        "--ratio",
        "1.5"
      ],
      "expected": {
        "ncp": 2.1664102,
        "critical": 1.298045,
        "df": 52,
        "n1": 22,
        "n2": 32,
        "n_total": 54,
        "actual_power": 0.8072022
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R6-T10",
      "round": 6,
      "purpose": "coverage_gap",
      "inputs": {
        "tails": "Two",
        "d": "0.4",
        "alpha": "0.1",
        "power": "0.8",
        "ratio": "2"
      },
      "displayed": {
        "ncp": "2.5050857",
        "critical": "1.6536580",
        "df": "174",
        "n1": "59",
        "n2": "117",
        "n_total": "176",
        "actual_power": "0.8024864"
      },
      "mode": "a-priori",
      "cohort": "round6",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.4",
        "--alpha",
        "0.1",
        "--power",
        "0.8",
        "--ratio",
        "2"
      ],
      "expected": {
        "ncp": 2.5050857,
        "critical": 1.653658,
        "df": 174,
        "n1": 59,
        "n2": 117,
        "n_total": 176,
        "actual_power": 0.8024864
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-I04",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.9999999",
        "power": "0.9999999",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "0.5000000",
        "critical": "1.414214e-07",
        "df": "2",
        "n1": "2",
        "n2": "2",
        "n_total": "4",
        "actual_power": "0.9999999"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.9999999",
        "--power",
        "0.9999999",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 0.5,
        "critical": 1.414214e-07,
        "df": 2,
        "n1": 2,
        "n2": 2,
        "n_total": 4,
        "actual_power": 0.9999999
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_significant_scientific",
          "abs_tol": 5e-14
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-I05",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "20",
        "alpha": "0.0000001",
        "power": "0.9999999",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "34.6410162",
        "critical": "13.4394118",
        "df": "10",
        "n1": "6",
        "n2": "6",
        "n_total": "12",
        "actual_power": "1.0000000"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "20",
        "--alpha",
        "0.0000001",
        "--power",
        "0.9999999",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 34.6410162,
        "critical": 13.4394118,
        "df": 10,
        "n1": 6,
        "n2": 6,
        "n_total": 12,
        "actual_power": 1.0
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-N01",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "-0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "2"
      },
      "displayed": {
        "ncp": "-2.8284271",
        "critical": "-1.9768110",
        "df": "142",
        "n1": "48",
        "n2": "96",
        "n_total": "144",
        "actual_power": "0.8021395"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "-0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "2"
      ],
      "expected": {
        "ncp": -2.8284271,
        "critical": -1.976811,
        "df": 142,
        "n1": 48,
        "n2": 96,
        "n_total": 144,
        "actual_power": 0.8021395
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "R7-N02",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "-0.3",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "0.5"
      },
      "displayed": {
        "ncp": "-2.4979992",
        "critical": "-1.6497838",
        "df": "310",
        "n1": "208",
        "n2": "104",
        "n_total": "312",
        "actual_power": "0.8016943"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "-0.3",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "0.5"
      ],
      "expected": {
        "ncp": -2.4979992,
        "critical": -1.6497838,
        "df": 310,
        "n1": 208,
        "n2": 104,
        "n_total": 312,
        "actual_power": 0.8016943
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "R7-N03",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "-0.8",
        "alpha": "0.01",
        "power": "0.9",
        "ratio": "1.5"
      },
      "displayed": {
        "ncp": "-3.9613822",
        "critical": "-2.6258905",
        "df": "100",
        "n1": "41",
        "n2": "61",
        "n_total": "102",
        "actual_power": "0.9064985"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "-0.8",
        "--alpha",
        "0.01",
        "--power",
        "0.9",
        "--ratio",
        "1.5"
      ],
      "expected": {
        "ncp": -3.9613822,
        "critical": -2.6258905,
        "df": 100,
        "n1": 41,
        "n2": 61,
        "n_total": 102,
        "actual_power": 0.9064985
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "R7-N04",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "-1",
        "alpha": "0.1",
        "power": "0.95",
        "ratio": "3"
      },
      "displayed": {
        "ncp": "-3.0000000",
        "critical": "-1.3002280",
        "df": "46",
        "n1": "12",
        "n2": "36",
        "n_total": "48",
        "actual_power": "0.9546154"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "-1",
        "--alpha",
        "0.1",
        "--power",
        "0.95",
        "--ratio",
        "3"
      ],
      "expected": {
        "ncp": -3.0,
        "critical": -1.300228,
        "df": 46,
        "n1": 12,
        "n2": 36,
        "n_total": 48,
        "actual_power": 0.9546154
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "R7-P01",
      "round": 7,
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "2",
        "n2": "5000"
      },
      "displayed": {
        "ncp": "0.7069654",
        "critical": "1.9604386",
        "df": "5000",
        "power": "0.1089073"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "2",
        "--n2",
        "5000"
      ],
      "expected": {
        "ncp": 0.7069654,
        "critical": 1.9604386,
        "df": 5000,
        "power": 0.1089073
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-P02",
      "round": 7,
      "mode": "post-hoc",
      "inputs": {
        "tails": "One",
        "d": "1",
        "alpha": "0.05",
        "n1": "1",
        "n2": "1000"
      },
      "displayed": {
        "ncp": "0.9995004",
        "critical": "1.6463803",
        "df": "999",
        "power": "0.2591300"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "1",
        "--alpha",
        "0.05",
        "--n1",
        "1",
        "--n2",
        "1000"
      ],
      "expected": {
        "ncp": 0.9995004,
        "critical": 1.6463803,
        "df": 999,
        "power": 0.25913
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "n1",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "approved n>=2 threshold at existing combined group check; field projection is a project decision"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "R7-P03",
      "round": 7,
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "2",
        "alpha": "0.0000001",
        "n1": "3",
        "n2": "3"
      },
      "displayed": {
        "ncp": "2.4494897",
        "critical": "87.9922353",
        "df": "4",
        "power": "2.496182e-06"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "2",
        "--alpha",
        "0.0000001",
        "--n1",
        "3",
        "--n2",
        "3"
      ],
      "expected": {
        "ncp": 2.4494897,
        "critical": 87.9922353,
        "df": 4,
        "power": 2.496182e-06
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_significant_scientific",
          "abs_tol": 5e-13
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-P04",
      "round": 7,
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "0.004",
        "alpha": "0.05",
        "n1": "500000",
        "n2": "500000"
      },
      "displayed": {
        "ncp": "2.0000000",
        "critical": "1.9599664",
        "df": "999998",
        "power": "0.5160045"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.004",
        "--alpha",
        "0.05",
        "--n1",
        "500000",
        "--n2",
        "500000"
      ],
      "expected": {
        "ncp": 2.0,
        "critical": 1.9599664,
        "df": 999998,
        "power": 0.5160045
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-P05",
      "round": 7,
      "mode": "post-hoc",
      "inputs": {
        "tails": "One",
        "d": "0.0004",
        "alpha": "0.05",
        "n1": "50000000",
        "n2": "50000000"
      },
      "displayed": {
        "ncp": "2.0000000",
        "critical": "1.6448536",
        "df": "99999998",
        "power": "0.6387600"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0.0004",
        "--alpha",
        "0.05",
        "--n1",
        "50000000",
        "--n2",
        "50000000"
      ],
      "expected": {
        "ncp": 2.0,
        "critical": 1.6448536,
        "df": 99999998,
        "power": 0.63876
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-P06",
      "round": 7,
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "-0.3",
        "alpha": "0.01",
        "n1": "40",
        "n2": "120"
      },
      "displayed": {
        "ncp": "-1.6431677",
        "critical": "-2.6073037",
        "df": "158",
        "power": "0.1711038"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "-0.3",
        "--alpha",
        "0.01",
        "--n1",
        "40",
        "--n2",
        "120"
      ],
      "expected": {
        "ncp": -1.6431677,
        "critical": -2.6073037,
        "df": 158,
        "power": 0.1711038
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      },
      "counts_in_contract_numeric_rate": false,
      "counts_in_contract_error_rate": true
    },
    {
      "id": "R7-Q01",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1.3"
      },
      "displayed": {
        "ncp": "2.8287671",
        "critical": "1.9786708",
        "df": "128",
        "n1": "57",
        "n2": "73",
        "n_total": "130",
        "actual_power": "0.8016480"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1.3"
      ],
      "expected": {
        "ncp": 2.8287671,
        "critical": 1.9786708,
        "df": 128,
        "n1": 57,
        "n2": 73,
        "n_total": 130,
        "actual_power": 0.801648
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-Q02",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0.4",
        "alpha": "0.05",
        "power": "0.9",
        "ratio": "2.7"
      },
      "displayed": {
        "ncp": "2.9397850",
        "critical": "1.6504750",
        "df": "272",
        "n1": "74",
        "n2": "200",
        "n_total": "274",
        "actual_power": "0.9010587"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.4",
        "--alpha",
        "0.05",
        "--power",
        "0.9",
        "--ratio",
        "2.7"
      ],
      "expected": {
        "ncp": 2.939785,
        "critical": 1.650475,
        "df": 272,
        "n1": 74,
        "n2": 200,
        "n_total": 274,
        "actual_power": 0.9010587
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-Q03",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.6",
        "alpha": "0.01",
        "power": "0.9",
        "ratio": "0.37"
      },
      "displayed": {
        "ncp": "3.9014016",
        "critical": "2.5992184",
        "df": "212",
        "n1": "156",
        "n2": "58",
        "n_total": "214",
        "actual_power": "0.9023350"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.6",
        "--alpha",
        "0.01",
        "--power",
        "0.9",
        "--ratio",
        "0.37"
      ],
      "expected": {
        "ncp": 3.9014016,
        "critical": 2.5992184,
        "df": 212,
        "n1": 156,
        "n2": 58,
        "n_total": 214,
        "actual_power": 0.902335
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-Q04",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0.3",
        "alpha": "0.1",
        "power": "0.8",
        "ratio": "1.7"
      },
      "displayed": {
        "ncp": "2.1291626",
        "critical": "1.2855201",
        "df": "214",
        "n1": "80",
        "n2": "136",
        "n_total": "216",
        "actual_power": "0.8005309"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.3",
        "--alpha",
        "0.1",
        "--power",
        "0.8",
        "--ratio",
        "1.7"
      ],
      "expected": {
        "ncp": 2.1291626,
        "critical": 1.2855201,
        "df": 214,
        "n1": 80,
        "n2": 136,
        "n_total": 216,
        "actual_power": 0.8005309
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-Q05",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.8",
        "alpha": "0.05",
        "power": "0.95",
        "ratio": "0.6"
      },
      "displayed": {
        "ncp": "3.6796135",
        "critical": "1.9872899",
        "df": "88",
        "n1": "56",
        "n2": "34",
        "n_total": "90",
        "actual_power": "0.9534438"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.8",
        "--alpha",
        "0.05",
        "--power",
        "0.95",
        "--ratio",
        "0.6"
      ],
      "expected": {
        "ncp": 3.6796135,
        "critical": 1.9872899,
        "df": 88,
        "n1": 56,
        "n2": 34,
        "n_total": 90,
        "actual_power": 0.9534438
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-T01",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.65",
        "alpha": "0.1",
        "power": "0.85",
        "ratio": "1"
      },
      "displayed": {
        "ncp": "2.7191451",
        "critical": "1.6675723",
        "df": "68",
        "n1": "35",
        "n2": "35",
        "n_total": "70",
        "actual_power": "0.8524751"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.65",
        "--alpha",
        "0.1",
        "--power",
        "0.85",
        "--ratio",
        "1"
      ],
      "expected": {
        "ncp": 2.7191451,
        "critical": 1.6675723,
        "df": 68,
        "n1": 35,
        "n2": 35,
        "n_total": 70,
        "actual_power": 0.8524751
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-T02",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0.35",
        "alpha": "0.01",
        "power": "0.8",
        "ratio": "0.75"
      },
      "displayed": {
        "ncp": "3.1847280",
        "critical": "2.3374972",
        "df": "336",
        "n1": "193",
        "n2": "145",
        "n_total": "338",
        "actual_power": "0.8010961"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.35",
        "--alpha",
        "0.01",
        "--power",
        "0.8",
        "--ratio",
        "0.75"
      ],
      "expected": {
        "ncp": 3.184728,
        "critical": 2.3374972,
        "df": 336,
        "n1": 193,
        "n2": 145,
        "n_total": 338,
        "actual_power": 0.8010961
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-T03",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0.2",
        "alpha": "0.01",
        "power": "0.85",
        "ratio": "0.5"
      },
      "displayed": {
        "ncp": "3.3671612",
        "critical": "2.3292785",
        "df": "1274",
        "n1": "851",
        "n2": "425",
        "n_total": "1276",
        "actual_power": "0.8501871"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.2",
        "--alpha",
        "0.01",
        "--power",
        "0.85",
        "--ratio",
        "0.5"
      ],
      "expected": {
        "ncp": 3.3671612,
        "critical": 2.3292785,
        "df": 1274,
        "n1": 851,
        "n2": 425,
        "n_total": 1276,
        "actual_power": 0.8501871
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-T04",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0.75",
        "alpha": "0.01",
        "power": "0.85",
        "ratio": "3"
      },
      "displayed": {
        "ncp": "3.4265010",
        "critical": "2.3613721",
        "df": "108",
        "n1": "28",
        "n2": "82",
        "n_total": "110",
        "actual_power": "0.8547573"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.75",
        "--alpha",
        "0.01",
        "--power",
        "0.85",
        "--ratio",
        "3"
      ],
      "expected": {
        "ncp": 3.426501,
        "critical": 2.3613721,
        "df": 108,
        "n1": 28,
        "n2": 82,
        "n_total": 110,
        "actual_power": 0.8547573
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-T05",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0.35",
        "alpha": "0.025",
        "power": "0.8",
        "ratio": "3"
      },
      "displayed": {
        "ncp": "2.8109162",
        "critical": "1.9669246",
        "df": "342",
        "n1": "86",
        "n2": "258",
        "n_total": "344",
        "actual_power": "0.8003999"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.35",
        "--alpha",
        "0.025",
        "--power",
        "0.8",
        "--ratio",
        "3"
      ],
      "expected": {
        "ncp": 2.8109162,
        "critical": 1.9669246,
        "df": 342,
        "n1": 86,
        "n2": 258,
        "n_total": 344,
        "actual_power": 0.8003999
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-T06",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0.45",
        "alpha": "0.01",
        "power": "0.99",
        "ratio": "0.5"
      },
      "displayed": {
        "ncp": "4.6644886",
        "critical": "2.3341092",
        "df": "482",
        "n1": "323",
        "n2": "161",
        "n_total": "484",
        "actual_power": "0.9899646"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.45",
        "--alpha",
        "0.01",
        "--power",
        "0.99",
        "--ratio",
        "0.5"
      ],
      "expected": {
        "ncp": 4.6644886,
        "critical": 2.3341092,
        "df": 482,
        "n1": 323,
        "n2": 161,
        "n_total": 484,
        "actual_power": 0.9899646
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-T07",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.2",
        "alpha": "0.05",
        "power": "0.85",
        "ratio": "2"
      },
      "displayed": {
        "ncp": "2.9985174",
        "critical": "1.9623155",
        "df": "1010",
        "n1": "337",
        "n2": "675",
        "n_total": "1012",
        "actual_power": "0.8498295"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.2",
        "--alpha",
        "0.05",
        "--power",
        "0.85",
        "--ratio",
        "2"
      ],
      "expected": {
        "ncp": 2.9985174,
        "critical": 1.9623155,
        "df": 1010,
        "n1": 337,
        "n2": 675,
        "n_total": 1012,
        "actual_power": 0.8498295
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-T08",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.25",
        "alpha": "0.05",
        "power": "0.99",
        "ratio": "2"
      },
      "displayed": {
        "ncp": "4.2914644",
        "critical": "1.9617573",
        "df": "1324",
        "n1": "442",
        "n2": "884",
        "n_total": "1326",
        "actual_power": "0.9900542"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.25",
        "--alpha",
        "0.05",
        "--power",
        "0.99",
        "--ratio",
        "2"
      ],
      "expected": {
        "ncp": 4.2914644,
        "critical": 1.9617573,
        "df": 1324,
        "n1": 442,
        "n2": 884,
        "n_total": 1326,
        "actual_power": 0.9900542
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-T09",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.25",
        "alpha": "0.01",
        "power": "0.95",
        "ratio": "3"
      },
      "displayed": {
        "ncp": "4.2260354",
        "critical": "2.5790634",
        "df": "1522",
        "n1": "381",
        "n2": "1143",
        "n_total": "1524",
        "actual_power": "0.9500768"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.25",
        "--alpha",
        "0.01",
        "--power",
        "0.95",
        "--ratio",
        "3"
      ],
      "expected": {
        "ncp": 4.2260354,
        "critical": 2.5790634,
        "df": 1522,
        "n1": 381,
        "n2": 1143,
        "n_total": 1524,
        "actual_power": 0.9500768
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R7-T10",
      "round": 7,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.25",
        "alpha": "0.025",
        "power": "0.95",
        "ratio": "0.75"
      },
      "displayed": {
        "ncp": "3.8923650",
        "critical": "2.2448242",
        "df": "988",
        "n1": "566",
        "n2": "424",
        "n_total": "990",
        "actual_power": "0.9501192"
      },
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.25",
        "--alpha",
        "0.025",
        "--power",
        "0.95",
        "--ratio",
        "0.75"
      ],
      "expected": {
        "ncp": 3.892365,
        "critical": 2.2448242,
        "df": 988,
        "n1": 566,
        "n2": 424,
        "n_total": 990,
        "actual_power": 0.9501192
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R8-B01",
      "round": 8,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "20",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "6.999999"
      },
      "displayed": {
        "ncp": "17.3205081",
        "critical": "4.3026527",
        "df": "2",
        "n1": "1",
        "n2": "3",
        "n_total": "4",
        "actual_power": "0.9999996"
      },
      "cohort": "round8",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "20",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "6.999999"
      ],
      "expected": {
        "ncp": 17.3205081,
        "critical": 4.3026527,
        "df": 2,
        "n1": 1,
        "n2": 3,
        "n_total": 4,
        "actual_power": 0.9999996
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R8-B02",
      "round": 8,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "20",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "7"
      },
      "displayed": {
        "ncp": "17.3205081",
        "critical": "4.3026527",
        "df": "2",
        "n1": "1",
        "n2": "3",
        "n_total": "4",
        "actual_power": "0.9999996"
      },
      "cohort": "round8",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "20",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "7"
      ],
      "expected": {
        "ncp": 17.3205081,
        "critical": 4.3026527,
        "df": 2,
        "n1": 1,
        "n2": 3,
        "n_total": 4,
        "actual_power": 0.9999996
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R8-B03",
      "round": 8,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "20",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "7.000001"
      },
      "displayed": {
        "ncp": "0",
        "critical": "4.3026527",
        "df": "2",
        "n1": "0",
        "n2": "4",
        "n_total": "4",
        "actual_power": "0.0500000"
      },
      "cohort": "round8",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "20",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "7.000001"
      ],
      "expected": {
        "ncp": 0.0,
        "critical": 4.3026527,
        "df": 2,
        "n1": 0,
        "n2": 4,
        "n_total": 4,
        "actual_power": 0.05
      },
      "comparison": {
        "ncp": {
          "rule": "exact_zero",
          "abs_tol": 0.0
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R8-B04",
      "round": 8,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.55",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "2.9999999"
      },
      "displayed": {
        "ncp": "2.8511673",
        "critical": "1.9770537",
        "df": "140",
        "n1": "36",
        "n2": "106",
        "n_total": "142",
        "actual_power": "0.8082856"
      },
      "cohort": "round8",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.55",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "2.9999999"
      ],
      "expected": {
        "ncp": 2.8511673,
        "critical": 1.9770537,
        "df": 140,
        "n1": 36,
        "n2": 106,
        "n_total": 142,
        "actual_power": 0.8082856
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R8-B05",
      "round": 8,
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.55",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "3.0000001"
      },
      "displayed": {
        "ncp": "2.8245185",
        "critical": "1.9770537",
        "df": "140",
        "n1": "35",
        "n2": "107",
        "n_total": "142",
        "actual_power": "0.8009815"
      },
      "cohort": "round8",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.55",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "3.0000001"
      ],
      "expected": {
        "ncp": 2.8245185,
        "critical": 1.9770537,
        "df": 140,
        "n1": 35,
        "n2": 107,
        "n_total": 142,
        "actual_power": 0.8009815
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "df": {
          "rule": "exact_integer"
        },
        "n1": {
          "rule": "exact_integer"
        },
        "n2": {
          "rule": "exact_integer"
        },
        "n_total": {
          "rule": "exact_integer"
        },
        "actual_power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R8-B06",
      "round": 8,
      "mode": "post-hoc",
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.4999999",
        "n1": "3",
        "n2": "7"
      },
      "displayed": {
        "ncp": "0.7245688",
        "critical": "2.585991e-07",
        "df": "8",
        "power": "0.7656416"
      },
      "cohort": "round8",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.4999999",
        "--n1",
        "3",
        "--n2",
        "7"
      ],
      "expected": {
        "ncp": 0.7245688,
        "critical": 2.585991e-07,
        "df": 8,
        "power": 0.7656416
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_significant_scientific",
          "abs_tol": 5e-14
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R8-B07",
      "round": 8,
      "mode": "post-hoc",
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.5",
        "n1": "3",
        "n2": "7"
      },
      "displayed": {
        "ncp": "0.7245688",
        "critical": "6.848145e-17",
        "df": "8",
        "power": "0.7656417"
      },
      "cohort": "round8",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.5",
        "--n1",
        "3",
        "--n2",
        "7"
      ],
      "expected": {
        "ncp": 0.7245688,
        "critical": 6.848145e-17,
        "df": 8,
        "power": 0.7656417
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_significant_scientific",
          "abs_tol": 5e-24
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    },
    {
      "id": "R8-B08",
      "round": 8,
      "mode": "post-hoc",
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.5000001",
        "n1": "3",
        "n2": "7"
      },
      "displayed": {
        "ncp": "0.7245688",
        "critical": "-2.585991e-07",
        "df": "8",
        "power": "0.7656418"
      },
      "cohort": "round8",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.5000001",
        "--n1",
        "3",
        "--n2",
        "7"
      ],
      "expected": {
        "ncp": 0.7245688,
        "critical": -2.585991e-07,
        "df": 8,
        "power": 0.7656418
      },
      "comparison": {
        "ncp": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        },
        "critical": {
          "rule": "displayed_significant_scientific",
          "abs_tol": 5e-14
        },
        "df": {
          "rule": "exact_integer"
        },
        "power": {
          "rule": "displayed_decimals",
          "decimals": 7,
          "abs_tol": 5e-08
        }
      },
      "counts_in_success_rate": true,
      "cli_expectation": {
        "outcome": "success",
        "exit_code": 0,
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ],
        "expected_from": "vector.expected",
        "field_mapping": "cli_field_mapping",
        "strict_comparison_from": "vector.comparison",
        "contract_comparison": "contract_numeric_rule"
      },
      "counts_in_contract_numeric_rate": true,
      "counts_in_contract_error_rate": false
    }
  ],
  "invalid": [
    {
      "id": "INV-GUI-001",
      "source": "gpower_gui",
      "gui_outcome": "accepted_malformed_text",
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.050.05",
        "power": "0.950.95",
        "ratio": "11"
      },
      "observed_gui_behavior": "Malformed numeric text accepted without error: '0.050.05'->0.05, '0.950.95'->0.95, '11'->11 (leading numeric prefix). G*Power produced a result; NOT a GUI rejection. Run [2] was preceded by an unintended run [1] (Return key) with the GP-AP-001 inputs.",
      "observed_outputs": {
        "ncp": "3.3150375",
        "crit": "1.6475407",
        "df": "568",
        "n1": "48",
        "n2": "522",
        "N": "570",
        "power": "0.9521664"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.050.05",
        "--power",
        "0.950.95",
        "--ratio",
        "11"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_NOT_A_NUMBER"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "INVALID_VALUE",
        "field": "alpha",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "numeric format phase"
      }
    },
    {
      "id": "INV-GUI-002",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.03",
        "ratio": "1"
      },
      "observed_gui_behavior": "Modal 'Input error': 'Power must be greater than or equal to alpha.' Outputs reset to '?'. No protocol entry added.",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.03",
        "--ratio",
        "1"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_POWER_LT_ALPHA"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "INCONSISTENT",
        "field": "power",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "observed power < alpha rejection"
      }
    },
    {
      "id": "INV-GUI-003",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "observed_gui_behavior": "Modal 'Input error': 'In an a priori analysis, the absolute value of the effect size must be greater than 0.00001.' Outputs '?'.",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_D_TOO_SMALL"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "INV-GUI-004",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "1",
        "n2": "1"
      },
      "observed_gui_behavior": "Modal 'Input error': 'Total sample size is outside the admissible range (3, 2147483646)'. Outputs '?'.",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "1",
        "--n2",
        "1"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_N_TOTAL"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "n1",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "approved n>=2 threshold at existing combined group check; field projection is a project decision"
      }
    },
    {
      "id": "INV-GUI-005",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "0",
        "n2": "10"
      },
      "observed_gui_behavior": "Modal 'Input error': 'Sample size must be greater than or equal to 1.'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "0",
        "--n2",
        "10"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_N_GROUP"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "n1",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "approved n>=2 threshold at existing combined group check; field projection is a project decision"
      }
    },
    {
      "id": "INV-GUI-006",
      "source": "gpower_gui",
      "gui_outcome": "accepted_with_conversion",
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "10.5",
        "n2": "10"
      },
      "observed_gui_behavior": "fractional n1 accepted; outputs equal to n1=11 (round to nearest, .5 up); protocol echoes 10.5",
      "observed_outputs": {
        "ncp": "1.1443443",
        "crit": "2.0930241",
        "df": "19",
        "power": "0.1925307"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "10.5",
        "--n2",
        "10"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_NOT_INTEGER"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "INVALID_VALUE",
        "field": "n1",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "numeric format phase"
      }
    },
    {
      "id": "INV-GUI-007",
      "source": "gpower_gui",
      "gui_outcome": "accepted_with_conversion",
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "10.4",
        "n2": "10"
      },
      "observed_gui_behavior": "fractional n1 10.4 computed as 10",
      "observed_outputs": {
        "ncp": "1.1180340",
        "crit": "2.1009220",
        "df": "18",
        "power": "0.1850957"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "10.4",
        "--n2",
        "10"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_NOT_INTEGER"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "INVALID_VALUE",
        "field": "n1",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "numeric format phase"
      }
    },
    {
      "id": "INV-GUI-008",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "21",
        "alpha": "0.05",
        "n1": "10",
        "n2": "10"
      },
      "observed_gui_behavior": "Modal 'Input error': 'Effect size d is outside the admissible range (-20, 20).'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "21",
        "--alpha",
        "0.05",
        "--n1",
        "10",
        "--n2",
        "10"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_D_RANGE"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "INV-GUI-009",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0",
        "n1": "10",
        "n2": "10"
      },
      "observed_gui_behavior": "Modal 'Input error': 'Alpha is outside the admissible range (1e-07, 1).'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0",
        "--n1",
        "10",
        "--n2",
        "10"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_ALPHA_RANGE"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "alpha",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "INV-GUI-010",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "1",
        "n1": "10",
        "n2": "10"
      },
      "observed_gui_behavior": "Modal 'Input error': 'Alpha is outside the admissible range (1e-07, 1).' (alpha=1 rejected)",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "1",
        "--n1",
        "10",
        "--n2",
        "10"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_ALPHA_RANGE"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "alpha",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "INV-GUI-011",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "1",
        "ratio": "1"
      },
      "observed_gui_behavior": "Modal 'Input error': 'Power is outside the admissible range (1e-07, 1).'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "1",
        "--ratio",
        "1"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_POWER_RANGE"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "power",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "INV-GUI-012",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "0"
      },
      "observed_gui_behavior": "Modal 'Input error': 'The allocation ratio falls outside the admissible range (0.01, 100).'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "0"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_RATIO_RANGE"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "ratio",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "INV-GUI-013",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "101"
      },
      "observed_gui_behavior": "Modal 'Input error': 'The allocation ratio falls outside the admissible range (0.01, 100).'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "101"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_RATIO_RANGE"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "ratio",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "INV-GUI-022",
      "source": "gpower_gui",
      "gui_outcome": "accepted_malformed_text",
      "mode": "a-priori",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1/3"
      },
      "observed_gui_behavior": "ratio text '1/3' NOT evaluated as a fraction: computed as ratio 1 (64/64) while protocol echoes '1/3'",
      "observed_outputs": {
        "ncp": "2.8284271",
        "crit": "1.9789706",
        "df": "126",
        "n1": "64",
        "n2": "64",
        "N": "128",
        "power": "0.8014596"
      },
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1/3"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_NOT_A_NUMBER"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "INVALID_VALUE",
        "field": "ratio",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "numeric format phase"
      }
    },
    {
      "id": "INV-GUI-014",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.000000099",
        "n1": "20",
        "n2": "20"
      },
      "observed_gui_behavior": "Modal 'Input error': 'Alpha is outside the admissible range (1e-07, 1).'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.000000099",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_ALPHA_RANGE"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "alpha",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "INV-GUI-015",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "20.01",
        "alpha": "0.05",
        "n1": "20",
        "n2": "20"
      },
      "observed_gui_behavior": "Modal 'Input error': 'Effect size d is outside the admissible range (-20, 20).'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "20.01",
        "--alpha",
        "0.05",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_D_RANGE"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "INV-GUI-016",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "-20.01",
        "alpha": "0.05",
        "n1": "20",
        "n2": "20"
      },
      "observed_gui_behavior": "Modal 'Input error': 'Effect size d is outside the admissible range (-20, 20).'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "-20.01",
        "--alpha",
        "0.05",
        "--n1",
        "20",
        "--n2",
        "20"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_D_RANGE"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "INV-GUI-017",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "post-hoc",
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "n1": "1073741823",
        "n2": "1073741824"
      },
      "observed_gui_behavior": "Modal 'Input error': 'Total sample size is outside the admissible range (3, 2147483646)' (total 2147483647)",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "post-hoc",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--n1",
        "1073741823",
        "--n2",
        "1073741824"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_N_TOTAL"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "n_total",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "provisional mapping for observed post-hoc total limit; derived field"
      }
    },
    {
      "id": "INV-GUI-018",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0.0000099",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "observed_gui_behavior": "Modal 'Input error': 'In an a priori analysis, the absolute value of the effect size must be greater than 0.00001.'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.0000099",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_D_TOO_SMALL"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "provisional mapping for observed a-priori lower-d rejection"
      }
    },
    {
      "id": "INV-GUI-019",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.0499999",
        "ratio": "1"
      },
      "observed_gui_behavior": "Modal 'Input error': 'Power must be greater than or equal to alpha.'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.0499999",
        "--ratio",
        "1"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_POWER_LT_ALPHA"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "INCONSISTENT",
        "field": "power",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "observed power < alpha rejection"
      }
    },
    {
      "id": "INV-GUI-020",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "0.0099"
      },
      "observed_gui_behavior": "Modal 'Input error': 'The allocation ratio falls outside the admissible range (0.01, 100).'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "0.0099"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_RATIO_RANGE"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "ratio",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "INV-GUI-021",
      "source": "gpower_gui",
      "gui_outcome": "rejected_by_gui",
      "mode": "a-priori",
      "inputs": {
        "tails": "One",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "100.01"
      },
      "observed_gui_behavior": "Modal 'Input error': 'The allocation ratio falls outside the admissible range (0.01, 100).'",
      "observed_outputs": null,
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "1",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "100.01"
      ],
      "cohort": "legacy_input_22",
      "historical_expected_cli_spec_1_0_4": {
        "exit_code": 2,
        "stdout": "single-line JSON with only key error",
        "error_category": "E_RATIO_RANGE"
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "ratio",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "R7-I01",
      "round": 7,
      "mode": "a-priori",
      "kind": "rejected_by_gui",
      "protocol_run": null,
      "inputs": {
        "tails": "Two",
        "d": "0.5",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "-1"
      },
      "gui_message": "The allocation ratio falls outside the admissible range (0.01, 100).",
      "screenshot": "oracle/screenshots/R7-I01_01.png",
      "screenshot_sha256": "e115dfe9e72fd8948c4a9ea0850f5c3934eac0f16bd96e673b93b5efd77080ff",
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "0.5",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "-1"
      ],
      "gui_outcome": "rejected_by_gui",
      "observed_gui_behavior": "The allocation ratio falls outside the admissible range (0.01, 100).",
      "observed_outputs": null,
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "ratio",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "R7-I02",
      "round": 7,
      "mode": "a-priori",
      "kind": "rejected_by_gui",
      "protocol_run": null,
      "inputs": {
        "tails": "Two",
        "d": "20.01",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "gui_message": "Effect size d is outside the admissible range (-20, 20).",
      "screenshot": "oracle/screenshots/R7-I02_01.png",
      "screenshot_sha256": "8a8f4ee98b1913e03975d32e721c2537daac8d6fac4b06aa53517d749bfd2240",
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "20.01",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "gui_outcome": "rejected_by_gui",
      "observed_gui_behavior": "Effect size d is outside the admissible range (-20, 20).",
      "observed_outputs": null,
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    },
    {
      "id": "R7-I03",
      "round": 7,
      "mode": "a-priori",
      "kind": "rejected_by_gui",
      "protocol_run": null,
      "inputs": {
        "tails": "Two",
        "d": "-20.01",
        "alpha": "0.05",
        "power": "0.8",
        "ratio": "1"
      },
      "gui_message": "Effect size d is outside the admissible range (-20, 20).",
      "screenshot": "oracle/screenshots/R7-I03_01.png",
      "screenshot_sha256": "14cc487666ec72b37d29239f99274d1a1fbdbd6d2658831d8d1a90203f61b7f9",
      "cohort": "round7",
      "test": "t2-indep",
      "source": "gpower_gui",
      "cli_argv": [
        "--test",
        "t2-indep",
        "--mode",
        "a-priori",
        "--tails",
        "2",
        "--d",
        "-20.01",
        "--alpha",
        "0.05",
        "--power",
        "0.8",
        "--ratio",
        "1"
      ],
      "gui_outcome": "rejected_by_gui",
      "observed_gui_behavior": "Effect size d is outside the admissible range (-20, 20).",
      "observed_outputs": null,
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "OUT_OF_RANGE",
        "field": "d",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "CONTRACT section 5 or explicitly provisional narrower GUI range"
      }
    }
  ],
  "agent_cases": [
    {
      "id": "AG-01",
      "kind": "core",
      "question": "Yeni bir antihipertansif ilacı plaseboyla karşılaştıracağız (paralel iki bağımsız grup). Beklenen etki büyüklüğü Cohen d = 0,5; iki yönlü test, alfa 0,05 ve %95 güç istiyoruz. Gruplar eşit büyüklükte olacak. Her gruba kaç hasta almalıyız?",
      "expected_test": "t2-indep",
      "expected_parameters": {
        "mode": "a-priori",
        "tails": 2,
        "d": 0.5,
        "alpha": 0.05,
        "power": 0.95,
        "ratio": 1.0
      },
      "expected_n1": 105,
      "expected_n2": 105,
      "expected_n_total": 210,
      "reference_vector_id": "GP-AP-001",
      "expected_action": "call_tool_and_report_tool_result"
    },
    {
      "id": "AG-02",
      "kind": "core",
      "question": "Bir ağrı kesicinin plasebodan daha etkili olduğunu (tek yönlü hipotez) göstermek istiyoruz. Cohen d = 0,5, alfa 0,05, güç %95, iki bağımsız grup eşit büyüklükte. Toplam kaç katılımcı gerekir?",
      "expected_test": "t2-indep",
      "expected_parameters": {
        "mode": "a-priori",
        "tails": 1,
        "d": 0.5,
        "alpha": 0.05,
        "power": 0.95,
        "ratio": 1.0
      },
      "expected_n1": 88,
      "expected_n2": 88,
      "expected_n_total": 176,
      "reference_vector_id": "GP-AP-002",
      "expected_action": "call_tool_and_report_tool_result"
    },
    {
      "id": "AG-03",
      "kind": "core",
      "question": "İki bağımsız tedavi grubunda ortalama iyileşme süresini karşılaştıracağız. Etki büyük, Cohen d = 0,8. İki yönlü test, alfa 0,05, güç %80, eşit gruplar. Grup başına örneklem büyüklüğü nedir?",
      "expected_test": "t2-indep",
      "expected_parameters": {
        "mode": "a-priori",
        "tails": 2,
        "d": 0.8,
        "alpha": 0.05,
        "power": 0.8,
        "ratio": 1.0
      },
      "expected_n1": 26,
      "expected_n2": 26,
      "expected_n_total": 52,
      "reference_vector_id": "GP-AP-003",
      "expected_action": "call_tool_and_report_tool_result"
    },
    {
      "id": "AG-04",
      "kind": "core",
      "question": "Diyet programının kolesterolü kontrol grubuna göre düşürdüğünü (tek yönlü) test edeceğiz. Küçük bir etki bekliyoruz: Cohen d = 0,2. Alfa 0,05, güç %80, iki bağımsız eşit grup. Kaç kişiye ihtiyacımız var?",
      "expected_test": "t2-indep",
      "expected_parameters": {
        "mode": "a-priori",
        "tails": 1,
        "d": 0.2,
        "alpha": 0.05,
        "power": 0.8,
        "ratio": 1.0
      },
      "expected_n1": 310,
      "expected_n2": 310,
      "expected_n_total": 620,
      "reference_vector_id": "GP-AP-004",
      "expected_action": "call_tool_and_report_tool_result"
    },
    {
      "id": "AG-05",
      "kind": "core",
      "question": "İki farklı fizik tedavi protokolünü bağımsız gruplarda karşılaştıracağız. Cohen d = 0,5; iki yönlü test; anlamlılık düzeyini sıkı tutup alfa 0,01 alıyoruz; güç %90; eşit gruplar. Her grupta kaç hasta olmalı?",
      "expected_test": "t2-indep",
      "expected_parameters": {
        "mode": "a-priori",
        "tails": 2,
        "d": 0.5,
        "alpha": 0.01,
        "power": 0.9,
        "ratio": 1.0
      },
      "expected_n1": 121,
      "expected_n2": 121,
      "expected_n_total": 242,
      "reference_vector_id": "GP-AP-005",
      "expected_action": "call_tool_and_report_tool_result"
    },
    {
      "id": "AG-06",
      "kind": "core",
      "question": "Pilot nitelikli bir çalışmada iki bağımsız grubun ortalama kan şekeri değerlerini karşılaştıracağız. Cohen d = 0,3; iki yönlü test; alfa 0,10; güç %85; eşit gruplar. Toplam örneklem kaç olmalı?",
      "expected_test": "t2-indep",
      "expected_parameters": {
        "mode": "a-priori",
        "tails": 2,
        "d": 0.3,
        "alpha": 0.1,
        "power": 0.85,
        "ratio": 1.0
      },
      "expected_n1": 161,
      "expected_n2": 161,
      "expected_n_total": 322,
      "reference_vector_id": "GP-AP-006",
      "expected_action": "call_tool_and_report_tool_result"
    },
    {
      "id": "AG-07",
      "kind": "core",
      "question": "Grup 1 kontrol (plasebo), grup 2 yeni ilaç olacak ve grup 2, grup 1'in iki katı büyüklükte olacak (N2/N1 = 2). Cohen d = 0,5; iki yönlü test; alfa 0,05; güç %80. Her gruba kaç hasta almalıyız?",
      "expected_test": "t2-indep",
      "expected_parameters": {
        "mode": "a-priori",
        "tails": 2,
        "d": 0.5,
        "alpha": 0.05,
        "power": 0.8,
        "ratio": 2.0
      },
      "expected_n1": 48,
      "expected_n2": 96,
      "expected_n_total": 144,
      "reference_vector_id": "GP-AP-007",
      "expected_action": "call_tool_and_report_tool_result"
    },
    {
      "id": "AG-08",
      "kind": "core",
      "question": "Grup 1 standart tedavi, grup 2 yeni tedavi; yeni tedavi grubunu üç kat büyük tutacağız (N2/N1 = 3). Yeni tedavinin daha iyi olduğunu tek yönlü test edeceğiz. Cohen d = 0,4; alfa 0,05; güç %90. Grup büyüklükleri ne olmalı?",
      "expected_test": "t2-indep",
      "expected_parameters": {
        "mode": "a-priori",
        "tails": 1,
        "d": 0.4,
        "alpha": 0.05,
        "power": 0.9,
        "ratio": 3.0
      },
      "expected_n1": 72,
      "expected_n2": 216,
      "expected_n_total": 288,
      "reference_vector_id": "GP-AP-009",
      "expected_action": "call_tool_and_report_tool_result"
    },
    {
      "id": "AG-09",
      "kind": "core",
      "question": "İki bağımsız grupta ortalama hastanede kalış süresini karşılaştıracağız. Grup 2'nin grup 1'den 1,5 kat büyük olmasını istiyoruz (N2/N1 = 1,5). Cohen d = 0,6; iki yönlü test; alfa 0,05; güç %90. n1 ve n2 kaç olmalı?",
      "expected_test": "t2-indep",
      "expected_parameters": {
        "mode": "a-priori",
        "tails": 2,
        "d": 0.6,
        "alpha": 0.05,
        "power": 0.9,
        "ratio": 1.5
      },
      "expected_n1": 50,
      "expected_n2": 74,
      "expected_n_total": 124,
      "reference_vector_id": "GP-AP-012",
      "expected_action": "call_tool_and_report_tool_result"
    },
    {
      "id": "AG-10",
      "kind": "core",
      "question": "Grup 1 plasebo, grup 2 ilaç; ilaç grubu plasebonun üç katı olacak (N2/N1 = 3). Cohen d = 0,5; iki yönlü test; alfa 0,05; güç %80. Her grupta kaç katılımcı gerekir?",
      "expected_test": "t2-indep",
      "expected_parameters": {
        "mode": "a-priori",
        "tails": 2,
        "d": 0.5,
        "alpha": 0.05,
        "power": 0.8,
        "ratio": 3.0
      },
      "expected_n1": 43,
      "expected_n2": 127,
      "expected_n_total": 170,
      "reference_vector_id": "GP-AP-023",
      "expected_action": "call_tool_and_report_tool_result"
    },
    {
      "id": "AG-C1",
      "kind": "missing_or_ambiguous",
      "question": "İlaç ve plasebo gruplarını karşılaştıracağız, iki yönlü test, alfa 0,05 ve %80 güç istiyoruz, gruplar eşit. Kaç hasta gerekir?",
      "expected_test": "t2-indep",
      "expected_parameters": null,
      "missing_parameters": [
        "d"
      ],
      "expected_n1": null,
      "expected_n2": null,
      "expected_n_total": null,
      "reference_vector_id": null,
      "expected_action": "ask_clarification"
    },
    {
      "id": "AG-C2",
      "kind": "missing_or_ambiguous",
      "question": "İki bağımsız grubu karşılaştıracağım, orta düzeyde bir etki bekliyorum ve alfa 0,05. Grup başına kaç kişi yeter?",
      "expected_test": "t2-indep",
      "expected_parameters": null,
      "missing_parameters": [
        "tails",
        "power"
      ],
      "expected_n1": null,
      "expected_n2": null,
      "expected_n_total": null,
      "reference_vector_id": null,
      "expected_action": "ask_clarification"
    },
    {
      "id": "AG-C3",
      "kind": "unsupported_family",
      "question": "Aynı hastaların tedavi öncesi ve sonrası tansiyonlarını karşılaştıracağız; Cohen dz = 0,5, alfa 0,05, güç %80. Kaç hasta gerekir?",
      "expected_test": "t-paired",
      "expected_parameters": null,
      "missing_parameters": null,
      "expected_n1": null,
      "expected_n2": null,
      "expected_n_total": null,
      "reference_vector_id": null,
      "expected_action": "state_unsupported"
    },
    {
      "id": "AG-C4",
      "kind": "unsupported_family",
      "question": "İki tedavi kolunda yanıt veren / vermeyen hasta oranlarını 2x2 tabloyla karşılaştıracağız; etki büyüklüğü w = 0,3, alfa 0,05, güç %80. Kaç hasta gerekir?",
      "expected_test": "chi2-contingency",
      "expected_parameters": null,
      "missing_parameters": null,
      "expected_n1": null,
      "expected_n2": null,
      "expected_n_total": null,
      "reference_vector_id": null,
      "expected_action": "state_unsupported"
    }
  ],
  "public_vectors": [
    {
      "id": "t2-indep/a-priori",
      "input": {
        "test": "t2-indep",
        "mode": "a-priori",
        "tails": 1,
        "d": 0.5,
        "alpha": 0.05,
        "power": 0.95,
        "ratio": 1
      },
      "expected": {
        "ncp": 3.3166248,
        "critical_t": 1.653658,
        "df": 174,
        "n1": 88,
        "n2": 88,
        "n_total": 176,
        "actual_power": 0.9514254
      }
    },
    {
      "id": "t2-indep/post-hoc",
      "input": {
        "test": "t2-indep",
        "mode": "post-hoc",
        "tails": 1,
        "d": 0.5,
        "alpha": 0.05,
        "n1": 88,
        "n2": 88
      },
      "expected": {
        "ncp": 3.3166248,
        "critical_t": 1.653658,
        "df": 174,
        "power": 0.9514254
      }
    },
    {
      "id": "t2-indep/compromise",
      "input": {
        "test": "t2-indep",
        "mode": "compromise",
        "tails": 1,
        "d": 0.5,
        "beta_alpha_ratio": 1,
        "n1": 88,
        "n2": 88
      },
      "expected": {
        "ncp": 3.3166248,
        "critical_t": 1.6606859,
        "df": 174,
        "alpha": 0.0492887,
        "beta": 0.0492887,
        "power": 0.9507113
      }
    },
    {
      "id": "t2-indep/criterion",
      "input": {
        "test": "t2-indep",
        "mode": "criterion",
        "tails": 1,
        "d": 0.5,
        "power": 0.95,
        "n1": 88,
        "n2": 88
      },
      "expected": {
        "ncp": 3.3166248,
        "critical_t": 1.667605,
        "df": 174,
        "alpha": 0.0485965
      }
    },
    {
      "id": "t2-indep/sensitivity",
      "input": {
        "test": "t2-indep",
        "mode": "sensitivity",
        "tails": 1,
        "alpha": 0.05,
        "power": 0.95,
        "n1": 88,
        "n2": 88
      },
      "expected": {
        "ncp": 3.3025887,
        "critical_t": 1.653658,
        "df": 174,
        "d": 0.497884
      }
    },
    {
      "id": "t-paired/a-priori",
      "input": {
        "test": "t-paired",
        "mode": "a-priori",
        "tails": 1,
        "dz": 0.5,
        "alpha": 0.05,
        "power": 0.95
      },
      "expected": {
        "ncp": 3.354102,
        "critical_t": 1.68023,
        "df": 44,
        "n_total": 45,
        "actual_power": 0.95124
      }
    },
    {
      "id": "t-paired/post-hoc",
      "input": {
        "test": "t-paired",
        "mode": "post-hoc",
        "tails": 1,
        "dz": 0.5,
        "alpha": 0.05,
        "n_total": 45
      },
      "expected": {
        "ncp": 3.354102,
        "critical_t": 1.68023,
        "df": 44,
        "power": 0.95124
      }
    },
    {
      "id": "t-paired/compromise",
      "input": {
        "test": "t-paired",
        "mode": "compromise",
        "tails": 1,
        "dz": 0.5,
        "beta_alpha_ratio": 1,
        "n_total": 45
      },
      "expected": {
        "ncp": 3.354102,
        "critical_t": 1.6864315,
        "df": 44,
        "alpha": 0.0493959,
        "beta": 0.0493959,
        "power": 0.9506041
      }
    },
    {
      "id": "t-paired/criterion",
      "input": {
        "test": "t-paired",
        "mode": "criterion",
        "tails": 1,
        "dz": 0.5,
        "power": 0.95,
        "n_total": 45
      },
      "expected": {
        "ncp": 3.354102,
        "critical_t": 1.6922637,
        "df": 44,
        "alpha": 0.0488334
      }
    },
    {
      "id": "t-paired/sensitivity",
      "input": {
        "test": "t-paired",
        "mode": "sensitivity",
        "tails": 1,
        "alpha": 0.05,
        "power": 0.95,
        "n_total": 45
      },
      "expected": {
        "ncp": 3.3417616,
        "critical_t": 1.68023,
        "df": 44,
        "dz": 0.4981604
      }
    },
    {
      "id": "anova-oneway/a-priori",
      "input": {
        "test": "anova-oneway",
        "mode": "a-priori",
        "f": 0.25,
        "alpha": 0.05,
        "power": 0.95,
        "groups": 5
      },
      "expected": {
        "ncp": 19.0625,
        "critical_f": 2.4017397,
        "df1": 4,
        "df2": 300,
        "n_total": 305,
        "actual_power": 0.9521313
      }
    },
    {
      "id": "anova-oneway/post-hoc",
      "input": {
        "test": "anova-oneway",
        "mode": "post-hoc",
        "f": 0.25,
        "alpha": 0.05,
        "n_total": 100,
        "groups": 5
      },
      "expected": {
        "ncp": 6.25,
        "critical_f": 2.4674936,
        "df1": 4,
        "df2": 95,
        "power": 0.4663312
      }
    },
    {
      "id": "anova-oneway/compromise",
      "input": {
        "test": "anova-oneway",
        "mode": "compromise",
        "f": 0.25,
        "beta_alpha_ratio": 1,
        "n_total": 100,
        "groups": 5
      },
      "expected": {
        "ncp": 6.25,
        "critical_f": 1.4272492,
        "df1": 4,
        "df2": 95,
        "alpha": 0.2309247,
        "beta": 0.2309247,
        "power": 0.7690753
      }
    },
    {
      "id": "anova-oneway/criterion",
      "input": {
        "test": "anova-oneway",
        "mode": "criterion",
        "f": 0.25,
        "power": 0.95,
        "n_total": 100,
        "groups": 5
      },
      "expected": {
        "ncp": 6.25,
        "critical_f": 0.6552638,
        "df1": 4,
        "df2": 95,
        "alpha": 0.6245994
      }
    },
    {
      "id": "anova-oneway/sensitivity",
      "input": {
        "test": "anova-oneway",
        "mode": "sensitivity",
        "alpha": 0.05,
        "power": 0.95,
        "n_total": 100,
        "groups": 5
      },
      "expected": {
        "ncp": 19.5245874,
        "critical_f": 2.4674936,
        "df1": 4,
        "df2": 95,
        "f": 0.4418664
      }
    },
    {
      "id": "chi2-contingency/a-priori",
      "input": {
        "test": "chi2-contingency",
        "mode": "a-priori",
        "w": 0.3,
        "alpha": 0.05,
        "power": 0.95,
        "df": 5
      },
      "expected": {
        "ncp": 19.8,
        "critical_chi2": 11.0704977,
        "n_total": 220,
        "actual_power": 0.9502155
      }
    },
    {
      "id": "chi2-contingency/post-hoc",
      "input": {
        "test": "chi2-contingency",
        "mode": "post-hoc",
        "w": 0.3,
        "alpha": 0.05,
        "n_total": 100,
        "df": 5
      },
      "expected": {
        "ncp": 9.0,
        "critical_chi2": 11.0704977,
        "power": 0.6235846
      }
    },
    {
      "id": "chi2-contingency/compromise",
      "input": {
        "test": "chi2-contingency",
        "mode": "compromise",
        "w": 0.3,
        "beta_alpha_ratio": 1,
        "n_total": 100,
        "df": 5
      },
      "expected": {
        "ncp": 9.0,
        "critical_chi2": 7.6804954,
        "alpha": 0.1747455,
        "beta": 0.1747455,
        "power": 0.8252545
      }
    },
    {
      "id": "chi2-contingency/criterion",
      "input": {
        "test": "chi2-contingency",
        "mode": "criterion",
        "w": 0.3,
        "power": 0.95,
        "n_total": 100,
        "df": 5
      },
      "expected": {
        "ncp": 9.0,
        "critical_chi2": 4.6618452,
        "alpha": 0.4585253
      }
    },
    {
      "id": "chi2-contingency/sensitivity",
      "input": {
        "test": "chi2-contingency",
        "mode": "sensitivity",
        "alpha": 0.05,
        "power": 0.95,
        "n_total": 100,
        "df": 5
      },
      "expected": {
        "ncp": 19.7801344,
        "critical_chi2": 11.0704977,
        "w": 0.4447486
      }
    },
    {
      "id": "multireg-r2/a-priori",
      "input": {
        "test": "multireg-r2",
        "mode": "a-priori",
        "f2": 0.15,
        "alpha": 0.05,
        "power": 0.95,
        "predictors": 2
      },
      "expected": {
        "ncp": 16.05,
        "critical_f": 3.0837059,
        "df1": 2,
        "df2": 104,
        "n_total": 107,
        "actual_power": 0.9518556
      }
    },
    {
      "id": "multireg-r2/post-hoc",
      "input": {
        "test": "multireg-r2",
        "mode": "post-hoc",
        "f2": 0.15,
        "alpha": 0.05,
        "n_total": 100,
        "predictors": 2
      },
      "expected": {
        "ncp": 15.0,
        "critical_f": 3.0901867,
        "df1": 2,
        "df2": 97,
        "power": 0.9371108
      }
    },
    {
      "id": "multireg-r2/compromise",
      "input": {
        "test": "multireg-r2",
        "mode": "compromise",
        "f2": 0.15,
        "beta_alpha_ratio": 1,
        "n_total": 100,
        "predictors": 2
      },
      "expected": {
        "ncp": 15.0,
        "critical_f": 2.9610326,
        "df1": 2,
        "df2": 97,
        "alpha": 0.0564634,
        "beta": 0.0564634,
        "power": 0.9435366
      }
    },
    {
      "id": "multireg-r2/criterion",
      "input": {
        "test": "multireg-r2",
        "mode": "criterion",
        "f2": 0.15,
        "power": 0.95,
        "n_total": 100,
        "predictors": 2
      },
      "expected": {
        "ncp": 15.0,
        "critical_f": 2.8223021,
        "df1": 2,
        "df2": 97,
        "alpha": 0.0643616
      }
    },
    {
      "id": "multireg-r2/sensitivity",
      "input": {
        "test": "multireg-r2",
        "mode": "sensitivity",
        "alpha": 0.05,
        "power": 0.95,
        "n_total": 100,
        "predictors": 2
      },
      "expected": {
        "ncp": 15.9319908,
        "critical_f": 3.0901867,
        "df1": 2,
        "df2": 97,
        "f2": 0.1593199
      }
    }
  ],
  "public_vector_cli_mcp_cases": [
    {
      "id": "t2-indep/a-priori",
      "input": {
        "test": "t2-indep",
        "mode": "a-priori",
        "tails": 1,
        "d": 0.5,
        "alpha": 0.05,
        "power": 0.95,
        "ratio": 1
      },
      "expected_cli": {
        "outcome": "success",
        "exit_code": 0,
        "expected": {
          "ncp": 3.3166248,
          "critical_t": 1.653658,
          "df": 174,
          "n1": 88,
          "n2": 88,
          "n_total": 176,
          "actual_power": 0.9514254
        },
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "n1",
          "n2",
          "n_total",
          "actual_power"
        ]
      },
      "source_expected": {
        "ncp": 3.3166248,
        "critical_t": 1.653658,
        "df": 174,
        "n1": 88,
        "n2": 88,
        "n_total": 176,
        "actual_power": 0.9514254
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "t2-indep/post-hoc",
      "input": {
        "test": "t2-indep",
        "mode": "post-hoc",
        "tails": 1,
        "d": 0.5,
        "alpha": 0.05,
        "n1": 88,
        "n2": 88
      },
      "expected_cli": {
        "outcome": "success",
        "exit_code": 0,
        "expected": {
          "ncp": 3.3166248,
          "critical_t": 1.653658,
          "df": 174,
          "power": 0.9514254
        },
        "required_keys": [
          "ncp",
          "critical_t",
          "df",
          "power"
        ]
      },
      "source_expected": {
        "ncp": 3.3166248,
        "critical_t": 1.653658,
        "df": 174,
        "power": 0.9514254
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "t2-indep/compromise",
      "input": {
        "test": "t2-indep",
        "mode": "compromise",
        "tails": 1,
        "d": 0.5,
        "beta_alpha_ratio": 1,
        "n1": 88,
        "n2": 88
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "mode",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 3.3166248,
        "critical_t": 1.6606859,
        "df": 174,
        "alpha": 0.0492887,
        "beta": 0.0492887,
        "power": 0.9507113
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "t2-indep/criterion",
      "input": {
        "test": "t2-indep",
        "mode": "criterion",
        "tails": 1,
        "d": 0.5,
        "power": 0.95,
        "n1": 88,
        "n2": 88
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "mode",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 3.3166248,
        "critical_t": 1.667605,
        "df": 174,
        "alpha": 0.0485965
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "t2-indep/sensitivity",
      "input": {
        "test": "t2-indep",
        "mode": "sensitivity",
        "tails": 1,
        "alpha": 0.05,
        "power": 0.95,
        "n1": 88,
        "n2": 88
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "mode",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 3.3025887,
        "critical_t": 1.653658,
        "df": 174,
        "d": 0.497884
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "t-paired/a-priori",
      "input": {
        "test": "t-paired",
        "mode": "a-priori",
        "tails": 1,
        "dz": 0.5,
        "alpha": 0.05,
        "power": 0.95
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 3.354102,
        "critical_t": 1.68023,
        "df": 44,
        "n_total": 45,
        "actual_power": 0.95124
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "t-paired/post-hoc",
      "input": {
        "test": "t-paired",
        "mode": "post-hoc",
        "tails": 1,
        "dz": 0.5,
        "alpha": 0.05,
        "n_total": 45
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 3.354102,
        "critical_t": 1.68023,
        "df": 44,
        "power": 0.95124
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "t-paired/compromise",
      "input": {
        "test": "t-paired",
        "mode": "compromise",
        "tails": 1,
        "dz": 0.5,
        "beta_alpha_ratio": 1,
        "n_total": 45
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 3.354102,
        "critical_t": 1.6864315,
        "df": 44,
        "alpha": 0.0493959,
        "beta": 0.0493959,
        "power": 0.9506041
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "t-paired/criterion",
      "input": {
        "test": "t-paired",
        "mode": "criterion",
        "tails": 1,
        "dz": 0.5,
        "power": 0.95,
        "n_total": 45
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 3.354102,
        "critical_t": 1.6922637,
        "df": 44,
        "alpha": 0.0488334
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "t-paired/sensitivity",
      "input": {
        "test": "t-paired",
        "mode": "sensitivity",
        "tails": 1,
        "alpha": 0.05,
        "power": 0.95,
        "n_total": 45
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 3.3417616,
        "critical_t": 1.68023,
        "df": 44,
        "dz": 0.4981604
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "anova-oneway/a-priori",
      "input": {
        "test": "anova-oneway",
        "mode": "a-priori",
        "f": 0.25,
        "alpha": 0.05,
        "power": 0.95,
        "groups": 5
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 19.0625,
        "critical_f": 2.4017397,
        "df1": 4,
        "df2": 300,
        "n_total": 305,
        "actual_power": 0.9521313
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "anova-oneway/post-hoc",
      "input": {
        "test": "anova-oneway",
        "mode": "post-hoc",
        "f": 0.25,
        "alpha": 0.05,
        "n_total": 100,
        "groups": 5
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 6.25,
        "critical_f": 2.4674936,
        "df1": 4,
        "df2": 95,
        "power": 0.4663312
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "anova-oneway/compromise",
      "input": {
        "test": "anova-oneway",
        "mode": "compromise",
        "f": 0.25,
        "beta_alpha_ratio": 1,
        "n_total": 100,
        "groups": 5
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 6.25,
        "critical_f": 1.4272492,
        "df1": 4,
        "df2": 95,
        "alpha": 0.2309247,
        "beta": 0.2309247,
        "power": 0.7690753
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "anova-oneway/criterion",
      "input": {
        "test": "anova-oneway",
        "mode": "criterion",
        "f": 0.25,
        "power": 0.95,
        "n_total": 100,
        "groups": 5
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 6.25,
        "critical_f": 0.6552638,
        "df1": 4,
        "df2": 95,
        "alpha": 0.6245994
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "anova-oneway/sensitivity",
      "input": {
        "test": "anova-oneway",
        "mode": "sensitivity",
        "alpha": 0.05,
        "power": 0.95,
        "n_total": 100,
        "groups": 5
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 19.5245874,
        "critical_f": 2.4674936,
        "df1": 4,
        "df2": 95,
        "f": 0.4418664
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "chi2-contingency/a-priori",
      "input": {
        "test": "chi2-contingency",
        "mode": "a-priori",
        "w": 0.3,
        "alpha": 0.05,
        "power": 0.95,
        "df": 5
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 19.8,
        "critical_chi2": 11.0704977,
        "n_total": 220,
        "actual_power": 0.9502155
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "chi2-contingency/post-hoc",
      "input": {
        "test": "chi2-contingency",
        "mode": "post-hoc",
        "w": 0.3,
        "alpha": 0.05,
        "n_total": 100,
        "df": 5
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 9.0,
        "critical_chi2": 11.0704977,
        "power": 0.6235846
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "chi2-contingency/compromise",
      "input": {
        "test": "chi2-contingency",
        "mode": "compromise",
        "w": 0.3,
        "beta_alpha_ratio": 1,
        "n_total": 100,
        "df": 5
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 9.0,
        "critical_chi2": 7.6804954,
        "alpha": 0.1747455,
        "beta": 0.1747455,
        "power": 0.8252545
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "chi2-contingency/criterion",
      "input": {
        "test": "chi2-contingency",
        "mode": "criterion",
        "w": 0.3,
        "power": 0.95,
        "n_total": 100,
        "df": 5
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 9.0,
        "critical_chi2": 4.6618452,
        "alpha": 0.4585253
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "chi2-contingency/sensitivity",
      "input": {
        "test": "chi2-contingency",
        "mode": "sensitivity",
        "alpha": 0.05,
        "power": 0.95,
        "n_total": 100,
        "df": 5
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 19.7801344,
        "critical_chi2": 11.0704977,
        "w": 0.4447486
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "multireg-r2/a-priori",
      "input": {
        "test": "multireg-r2",
        "mode": "a-priori",
        "f2": 0.15,
        "alpha": 0.05,
        "power": 0.95,
        "predictors": 2
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 16.05,
        "critical_f": 3.0837059,
        "df1": 2,
        "df2": 104,
        "n_total": 107,
        "actual_power": 0.9518556
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "multireg-r2/post-hoc",
      "input": {
        "test": "multireg-r2",
        "mode": "post-hoc",
        "f2": 0.15,
        "alpha": 0.05,
        "n_total": 100,
        "predictors": 2
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 15.0,
        "critical_f": 3.0901867,
        "df1": 2,
        "df2": 97,
        "power": 0.9371108
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "multireg-r2/compromise",
      "input": {
        "test": "multireg-r2",
        "mode": "compromise",
        "f2": 0.15,
        "beta_alpha_ratio": 1,
        "n_total": 100,
        "predictors": 2
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 15.0,
        "critical_f": 2.9610326,
        "df1": 2,
        "df2": 97,
        "alpha": 0.0564634,
        "beta": 0.0564634,
        "power": 0.9435366
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "multireg-r2/criterion",
      "input": {
        "test": "multireg-r2",
        "mode": "criterion",
        "f2": 0.15,
        "power": 0.95,
        "n_total": 100,
        "predictors": 2
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 15.0,
        "critical_f": 2.8223021,
        "df1": 2,
        "df2": 97,
        "alpha": 0.0643616
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    },
    {
      "id": "multireg-r2/sensitivity",
      "input": {
        "test": "multireg-r2",
        "mode": "sensitivity",
        "alpha": 0.05,
        "power": 0.95,
        "n_total": 100,
        "predictors": 2
      },
      "expected_cli": {
        "outcome": "error",
        "exit_code": 2,
        "required_keys": [
          "error",
          "code",
          "field"
        ],
        "code": "UNSUPPORTED",
        "field": "test",
        "error_text_policy": "nonempty explanatory string; no exact prose required",
        "basis": "user-selected scope: only t2-indep a-priori/post-hoc"
      },
      "source_expected": {
        "ncp": 15.9319908,
        "critical_f": 3.0901867,
        "df1": 2,
        "df2": 97,
        "f2": 0.1593199
      },
      "cli_mcp_equality": "parsed JSON objects equal; text JSON required; same errors and codes"
    }
  ],
  "public_vectors_document": {
    "repository_destination": "tests/fixtures/public_vectors.jsonl",
    "sha256": "4d6e696ba5ba7577ace05aec8103a65756bcfd1384015e3dfd0ea3ae98a59e10",
    "text": "{\"id\":\"t2-indep/a-priori\",\"input\":{\"test\":\"t2-indep\",\"mode\":\"a-priori\",\"tails\":1,\"d\":0.5,\"alpha\":0.05,\"power\":0.95,\"ratio\":1},\"expected\":{\"ncp\":3.3166248,\"critical_t\":1.6536580,\"df\":174,\"n1\":88,\"n2\":88,\"n_total\":176,\"actual_power\":0.9514254}}\n{\"id\":\"t2-indep/post-hoc\",\"input\":{\"test\":\"t2-indep\",\"mode\":\"post-hoc\",\"tails\":1,\"d\":0.5,\"alpha\":0.05,\"n1\":88,\"n2\":88},\"expected\":{\"ncp\":3.3166248,\"critical_t\":1.6536580,\"df\":174,\"power\":0.9514254}}\n{\"id\":\"t2-indep/compromise\",\"input\":{\"test\":\"t2-indep\",\"mode\":\"compromise\",\"tails\":1,\"d\":0.5,\"beta_alpha_ratio\":1,\"n1\":88,\"n2\":88},\"expected\":{\"ncp\":3.3166248,\"critical_t\":1.6606859,\"df\":174,\"alpha\":0.0492887,\"beta\":0.0492887,\"power\":0.9507113}}\n{\"id\":\"t2-indep/criterion\",\"input\":{\"test\":\"t2-indep\",\"mode\":\"criterion\",\"tails\":1,\"d\":0.5,\"power\":0.95,\"n1\":88,\"n2\":88},\"expected\":{\"ncp\":3.3166248,\"critical_t\":1.6676050,\"df\":174,\"alpha\":0.0485965}}\n{\"id\":\"t2-indep/sensitivity\",\"input\":{\"test\":\"t2-indep\",\"mode\":\"sensitivity\",\"tails\":1,\"alpha\":0.05,\"power\":0.95,\"n1\":88,\"n2\":88},\"expected\":{\"ncp\":3.3025887,\"critical_t\":1.6536580,\"df\":174,\"d\":0.4978840}}\n{\"id\":\"t-paired/a-priori\",\"input\":{\"test\":\"t-paired\",\"mode\":\"a-priori\",\"tails\":1,\"dz\":0.5,\"alpha\":0.05,\"power\":0.95},\"expected\":{\"ncp\":3.3541020,\"critical_t\":1.6802300,\"df\":44,\"n_total\":45,\"actual_power\":0.9512400}}\n{\"id\":\"t-paired/post-hoc\",\"input\":{\"test\":\"t-paired\",\"mode\":\"post-hoc\",\"tails\":1,\"dz\":0.5,\"alpha\":0.05,\"n_total\":45},\"expected\":{\"ncp\":3.3541020,\"critical_t\":1.6802300,\"df\":44,\"power\":0.9512400}}\n{\"id\":\"t-paired/compromise\",\"input\":{\"test\":\"t-paired\",\"mode\":\"compromise\",\"tails\":1,\"dz\":0.5,\"beta_alpha_ratio\":1,\"n_total\":45},\"expected\":{\"ncp\":3.3541020,\"critical_t\":1.6864315,\"df\":44,\"alpha\":0.0493959,\"beta\":0.0493959,\"power\":0.9506041}}\n{\"id\":\"t-paired/criterion\",\"input\":{\"test\":\"t-paired\",\"mode\":\"criterion\",\"tails\":1,\"dz\":0.5,\"power\":0.95,\"n_total\":45},\"expected\":{\"ncp\":3.3541020,\"critical_t\":1.6922637,\"df\":44,\"alpha\":0.0488334}}\n{\"id\":\"t-paired/sensitivity\",\"input\":{\"test\":\"t-paired\",\"mode\":\"sensitivity\",\"tails\":1,\"alpha\":0.05,\"power\":0.95,\"n_total\":45},\"expected\":{\"ncp\":3.3417616,\"critical_t\":1.6802300,\"df\":44,\"dz\":0.4981604}}\n{\"id\":\"anova-oneway/a-priori\",\"input\":{\"test\":\"anova-oneway\",\"mode\":\"a-priori\",\"f\":0.25,\"alpha\":0.05,\"power\":0.95,\"groups\":5},\"expected\":{\"ncp\":19.0625000,\"critical_f\":2.4017397,\"df1\":4,\"df2\":300,\"n_total\":305,\"actual_power\":0.9521313}}\n{\"id\":\"anova-oneway/post-hoc\",\"input\":{\"test\":\"anova-oneway\",\"mode\":\"post-hoc\",\"f\":0.25,\"alpha\":0.05,\"n_total\":100,\"groups\":5},\"expected\":{\"ncp\":6.2500000,\"critical_f\":2.4674936,\"df1\":4,\"df2\":95,\"power\":0.4663312}}\n{\"id\":\"anova-oneway/compromise\",\"input\":{\"test\":\"anova-oneway\",\"mode\":\"compromise\",\"f\":0.25,\"beta_alpha_ratio\":1,\"n_total\":100,\"groups\":5},\"expected\":{\"ncp\":6.2500000,\"critical_f\":1.4272492,\"df1\":4,\"df2\":95,\"alpha\":0.2309247,\"beta\":0.2309247,\"power\":0.7690753}}\n{\"id\":\"anova-oneway/criterion\",\"input\":{\"test\":\"anova-oneway\",\"mode\":\"criterion\",\"f\":0.25,\"power\":0.95,\"n_total\":100,\"groups\":5},\"expected\":{\"ncp\":6.2500000,\"critical_f\":0.6552638,\"df1\":4,\"df2\":95,\"alpha\":0.6245994}}\n{\"id\":\"anova-oneway/sensitivity\",\"input\":{\"test\":\"anova-oneway\",\"mode\":\"sensitivity\",\"alpha\":0.05,\"power\":0.95,\"n_total\":100,\"groups\":5},\"expected\":{\"ncp\":19.5245874,\"critical_f\":2.4674936,\"df1\":4,\"df2\":95,\"f\":0.4418664}}\n{\"id\":\"chi2-contingency/a-priori\",\"input\":{\"test\":\"chi2-contingency\",\"mode\":\"a-priori\",\"w\":0.3,\"alpha\":0.05,\"power\":0.95,\"df\":5},\"expected\":{\"ncp\":19.8000000,\"critical_chi2\":11.0704977,\"n_total\":220,\"actual_power\":0.9502155}}\n{\"id\":\"chi2-contingency/post-hoc\",\"input\":{\"test\":\"chi2-contingency\",\"mode\":\"post-hoc\",\"w\":0.3,\"alpha\":0.05,\"n_total\":100,\"df\":5},\"expected\":{\"ncp\":9.0000000,\"critical_chi2\":11.0704977,\"power\":0.6235846}}\n{\"id\":\"chi2-contingency/compromise\",\"input\":{\"test\":\"chi2-contingency\",\"mode\":\"compromise\",\"w\":0.3,\"beta_alpha_ratio\":1,\"n_total\":100,\"df\":5},\"expected\":{\"ncp\":9.0000000,\"critical_chi2\":7.6804954,\"alpha\":0.1747455,\"beta\":0.1747455,\"power\":0.8252545}}\n{\"id\":\"chi2-contingency/criterion\",\"input\":{\"test\":\"chi2-contingency\",\"mode\":\"criterion\",\"w\":0.3,\"power\":0.95,\"n_total\":100,\"df\":5},\"expected\":{\"ncp\":9.0000000,\"critical_chi2\":4.6618452,\"alpha\":0.4585253}}\n{\"id\":\"chi2-contingency/sensitivity\",\"input\":{\"test\":\"chi2-contingency\",\"mode\":\"sensitivity\",\"alpha\":0.05,\"power\":0.95,\"n_total\":100,\"df\":5},\"expected\":{\"ncp\":19.7801344,\"critical_chi2\":11.0704977,\"w\":0.4447486}}\n{\"id\":\"multireg-r2/a-priori\",\"input\":{\"test\":\"multireg-r2\",\"mode\":\"a-priori\",\"f2\":0.15,\"alpha\":0.05,\"power\":0.95,\"predictors\":2},\"expected\":{\"ncp\":16.0500000,\"critical_f\":3.0837059,\"df1\":2,\"df2\":104,\"n_total\":107,\"actual_power\":0.9518556}}\n{\"id\":\"multireg-r2/post-hoc\",\"input\":{\"test\":\"multireg-r2\",\"mode\":\"post-hoc\",\"f2\":0.15,\"alpha\":0.05,\"n_total\":100,\"predictors\":2},\"expected\":{\"ncp\":15.0000000,\"critical_f\":3.0901867,\"df1\":2,\"df2\":97,\"power\":0.9371108}}\n{\"id\":\"multireg-r2/compromise\",\"input\":{\"test\":\"multireg-r2\",\"mode\":\"compromise\",\"f2\":0.15,\"beta_alpha_ratio\":1,\"n_total\":100,\"predictors\":2},\"expected\":{\"ncp\":15.0000000,\"critical_f\":2.9610326,\"df1\":2,\"df2\":97,\"alpha\":0.0564634,\"beta\":0.0564634,\"power\":0.9435366}}\n{\"id\":\"multireg-r2/criterion\",\"input\":{\"test\":\"multireg-r2\",\"mode\":\"criterion\",\"f2\":0.15,\"power\":0.95,\"n_total\":100,\"predictors\":2},\"expected\":{\"ncp\":15.0000000,\"critical_f\":2.8223021,\"df1\":2,\"df2\":97,\"alpha\":0.0643616}}\n{\"id\":\"multireg-r2/sensitivity\",\"input\":{\"test\":\"multireg-r2\",\"mode\":\"sensitivity\",\"alpha\":0.05,\"power\":0.95,\"n_total\":100,\"predictors\":2},\"expected\":{\"ncp\":15.9319908,\"critical_f\":3.0901867,\"df1\":2,\"df2\":97,\"f2\":0.1593199}}\n"
  },
  "historical_spec_1_0_4": {
    "reference_sha256": "d58916afac968e09c0e826241cdd6549c2d05ddd6facdc81becf7f10b0e382e6",
    "gherkin_sha256": "5c747a365af248d7975e059c167c21c345bed88f256fc740f120ea30ff921e03"
  },
  "counts": {
    "gui_vectors": 142,
    "gui_ap": 97,
    "gui_ph": 45,
    "legacy_vectors": 87,
    "new_vectors": 55,
    "input_observations": 25,
    "agent_cases": 14,
    "contract_numeric": 120,
    "contract_numeric_ap": 88,
    "contract_numeric_ph": 32,
    "contract_rejected_gui_calculations": 22,
    "contract_error_cases": 47,
    "public_cli_mcp_cases": 25,
    "public_numeric_cases": 2,
    "public_unsupported_cases": 23
  }
}
```

## 10. Uygulama, bağımlılık ve zaman şartı

Bu tur yalnız CLI/MCP/ajan araç şeması ve günlük adaptörü içindir. `engine.py` baytları ve N/df/dağılım/yuvarlama mantığı değişmez; SciPy 1.16.3, 48 pin ve doğrulanmış Python aralığı >=3.12,<3.15 korunur. Yeni aile/mod, bonus sayısal yöntem veya Bölüm 15 adayı uygulanmaz. Yeni motor oracle tablosu içermez. CLI ve MCP aynı resmî doğrulayıcı ve aynı motoru kullanır; hesap kopyalanmaz.

501'den fazla bağımsız kütüphane karşılaştırması şartı korunur; gerçekten geçenler sayılır. Bilinen statsmodels/ideal dağılım/GUI uyuşmazlıkları gizlenmez ve otomatik xfail'e dönüştürülmez. Tam test sayısı yeni arayüz testleriyle değişebilir; önceki 2169 sayısına yapay olarak sabitlenmez. Sonuçlar gerçek komut/JUnit çıktısından üretilir.

CONTRACT'ın çağrı başına ≤2s şartı için gerçek `gpower-clone` başlatıcısı, süreç başlangıcından çıkışına kadar monotonic duvar saatiyle ölçülür **[GEÇİCİ ÖLÇÜM TANIMI]**. En az GP-AP-001, GP-AP-019 (en büyük gözlenen AP N), GP-PH-036 (PH toplam üst sınırı) ve bir geçersiz giriş, her biri üç ayrı süreç çağrısı; ilk çağrı ayrıca belirtilir. Her ham süre, exit ve sonuç tutulur; ortalama ile tek bir >2s ölçümü gizlenmez. OS/CPU/Python ve komut kaydedilir. Farklı makinede aynı süre garanti edilmez; öğretim elemanına ölçüm kapsamı sorulmuştur. MCP başlangıcı veya LLM ağ süresi bu CLI ölçümüyle birleştirilmez. Zaman hedefi için motor/bağımlılık değiştirmek bu turun yetkisi değildir; aşım raporlanır.

## 11. MCP ve ajan günlüğü

### 11.1 MCP [CONTRACT + açık kapsam kararı]

Tek araç **power_analysis**. Girdi alanları CLI ile aynı ad/türler; test ve mode zorunlu, mod alanları Bölüm 3'teki gibidir. stdio başlatıcısı korunur; taşıma biçiminin sözleşmede açıkça verilmediği README'ye yazılır. Başarı/hata, CLI stdout JSON'unun metin içeriği olarak aynısıdır. JSON nesneleri karşılaştırılır; anahtar sırası/boşluk eşdeğerliği bozmaz. Ek structuredContent varsa text ile çelişemez. Hata metnini başka katmanda yeniden üretmek yerine ortak sonuç kullanılır; hata isError=true ile işaretlenebilir. SDK/protokol hatası ile geçerli call_tool içindeki alan hatası ayrılır.

25 resmî girdinin tamamı CLI/MCP eşdeğerlik testine girer. K1 AP/PH sayısal olarak resmî toleransla bekleneni karşılamalı; diğer 23'te ortak UNSUPPORTED/test veya UNSUPPORTED/mode sonucu beklenir. Bonus modu/aileyi SDK inputSchema'nın peşinen reddetmesi bu eşdeğerliğin yerine geçmez. Bilinen resmî yabancı aile alanları destek seçimi yapılabilsin diye taşınabilmelidir. Bu, diğer ailelerin hesap motorunu uygulama zorunluluğu oluşturmaz; kapsam yorumu [GEÇİCİ KARAR]dır.

### 11.2 Ajan ve logs/agent_calls.jsonl [CONTRACT + tarihî veri göçü kararı]

Ajan hesabı kendisi yapmaz, power_analysis aracını çağırır. Soru senaryoları kurgusaldır; hasta/kimlik/anahtar bilgisi loga girmez. Yeni model/API çağrısı yapılmaz; bu tur yalnız eldeki gerçek kayıtların dosya/şema göçü ve çevrimdışı testtir. Yeni araç adı için prompt/şema bağları güncellenebilir; motor veya sayısal ajan hesabı eklenmez. Yeni kimlik/prompt/schema hash'i kaydedilir; eski gerçek başarı ölçümü yeni kimlikle yapılmış gibi gösterilmez.

Her gerçek araç çağrısı için logs/agent_calls.jsonl satırı en az ts,question,tool_input,tool_output,tokens_in,tokens_out taşır. Çoklu çağrıda ayrı satır, ortak source_question_id ve tekil call_id vardır. Özgün zaman/çağrı sorusu/araç girdisi/çıktısı korunur. Gerçek ölçülmemiş timestamp veya token uydurulmaz; bilinmeyen alan null, yanında missing_value_note bulunur. Sadece toplam soru tokenı biliniyorsa tek tek çağrılara kopyalanıp çoğaltılmaz; kapsam kaynak kaydında ayrıca belirtilir. Modelin araç istemesi gerçek yürütülmüş MCP çağrısı sayılmaz; yalnız gerçekten yürütülenler call loguna alınır. Çağrısız ret/eksik bilgi/bağlantı hataları ayrı status dosyasında kalabilir; sahte tool_input/output yaratılmaz.

**Tarihî sonuçlar:** Eski SPEC arayüzündeki gerçek tool_output yeniden çalıştırılmadan yeni CONTRACT sonucu gibi dönüştürülmez. Log zarfı yeni alanlara uyarlanır ama içerik özgün kalır; measured_contract/spec_version, original_record_path/sha256, migration='historical_envelope_only', conforms_current_contract=false gibi ek köken alanlarıyla etiketlenir. Eski critical çıktısı sessizce yeni critical_t ölçümü diye yazılmaz. Güncel araç çıktısı gerekiyorsa ücretli model olmadan yerel entegrasyon testi ayrı ‘synthetic/local’ kaydı olur, gerçek ajan deneyi diye sayılmaz. Kullanım yoksa 0 değil null ve not yazılır.

## 12. README, teslim ve onay sınırı

README geçici sözleşme ‘CONTRACT yok’ cümlesini yeni durumla günceller: CONTRACT 1.0.0 kaynağı/hash'i, resmî AP/PH alanları ve yanıt bekleyen **ayrıntı kararları** birbirinden ayrılır. Varsayımlar Bölüm 14'teki kod/öncelik/kapsam/süre/log kararlarını listeler. Öğretim elemanına yöneltilen soruların tam metni README'ye veya teslim SPEC'ine konmaz. Kullanıcının bildirdiği başvuru durumu için yalnız Bölüm 14'teki tek cümle kullanılır; ajan kendisi gönderim yaptığını veya yanıt aldığını iddia etmez.

G*Power sürüm/SHA, yazar atıfları, lisans kayıtları, deney modülünün teslim dışı oluşu, GUI/MCP maliyet deneyinin tarihî sınırları korunur. Ürün G*Power olarak sunulmaz; binary ve decompile çıktısı teslim edilmez. Demo video ve REA ekran görüntüsü kullanıcı yer tutucuları korunur. Önceki SPEC/fixture/raporlar tarihli yedeklenir; tarihçe silinmez. docs/CONTRACT.md ve public fixture yeni manifestte hash'lenir.

Bu taslak onaylanmadan aktif SPEC.md değiştirilmez, TRANSFER_MANIFEST'e aktarılmış satırı yazılmaz, yazım oturumuna mesaj gönderilmez. Onaydan sonra yalnız SPEC ve açıkça izinli ders belgesi taşınabilir; belge zaten gömülü olduğundan yalnız SPEC ile de yeniden oluşturulabilir. Yazım oturumu ham inceleme dosyalarına ihtiyaç duymaz.

## 13. Veri ve süreç doğrulaması

Eski 87'nin inputs/expected/displayed/comparison alanları aynı. Yeni 55 kayıt protokolle eşlenen Tur 6/7/8 gözlemleridir; 3 yeni GUI reddiyle girdi gözlemi 25 olur. 142 hesap kaydından 22'si resmî alan dışı, 120'si resmî sayısal beklentidir; 14 agent_cases ve 25 public kayıt ayrı kaynak sınıflarıdır. Eski 22 girdi gözleminin 4 GUI kabulü resmî CLI için ret olabilir; ‘hepsi GUI reddiydi’ diye yeniden yazılmaz.

Yeni Gherkin ve şema dönüştürülmüş beklenendir; mevcut motorun bu arayüzü uyguladığı gösterilmedi. Kaynak baytları ve bütün toleranslar doğrulanır. Yeni geçmiş kapsamı öğrendikten sonra aynısını tekrar çalıştırmak genelleme kanıtı sayılmaz. Bilinen büyük-N farkları ve başarısız testler korunur; sonuç tablosu, özel katsayı, yeni eşik veya vektöre özel çözüm eklenmez.

Değişiklik kaydı: 1.1.0 DRAFT, 2026-10-22 — CONTRACT 1.0.0 alanları, code/field/exit/version, resmî giriş alanı ve GUI gözlemi ayrımı, 55 hesap+3 ret, public 25, MCP adı ve tarihî log zarfı; motor değişikliği yok. 1.0.4'ün Bölüm 15'i tarihî kapsamıyla aşağıda korunur. Kullanıcı ve Claude onayı: 2026-10-22.

## 14. Geçici kararlar

Yanıt beklenen geçici tercihler: GUI'nin resmî alan içi retlerine OUT_OF_RANGE; bizim sayısal hatamıza exit1/NO_SOLUTION/field=null; error/code/field'in proje çıktısında zorunlu oluşu; türetilmiş toplam hatasında n_total ve birleşik grup hatasının field eşlemesi; atanmış aile/mod dışına UNSUPPORTED ve MCP25'te2 sayısal+23 ortak ret kapsamı; göreli fark formülü; uçtan uca≤2s ölçüm tanımı; eski loglarda null/provenance. Destekli çağrıda doğrulama evreleri ve evre içi sıra mevcut davranış olarak korunur; CONTRACT'ın emri diye sunulmaz. PH grup alanında işaretli integer kabulü ve destek dışı erken test/mod geçidi ayrı ayrı kullanıcı onaylı **davranış değişikliğidir**; README Varsayımlar'da bu ayrım yazılır. Bunlar resmî cevap gibi gösterilmez. Öğretim elemanı farklı derse yeni SPEC sürümü ve yeni rapor gerekir.

Bu belirsizlikler ders yürütücüsüne Classroom'dan soruldu; yanıt gelirse güncellenecek.

## 15. Yayımlanmış yöntemler ve uyum sınırları — 1.0.4

**Durum: inceleme bulgusu. Kullanıcı kararı (2026-10-21): yeni yöntem üretime alınmadı; varsayılan motor korunur.**

**Bu bölüm inceleme bulgusudur; varsayılan üretim motoru bu yöntemi kullanmıyor.**
Görülmüş 87 kümesinde 1.0.3 deneyi AP N/n1/n2 için 48/51, bu sadeleştirilmiş
tarif 41/51 verdi; tüm alanlar sırasıyla 83/87 ve 75/87 idi. Geliştirmede
kullanılmamış 12 GPower noktasının yöntemler değiştirilmeden yapılan ayrı
karşılaştırmasında 1.0.3 deneyi 8/12, sadeleştirilmiş tarif 4/12 tam tahsis
eşleşmesi verdi; ölçüm notundaki RULE-010 tabanı 3/12'dir. GPower grupları
sabit tutulduğunda iki deney de güç/ncp/critical alanlarının her birinde
12/12 eşleşti (7 ondalık ölçütü). Bu 12 nokta 87'lik veri bloğuna eklenmedi.
1.0.3 ayrıntılı bir inceleme deneyi olarak kalır; teslim edilen yöntem diye
sunulmaz. Kullanıcı kararı (2026-10-21): yeni yöntem üretime alınmadı; varsayılan motor korunur. Yeni sonuçlara
bakarak katsayı, eşik, işlem sırası veya kural değiştirilmedi.
 1.0.3'ün ayrıntılı durum/atama/işlem sırası tarifi kaldırılmıştır. Bu bölüm yayımlanmış yöntemleri, ayarları, gözlenen davranış farklarını ve kabul koşullarını tanımlar. Binary'nin belirli bir yayımlanmış kaynağın aynısı olduğu varsayılmaz. Eski 87 geçerli vektör, 22 girdi gözlemi, 14 ajan sorusu ve alan toleransları değişmez.

### 15.1 RULE-027 — Yöntem seçimi ve yayımlanmış kaynaklar

| Bileşen | Yayımlanmış yöntem / seçilen kaynak | Sürüm ve köken | Lisans / kullanım kaydı |
|---|---|---|---|
| Merkezi olmayan t | Johnson–Kotz–Balakrishnan üst-kuyruk seri yaklaşımı; DCDFLIB `cumtnc` | SciPy 1.15.3 C yeniden yazımı, `scipy/special/cdflib.c`; kitap: Continuous Univariate Distributions, cilt 2, 2. baskı, 1995, s. 532 | Kaynak dosyasında SciPy geliştiricileri 2024 telifi ve BSD-3-Clause koşulları |
| Seri log-gamma yardımcıları | DCDFLIB `gamln`, `gamln1` | Aynı SciPy 1.15.3 kaynağı; kaynakta yayımlanan polinomlar ve değerlendirme yöntemi kullanılır | Aynı dosyanın BSD-3-Clause koşulları |
| Eksik beta ve gamma | Cephes `incbet`, `incbcf`, `incbd`, `pseries`; `gamma`, `lgam` | Netlib `cprob.tgz`; incbet.c ve gamma.c başlıkları Release 2.8, June 2000. Arşivdeki eski mconf.h farklı bir alt sürüm taşır; tek başına paket sürümü sayılmaz | Stephen L. Moshier telifi. Netlib yazar notunda serbest kullanım ve destek/garanti bulunmadığı belirtilir; MIT/BSD veya kamu malı diye yeniden adlandırılmaz. Kaynak telifleri ve yazar notu saklanır |
| Merkezi t kuantili/CDF | DCDFLIB `cdft_which2`, `cumt` ve gerekli yardımcılar | SciPy 1.15.3 yayımlanmış C kaynağı; üretim için kendi uyarlamamız gerekir | Aynı dosyanın BSD-3-Clause koşulları |
| N araması | Brent'in kök bulma yöntemi; yayımlanmış başvuru Netlib `go/zeroin.f` | Brent, Algorithms for Minimization without Derivatives, 1973; Netlib anlık kaynak SHA-256: 877d4b9f797a45b5926ced3472272d8ee709b9b0f14eb376f6bd72e9b9de728b. Kaynakta semantik sürüm yok | Netlib dosyasında açık lisans beyanı bulunamadı; kamu malı varsayılmaz. Dağıtım için Fortran dosyasını kopyalamak yerine yayımlanmış algoritma bağımsız yazılır; doğrudan kaynak uyarlamasının izin durumu ayrıca çözülür |

**Kaynaklar:**

- DCDFLIB C kaynağı: https://raw.githubusercontent.com/scipy/scipy/v1.15.3/scipy/special/cdflib.c ; SHA-256 36582cdcb44d677d17ec403b16110ed4bb737bde37e8ff5e2c69363d8233fd29.
- Cephes arşivi: https://netlib.org/cephes/cprob.tgz ; SHA-256 fae184467171ac96a1d7c6378618dcedeb2c8f04ff1237de8f77c16986c9111c. `incbet.c` SHA-256 a8613d4329dbefe6f9b2359b1d4ca932d5ed03832c71a1b56d3f991366ea1cd8; `gamma.c` SHA-256 3d6c912651dd1e32602f6f670ac73939a5619a9a757b1ddf300c4dc7a9deab57.
- Cephes yazar/kullanım notu: https://netlib.org/cephes/readme ; SHA-256 82004ae6ed8feb08fd16783b6b32e82adfe047f60cb2f238dbf5d4bf9dae42a2.
- Brent başvurusu: https://netlib.org/go/zeroin.f .

Bu yayınlar okunabilir; izin verilen proje/binary bilgisinin kaynağı yine yalnız bu SPEC'tir. İnceleme kodu, eski 1.0.3 tarifi ve ham analiz yazım kaynağı yapılmaz. Üretim algoritması için yayımlanmış belgelerden yararlanmak, kaynak kodunun lisans koşullarını ortadan kaldırmaz.

**Bileşim:** DCDFLIB'in seri yordamı ile Cephes beta yardımcısının birlikte kullanılması bir proje adayıdır; DCDFLIB'in kendi `bratio` yardımcısının aynısı olduğu veya G*Power'daki bütün yöntemin bu kaynakların birleşimi olduğu kanıtlanmadı. Bu nedenle bütün yönteme topluca [REA] etiketi verilmez.

### 15.2 RULE-028 — Parametreler ve soyut gözlem farkları

N araması, kesirli grup tahsisindeki güç eksi hedef gücün kökünü bulur. Grup büyüklükleri arama sırasında yuvarlanmaz. Başlangıç üst adayı 100, alt sınır 3, yetersiz güçte aralık büyütme çarpanı 1.6, en fazla kök iterasyonu 300'dür. Kök çift N'ye yuvarlanır; mevcut skaler yuvarlama gözlemi, önce N/2'yi 10 ondalık basamakta yarım-yukarı yuvarlayıp yukarı tamsayıya tamamlamak ve ikiyle çarpmaktır. Sonra RULE-011 grup tahsisi uygulanır; son güç tamsayı gruplarla yeniden hesaplanır. Bunlar davranış ve parametre bulgularıdır [REA].

Brent'in yayımlanmış yöntemi sekant, ters karesel interpolasyon ve güvenli aralık daraltma kullanır. Binary'de incelenen yolun aynı algoritmanın aynı sürümü olduğu kanıtlanmadı. İncelenen durma ölçeği, mutlak adayın 1.1102230246251565e-16 katıdır; gönderilen 1e-10 parametresinin bu yoldaki durma hesabında kullanıldığı görülmedi [REA]. Yayımlanmış zeroin varsayılan toleransı farklıdır. İncelenen başlatma yolunda interpolasyon sekant dalında kalır [REA]. Son aday, yayımlanmış güvenli aralık yönteminin doğrusal interpolasyon seçeneğini kullanır; ters karesel interpolasyon kapalı, mutlak tolerans 0 ve bağıl durma ölçeği 1.1102230246251565e-16'dır. Bu yöntem standart Brent ile aynı diye sunulmaz; bit eşitliği garantisi değildir. Durum değişkenlerinin atama tarifi aktarılmaz.

Merkezi olmayan t serisinde gözlenen bağıl terim durma ölçütü 2^-54, merkezileşme eşiği mutlak noncentrality için 1e-100 mertebesindedir [REA]. Yayımlanmış `cumtnc` sırasıyla 1e-7 ve 1e-10 kullanır. Aday denemede bu iki parametre değiştirilir. Ayrıca yayımlanmış yordamın beta neredeyse 0/1 olduğunda yaptığı erken normal yaklaşımı, incelenen binary gövdesinde görülmedi [REA]; son adayda bu iki kestirim kapalıdır. Tam sıfır t için normal limit ve merkezileşme durumu korunur. Seri biçimi veya toplama sırası binary tarifine çevrilmez. Her yönde 50000 terim deneme bütçesi uygulanır; sınırın dolması başarı sayılmaz.

Beta dönüşümünde küçük koordinatın büyük koordinatın 1'den çıkarılması yerine doğrudan hesaplanması gözlendi [REA]. Adayda her iki matematiksel koordinat doğrudan hesaplanır, küçük koordinatın beta tamamlayıcısı için standart simetri özdeşliği kullanılır. Yayımlanmış yöntemden yapılan bu soyut sapma ayrıca sınanır. Binary'ye özgü toplama sırası, geçici durum dizisi veya değerlendirme reçetesi aktarılmaz.

Seri ağırlıkları ve beta normalizasyonu için iki ayrı gamma yaklaşımı bulundu [REA]. Bu, gamma yardımcılarının her derleyicide aynı bitleri vereceğini göstermez. Yukarıdaki yayımlanmış yardımcılar kendi kaynak yöntemleriyle uygulanır; binary'deki parantezlere göre yeniden düzenlenmez ve katsayıları G*Power sonucuna uydurulmaz.

### 15.3 İnceleme deneyi ve üretim koşulları

İlk inceleme iki profili sonuçlar görülmeden belirledi: yayımlanmış parametreler ve ilk soyut parametreler. Bu ilk sonuçlar saklandı. Yüksek güçte yayımlanmış beta kestirimi nedeniyle bir regresyon görülünce, [REA] dayanaklı iki ek soyut fark (beta kestiriminin kapatılması ve yalnız doğrusal interpolasyon) ayrı bir ikinci deney planında, yeni sonuçlar görülmeden kaydedildi. Temel profil ve ara teşhis profiliyle birlikte raporlanır; en yüksek puanı veren profil sessizce seçilmez. Hepsi aynı yayımlanmış Cephes/DCDFLIB bileşimini kullanır. Merkezi kuantil/CDF için yalnız inceleme adaptöründe SciPy 1.16.3 kullanılmaktadır. Bu paylaşılan yardımcı açık bir sınırdır; deney SciPy'siz üretim prototipi değildir.

87 görülmüş vektörde referans gruplarla güç, kendi bulduğu AP N/n1/n2 (51 örnek) ve bütün alanların başarısı ayrı raporlanır. Bu oranlar yeni G*Power ölçümü veya genelleme kanıtı değildir. 1.0.3'ün inceleme adayı 48/51 ve 83/87 idi; korunması varsayılmaz. Beklentiler, toleranslar, paydalar ve başarısız kayıtlar değişmez. Uyuşmazlıklar sonuç tablosu/özel katsayı/etki büyüklüğü eşiğiyle kapatılmaz.

Yeni yöntem teslimde kullanılacaksa:

- 1.0.3'e göre oluşturulmuş deney modülü teslim edilen repo dışında tutulur; tarihçe silinmeden süreç notunda belirtilir. Gelecekte ayrıca onaylanacak yeni uygulama, bu belge ve yayımlanmış kaynaklardan hazırlanır.
- Noncentral dağılım kendi yazıldığında merkezi kuantil dahil dağılım hesabı kendi kodumuzda yapılır; SciPy yalnız testlerdedir. N için hazır çözücü kullanılmaz; Brent algoritması kendimiz yazılır.
- Yeni G*Power doğrulama noktaları Claude tarafından geliştirmeden bağımsız seçilip ölçümden önce liste/hash/tarihle dondurulur. Aday yöntem de sonuçlar görülmeden dondurulur. Yeni ölçümler yalnız karşılaştırılır; yöntem bunlara göre ayarlanmaz.
- Üretime geçiş için bağımsız doğrulamada önceden kararlaştırılmış yüksek AP N uyumu, eski 70 dahil eski başarılı regresyonların korunması ve bütün yönerge koşulları aranır. Yerel testteki %90, hocanın gizli testindeki %90'ın yerine geçmez. Koşullar sağlanmazsa varsayılan motor korunur, bulgu uyuşmazlık açıklaması olarak raporlanır.
- Gerçek ajan/GUI deneyleri eski motor kimlikleriyle korunur; yeni yöntemle yapılmış gibi sunulmaz. Yeni ücretli model API çağrısı veya GUI deneyi bu belgenin parçası değildir.

**Süreç açıklığı:** 1.0.3'ün ayrıntılı tarifi yazım oturumunda okunmuştur. Bu belge o tarihçeyi silmez veya önceki okumanın gerçekleşmediğini iddia etmez. Öğretim elemanının soyutlama yorumu kesinleşmiş sayılmaz; bu belge daha sınırlı bir aktarım yaklaşımıdır.

