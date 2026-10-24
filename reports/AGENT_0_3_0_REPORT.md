# Ajan 0.3.0 — kapsam ve sayısal girdi kaynağı denetimi

# Türkçe ajan 0.3.0 — gerçek görülmüş-soru regresyonu

Kaynak `reports/agent_runs/20261019_162441_194101`; kullanıcı tarafından başlatıldı. 14 tek deneme,
14 istek, 14 benzersiz model yanıtı.
Model Groq/qwen/qwen3.8-27b. Yazım ajanı yeni API isteği göndermedi.
Ölçümün özgün SPEC kaynağı **1.0.1**,
SHA-256 `aebcfdf0b0f220041237e812ea36a01756160a7bff779580d34c1d77c8b39221`. Güncel SPEC'e yeniden etiketlenmedi.

| Ölçüt | Esas 10 | Zorlayıcı 4 | Toplam |
|---|---|---|---|
| Guard sonrası sistem tam başarı | 10/10 | 4/4 | 14/14 |
| Ham model karar başarısı | 10/10 | 3/4 | 13/14 |

Gerçek MCP wire parametre/sonuç kontrolü 10/10.
Guard müdahaleleri:

- AG-C3: scope_block; ham `{"name": "ask_clarification", "arguments": {"missing": ["mode", "d", "alpha", "power", "family"]}, "call_id": "eam3p11zd"}`; son `t-paired/state_unsupported`; yürütülen araç 0, sayısal sonuç `null`.

Guard başarısı ham modelin kararını doğru diye yeniden puanlamaz.

| Gerçek ölçüm | Esas 10 | Tüm 14 |
|---|---|---|
| Input token | 12522 | 17414 |
| Output token | 834 | 980 |
| Toplam token | 13356 | 18394 |
| API süreleri toplamı (s) | 11.7041827 | 14.6690566 |
| Deneme süresi toplamı, pacing hariç (s) | 38.9091613 | 41.8837643 |

Invocation 260.6845006 s; pacing
218.7303480 s ayrı. API gecikmesi, MCP roundtrip ve
deneme toplamı iç içe bileşenlerdir; iki kez toplanmaz. Para maliyeti ölçülmedi.
Araç JSON byte boyutu model tokenı değildir; bölüm token/para maliyeti null.

Bu görülmüş SPEC sorularında değişiklik sonrası regresyondur, holdout veya
genel yüzde100 değildir. 0.2.2 baseline 10/10+2/4=12/14 aynen korunur;
yeni kimlik eski koşuya eklenmedi. Kaynak9 dosya/prompt/config, evaluator
ve SPEC kimliği eşleşti. Yeni özgün dosyalar agent_run_reviews altındaki
değişmez hash manifestiyle sabitlendi.

Temiz GUI aktarımı tamamlandı: ilk teknik iş akışı 7/10, ilk model planı 8/10, belgeli toparlanma sonrası N 10/10; sayısal okuma 60/70. GUI 64753 bilinen token, MCP esas10 13356; iki reddin usage'ı null. Koordinatör model kullanımı/maliyeti ölçülmedi ve toplama dahil değil. İnsan işletimli GUI; otonom kontrol kanıtı yok. Ayrıntı: [son GUI–MCP raporu](GUI_MCP_TEMIZ_RAPOR.md).
Gerçek sıra MCP önce, GUI sonradır. Para tasarrufu, genel hızlanma veya
dengeli sıra iddiası yoktur. Pratik yürütme rehberi:
docs/GUI_EXPERIMENT_GUIDE.md. GPower ekranları yazım oturumunda açılmadı.


Eski 0.2.2 baseline,
14 ilk istekte 10/10 esas + 2/4 zorlayıcı = 12/14 olarak aynen durur.
Yeni kuralların aynı sorulardaki denemesi değişiklik sonrası
regresyondur; görülmemiş performans ölçümü değildir. Yazım ajanı gerçek
model API'si çağırmadı. Model/servis otomatik değiştirilmedi.

## Davranış

Tek engine/CLI/MCP hesap kapsamı değişmedi. Model kararı alındıktan sonra,
hesap aracından önce genel Türkçe kaynak koruması uygulanır. Kategorik oran,
2x2/ki-kare, eşleştirilmiş, çoklu grup veya regresyon gibi tanınan destek
dışı kaynaklar t motoruna verilmez. w/dz/R² Cohen d olarak kullanılamaz.
Tahsis oranı N2/N1 kategorik sonuç oranı sayılmaz; açık olumsuzlama ve
desteklenen yakın ifadeler regresyon testindedir. Vaka ID'si, soru metni/N
tablosu veya üretimde oracle erişimi yoktur.

Etiketli değerler, sayı token sınırları, Türkçe ondalık virgül/nokta ve yüzde
yalnız kaynakta ifade edildiği gibi okunur. Eksik/çelişkili tüm zorunlu
alanlar açıklama isteğine eklenir; tails/power/ratio varsayılmaz. Modelin
kendi temkinli açıklaması veya kapsam reddi korunur. Hesap girdisi açık
kaynağıyla uyuşmuyorsa hesap yerine açıklama istenir. Koruma N/güç hesabı
yapmaz; sayılar yine yalnız MCP aracından gelir.

Bu sınırlı, konservatif bir dil ayrıştırıcısıdır. Her Türkçe anlatımı,
karmaşık olumsuzlamayı veya istatistiksel tasarımı anlayan bir sınıflandırıcı
değildir; anlaşılmayan meşru soruda da açıklama isteyebilir. Kapsam dışında
reddedilen soruların istatistik çözümünü geliştirmez.

## Ham model ve sistem sonucu

raw_model_choice, source_guard ve intervened/action gerekçesi tutulur.
metrics nihai guard sonrası sistemin skorudur. raw_model_metrics aile,
parametre ve araç seçimini ayrı puanlar. Engellenmiş ham karar için motor
yeniden çalıştırılmaz; raw N/full_success null ve ilgili payda 0 kalabilir.
Alan paydaları, müdahale sayısı/gerekçeleri ayrı raporlanır. Bir sistem
reddinin doğru olması, yanlış ham LLM seçimini doğruya dönüştürmez.

## Kimlik ve geçmiş

agent_version 0.3.0, policy scope-origin-v1.
Prompt SHA-256 `99f797278a32a33e006c0fc3b9d1fe7b5d56f44d55997f264260459cb3d35453`;
config `fe53c45ddb28766fe99be7cb9f9750ca9455b7b30e5754876c0495aa8a2f402c`;
source `73dac118238ffc47f569f7e39ac0a8c6bea4451715fbda5c4a2513e9371c7db9`.
Araç şeması ve dosya hash'leri agent_0_3_0_identity.json içinde.
Kimlik sır içermez. Yeni metadata/attempt/summary kimliği, evaluator hash'i
ve regresyon etiketi kaydeder. Farklı kimlik veya eski kimliksiz baseline
ile resume reddedilir; eski dosyaya yeni kimlik eklenmez. Pacing ayarı ayrı
run_config hash'idir. 0.2.2 kaynakları/talimatı reports/history/agent_0_2_2_baseline
altında arşivlidir; eski çalışma kendi dosyalarıyla kalır.

## Doğrulama ve ölçüm sınırı

İlk parser testinde 8/29 başarısızlık saklandı. Düzeltilmiş çekirdek girdi
ve farklı Türkçe/negatif kontrol testleri 31/31 geçti. Yeni kimlik, skor,
taşıma, pacing ve dispatch testleri gerçek API kullanmaz. Son tam test kaydı
1994/2075, 81 başarısız;
ayrı entegrasyon 185/185. Bu SPEC1.0.1 tarihî koşusunun üç oracle/78 kütüphane farkı
gizlenmedi. Yeni gerçek model başarısı bu sayaçlardan çıkarılmaz.
Güncel SPEC 1.0.2 diferansiyel sonuçları DIFFERENTIAL_REPORT.md içindedir;
eski ajan ölçümüne yeni SPEC kimliği eklenmez.

Baseline MCP on sorunun token/süreleri ayrı
gui_mcp_protocol_groq_baseline_0_2_2.json içindedir. GUI on satırı null;
göreli süre/token tasarrufu iddia edilmez. Kanonik araç JSON byte sayısı
model tokenı değildir; yapılandırılmış araç bölümünün token/para maliyeti
dökümü API'den dönmediği için null bırakılır. Eski 14 yanıt toplamı
15272 prompt + 1016 completion = 16288 token, gerçek pacing
160.84493739996105 saniye; para maliyeti doğrulanmadı.

0.3.0 MCP ve temiz GUI ölçümleri gui_mcp_protocol_groq_0_3_0.json içindedir;
eski protokoller üzerine yazılmaz. Güncel sonuç yukarıdaki ajan raporunda ve
GUI_MCP_TEMIZ_RAPOR.md içinde ayrı skorlarla gösterilir. Gerçek sıra MCP önce,
GUI sonradır. İnsan destekli akış ve farklı süre/usage kapsamları korunur.

## İleride ayrı kullanıcı koşusu yapılırsa

Anahtar yalnız kullanıcının yeni terminalinde tanımlanır. Önce hazırlık
(API çağırmaz), kullanıcı seçerse ayrı yeni preflight:

```powershell
.\.release-venv\Scripts\python.exe scripts/evaluate_agent.py --provider groq
.\.release-venv\Scripts\python.exe scripts/evaluate_agent.py --provider groq --preflight --run --min-interval-seconds 20
```

Başarılı yeni preflight'ın yazdırdığı **yeni** klasörle devam:

```powershell
.\.release-venv\Scripts\python.exe scripts/evaluate_agent.py --provider groq --run --resume 'reports/agent_runs/YENI_0_3_0_KLASORU' --min-interval-seconds 20
```

Eski 20261019_112450_630916 klasörü resume edilmez. 20 saniye aralık kota
garantisi değildir; otomatik retry yok, 429'da açık durma/resume korunur.
