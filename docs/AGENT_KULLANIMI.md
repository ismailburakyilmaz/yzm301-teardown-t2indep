# Türkçe ajanı çalıştırma

Yerel CLI, MCP ve testler model API anahtarı gerektirmez. Aşağıdaki Türkçe ajan komutu ise gerçek model isteği yapar; bu kapanışta çalıştırılmadı. Tarihî değerlendirme kanıtları README’de bağlıdır.

Groq için yeni anahtarı yalnız kendi PowerShell sürecine tanımlayın; dosyaya veya repoya koymayın:

```powershell
$env:GROQ_API_KEY = [System.Net.NetworkCredential]::new('', (Read-Host 'Groq anahtari' -AsSecureString)).Password
$env:GROQ_MODEL = 'qwen/qwen3.8-27b'
.\.run\.venv\Scripts\t2-power-agent.exe --provider groq "İki bağımsız grup, Cohen d=0.5, alfa=0.05, güç=0.95, iki yönlü ve eşit gruplar. Kaç kişi gerekir?"
```

Model adı projedeki tarihî ölçümün adıdır; sağlayıcıda bugün erişilebilirliği bu kapanışta yeniden sınanmadı. Anahtar ve model erişimi yalnız bu isteği çalıştıracağınızda gereklidir.
