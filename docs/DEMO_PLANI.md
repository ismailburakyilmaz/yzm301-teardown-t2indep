# Açıklamalı ve yazma efektli 60 saniyelik CLI demo

Yönerge: docs/ODEV_METNI.txt, “Demo (60 saniyelik CLI videosu)”. Seslendirme gerekmez. Komutlar yaklaşık 28 karakter/s hızında **yalnız gösterim amacıyla** ekrana yazılır; yazım bittikten sonra gerçek program aynı argümanlarla çağrılır. JSON yanıtları canlıdır; çıktı önceden hazırlanmaz veya harf harf taklit edilmez. Yazma süresi hesap/MCP çağrı süresine katılmaz; ayrı kaydedilir.

## Çalıştırma

Kurulumdan sonra, proje kökünde bir kez hızlı prova:

```powershell
& .\docs\DEMO_CLI.ps1 -Quick
```

Quick yazma efektini ve okuma aralıklarını atlar; gerçek çağrıları ve bütün sonuç kontrollerini yapar. Video kaydı için:

```powershell
& .\docs\DEMO_CLI.ps1
```

CMD'den:

```cmd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\docs\DEMO_CLI.ps1
```

Gerçek CLI teslim klasörünün `.run` kurulumudur; başta `Çalıştırılan: .\.run\.venv\Scripts\gpower-clone.exe` gösterilir. Başlatıcı `-CliPath` vermez. Başka kurulum açıkça seçilirse tam gerçek yol gösterilir. Bölümler arasında ekran temizlenir. Her hesapta tek satırlık soru, gerçek komut/JSON ve tek satırlık cevap vardır; kaynak ve hipotez notları ayrıca gösterilir. Windows Terminal, büyük pencere ve 20–22 pt yazı önerilir.

| Yaklaşık başlangıç | Gösterim |
|---|---|
| 0 s | Genel başlık, gerçek exe ve yazma efektinin yalnız sunum olduğunun açıklaması |
| 3 s | İki yönlü a priori: d=0.5, alfa=0.05, güç=0.95, oran=1 → 105/105/210; GP-AP-001 girdileri/tahsisi CSV'den doğrulanır ve ekran yolu gösterilir |
| 11 s | Yalnız kuyruk değişir: tek yönlü → 88/88/176; GP-AP-002 ve resmî kılavuz notu. Tek yön hipoteze baştan dayanmalıdır |
| 19 s | Ayrı tasarım: iki yönlü, d=0.5, alfa=0.05, güç=0.8, oran=2 → 48/96/144; GP-AP-007 ile karşılaştırma. İlk tasarıma göre hem güç hem oran farklıdır; yalnız oranın etkisiymiş gibi sunulmaz |
| 27 s | İlk tasarım için 105/105 ile post hoc; gerçekleşen güç ilk a priori çıktısıyla doğrulanır |
| 34 s | Aynı ilk soru gerçek yerel MCP power_analysis çağrısıyla; 105/105/210 ve tam CLI JSON'u birebir eşit |
| 42 s | Negatif d → OUT_OF_RANGE/d, exit 2; ham JSON ve çözülmüş Türkçe hata |
| 49 s | Eksik power → MISSING_PARAM/power, exit 2 |
| 55–60 s | Mevcut kayıtlardan 142 vektör, belirtilen AP bölgesinde 75/75; 2280/2178/102 ve 102'nin dağılımı. README ve sınırlamalar |

## Gerçeklik ve sınırlar

Altı gerçek CLI çağrısı ve bir gerçek MCP çağrısı yapılır. docs/DEMO_MCP.py, aynı kurulumun Python yorumlayıcısıyla çalışır; gerçek MCP SDK üzerinden ayrı `independent_t.mcp_server` sürecini stdio ile başlatır, tools/list ve power_analysis çağrısını yapar. Sunucunun gerçek metin JSON'unu yazdırır; ana betik bunu ilk CLI çıktısıyla birebir karşılaştırır. Sunucudan hata gelirse veya eşleşme bozulursa demo durur. Bu bir LLM/Türkçe ajan çağrısı değildir; dış ağ, yeni model/API veya anahtar gerektirmez. Windows sandbox asyncio/socketpair engeli varsa yalnız bu yerel doğrulama için normal terminal veya ayrı araç izni gerekebilir.

Oracle örneklerinin bütün girdileri, n1/n2/N değerleri ve ekran dosyaları doğrulanır. GP-AP-001 için oracle/screenshots/GP-AP-001_01.png yolu korunur. GP-AP-002 kılavuz notu docs/KILAVUZ_ORNEKLERI.md içindedir; yeni GUI ölçümü değildir. Bir referans veya hata uyuşmazlığında demo durur. Üretim motoru, sözleşme, oracle, sayısal beklentiler ve toleranslar değişmez.

142 vektörün hepsinin CLI kapsamına girdiği veya başarılı olduğu söylenmez. 75/75 yalnız belirtilen CONTRACT/AP bölgesidir. Aynı 11 büyük N kaydı iki ölçütte başarısızdır (22 test), buna 2 ek sınır/alan ve 78 statsmodels eklenir. Tam testler videoda tekrar koşulmaz; mevcut raporlar okunur. Gerçek gecikmeler videodan kesilerek gizlenmez. Akış normal ortamda yaklaşık 60 saniyedir; yavaş çağrılar veya MCP başlangıcı bunu aşırabilir. Her ortamda 2 s veya soğuk başlangıç garantisi yoktur.

Videoda kişisel isim veya takım kimliği gösterilmez; gerçek --version çıktısı değiştirilmez ve video akışında çağrılmaz. Kimlik bilgileri README içindedir. Son ekran geldiğinde kaydı durdurun; video bağlantısı README'deki tek yer tutucusuna eklenecek.
