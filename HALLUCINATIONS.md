# HALLUCINATIONS — birleşik özet

Durum: teslim belgesi. Kaynak günlükler docs/process/ altında baytları korunarak bulunur.

İnceleme kayıtlarının H-001…H-015 kimlikleri korunur. Y-001…Y-024 bu özette yazım kaynağındaki paragraflara verilmiş izleme kimlikleridir; özgün günlüğü yeniden numaralandırmaz. Ürün ajanı hataları, elenen hipotezler ve ortam/süreç hataları türleriyle belirtilir; hepsi yazım modelinin yeni halüsinasyonu diye sayılmaz. Bir testin adı veya yakalama yöntemi kayıtta yoksa uydurulmaz.

## Kaynaklar

- [İnceleme günlüğü](docs/process/HALLUCINATIONS_INCELEME.md); SHA-256 `b343dfe2bb0277340a8fe67d29030243d25ede81894ca9b2c45b213c0b667377`.
- [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md); SHA-256 `6ac6157567955e53806e9e0fb4f314481b429df1e62abebb65601179f2286420`.

## İnceleme oturumu

### H-001 — Grupları ayrı yuvarlama

- **Ajanın yanlış çıkardığı şey:** n2'nin n1×oran ile veya her grubun bağımsız yuvarlanmasıyla bulunacağı sanıldı.
- **Nasıl fark edildi:** Oran 1,5 ve 3 örnekleri bu varsayıma karşı sonuç verdi.
- **Hangi test yakaladı:** GP-AP-012, GP-AP-022, GP-AP-023 ve PROBE-R3 gözlemleri.
- **Düzeltme / kapsam:** n2=N−n1 kuralı kaydedildi.
- **Kaynak:** [H-001](docs/process/HALLUCINATIONS_INCELEME.md).

### H-002 — N için basit tavan

- **Ajanın yanlış çıkardığı şey:** Gerekli toplam N, sürekli çözümün yukarı yuvarlandığı en küçük tamsayı sanıldı.
- **Nasıl fark edildi:** 12561 hedef gücü sağlarken a priori sonucun 12562 olmasıyla çelişki görüldü.
- **Hangi test yakaladı:** GP-AP-014 ↔ GP-PH-020 çapraz kontrolü; GP-PH-012 ve GP-PH-021.
- **Düzeltme / kapsam:** Çift N gözlemi kaydedildi. Sonraki küçük d ölçümleri en küçük çift N genellemesinin büyük N sınırını ortaya çıkardı; evrensel iç algoritma kanıtı sayılmaz.
- **Kaynak:** [H-002](docs/process/HALLUCINATIONS_INCELEME.md).

### H-003 — Kritik t işaretini yalnız d ile açıklama

- **Ajanın yanlış çıkardığı şey:** Pozitif d'nin kritik t'yi her zaman pozitif yapacağı genellendi.
- **Nasıl fark edildi:** Bağımsız inceleme cebirsel çelişkiyi buldu; tek yönlü α=0,75 ölçümü negatif kritik değer verdi.
- **Hangi test yakaladı:** GP-PH-024…031 ve GP-AP-025…027; ilk yakalama inceleme, ardından GUI doğrulaması.
- **Düzeltme / kapsam:** Kuantil ve kuyruk yönü birlikte dikkate alındı.
- **Kaynak:** [H-003](docs/process/HALLUCINATIONS_INCELEME.md).

### H-004 — r ile 1/r için genel ayna kuralı

- **Ajanın yanlış çıkardığı şey:** Birkaç eşleşen örnekten bütün oranların tersinde grupların aynalanacağı çıkarıldı.
- **Nasıl fark edildi:** 0,3333333 ve 3 oranlarındaki grup tahsisleri karşılaştırıldı.
- **Hangi test yakaladı:** GP-AP-032 ile oran 3 karşı örneği; GUI gözlemi.
- **Düzeltme / kapsam:** İddia gözlenen çiftlerle sınırlandı.
- **Kaynak:** [H-004](docs/process/HALLUCINATIONS_INCELEME.md).

### H-005 — Alt olasılık sınırını açık sanma

- **Ajanın yanlış çıkardığı şey:** α ve güç için 1e-7 alt sınırının dışlandığı düşünüldü.
- **Nasıl fark edildi:** Tam sınırdaki değerler G*Power tarafından kabul edildi.
- **Hangi test yakaladı:** GP-PH-032 ve GP-AP-033.
- **Düzeltme / kapsam:** Gözlenen alt sınır 1e-7 ≤ x olarak düzeltildi.
- **Kaynak:** [H-005](docs/process/HALLUCINATIONS_INCELEME.md).

### H-006 — Kayıt kapsamını abartma

- **Ajanın yanlış çıkardığı şey:** Sonuç üreten INV-GUI-001 geçersiz sayıldı; minimalite bütün AP örneklerinde doğrulanmış gibi yazıldı.
- **Nasıl fark edildi:** Bağımsız inceleme, gerçek kabulü ve yalnız üç doğrudan minimalite kontrolünü ayırdı.
- **Hangi test yakaladı:** Test değil, bağımsız inceleme yakaladı; INV-GUI-001 kaydı ve üç AP/PH çifti dayanak.
- **Düzeltme / kapsam:** Sınıflandırma ve doğrulama kapsamı daraltıldı.
- **Kaynak:** [H-006](docs/process/HALLUCINATIONS_INCELEME.md).

### H-007 — Tokenların ölçülemeyeceğini varsayma

- **Ajanın yanlış çıkardığı şey:** Yerel yanıt usage alanı incelenmeden API başına token ölçülemez denildi.
- **Nasıl fark edildi:** Kullanıcının sorusu üzerine Claude yerel dökümündeki usage alanı bulundu.
- **Hangi test yakaladı:** Test değil, oturum dökümü incelemesi yakaladı.
- **Düzeltme / kapsam:** Ölçülen değerler eklendi; görüntü payı ve para maliyeti ayrı tutuldu.
- **Kaynak:** [H-007](docs/process/HALLUCINATIONS_INCELEME.md).

### H-008 — Hata dizelerini kök aramaya özgü sanma

- **Ajanın yanlış çıkardığı şey:** İki sayısal hata mesajı tek başına N kök çözücüsünün işareti kabul edildi.
- **Nasıl fark edildi:** Aynı mesajların yayımlanmış integral kaynağında da bulunduğu görüldü.
- **Hangi test yakaladı:** Test değil, kaynak/çağrı yolu incelemesi yakaladı.
- **Düzeltme / kapsam:** Dizeler tek başına çözücü tanısı sayılmadı; elenen yol yeniden etiketlenmedi.
- **Kaynak:** [H-008](docs/process/HALLUCINATIONS_INCELEME.md).

### H-009 — Tek yön girdisini iki yön hesaplama

- **Ajanın yanlış çıkardığı şey:** Üç örneklik inceleme denemesinde One girdisine rağmen iki yön kuantili sabitlendi.
- **Nasıl fark edildi:** Beklenmedik güç sonuçlarından sonra tails girdisi kontrol edildi.
- **Hangi test yakaladı:** Üç örneğin aynı girdilerle yeniden karşılaştırılması; kaynakta ayrıca test fonksiyonu adı yok.
- **Düzeltme / kapsam:** Deneme girdisi düzeltildi; üretim motoru ve beklenenler değişmedi.
- **Kaynak:** [H-009](docs/process/HALLUCINATIONS_INCELEME.md).

### H-010 — Cebirsel eşdeğerliği kayan nokta eşdeğerliği sayma

- **Ajanın yanlış çıkardığı şey:** Cebirsel olarak aynı sayısal ifadelerin uygulamada da aynı sonucu vereceği varsayıldı.
- **Nasıl fark edildi:** Tarihî inceleme deneyinde farklı değerlendirme düzenleri farklı N eşleşmeleri verdi.
- **Hangi test yakaladı:** Görülmüş 51 AP vektöründeki inceleme deneyi: 41/51 ile 48/51 farkı; holdout değildir.
- **Düzeltme / kapsam:** Kaynağın 1.0.3 tarifine ilişkin düzeltmesi tarihîdir. Bu tarif üretime alınmadı; 1.0.4 ile soyutlamaya dönüldü. Ayrıntılı tarif burada yeniden üretilmez.
- **Kaynak:** [H-010](docs/process/HALLUCINATIONS_INCELEME.md).

### H-011 — Bilimsel gösterimden yanlış tolerans örneği

- **Ajanın yanlış çıkardığı şey:** 3.05715e-05 gösteriminin yarım son basamağı 5e-8 sınırından büyükmüş gibi örnek verildi.
- **Nasıl fark edildi:** Taslak okunurken bu değerin yarım son basamağının 5e-11 olduğu fark edildi.
- **Hangi test yakaladı:** Test değil, Codex bağımsız incelemesi yakaladı; Classroom gönderiminden önce düzeltildi.
- **Düzeltme / kapsam:** İddiayı gerçekten destekleyen daha az ondalıklı örnekler kullanıldı.
- **Kaynak:** [H-011](docs/process/HALLUCINATIONS_INCELEME.md).

### H-012 — Hata önceliğini tahmin etme

- **Ajanın yanlış çıkardığı şey:** Doğrulayıcı soldan sağa çalışıyor sanıldı; ardından evre içi sırayı CONTRACT tablosuna göre değiştirmek önerildi.
- **Nasıl fark edildi:** Codex mevcut evreli davranışla talimat arasındaki farkı taslak hazırlarken sordu.
- **Hangi test yakaladı:** İlk yakalama incelemeydi; korunan sözleşme davranışı 139/139 testle doğrulandı.
- **Düzeltme / kapsam:** Mevcut evre ve evre içi sıra korundu; bu kapsamda kod değişmedi.
- **Kaynak:** [H-012](docs/process/HALLUCINATIONS_INCELEME.md).

### H-013 — NaN çiftlerini farklı sonuç sayma

- **Ajanın yanlış çıkardığı şey:** != karşılaştırması nedeniyle iki NaN da yöntemler arası fark sayıldı; 3000 girdide 290 fark diye bildirildi.
- **Nasıl fark edildi:** NaN eşitliği ayrı ele alındı ve SciPy kaynak bağlantısı kontrol edildi.
- **Hangi test yakaladı:** NaN durumları ayrılan 20000 girdilik karşılaştırmada fark 0; kayıttaki üç fonksiyon çifti.
- **Düzeltme / kapsam:** Kullanıcıya düzeltme yapıldı; yanlış iddia yazım talimatına girmedi, motor/SPEC değişmedi.
- **Kaynak:** [H-013](docs/process/HALLUCINATIONS_INCELEME.md).

### H-014 — Başarısızları çıkarmayı N eşiğiyle aynı sanma

- **Ajanın yanlış çıkardığı şey:** Bilinen 11 uyuşmazlık dışındaki 77 AP örneğinin hepsinin N ≤ 3·10⁷ olduğu varsayıldı; eşik bölmesi hesaplanmadan 77/77 ve 0/11 önerildi.
- **Nasıl fark edildi:** Codex taslak hazırlığında kayıtları referans N ile böldü: alt bölge 75/75, üst bölge 2/13. GP-AP-045 ve GP-AP-046 eşik üstünde olmasına rağmen eşleşiyordu. İnceleme tarafı CSV kayıtlarından aynı sonucu bağımsız doğruladı.
- **Hangi test yakaladı:** Test değil, kayıt/CSV incelemesi ve karşılaştırma hesabı yakaladı; yeni motor veya G*Power ölçümü yapılmadı. Dayanak: gpower_vectors.csv, contract_expectations.csv ve N_REGION_CHECK.json.
- **Düzeltme / kapsam:** Yanlış satır README’ye uygulanmadan düzeltildi; toplam 77/88 değişmedi. Kod, SPEC ve tolerans değişmedi.
- **Kaynak:** [H-014](docs/process/HALLUCINATIONS_INCELEME.md).

### H-015 — Dosyanın bir kısmını okuyup tamamı hakkında hüküm verme

- **Ajanın yanlış çıkardığı şey:** `.gitignore` yalnız `head -30` ile okunup `experiments/` ve `SPEC_QUESTIONS.md` dosyalarının dışlanmadığı birlikte iddia edildi; kesilmiş çıktı dosyanın tamamı sanıldı.
- **Nasıl fark edildi:** Codex bulguyu kendi kaydıyla karşılaştırınca dosyanın 39 satır olduğunu ve son satırlarda 1.0.3 deney dosyalarının zaten dışlandığını gördü. Dosyanın tamamı okununca iddianın yalnız `SPEC_QUESTIONS.md` kısmının geçerli olduğu anlaşıldı.
- **Hangi test yakaladı:** Test değil, Codex'in dosyanın tamamını ve denetim iddiasını karşılaştırdığı inceleme yakaladı; kaynak günlüğünde bunu yakalayan bir test adı yok. Denetim raporu düzeltildi; kod ve SPEC değiştirilmedi.
- **Kaynak:** [H-015](docs/process/HALLUCINATIONS_INCELEME.md).

## Yazım oturumu ve ürün ajanı kayıtları

### Y-001 — Yanlış hata alanı bekleme

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Bozuk sayıyı bulmadan ilk alpha/power/ratio alanı hata alanı seçildi.
- **Nasıl fark edildi:** ratio=1/3 için alpha beklenmesi ilk çalışmada ortaya çıktı.
- **Hangi test yakaladı:** İlk CLI hata testi, INV-GUI-022; test fonksiyonunun adı kaynakta yok.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-002 — Kurulum bitmeden sürüm doğrulandı izlenimi

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Kurulum sürerken açılan test dosyasının adı sürümün değiştiği izlenimi verdi; gerçek sürüm 1.18.1 idi.
- **Nasıl fark edildi:** Çalışan ortamın gerçek paket sürümü kontrol edildi.
- **Hangi test yakaladı:** Test değil, kurulum/sürüm incelemesi yakaladı; koşu alternatif sürüm kanıtı sayılmadı.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-003 — solve_power her zaman sonlu skaler sanma

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Kütüphane kök sonucunun her zaman sonlu bir skaler olacağı varsayıldı.
- **Nasıl fark edildi:** Ek karşılaştırma verilerinde array/NaN çıktı görüldü.
- **Hangi test yakaladı:** Ek diferansiyel karşılaştırma vakaları; özel test adı kaynakta yok. Skaler ve sonluluk kontrolü eklendi.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-004 — Denetleyicinin kendi sabitini sır sanması

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Python denetleyicisindeki anahtar başlığı sabiti gerçek gizli anahtar diye işaretlendi.
- **Nasıl fark edildi:** Denetimin hangi satırda durduğu incelendi.
- **Hangi test yakaladı:** Test değil, teslim manifesti/sır taraması yakaladı; gerçek sır bulunduğu iddia edilmedi.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-005 — MCP handshake varsayımı

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Auto modunun initialize yapacağı varsayıldı.
- **Nasıl fark edildi:** Gerçek tel kaydında server/discover akışı görülüp protokol beklentisi ayrıldı.
- **Hangi test yakaladı:** MCP kanıt denetimi ve gerçek tel kaydı; ilk kayıt saklandı, legacy modu seçildi.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-006 — Kök kalanını başarıya katmama

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Kök kalanı kaydedildiği hâlde başarı kararında kullanılmadı.
- **Nasıl fark edildi:** Aynı ölçütlerle EX-058 yeniden değerlendirildi; ek karşılaştırma 562/630 yerine 561/630 oldu.
- **Hangi test yakaladı:** EX-058 yeniden karşılaştırması; SPEC 1.0.1 kök-kalanı kontrolü başarı koşuluna eklendi.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-007 — Yanıtsız 403 çalışmasını model değerlendirmesi sayma

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** 14 HTTP403 isteği evaluated_real_model adıyla model kalitesi ölçümü izlenimi verdi.
- **Nasıl fark edildi:** Gerçek kayıtlarda model yanıtı/usage olmadığı görüldü.
- **Hangi test yakaladı:** Test değil, kullanıcının 14 istek makbuzunun incelemesi yakaladı; sonraki 401/403 durdurma kontrolleri eklendi.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-008 — Groq hatasına Gemini yardımı verme

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** required_connection sağlayıcı kontrol edilmeden Google AI Studio diyordu.
- **Nasıl fark edildi:** Kullanıcının tek Groq preflight sonucuyla görüldü.
- **Hangi test yakaladı:** Gerçek Groq preflight; düzeltme sonrası üç sağlayıcının 401/403 batch kontrolleri. Özgün makbuz değişmedi.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-009 — JSON olmayan hata gövdesini tamamen atma

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Tanılayıcı JSON olmayan gövdeleri atınca eski 403 nedenine dair güvenli özet de kayboldu.
- **Nasıl fark edildi:** Eski preflight kaydında safe_error eksikliği görüldü.
- **Hangi test yakaladı:** Test değil, tanı kaydı incelemesi yakaladı; kayıp eski gövde sonradan varmış gibi doldurulmadı.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-010 — Boş ortam pip check sonucunu yanlış yorumlama riski

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** DNS nedeniyle kurulamamış ortamda sonraki pip check başarılı görünüyordu.
- **Nasıl fark edildi:** Önceki pip kurulumunun başarısız olduğu logdan ayrıldı.
- **Hangi test yakaladı:** Test değil, kurulum adımlarının çıkış kodu/log incelemesi yakaladı; boş ortam kurulum başarısı sayılmadı.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-011 — Ürün ajanının ilk iki zorlayıcı kararı

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Ürün modeli AG-C2 için yanlış eksikleri sordu; AG-C4 ki-kareyi t2-indep sanıp yanlış araç çağırdı.
- **Nasıl fark edildi:** 10+4 gerçek soru değerlendirmesinde beklenen aile ve parametrelerle karşılaştırıldı.
- **Hangi test yakaladı:** AG-C2 ve AG-C4 gerçek model değerlendirmesi; 10/10 esas, 2/4 zorlayıcı. Bu yazım ajanının çıkarımı değil, ürün ajanı hatasıdır.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-012 — Sözdizimi kontrolünden önce durum bildirimi

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Güç kesintisi sonrasında durum notu sözdizimi doğrulanmadan olumlu izlenim verdi.
- **Nasıl fark edildi:** __init__.py içinde 87 NUL baytı görülüp gerçek durum yeniden yazıldı.
- **Hangi test yakaladı:** Test değil, dosya/sözdizimi incelemesi yakaladı. NUL bozulmasının kendisi model halüsinasyonu diye sınıflanmadı.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-013 — Genel sayı çıkarımında sınır ve sahiplenme hatası

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** NUMBER kalıbı cümle virgülünü dışlıyor; yüzde eşleşmesi aynı sayıyı iki kez veya komşu alanda kullanabiliyordu.
- **Nasıl fark edildi:** İlk 29 regresyon testinin 8 başarısızlığı ayrıştırıldı.
- **Hangi test yakaladı:** 29 testlik kaynak koruma regresyonu; aynı beklentiler ve iki ek genel akışla 31/31. Sentetik/parser testi, gerçek LLM başarısı değil.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-014 — Hassasiyeti azaltmanın median farkını çözeceği hipotezi

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Desteklenmeyen hipotez: genel hassasiyet azaltma kritik median gürültüsünü çözebilirdi.
- **Nasıl fark edildi:** Double ve float32 yolları referanslarla karşılaştırıldı; uyum bozuldu.
- **Hangi test yakaladı:** 70 vektörlük test deneyi: double 69/70, float32 kernel 14/70, çıktı float32 43/70. Üretim/tolerans değişmedi; doğru diye sunulmuş yeni motor hatası değil, elenen hipotez.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-015 — Ürün ajanının AG-C3 kapsam kararı

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Ham model eşleştirilmiş kapsamı reddetmek yerine ek parametre açıklaması istedi.
- **Nasıl fark edildi:** Ham karar ile guard sonrası sistem sonucu ayrı ölçüldü.
- **Hangi test yakaladı:** AG-C3 gerçek 0.3.0 regresyonu; ham 13/14, sistem 14/14. Scope guard engelledi; sayısal araç çalışmadı.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-016 — MCP tamamlanmadan rapor üretme

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Yeni MCP süreci bitmeden rapor üretimi başlatılmak istendi.
- **Nasıl fark edildi:** Kaynak hash/freshness denetimi eski taşıma kaydını reddedip durdu.
- **Hangi test yakaladı:** Rapor üreticisinin kaynak hash kontrolü; otomatik koruma yakaladı. Taşıma bittikten sonra rapor yeniden üretildi.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-017 — Çakışan Python seçim bayrakları

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** only-managed Python ayarı ile --managed-python bayrağı birlikte kullanıldı.
- **Nasıl fark edildi:** Gerçek kurulum komutu bayrak çakışmasıyla durdu.
- **Hangi test yakaladı:** Test değil, kurulumun gerçek hata çıktısı yakaladı; düzeltme yeni boş dizinde doğrulandı.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-018 — Güncel görev yerine eski aktarım sorusuna yanıt

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Teslim kapanışı sırasında eski SPEC 1.0.2 aktarım sorusuna yanıt verildi.
- **Nasıl fark edildi:** Koordinatör mevcut görev bağlamını düzeltti.
- **Hangi test yakaladı:** Test değil, koordinatör incelemesi yakaladı. SPEC aktarımı veya sürüm düşürme yapılmadı.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-019 — Python desteğini ham CSV metin eşitliğine bağlama

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Betik taslağı Python destek kapısını ham CSV metin eşitliğiyle tanımladı.
- **Nasıl fark edildi:** Tam testler başlamadan önce destek ölçütünün bu olmadığı fark edildi.
- **Hangi test yakaladı:** Test değil, betik/talimat incelemesi yakaladı; tam sayılar ve mevcut SPEC hassasiyeti esas alındı.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-020 — Timeoutta kısmi çıktıyı kaydetmeme

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** İlk timeout işleyicisi kısmi kurulum stdout/stderr kaydını korumuyordu.
- **Nasıl fark edildi:** 3.12 yardımcı betiği 1200 saniyede durduğunda çıktı eksikliği görüldü.
- **Hangi test yakaladı:** Test değil, gerçek timeout ve ATTEMPT_TIMEOUT.json incelemesi yakaladı; sonraki akış canlı dosya kaydı kullandı.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-021 — PowerShell modül yüklemesini yeterli sanma

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Utility modülünü açık yüklemenin Get-FileHash/5.1 sorununu gidereceği düşünüldü.
- **Nasıl fark edildi:** 5.1 makbuz adımı yine çalışmadı; kurulu paketler test başarısı sayılmadı.
- **Hangi test yakaladı:** Test değil, gerçek makbuz/komut hatası yakaladı; mevcut PowerShell 7.6.5 ile kapanış doğrulandı.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-022 — Geçici metadata değişimini tarihî hash testine taşıma

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Kurulum için geçici pyproject aralığı tam koşunun tarihî hash denetimine taşındı.
- **Nasıl fark edildi:** 2076/2169 içindeki ek iki başarısızlığın sayısal değil metadata kaynaklı olduğu ayrıldı.
- **Hangi test yakaladı:** İki tarihî metadata/hash testi yakaladı; kaynak geri alınıp tekrar ölçüldü. Sonradan kullanıcı onaylı dar istisna ile 2078/2169 korundu.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-023 — JSON literal türünden alan toleransı seçme

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Karşılaştırıcı ncp=0 JSON integer göründüğü için alanı integer kabul etti.
- **Nasıl fark edildi:** SPEC integer alan listesiyle karşılaştırıldığında ncp için yanlış sınıf görüldü.
- **Hangi test yakaladı:** Karşılaştırıcı/SPEC denetimi; kaynakta ilk yakalayan test fonksiyonunun adı belirtilmemiş. Listeye göre düzeltildi, oracle/tolerans değişmedi.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

### Y-024 — Çok büyük integer ile otomatik pytest vaka adı

- **Ajanın yanlış çıkardığı şey / sınanan varsayım:** Çok büyük integer için otomatik vaka adı üretiminin sorunsuz olacağı varsayıldı.
- **Nasıl fark edildi:** Pytest daha testler çalışmadan koleksiyon hatası verdi.
- **Hangi test yakaladı:** Pytest collection aşaması yakaladı; açık vaka kimliği eklendi, sayısal beklenti değişmedi.
- **Kaynak:** [Yazım günlüğü](docs/process/HALLUCINATIONS_YAZIM.md)

## K-001 — 22 Ekim temiz oda olayı (dört satırlık özet)

- **Yanlış çıkarım / kök neden:** SPEC 1.0.3'e REA'dan türetilmiş fazla ayrıntılı tarif girdi; 1.0.4 karantinasında bunu taşıyan SPEC_QUESTIONS.md gözden kaçtı ve repo içi soru dosyası güvenli okuma kaynağı varsayıldı.
- **Nasıl fark edildi:** 22 Ekim'de eski teşhisleri okuduğunu yazım oturumunun kendisi fark edip bildirdi ve durdu; yeni Ghidra/decompile dosyası okunduğu iddia edilmez.
- **Hangi test / kanıt:** Test değil, yazım oturumunun kendi kapsam kontrolü yakaladı. engine.py ve contract.py hash'leri tarihî kayıtlarla aynı kaldı; bu, geçmiş erişimi yok saydıran veya öğretim elemanı adına uygunluk kararı veren bir kanıt değildir.
- **Önlem / kaynak:** Geçmişsiz Kapanış C'ye geçildi; eski deney, SPEC_QUESTIONS ve türevleri yeni paketlerden çıkarıldı; kaynak günlük ve A/B kanıtları korundu.

Kanıt atıfları: [Yazım olay kaydı](docs/process/HALLUCINATIONS_YAZIM.md), [A/B raporu](docs/process/INCIDENT_A_B_RAPORU.md), [Geçmişsiz kapanışın bağımsız paket denetimi](docs/process/C_CLOSURE_KISA_RAPOR.md).

## Hata sayısı olarak eklenmeyen süreç notları

Yazım kaynağındaki 20 Ekim GUI ölçüm kapsamı, SPEC 1.0.2 veri artışı, aday yöntemin görülmüş küme sınırı, SPEC 1.0.4 teslim ayrımı, DNS/ağ engelinin Python uyumsuzluğu sayılmaması, REA araç listesinin çağrı sayılmaması, Classroom beyanının bağımsız erişim sayılmaması ve xfail uygulanmaması korunmuş kapsam notlarıdır. Bunlar için yeni yanlış iddia veya yeni yakalayan test uydurulmadı. 3.12/3.13 kapanışındaki aynı sayısal sonuçlar ve olay sonrası hash doğrulaması da ayrı halüsinasyon sayısını artırmaz. Yinelenen 22 Ekim durdurma/koordinatör notları K-001'de tek olay olarak özetlenmiştir.

Bu özet tarihî bir “düzeltildi” ifadesini güncel üretim tercihi gibi yeniden uygulamaz. Özellikle H-010'un 1.0.3 deneyi teslim motoru değildir. Çekirdek, CONTRACT, SPEC, testler ve toleranslar değiştirilmedi.

## Son performans kapanışı notu

Yukarıdaki çekirdek değişmezliği ifadeleri, kaynak olayların ve özetin hazırlandığı aşamayı anlatır. 23 Ekim 0.4.3 kapanışında kullanıcı onayıyla yalnız engine dağılım importu ve yayımlanmış SciPy davranışını koruyan skaler sarmalayıcı değiştirildi; N araması, tahsis, yuvarlama, SPEC, CONTRACT ve sayısal beklentiler korunmuştur. Bu onaylı performans değişikliği, 22 Ekim olayında motorun değişmediği tarihî kanıtı yeniden yazmaz. Güncel hash ve gerçek regresyon sonucu TESLIM_KONTROLU.md içindedir.
