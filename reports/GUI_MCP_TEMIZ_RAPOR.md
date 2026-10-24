# GUI–MCP ölçüm raporu — 10 soru

Model: `qwen/qwen3.8-27b`. Aynı 10 SPEC1.0.1 sorusu,19 Ekim 2026. Önce MCP, sonra GUI ölçüldü. Sonuçlar geliştirmede görülmüş sorulara aittir.

Son örneklem yanıtları iki yolda da 10/10 doğru. GUI yolunda AG-01 ve AG-05 ek açıklama/düzeltme gerektirdi; AG-10 teknik kota reddinden sonra tekrarlandı. Bu sonuç yardımsız ilk denemede %100 başarı anlamına gelmez.

| Ölçüm | GUI | MCP |
|---|---:|---:|
| Son N yanıtı (belgeli düzeltmeler sonrası) |10/10|10/10|
| İlk teknik iş akışı: doğru çekirdek test/girdi, gerçek çalıştırma, doğru N; düzeltme/teknik tekrar olmadan |7/10|10/10|
| İlk alınan model yanıtında çekirdek test/girdi planı |8/10|10/10|
| GUI ekrandaki yedi sayısal alanın doğruluğu |60/70|GUI okuması yok|
| Bildirilmiş toplam model token’ı |64,753|13,356|
| Gerçek API isteği |25|10|
| Kullanımı bildirilmemiş ret |2 (413,429)|0|
| Para maliyeti |Ölçülmedi|Ölçülmedi|

İlk teknik iş akışı ölçütü protokoldeki doğru test/girdi+gerçek çalıştırma+doğru N koşulunu, teknik hataları ve yardımları gizlemeden uygular. GUI 7/10 bir sistem/iş akışı sonucudur; yakalama ve kota sorunları yalnız model kalitesine yüklenemez. Tam otonom GUI kontrolü kanıtlanmadı; fare/klavye işlemlerini insan yaptı.

| Soru | n1 | n2 | N | GUI sayısal okuma | Belgeli durum | GUI bildirilen token | MCP token |
|---|---:|---:|---:|---:|---|---:|---:|
|AG-01|105|105|210|6/7|yardımlı düzeltme; teknik ret/yeniden başlatma; yanlış: ncp|10174|1347|
|AG-02|88|88|176|7/7|sayısal değerler doğru|5739|1331|
|AG-03|26|26|52|6/7|yanlış: actual_power|5897|1332|
|AG-04|310|310|620|6/7|yanlış: critical|5795|1333|
|AG-05|121|121|242|7/7|yardımlı düzeltme|8063|1329|
|AG-06|161|161|322|5/7|yanlış: ncp; okunamadı: critical|5539|1327|
|AG-07|48|96|144|7/7|sayısal değerler doğru|5794|1338|
|AG-08|72|216|288|6/7|yanlış: ncp|5768|1335|
|AG-09|50|74|124|5/7|yanlış: ncp, critical|5923|1354|
|AG-10|43|127|170|5/7|teknik ret/yeniden başlatma; yanlış: ncp, actual_power|6061|1330|

GUI toplamı içinde yanlış uygulama görüntüsüne giden 1993 token korunur. Bu teknik kayıt çıkarıldığında geçerli görüntü zincirlerinde bildirilen toplam 62,760 token vardır. 413 ve 429 için kullanım dönmedi; gerçek toplam ya da fatura tutarı bunlardan hesaplanamaz.

Bu gözlenen süreçlerde MCP, bildirilmiş token toplamında %79.37 daha az kullandı. Bu yalnız bu süreçlerin betimsel oranıdır; parasal tasarruf veya genel/yalnız arayüze bağlanabilen bir verim iddiası değildir.

GUI soru içi süre toplamı 3220.279 saniye; saf API süreleri toplamı 49.110 saniye. Soru içi süre insan, sohbet, koordinasyon ve teknik toparlanmayı içerir. İlk istekten son yanıta toplam takvim aralığı 19707.824 saniyedir ve sorular arasındaki uzun molaları da kapsar.
MCP 10 soru için deneme süreleri toplamı 38.909 saniye, API sağlayıcı süreleri 11.704 saniye ve ayrı kota beklemesi 144.656 saniyedir. Bu farklı süre kapsamlarından genel bir hızlanma oranı çıkarılmadı.

GUI yardımcı alanlarında 9 yanlış sayısal okuma ve 1 açık okuyamama(null) kaydı var. Tüm yedi alanın doğru olduğu sorular AG-02, AG-05 ve AG-07. AG-05 ilk planı hatalıydı; son alanlarının doğru olması ilk hatayı silmez.

Sayısal değerlendirmede critical_t→critical, ncp_delta→ncp ve açık results nesnesi normalleştirildi. Ham model çıktısı değiştirilmedi; istenen düz JSON anahtarlarına uyum ayrı alan olarak korundu. AG-05’te değerlendiricinin ilk görsel transkripsiyonu yanlış çıktı; doğrudan GPower erişilebilirlik metniyle düzeltildi. Eski transkripsiyon ve ara denetim saklandı; model yanıtı değiştirilmedi.

AG-07, AG-08 ve AG-10 model yönergelerinde ek arayüz anlatımı hataları vardı. AG-10’daki gereksiz Determine adımının kullanıcı tarafından uygulanıp uygulanmadığı ölçülmedi. Bu nedenle çekirdek test/girdi doğruluğu tüm arayüz yönergelerinin doğruluğu olarak sunulamaz.

Bu rapor ve GUI_MCP_TEMIZ_OZET.json temiz sayısal/süreç aktarımı içindir. Ekranlar, UIA dökümleri, ilk hatalı yakalama ve ham REA belgeleri inceleme alanında kalır. MCP’nin 4 zorlayıcı sorusu bu 10 soruluk karşılaştırmaya katılmadı; ayrı kayıtta sistem 14/14, ham karar13/14 sonucu değişmedi.


Token toplamları yalnız Groq API makbuzlarını kapsar. Koordinasyonu yapan Codex modelinin token ve para maliyeti ölçülmedi ve bu sayılara dahil değildir. Bu tablo toplam yapay zekâ veya toplam proje maliyeti olarak sunulamaz.
