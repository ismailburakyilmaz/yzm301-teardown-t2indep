# Kaynaklar ve doğrulama sınırları
Hazırlama tarihi: 18 Ekim 2026.

## Birincil görev kaynağı
Kullanıcının paylaştığı YZM301 Teardown Sprint ödev metni: bu klasördeki ODEV_METNI.txt. Puanlar, iki oturum şartı, CLI örneği, oracle sayısı ve teslim kuralları buradan alınmıştır.

Kullanıcının netleştirdiği kararlar: büyük olasılıkla tek kişilik takım; atanan aile iki bağımsız ortalama t testi; bonus yapma isteği; uygulama ortamı Codex veya Claude Code olabilir; kurulumu kullanıcı yapıyor.

## Prompt hazırlama kaynağı
[OpenAI — Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex)

Bu kaynaktaki açık hedef, dosyada tutulan çalışma bağlamı, aşama bazlı kabul koşulları ve doğrulama yaklaşımından yararlanıldı. Ürünler arası performans karşılaştırması yapılmadı. Promptlar ürünün özel bir komutuna veya seçili model adına bağlı değildir; mevcut araçların gerçekten bulunduğu başlangıçta kontrol edilir.

## Yerel REA bilgisi
Kurulu reverse-engineer-anything becerisi, sürüm 42, okundu. REA binary_session kontrolünde sunucu rea-agents 6.5.0 ve 207 araç bildirdi. Ghidra adayı “not_configured” durumundaydı; GHIDRA_INSTALL_DIR ile Ghidra 12.1.x konumu isteniyordu. Bunlar kontrol anındaki yerel bulgulardır; kullanıcı kurulum yaptıktan sonra yeniden doğrulanmalıdır.

Ghidra'nın hedef üzerinde çalıştığı, Java sürümü uyumluluğu veya G*Power dosya kimliği bu hazırlık sırasında doğrulanmadı.

## Proje tercihlerimiz
36 referans hedefi, Python/SciPy/pytest başlangıç tercihi, PowerBridge geçici adı, tek dosyalık SPEC veri aktarımı, ayrı çalışma klasörleri ve 4 ek zorlayıcı ajan sorusu proje önerileridir. Bunlar öğretim elemanının ek zorunluluğu diye sunulmaz.

## Henüz doğrulanmayanlar
- CONTRACT.md'nin tamamı. Teslim tarihi kullanıcı tarafından 23 Ekim 2026 Cuma 23.59 Türkiye saati olarak kesinleştirildi.
- Hedefin gerçek sürümü/hash'i.
- t2-indep iç formülleri, yuvarlama, oran dağıtımı ve limit davranışı.
- Herhangi bir referans sonuç, sayısal uyum veya token tasarrufu.
- Gizli test başarısı.
- Kodun, MCP'nin veya ajanın çalışması.

Bu paket hiçbirini kanıtlanmış gibi sunmaz. Bunlar iki çalışma oturumunun görevleridir.

## Sürüm 1.1 kullanıcı bilgileri
Kullanıcı G*Power için `C:\Users\Burak\Desktop\GPower_3.1.9.7_143\GPowerNT.exe`, Ghidra başlatıcısı için `C:\Users\Burak\Desktop\ghidra_12.1.4_PUBLIC\ghidraRun.bat` yollarını verdi. Her iki dosyanın varlığı kontrol edildi; bu güncellemede programlar çalıştırılmadı ve binary analizi yapılmadı. CONTRACT.md'nin elde olmadığı teyit edildi. Prompt ve çalışma takvimi buna göre güncellendi.

