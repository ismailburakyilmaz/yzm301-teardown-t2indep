[CmdletBinding()]
param([string]$CliPath, [switch]$Quick, [string]$ReceiptPath)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$demoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if (-not $CliPath) { $CliPath = Join-Path $demoRoot '.run\.venv\Scripts\gpower-clone.exe' }
$CliPath = [IO.Path]::GetFullPath($CliPath)
if (-not (Test-Path -LiteralPath $CliPath -PathType Leaf)) { throw 'Kurulu CLI yok; önce install.ps1 çalıştırın.' }
$demoPython = Join-Path (Split-Path -Parent $CliPath) 'python.exe'
$demoMcpScript = Join-Path $PSScriptRoot 'DEMO_MCP.py'
if (-not (Test-Path -LiteralPath $demoPython -PathType Leaf) -or -not (Test-Path -LiteralPath $demoMcpScript -PathType Leaf)) { throw 'MCP demo istemcisi veya kurulu Python bulunamadı.' }
$demoClock = [Diagnostics.Stopwatch]::StartNew()
$demoCalls = [Collections.Generic.List[object]]::new()
$demoEvents = [Collections.Generic.List[object]]::new()
$demoTyping = [Collections.Generic.List[object]]::new()

function Wait-DemoMoment([double]$Seconds) {
    if ($Quick) { return }
    while ($demoClock.Elapsed.TotalSeconds -lt $Seconds) { Start-Sleep -Milliseconds 50 }
}
function Show-DemoNote([string]$Text, [string]$Color = 'Gray') {
    Write-Host $Text -ForegroundColor $Color
    $demoEvents.Add([pscustomobject]@{ elapsed_seconds=$demoClock.Elapsed.TotalSeconds; text=$Text })
}
function Show-DemoSection([string]$Title, [string]$Question) {
    Clear-Host
    Write-Host 'YZM301 | gpower-clone CLI demo' -ForegroundColor Green
    Show-DemoNote -Text $Title -Color Cyan
    Show-DemoNote -Text ('Soru: ' + $Question)
}
function Show-TypedDemoLine([string]$Text) {
    $typedStart = $demoClock.Elapsed.TotalSeconds
    if ($Quick) { Write-Host $Text -ForegroundColor Cyan }
    else {
        $typingTimer = [Diagnostics.Stopwatch]::StartNew()
        $characterIndex = 0
        foreach ($letter in $Text.ToCharArray()) {
            Write-Host -NoNewline $letter -ForegroundColor Cyan
            $characterIndex++
            $deadlineMs = $characterIndex * 1000.0 / 28.0
            while ($typingTimer.Elapsed.TotalMilliseconds -lt $deadlineMs) { [Threading.Thread]::Sleep(1) }
        }
        $typingTimer.Stop()
        Write-Host ''
    }
    $demoTyping.Add([pscustomobject]@{text=$Text; characters=$Text.Length; started_seconds=$typedStart; finished_seconds=$demoClock.Elapsed.TotalSeconds; display_only=$true})
}
function Show-DemoCommand([string[]]$CliArguments, [int]$ExpectedExit = 0) {
    Write-Host ''
    Show-TypedDemoLine -Text ('PS> gpower-clone ' + ($CliArguments -join ' '))
    $timer = [Diagnostics.Stopwatch]::StartNew()
    $lines = @(& $CliPath @CliArguments)
    $actualExit = $LASTEXITCODE
    $timer.Stop()
    $rawText = $lines -join "`n"
    $value = $rawText | ConvertFrom-Json
    Write-Host $rawText
    if ($ExpectedExit -ne 0 -and $value.PSObject.Properties.Name -contains 'error') { Write-Host ('Hata (Türkçe): ' + $value.error) -ForegroundColor Yellow }
    Write-Host ('Çıkış kodu: ' + $actualExit) -ForegroundColor DarkGray
    if ($actualExit -ne $ExpectedExit) { throw ('Beklenmeyen çıkış: ' + $actualExit) }
    $demoCalls.Add([pscustomobject]@{kind='cli';cli_path=$CliPath;argv=$CliArguments;exit_code=$actualExit;stdout=$rawText;elapsed_seconds=$timer.Elapsed.TotalSeconds})
    return $value
}
function Confirm-DemoOracle([string]$Id, [string[]]$Arguments, $Actual) {
    if (-not $demoOracleById.ContainsKey($Id)) { throw ('Oracle kaydı yok: ' + $Id) }
    $row = $demoOracleById[$Id]
    if ($row.source -ne 'gpower_gui' -or $row.target_version -ne '3.1.9.7' -or $row.mode -ne 'a-priori') { throw 'Beklenmeyen referans kaynağı.' }
    $inputValues = $row.inputs_json | ConvertFrom-Json
    $argMap = @{}
    for ($index=0; $index -lt $Arguments.Count; $index+=2) { $argMap[$Arguments[$index].Substring(2)]=$Arguments[$index+1] }
    $tails = switch ($inputValues.tails) { 'One' {1}; 'Two' {2}; default {throw 'Referans tails tanınmıyor.'} }
    if ($argMap['test'] -ne $row.test -or $argMap['mode'] -ne $row.mode -or [int]$argMap['tails'] -ne $tails) { throw 'Referans ve gerçek çağrının kimliği farklı.' }
    foreach ($field in @('d','alpha','power','ratio')) {
        $expectedInput = [double]::Parse([string]$inputValues.$field,[Globalization.CultureInfo]::InvariantCulture)
        $actualInput = [double]::Parse([string]$argMap[$field],[Globalization.CultureInfo]::InvariantCulture)
        if ($expectedInput -ne $actualInput) { throw ('Referans ve CLI girdisi farklı: '+$field) }
    }
    $expected = $row.expected_json | ConvertFrom-Json
    foreach ($field in @('n1','n2','n_total')) { if ($Actual.$field -ne $expected.$field) { throw ('Referans tahsisi eşleşmiyor: '+$Id+'/'+$field) } }
    $screenshots = @($row.screenshot_paths_json | ConvertFrom-Json)
    $screenshot = [string]$screenshots[0]
    if (-not (Test-Path -LiteralPath (Join-Path -Path $demoRoot -ChildPath $screenshot) -PathType Leaf)) { throw ('Referans ekranı yok: '+$Id) }
    return [pscustomobject]@{id=$Id;reference=$expected;inputs=$inputValues;screenshot=$screenshot}
}

$demoOracleRows = @(Import-Csv -LiteralPath (Join-Path $demoRoot 'oracle\gpower_vectors.csv') -Encoding UTF8)
$demoOracleById = @{}
foreach ($row in $demoOracleRows) { if ($demoOracleById.ContainsKey($row.vector_id)) {throw 'Yinelenen oracle kimliği.'}; $demoOracleById[$row.vector_id]=$row }

Clear-Host
Write-Host 'YZM301 | gpower-clone CLI demo' -ForegroundColor Green
$demoLocalCli = [IO.Path]::GetFullPath((Join-Path $demoRoot '.run\.venv\Scripts\gpower-clone.exe'))
$demoDisplayedCli = if ([string]::Equals($CliPath,$demoLocalCli,[StringComparison]::OrdinalIgnoreCase)) { '.\.run\.venv\Scripts\gpower-clone.exe' } else {$CliPath}
Show-DemoNote -Text ('Çalıştırılan: '+$demoDisplayedCli) -Color DarkGray
Show-DemoNote -Text 'Komutlarda yazma efekti var; ardından gerçekten çalıştırılır. JSON yanıtları canlıdır.' -Color DarkGray

Wait-DemoMoment 3
Show-DemoSection -Title '1. İKİ YÖNLÜ / A PRIORI' -Question 'd=0.5, alfa=%5, güç=%95; eşit iki gruba kaç kişi gerekli?'
$demoApArguments=@('--test','t2-indep','--mode','a-priori','--tails','2','--d','0.5','--alpha','0.05','--power','0.95','--ratio','1')
$demoAp=Show-DemoCommand -CliArguments $demoApArguments
if ($demoAp.n1 -ne 105 -or $demoAp.n2 -ne 105 -or $demoAp.n_total -ne 210) {throw 'İlk örnek doğrulanamadı.'}
$demoFirst=Confirm-DemoOracle -Id 'GP-AP-001' -Arguments $demoApArguments -Actual $demoAp
if ($demoFirst.screenshot -ne 'oracle/screenshots/GP-AP-001_01.png') {throw 'İlk örneğin ekran yolu değişti.'}
Show-DemoNote -Text ('Cevap: '+$demoAp.n1+' + '+$demoAp.n2+' = '+$demoAp.n_total+' kişi. G*Power kaydı da aynı.') -Color Yellow
Show-DemoNote -Text ('Kanıt: '+$demoFirst.screenshot) -Color DarkGray

Wait-DemoMoment 11
Show-DemoSection -Title '2. TEK YÖNLÜ / KILAVUZ ÖRNEĞİ' -Question 'Diğer girdiler aynı, test tek yönlü olursa kaç kişi gerekli?'
$demoSecondArguments=@('--test','t2-indep','--mode','a-priori','--tails','1','--d','0.5','--alpha','0.05','--power','0.95','--ratio','1')
$demoSecondAp=Show-DemoCommand -CliArguments $demoSecondArguments
$demoSecond=Confirm-DemoOracle -Id 'GP-AP-002' -Arguments $demoSecondArguments -Actual $demoSecondAp
foreach ($field in @('d','alpha','power','ratio')) { if ($demoFirst.inputs.$field -ne $demoSecond.inputs.$field) {throw 'Kuyruk dışında değişen girdi var.'} }
Show-DemoNote -Text ('Cevap: '+$demoSecondAp.n1+' + '+$demoSecondAp.n2+' = '+$demoSecondAp.n_total+' kişi. G*Power kaydı da aynı.') -Color Yellow
Show-DemoNote -Text 'Bu, G*Power 3.1 kılavuzundaki örnekle de aynı (docs/KILAVUZ_ORNEKLERI.md).' -Color DarkGray
Show-DemoNote -Text 'Tek yön seçimi hipoteze baştan dayanır; sonuca göre N azaltmak için seçilmez.' -Color DarkGray

Wait-DemoMoment 19
Show-DemoSection -Title '3. EŞİT OLMAYAN GRUPLAR / 2:1' -Question 'Bu örnekte güç=%80 ve n2/n1=2; gruplara kaç kişi gerekli?'
$demoUnequalArguments=@('--test','t2-indep','--mode','a-priori','--tails','2','--d','0.5','--alpha','0.05','--power','0.8','--ratio','2')
$demoUnequalAp=Show-DemoCommand -CliArguments $demoUnequalArguments
$demoUnequal=Confirm-DemoOracle -Id 'GP-AP-007' -Arguments $demoUnequalArguments -Actual $demoUnequalAp
if ($demoUnequalAp.n2 -ne (2*$demoUnequalAp.n1)) {throw '2:1 dağılımı doğrulanamadı.'}
Show-DemoNote -Text ('Cevap: '+$demoUnequalAp.n1+' / '+$demoUnequalAp.n2+' kişi; toplam '+$demoUnequalAp.n_total+'. G*Power da aynı; grup 2 iki kat büyük.') -Color Yellow
Show-DemoNote -Text ('Kanıt: '+$demoUnequal.screenshot) -Color DarkGray

Wait-DemoMoment 27
Show-DemoSection -Title '4. POST HOC / GERİ KONTROL' -Question 'İlk örnekteki 105/105 kişinin gerçekleşen gücü nedir?'
$demoPh=Show-DemoCommand -CliArguments @('--test','t2-indep','--mode','post-hoc','--tails','2','--d','0.5','--alpha','0.05','--n1','105','--n2','105')
if ([Math]::Abs($demoPh.power-$demoAp.actual_power) -gt 1e-12) {throw 'AP/PH güçleri tutarsız.'}
Show-DemoNote -Text ('Cevap: yaklaşık %'+($demoPh.power*100).ToString('F2')+'. İlk a priori hesabıyla tutarlı; post hoc yeni N aramaz.') -Color Yellow

Wait-DemoMoment 34
Show-DemoSection -Title '5. AYNI SORU / GERÇEK YEREL MCP' -Question 'İlk örnek MCP power_analysis aracı üzerinden aynı sonucu verir mi?'
$demoMcpDisplayedPython=if ([string]::Equals($CliPath,$demoLocalCli,[StringComparison]::OrdinalIgnoreCase)) {'.\.run\.venv\Scripts\python.exe'} else {'"'+$demoPython+'"'}
Show-TypedDemoLine -Text ('PS> '+$demoMcpDisplayedPython+' -I .\docs\DEMO_MCP.py')
$demoMcpTimer=[Diagnostics.Stopwatch]::StartNew()
$demoMcpLines=@(& $demoPython -I $demoMcpScript)
$demoMcpExit=$LASTEXITCODE
$demoMcpTimer.Stop()
$demoMcpText=$demoMcpLines -join "`n"
if ($demoMcpExit -ne 0) {throw 'Gerçek MCP çağrısı başarısız.'}
$demoMcp=$demoMcpText | ConvertFrom-Json
Write-Host $demoMcpText
Write-Host ('Çıkış kodu: '+$demoMcpExit) -ForegroundColor DarkGray
if ($demoMcpText -cne $demoCalls[0].stdout) {throw 'MCP ve ilk CLI JSON çıktısı birebir eşleşmiyor.'}
$demoCalls.Add([pscustomobject]@{kind='mcp';python_path=$demoPython;argv=@('-I',$demoMcpScript);tool='power_analysis';exit_code=$demoMcpExit;stdout=$demoMcpText;elapsed_seconds=$demoMcpTimer.Elapsed.TotalSeconds})
Show-DemoNote -Text ('Cevap: '+$demoMcp.n1+'/'+$demoMcp.n2+'/'+$demoMcp.n_total+'; CLI ile JSON birebir aynı. Ayrı yerel sunucu, API/model yok.') -Color Yellow

Wait-DemoMoment 42
Show-DemoSection -Title '6. HATA KONTROLÜ / ARALIK' -Question 'Sözleşmeye aykırı negatif d gönderilirse ne olur?'
$demoInvalid=Show-DemoCommand -ExpectedExit 2 -CliArguments @('--test','t2-indep','--mode','post-hoc','--tails','2','--d','-1','--alpha','0.05','--n1','105','--n2','105')
if ($demoInvalid.code -ne 'OUT_OF_RANGE' -or $demoInvalid.field -ne 'd') {throw 'Aralık hatası doğrulanamadı.'}
Show-DemoNote -Text 'Cevap: OUT_OF_RANGE, field=d, exit 2; hatalı girdi reddedildi.' -Color Yellow

Wait-DemoMoment 49
Show-DemoSection -Title '7. HATA KONTROLÜ / EKSİK ALAN' -Question 'Hedef güç (--power) hiç verilmezse ne olur?'
$demoMissing=Show-DemoCommand -ExpectedExit 2 -CliArguments @('--test','t2-indep','--mode','a-priori','--tails','2','--d','0.5','--alpha','0.05','--ratio','1')
if ($demoMissing.code -ne 'MISSING_PARAM' -or $demoMissing.field -ne 'power') {throw 'Eksik alan hatası doğrulanamadı.'}
Show-DemoNote -Text 'Cevap: MISSING_PARAM, field=power, exit 2; eksik alan açıkça bildirildi.' -Color Yellow

Wait-DemoMoment 55
Show-DemoSection -Title 'DOĞRULAMA KAPSAMI / KAYITLI SONUÇLAR' -Question 'Uyum ve bilinen sınırlamalar nerede?'
$demoTestSummary = Join-Path $demoRoot 'reports\final_submission\test_summary.json'
$demoTests = Get-Content -LiteralPath $demoTestSummary -Raw -Encoding UTF8 | ConvertFrom-Json
$demoDiff = Get-Content -LiteralPath (Join-Path $demoRoot 'reports\spec_1_1_0\differential.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$demoPytest = Get-Content -LiteralPath (Join-Path $demoRoot 'reports\spec_1_1_0\release_0_4_3_20261023\pytest_3_14_summary.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($demoTests.tests -ne $demoPytest.tests -or $demoTests.passed -ne $demoPytest.passed -or $demoTests.failures -ne $demoPytest.failures) { throw 'Tam test kayıtları tutarsız.' }
if (@($demoDiff.records).Count -ne $demoOracleRows.Count) { throw 'Diferansiyel kayıt ve oracle sayıları tutarsız.' }
$demoRegion = @($demoDiff.records | Where-Object {
    if ($_.mode -ne 'a-priori' -or -not $_.contract_numeric_eligible) { return $false }
    if (-not $demoOracleById.ContainsKey($_.id)) { throw 'Diferansiyel kaydın oracle karşılığı yok.' }
    $demoNative = $demoOracleById[$_.id].expected_json | ConvertFrom-Json
    return [long]$demoNative.n_total -le 30000000
})
$demoRegionPassed = @($demoRegion | Where-Object { $_.contract_allocation_passed }).Count
$demoStrictFailures = @($demoPytest.failed_ids | Where-Object { $_ -match '::test_ac107_strict_raw_oracle\[' } | ForEach-Object { [regex]::Match($_, '\[([^\]]+)\]$').Groups[1].Value })
$demoOfficialFailures = @($demoPytest.failed_ids | Where-Object { $_ -match '::test_ac101_102_official_gui_expectation\[' } | ForEach-Object { [regex]::Match($_, '\[([^\]]+)\]$').Groups[1].Value })
$demoSharedFailures = @($demoStrictFailures | Where-Object { $demoOfficialFailures -contains $_ })
$demoBoundaryFailures = @($demoStrictFailures | Where-Object { $demoOfficialFailures -notcontains $_ })
$demoStatsmodelsFailures = @($demoPytest.failed_ids | Where-Object { $_ -match '::test_statsmodels_crosscheck\[' }).Count
if ($demoSharedFailures.Count -ne $demoOfficialFailures.Count -or ($demoStrictFailures.Count + $demoOfficialFailures.Count + $demoStatsmodelsFailures) -ne $demoTests.failures) { throw 'Başarısızlık grupları kayıtlarla açıklanamıyor.' }
foreach ($demoFailedId in $demoSharedFailures) {
    $demoFailedNative = $demoOracleById[$demoFailedId].expected_json | ConvertFrom-Json
    if ([long]$demoFailedNative.n_total -le 30000000) { throw 'Büyük N olarak sınıflanan kayıt eşiği karşılamıyor.' }
}
Show-DemoNote -Text ($demoOracleRows.Count.ToString()+' vektör | CONTRACT alanındaki AP, N ≤ 3·10⁷: '+$demoRegionPassed+'/'+$demoRegion.Count)
Show-DemoNote -Text ($demoTests.tests.ToString()+' test: '+$demoTests.passed+' geçen, '+$demoTests.failures+' başarısız (kayıtlı koşu).')
Show-DemoNote -Text ('Başarısızlık: '+$demoSharedFailures.Count+' büyük N iki ölçütle ('+($demoSharedFailures.Count*2)+'), '+$demoBoundaryFailures.Count+' sınır/alan, '+$demoStatsmodelsFailures+' statsmodels.')
Wait-DemoMoment 58
Show-DemoNote -Text 'Cevap: Kanıtlar README içinde. Gizli test veya tüm çağrılarda 2 s garantisi yok.' -Color DarkGray
Show-DemoNote -Text 'Tam testler bu videoda yeniden koşulmadı. G*Power ürünü değildir.' -Color DarkGray
Wait-DemoMoment 60
$demoClock.Stop()
if ($ReceiptPath) {
    [ordered]@{
        purpose='real_cli_video_demo';quick_mode=[bool]$Quick;elapsed_seconds=$demoClock.Elapsed.TotalSeconds
        cli_path=$CliPath;calls=$demoCalls.ToArray();explanatory_events=$demoEvents.ToArray();typing_events=$demoTyping.ToArray()
        display_animation_only=$true;typing_target_characters_per_second=28.0
        oracle_vector_id=$demoFirst.id;oracle_group_sizes=@($demoAp.n1,$demoAp.n2,$demoAp.n_total);screenshot=$demoFirst.screenshot
        second_oracle_vector_id=$demoSecond.id;second_oracle_group_sizes=@($demoSecondAp.n1,$demoSecondAp.n2,$demoSecondAp.n_total)
        unequal_oracle_vector_id=$demoUnequal.id;unequal_group_sizes=@($demoUnequalAp.n1,$demoUnequalAp.n2,$demoUnequalAp.n_total)
        mcp_equal_to_cli=$true;error_cases=@([ordered]@{code=$demoInvalid.code;field=$demoInvalid.field},[ordered]@{code=$demoMissing.code;field=$demoMissing.field})
        recorded_coverage=[ordered]@{vectors=$demoOracleRows.Count;region_ap_passed=$demoRegionPassed;region_ap_total=$demoRegion.Count;tests=$demoTests.tests;passed=$demoTests.passed;failures=$demoTests.failures;large_n_unique=$demoSharedFailures.Count;large_n_test_failures=($demoSharedFailures.Count*2);extra_boundary_ids=$demoBoundaryFailures;statsmodels_failures=$demoStatsmodelsFailures}
        model_api_used=$false;core_tests_reexecuted=$false;os_disk_cache_cold_claim=$false
    } | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $ReceiptPath -Encoding UTF8
}
