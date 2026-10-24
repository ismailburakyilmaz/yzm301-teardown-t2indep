Bu projede ikinci oturumsun: temiz oda yazımı. Bu yeni oturumun tek proje bilgi kaynağı çalışma klasöründeki SPEC.md'dir. Bu prompt çalışma kurallarını verir; ürün davranışını SPEC belirler. İlk oturumun geçmişini veya çıktılarının bulunduğu klasörü okumayacaksın.

Amaç: SPEC'teki t2-indep a priori ve post hoc davranışlarını, kabul testleriyle doğrulanan bir hesap motoru ve sözleşmeye uygun CLI olarak yeniden uygulamak. Temel doğruluk sağlanırsa aynı motorla MCP, sonra SPEC'in gerektirdiği değerlendirmelerle Türkçe ajan ekle.

Temiz oda sınırı:
- İlk olarak yalnızca SPEC.md'yi oku; başlangıç promptunun tam metnini prompts/02_yazim_ilk_prompt.md olarak kaydet.
- İnceleme klasörünü, LEDGER'ı, GPowerNT.exe'yi, decompile/assembly çıktısını, ilk oturumun günlüklerini veya eski sohbetleri arama ve okuma. REA/Ghidra ile hedefi inceleme; G*Power GUI'sine bu yazım oturumundan bağlanma.
- Yeniden yazımın kendi dosyalarını, testlerini ve seçilen dil/kütüphanelerin resmî API belgelerini kullanabilirsin. G*Power'a özgü boşlukları internetten kod kopyalayarak veya genel istatistik bilgisinden varsayarak doldurma.
- Yanlışlıkla ham inceleme içeriğiyle karşılaşırsan daha fazlasını okuma; hangi dosyanın görüldüğünü bildir. Kullanıcı temiz yeni yazım oturumu açabilsin.

İlk kontrol:
- SPEC sürümünü ve SHA-256 değerini hesaplayıp kendi çalışma kaydına yaz.
- SPEC READY_FOR_IMPLEMENTATION değilse veya zorunlu davranış/sözleşme/veri eksikse bunu kesin maddelerle bildir; davranış uydurma. Bağımsız proje iskeleti veya mevcut kesin kriterlerin test hazırlığı yapılabilir, ancak eksik davranış uygulanmış ve doğrulanmış gibi sunulamaz.
- SPEC'teki gömülü referans bloğunu parse et; vektör kimlikleri, mod kapsamı, beklenen alanlar ve hassasiyet kurallarını doğrula. En az 30 geçerli G*Power kaydı yoksa eksikliği raporla.
- Önce kısa, aşamalı bir plan çıkar ve STATUS.md'ye kaydet; sonra uygula. Yalnızca plan üretip durma.
- SPEC aksini söylemiyorsa Python + SciPy + pytest başlangıç tercihidir. Uyumlu sürümleri doğrula ve sabitle. Hazır bir N çözücüsünü motor yerine koyma.

Uygulama sırası:
1. SPEC'in gerçek örneklerini ve Gherkin kabul kriterlerini çalıştırılabilir testlere çevir. İlk başarısız durumları kaydet; ardından motoru geliştir. Kabul testleri için yeni sayısal beklenen değer uydurma.
2. Dağılım fonksiyonlarını izin verilen kütüphaneden kullan. N arama, grup dağıtımı, tamsayı kuralları, df ve doğrulama davranışı SPEC'e göre uygulansın.
3. Motoru terminal, MCP ve LLM'den bağımsız tut. CLI tek satır JSON üretsin; günlükler stdout'u bozmasın. Başarı/hata çıkış kodları, eksik/yanlış argümanlar ve desteklenmeyen test/mod kombinasyonları sözleşmeye uysun.
4. Sabit sonuç tabloları, referans vektör ID'sine özel dallar veya örneğe özel düzeltme katsayıları kullanma.
5. G*Power referansları için alan bazında diferansiyel test raporu üret. N/n1/n2 tam eşitlik; diğer alanlar yalnızca SPEC'in belirlediği hassasiyetle karşılaştırılsın.
6. En az 501 ek vektörü sabit seed ve belgelenmiş parametre kapsamıyla üret; uygun statsmodels veya pwr karşılaştırmasını ayrı raporla. Sürekli/kesirli N ile tamsayı N'yi gelişigüzel eşitleme; parametre ve kuyruk tanımlarını resmî belgelerle kontrol et.
7. A priori sonucunu post hoc ile yeniden hesaplama gibi anlamlı tutarlılık testleri ekle. Bunları orijinal programla uyumun yerine geçirme.
8. Hataları en küçük tekrar üretilebilir girdiye indir. Test beklentisini veya toleransı test geçsin diye değiştirme.
9. Fark kendi uygulamandan kaynaklanıyorsa düzelt. SPEC belirsiz veya çelişkiliyse SPEC_QUESTIONS.md'ye girdi, beklenen/gözlenen çıktı, fark ve net soruyu yaz. Kullanıcı bunu birinci oturuma iletecek. Ham analiz çıktısı isteme; düzeltilmiş SPEC bekle.
10. SPEC güncellenirse sürüm/hash değişimini kaydet ve etkilenen testleri yeniden çalıştır. Eski beklenen değerleri sessizce değiştirme.

Bonus kapısı:
- Önce temel sözleşme ve referans testleri geçmeli; açıklanmamış hesap farkı kalmamalı.
- MCP yalnızca aynı motoru çağıran adaptör olsun. Şemayı README'de belgele; CLI ve MCP için eşdeğerlik testleri ve gerçek MCP çağrı kaydı oluştur. Doğrudan fonksiyon testi tek başına MCP entegrasyon kanıtı değildir.
- Türkçe ajan yalnızca araçtan gelen sayıları kullansın. Eksik girdiyi sorsun; başka aileleri destekliyormuş gibi cevaplamasın.
- SPEC'teki 10 soruluk değerlendirmeyi ve aynı sorularla GUI–MCP token/süre/doğruluk ölçümünü uygula. GUI yolunun ölçümü birinci oturum/kullanıcı tarafından yürütülür; bu oturum G*Power ekranlarına erişmez. Aynı senaryo setini ve ölçüm protokolünü kullan.
- Gerekli anahtar, ölçüm erişimi veya zaman yoksa eksik bonusu tamamlandı sayma. Temel teslimin çalışmasını koru.

Teslim:
- src/, tests/, sabitlenmiş bağımlılıklar, kurulum/çalıştırma yönergeleri, README, diferansiyel uyum raporu, varsa MCP/ajan değerlendirmeleri üret.
- Gömülü referans verisini tests/fixtures/ altında aynen çıkar; kaynak SPEC sürümü/hash'iyle ilişkilendir. Gerçek oracle ekran görüntüleri daha sonra kullanıcı tarafından teslim paketine eklenecek.
- HALLUCINATIONS_YAZIM.md ve AGENT_COST_YAZIM.md içinde gerçek yanlış çıkarımları ve ölçümleri tut; olay veya token sayısı uydurma.
- LEDGER ve birinci oturumun kanıtlarını yeniden üretmeye veya tahminle doldurmaya çalışma. Bunları final birleştirmede kullanıcı ekleyecek.
- README'ye desteklenen kapsamı, gerçekten tamamlanan katmanları, test paydalarını, sınırlamaları, G*Power sürüm/hash bilgisini (SPEC'ten), yazarlara atfı ve 60 saniyelik demo adımlarını koy. Çekilmemiş video için sahte bağlantı yazma.
- GPowerNT.exe, dağıtım arşivi, sırlar ve ham decompile çıktısı repoya girmesin. .gitignore oluştur; ürünün bağımsız eğitim çalışması olduğunu belirt.
- Temiz bir yerel ortamda kurulumu ve belgelenmiş komutları doğrula. Testlerin gerçekten çalıştırılıp çalıştırılmadığını açıkça raporla.
- GitHub'a yayınlama, ücretli hizmet açma veya ek test aileleri geliştirme kapsamı kendiliğinden eklenmesin.

Son mesajında çalışan komutları, test sonuçlarını (geçen/toplam), bonus durumunu, teslim dosyalarını ve varsa engelleri belirt. Başarıyı yalnızca kodun yazılmış olmasına göre ilan etme.

