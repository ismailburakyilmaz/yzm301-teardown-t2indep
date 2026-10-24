# Ayrı statsmodels karşılaştırması

Seed: `20261018`. **552/630** karşılaştırma geçti.
Ana 600 girdide **522/600**, özel 30 girdide **30/30**. Pozitif etki büyüklüğü olarak belgelenen API alanındaki geçen karşılaştırma sayısı **546**. Özel setteki 6 d=0 öğesi belgelenen pozitif etki alanı dışında keşif probudur; 501 geçerli karşılaştırma şartına dayanılmaz.
Durum sayıları: `{"library_convergence_warning": 5, "library_nonfinite": 55, "library_root_residual": 18, "passed": 552}`. NaN/Infinity JSON dosyasında null; durum alanı nedeni korur. Geçerli girdilerden kütüphane sonlu sonuç üretmezse karşılaştırma başarılı sayılmaz. Çözücü sonuçlarında hedef güç kalanı ayrıca kaydedilir; yanlış kökler motor hatası diye etiketlenmez.
Bu veri G*Power oracle verisi değildir. İki uygulama SciPy dağılımlarını paylaştığından bağımsız sayısal oracle sayılmaz.

600 ana girdi: 300 a priori, 300 post hoc. Her modda 150 tek/150 iki yönlü ve 150 negatif/150 pozitif d.
d büyüklüğü log-uniform [0.05,2]; alpha seçimi {1e-7,1e-4,0.001,0.01,0.05,0.1,0.25}. A priori güç uniform [0.6,0.99], ratio log-uniform [0.01,100]. Post hoc n1 tamsayı [1,1000], n2=max(1,round(n1*log-uniform[0.01,100])); N≥3 korunur. Gerçek girdiler extra_inputs.json içinde sabittir.
Ayrı 30 girdi: alpha={0.5,0.75,0.9999999}, tails={1,2}, d={-20,-0.5,0,0.5,20}, n1=20,n2=37.

## Parametre eşleme

Resmî statsmodels API: effect_size ortalama farkı/SD; nobs2=nobs1*ratio; pooled df=N−2. API pozitif effect_size belgeler. SPEC d işaretinde güç değişmez olduğundan karşılaştırma abs(d) ile yönü normalize eder: tek yön için larger, iki yön için two-sided. Negatif d ile larger gelişigüzel kullanılmaz. α≥0.5 ve sıfır/negatif d alt grupları aşağıda ayrı gösterilir.
A priori solve_power yalnız doğrulama kodunda kullanılır: sürekli n1 ve N ayrı saklanır. Bu N, RULE-010 uyarınca üst çift tamsayıya, ardından RULE-011 ile gruplara dönüştürülür. Motorun tamsayı gruplardaki gücü, statsmodels’a gerçekleşen n2/n1 oranıyla tekrar hesaplatılır. Sürekli N ile tamsayı N doğrudan eşit sayılmaz.
Kütüphane çapraz kontrol güç eşiği 1e-10; bu eşik G*Power toleranslarını değiştirmez. N projeksiyonu tam eşitliktir.
A priori kök kalanı ≤1e-6, sonlu sonuçlar ve başarısız yakınsama uyarısı bulunmaması da başarı kararının parçasıdır.

| Alt grup | Geçen / toplam | Sonlu olmayan | Kök hatası | Yakınsama uyarısı | En büyük sonlu güç farkı |
|---|---|---|---|---|---|
| a-priori/tails=1/d<0/alpha<0.5 | 74/75 | 0 | 0 | 1 | 3.83934e-11 |
| a-priori/tails=1/d>0/alpha<0.5 | 74/75 | 0 | 0 | 1 | 3.89371e-11 |
| a-priori/tails=2/d<0/alpha<0.5 | 55/75 | 13 | 5 | 2 | 3.86582e-11 |
| a-priori/tails=2/d>0/alpha<0.5 | 48/75 | 13 | 13 | 1 | 4.08034e-11 |
| post-hoc/tails=1/d<0/alpha<0.5 | 75/75 | 0 | 0 | 0 | 3.23419e-14 |
| post-hoc/tails=1/d<0/alpha>=0.5 | 6/6 | 0 | 0 | 0 | 0 |
| post-hoc/tails=1/d=0/alpha>=0.5 | 3/3 | 0 | 0 | 0 | 4.51639e-12 |
| post-hoc/tails=1/d>0/alpha<0.5 | 74/75 | 1 | 0 | 0 | 3.77836e-11 |
| post-hoc/tails=1/d>0/alpha>=0.5 | 6/6 | 0 | 0 | 0 | 0 |
| post-hoc/tails=2/d<0/alpha<0.5 | 61/75 | 14 | 0 | 0 | 2.13993e-11 |
| post-hoc/tails=2/d<0/alpha>=0.5 | 6/6 | 0 | 0 | 0 | 1.70541e-12 |
| post-hoc/tails=2/d=0/alpha>=0.5 | 3/3 | 0 | 0 | 0 | 9.03277e-12 |
| post-hoc/tails=2/d>0/alpha<0.5 | 61/75 | 14 | 0 | 0 | 2.36323e-11 |
| post-hoc/tails=2/d>0/alpha>=0.5 | 6/6 | 0 | 0 | 0 | 1.70541e-12 |

## Tek çağrıya indirgenmiş kütüphane sorunları

library_nonfinite: `EX-008`. Girdi: `{"test": "t2-indep", "mode": "a-priori", "tails": 2, "d": -1.2868876470598902, "alpha": 1e-07, "power": 0.8658356970039598, "ratio": 5.593834160589138}`. Gözlenen ayrıntılar statsmodels_results.json içindeki aynı kimlikte bulunur.
library_root_residual: `EX-004`. Girdi: `{"test": "t2-indep", "mode": "a-priori", "tails": 2, "d": -1.1535551055197093, "alpha": 0.0001, "power": 0.8853474774992018, "ratio": 1.076800715080703}`. Gözlenen ayrıntılar statsmodels_results.json içindeki aynı kimlikte bulunur.

Tüm girdiler/sonuçlar ve kesirli N değerleri statsmodels_results.json dosyasında. Resmî belge bağlantıları SOURCES.md içinde; kullanılan sürüm statsmodels 0.15.0.
