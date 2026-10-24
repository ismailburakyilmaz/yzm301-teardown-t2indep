# Teslim kontrolü — 0.4.3

Bu klasör çalışma deposunun bütünü kopyalanmadan açık izin listesiyle oluşturuldu. GitHub’a gönderim veya ders teslimi yapılmadı.

- Python 3.12.15, 3.13.16 ve 3.14.8: her birinde 2280 test; 2178 geçti, aynı 102 başarısız, 0 hata/atlanan.
- Birleşik klasörün kendisinde yeniden tam koşu: **2280 / 2178 geçen / aynı 102 başarısız**. [JUnit](reports/final_submission/submission_junit.xml), [özet](reports/final_submission/test_summary.json).
- Başarısızlıklar: 13 katı oracle, aynı 11 büyük N örneğinin resmî karşılaştırması ve 78 statsmodels sınırı. Bunlar geçiş diye etiketlenmedi; skip/xfail eklenmedi.
- Son kaynak 142 vektörde önceki motorla tam aynı; 25 açık CLI–MCP eşdeğerliği release raporunda. N araması/tahsis/yuvarlama değişmedi.
- Oracle: 142 hesap, 25 girdi gözlemi, 12 ayrı holdout, 167 CONTRACT beklentisi; manifest 213 satır, eksik dosya veya SHA farkı yok.
- Paketlere experiments/, SPEC_QUESTIONS, 1.0.3 deney teşhisleri, hedef exe, API anahtarları, sanal ortamlar alınmadı.

## Korunan ve güncellenen kimlikler

- `SPEC.md`: `016233430d0f4337c8d1de36a51747654fea31da2448a0798e17c47217cccdbe` (korundu).
- `src/independent_t/contract.py`: `efcfc95beab44247e76836591e5dffc74b03cd49f9459e24975cda66de3ba357` (korundu).
- `requirements.lock.txt`: `67a121c8de8c1d69b6599c6bb42c1c0cc6756589a9a1485b7d9fcf54dd7298a8` (korundu).
- `engine.py`: `60d856fefe398633a4561adfa6d6ec48d04cc21cb04655be6cfce2170f52bd48` (onaylı import değişikliği).
- `scalar_distributions.py`: `bd73505472aa41ebf3865af5264b5e97e73ad55c5383f273edbbda31417d0147`.

## Süre ve doğruluk sınırları

Yeni üretim paketi için kurulum hazırlığı ve 20 ayrı süreç ölçümü [ham release serisinde](reports/spec_1_1_0/release_0_4_3_20261023/timing_21.json) bulunur. Ayrı inceleme adayının yeniden başlatma sonrası tek çağrısı 1.7091611 s; [makbuz ve sınırı](reports/performance_candidate/NOTE.md). Yeni üretim sarmalayıcısının yeniden başlatma sonrası ayrı ölçümü yapılmadı. Eski 0.4.2 ölçümündeki 5.9152954 s aşım silinmedi. Her ortamda 2 s garantisi verilmez. Performans değişikliği büyük N farklarını veya gizli test uyumunu düzeltmez.

## Kullanıcıya kalanlar

1. Yaklaşık 60 saniyelik demo videosunu kaydet ve README’deki tek video yer tutucusuna gerçek bağlantıyı ekle.
2. README/AGENT_COST/HALLUCINATIONS belgelerini ve bilinen farkları son kez gözden geçir. AGENT_COST sayıları kayıtlı kesite aittir; sonraki kapanış tokenları ölçülmüş gibi eklenmedi.
3. Onayından sonra yalnız bu birleşik klasörü kendi GitHub deposuna ve dersin istediği teslim kanalına gönder. Çalışma klasörlerini veya inceleme arşivlerini topluca gönderme. Video bağlantısı eklendiğinde belge/paket hash’leri değişir.
