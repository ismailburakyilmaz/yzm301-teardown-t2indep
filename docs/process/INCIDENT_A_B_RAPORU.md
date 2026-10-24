# A/B kanıt raporu — 22 Ekim 2026

A ve B tamamlandı. Eski yazım oturumu yeniden başlatılmadı, kapatılmadı veya arşivlenmedi. C başlatılmadı; bu rapor kullanıcı incelemesine sunuluyor. Motor, sayısal kaynaklar, SPEC, testler, toleranslar ve oracle beklentileri değiştirilmedi.

## A — okuma ve kapsam

- Dosya: `C:\Users\Burak\Documents\Codex\GPOWER_YAZIM\SPEC_QUESTIONS.md`.
- SHA-256: `26c43d8d27ab88d6d03e6ebcb809c93ded4bccfa2567d44a43847452a2c05e4a`.
- İşlem: `Get-Content SPEC_QUESTIONS.md -Tail 75`.
- Komut aralığı: **22 Ekim 2026, 13:40:16.114–13:40:17.202, Türkiye saati**. Tekil dosya okuma anı ayrıca araçlandırılmadı.
- Amaç: README/rapor/paket kapanışı için mevcut açık soruları gözden geçirmek. Kendi repo dosyasındaki eski 1.0.3 deney teşhisleriyle karşılaşıldı.

Dosyanın şu anki hash değeri, olaydan önce üretilmiş kaynak ZIP’indeki aynı dosyayla eşleşiyor. Okuma anında ayrıca hash alınmış gibi bir iddiada bulunulmuyor. Kayıtlı araç çağrısı ve süreç zamanları kendi yazım oturumunun JSONL kaydından doğrulandı; tüm ham konuşma veya düşünce içeriği dışa aktarılmadı. Yeni Ghidra/decompile dosyası açıldığına ilişkin bir bulgu yok. Bu, ders yürütücüsü adına temiz oda uygunluğu kararı değildir.

## Okumadan sonraki değişiklikler ve diff

Okumadan sonraki kayıtlı yazımlar ile bugün hâlâ mevcut dosyaların zaman bilgileri ayrı denetlendi. B ekleri öncesinde **10 dosya** saptandı: 7 kalıcı dosya ve 3 çalışma/önbellek dosyası.

| Dosya (yazım repo’suna göre) | Değişiklik / diff durumu |
|---|---|

| `STATUS.md` | Durdurma özeti ve gerçek test sayıları eklendi; başlangıç planı korundu. Kayıtlı iki yama tersine uygulanarak metinsel ön görüntü ve diff üretildi; bu, okuma anının özgün bayt snapshot’ı değildir. |

| `HALLUCINATIONS_YAZIM.md` | Önceki kayıtlara 636 bayt olay/test düzeltme notu eklendi; önceki baytlar aynı. |

| `AGENT_COST_YAZIM.md` | Önceki kayıtlara 555 bayt süre/maliyet kapsam notu eklendi; önceki baytlar aynı. |

| `reports/spec_1_1_0/CLEAN_ROOM_INCIDENT.json` | Yeni olay/durdurma kaydı. |

| `reports/spec_1_1_0/current_stdout.txt` | Okumadan önce başlamış test koşusunun tamamlanan çıktısı; okuma anı ön görüntüsü yok, tam diff verilemiyor. |

| `reports/spec_1_1_0/current_junit.xml` | Aynı koşunun yeni gerçek JUnit sonucu. |

| `reports/spec_1_1_0/current_run.json` | Aynı koşunun yeni makbuzu. |

| `.pytest_cache/v/cache/lastfailed` | Test önbelleği; okuma anı ön görüntüsü yok. |

| `.pytest_cache/v/cache/nodeids` | Test önbelleği; okuma anı ön görüntüsü yok. |

| `.tmp/pytest_spec110_current/test_ac110_112_real_public_mcp0/public_wire.jsonl` | Gerçek yerel MCP testi kaydı; 25 araç çağrısı doğrulandı. |

Tam yollar, zamanlar ve her dosyanın SHA-256 değeri: [dosya envanteri](<C:\Users\Burak\Documents\Codex\2026-10-18\bu-k\outputs\INCELEME_KONTROLU\INCIDENT_REVIEW_20261022\POST_READ_FILE_INVENTORY.csv>). Kayıtlı yazım işlemleri: [seçilmiş araç işlemleri](<C:\Users\Burak\Documents\Codex\2026-10-18\bu-k\outputs\INCELEME_KONTROLU\INCIDENT_REVIEW_20261022\POST_READ_TOOL_OPERATIONS.json>). Belge farkları: [diff dizini](<C:\Users\Burak\Documents\Codex\2026-10-18\bu-k\outputs\INCELEME_KONTROLU\INCIDENT_REVIEW_20261022\diffs>).

**Sınır:** Git deposu ve bütün dosya sisteminin okuma anı snapshot’ı yok. Bu nedenle silinmiş/geçici veya sonradan geri alınmış tüm yazımların eksiksiz listesi ve her dosyanın bayt düzeyinde öncesi/sonrası diff’i üretilemez. Kayıtlı işlemlerde kaynak kod düzenlemesi bulunmaması ve tarihî kaynak hash’lerinin aynı olması gösteriliyor; bunun ötesinde mutlak bir yokluk kanıtı iddia edilmiyor.

## Sayısal kaynaklar

- `src/independent_t/engine.py`: `439e43df7464de82d192c69d87d5e3b0c1230ca953bf0645346675f91d20838c`.
- `src/independent_t/contract.py`: `efcfc95beab44247e76836591e5dffc74b03cd49f9459e24975cda66de3ba357`.

Her iki dosya da SPEC 1.0.4 öncesi `reports/history/before_spec_1_0_4/protected_files.json`, SPEC 1.1.0 öncesi `reports/history/before_spec_1_1_0/snapshot_manifest.json`, bu dizindeki saklanmış kaynak dosyaları ve koordinatörün aktarım öncesi hash kayıtlarıyla aynı. Sayısal yol kendi kodumuzda bu iki dosyada; dış dağılım hesabı SciPy’dedir. `requirements.lock.txt` de aktarım öncesi kayıtla aynı; bu denetim dış kütüphanelerin tarihî kurulum baytlarını ayrıca karşılaştırdığı iddiasında değildir.

Aktif SPEC 1.1.0 iki tarafta eşit: `016233430d0f4337c8d1de36a51747654fea31da2448a0798e17c47217cccdbe`.

## ZIP / wheel / sdist denetimi

Son yayımlanmış üç arşiv **0.3.0 / SPEC 1.0.4** içindir. Üçünde de hem yol adı hem mevcut deney dosyalarının tam içerik hash’leriyle taramada `experiments/spec_1_0_3/` içeriği bulunmadı. Tarihî arşivler değiştirilmedi.

| Arşiv | SHA-256 |
|---|---|

| [source_zip](<C:\Users\Burak\Documents\Codex\GPOWER_YAZIM\deliverables\20261022_021423_397032\independent-t-power-0.3.0-spec1.0.4.zip>) | `57e5b93fb7e88c4b5a39a6dc39489b274b5f60a1d85ffbf49face9e943c11dff` |

| [wheel](<C:\Users\Burak\Documents\Codex\GPOWER_YAZIM\deliverables\20261022_021423_397032\python_dist\independent_t_power-0.3.0-py3-none-any.whl>) | `c40852fad4fbeb4e63b6044221116ff00c2a2af3dbeadf9878173da29cd0d791` |

| [sdist](<C:\Users\Burak\Documents\Codex\GPOWER_YAZIM\deliverables\20261022_021423_397032\python_dist\independent_t_power-0.3.0.tar.gz>) | `4a02f35d2b4a083257662264143905226d3fcdf21e339ae334419ff356784c0f` |

**Ek risk:** kaynak ZIP’inde kökte bir `SPEC_QUESTIONS.md` ve 7 tarihî kopyası bulunuyor; bunların bir kısmı eski deney teşhisleri içeriyor. Wheel/sdist’te bu dosya yok. Dolayısıyla “deney modülü hariç” sonucu bütün kaynak ZIP’inin temiz olduğu anlamına gelmez. Yeni kapanışta bu teşhis dosyaları teslim kapsamından ayrılmalı. Henüz 1.1.0 / 0.4.0 nihai arşivi yok; gelecekteki pakete bu denetimden onay verilmedi.

## SPEC 1.1.0 arayüzünün gerçek durumu

- CLI/MCP adaptörü uygulanmış ve gerçek yerel süreçlerle sınanmış durumda. Erken `UNSUPPORTED` geçidi ve işaretli post hoc grup sayıları dahil ek davranış denetimleri **18/18**.

- CONTRACT açık vektörlerinde gerçek CLI–MCP eşdeğerliği **25/25**. Yazım koşusunun yerel MCP wire kaydındaki 25 çağrı ayrıca bağımsız çağrılarla eşleştirildi. Yeni model/API çağrısı yapılmadı.

- Önceki 139 sözleşme testi, saklanmış özgün test kimlikleri ve kaynaklarıyla **139/139**. Bu, tüm eski arayüz beklentilerinin yeni arayüzde değişmeden kaldığı iddiası değildir; yeni sözleşmenin farkları ayrı test ediliyor.

- Gerçek tam koşu: **2167/2269 geçti; 102 başarısız; 0 hata; 0 atlanan**. Güncel JUnit’in test kimlikleri ve sonuçları koordinatörün bağımsız JUnit’iyle birebir aynı. 102 başarısızlık: 13 sıkı oracle + 11 yeni resmî sayısal karşılaştırma + 78 statsmodels. 11 yeni karşılaştırma mevcut sayısal sapmalara ait; sayılar gizlenmedi, xfail uygulanmadı.

- Gerçek `--version`: `{"contract_version": "1.0.0", "name": "Takim 20 - Ismail Burak Yilmaz", "engine": "Python 3.14.8"}`; çıkış 0, stdout ASCII güvenli.

- Yazım tarafının 12 CLI ölçümü: en yüksek **1.219214 sn**, 2 saniyeyi geçen yok. Koordinatörün 12 hedef ölçümünde en yüksek **0.885320 sn**; bütün 56 ölçülmüş CLI çağrısında en yüksek **0.919772 sn**. Bunlar ölçülmüş örneklerin sonucudur; her olası girdiye süre garantisi değildir.

- README’nin son sürüme getirilmesi, kalıcı rapor/manifest ve 0.4.0 paket kapanışı tamamlanmadı. Mevcut README’nin 1.0.4/0.3.0 bilgileri final kabul edilmedi.

Kanıtlar: [gerçek JUnit](<C:\Users\Burak\Documents\Codex\GPOWER_YAZIM\reports\spec_1_1_0\current_junit.xml>), [koşu makbuzu](<C:\Users\Burak\Documents\Codex\GPOWER_YAZIM\reports\spec_1_1_0\current_run.json>), [bağımsız çalışma denetimi](<C:\Users\Burak\Documents\Codex\2026-10-18\bu-k\outputs\INCELEME_KONTROLU\SPEC_1_1_0_AKTARIM_20261022_032855_172708\INDEPENDENT_RUNTIME_REVIEW.json>), [son karşılaştırma](<C:\Users\Burak\Documents\Codex\2026-10-18\bu-k\outputs\INCELEME_KONTROLU\INCIDENT_REVIEW_20261022\FINAL_INDEPENDENT_CHECK.json>).

## B — yalnız eklenen süreç kayıtları

2026-10-22T14:56:24+03:00 tarihinde koordinatör, [süreç günlüğü](<C:\Users\Burak\Documents\Codex\GPOWER_YAZIM\docs\CLEAN_ROOM_SCOPE.md>) ve [HALLUCINATIONS_YAZIM](<C:\Users\Burak\Documents\Codex\GPOWER_YAZIM\HALLUCINATIONS_YAZIM.md>) sonuna olayın doğrulanmış ek kaydını yazdı. Okunan dosya, zaman aralığı, amaç, sınırla neden bağdaşmadığı, değişmeyen kaynak hash’leri, gerçek test sonucu ve geçmişsiz kapanış kararı kaydedildi. Eski olay notu dahil hiçbir önceki kayıt değiştirilmedi.

İki dosyanın eski baytları tam önek olarak korundu; yalnız sırasıyla 2352 ve 2397 bayt eklendi. B sırasında **118 kaynak/test/betik/fixture/SPEC/kurulum dosyasının** hash’leri önce/sonra aynı. B’nin bu iki belge eki, A tablosundaki eski oturum değişikliklerinden ayrı işlemlerdir. [B makbuzu ve hash’ler](<C:\Users\Burak\Documents\Codex\2026-10-18\bu-k\outputs\INCELEME_KONTROLU\INCIDENT_REVIEW_20261022\PHASE_B_RECEIPT.json>).

## C — henüz başlatılmadı

Kullanıcı A/B sonucunu gördükten sonra başlatılacak geçmişsiz kapanış oturumunun kapsamı yalnız SPEC 1.1.0 ile repo içindeki güvenli README/rapor/test çıktılarıdır. `experiments/`, eski deney teşhisleri, `SPEC_QUESTIONS.md` ve inceleme dosyaları okunmayacak. Yalnız README/rapor/paket kapanışı yapılacak; kod, motor, test ve beklentiler değiştirilmeyecek. Test tekrarı gerekirse gerçek sonuç korunacak. Önceden bu içeriği görmüş eski yazım oturumu yeni kapanış için kullanılmayacak.
