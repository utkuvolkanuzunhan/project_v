# Tek görsel üretir ve süresini ölçer. Kullanım:
#   uret.ps1 -Istem "..." -Tohum 7 -Genislik 1024 -Yukseklik 1024 -Onek deneme
param(
    [Parameter(Mandatory)][string]$Istem,
    [int]$Tohum = 1,
    [int]$Genislik = 1024,
    [int]$Yukseklik = 1024,
    [string]$Onek = "deneme"
)
$kok = Split-Path $PSScriptRoot -Parent
$sunucu = "http://127.0.0.1:8188"
$akis = Get-Content -LiteralPath "$PSScriptRoot\klein_hizli.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$akis.'4'.inputs.text = $Istem
$akis.'10'.inputs.noise_seed = $Tohum
$akis.'8'.inputs.width = $Genislik;  $akis.'8'.inputs.height = $Yukseklik
$akis.'9'.inputs.width = $Genislik;  $akis.'9'.inputs.height = $Yukseklik
$akis.'13'.inputs.filename_prefix = $Onek
$govde = @{ prompt = $akis } | ConvertTo-Json -Depth 12 -Compress
$sw = [Diagnostics.Stopwatch]::StartNew()
$yanit = Invoke-RestMethod "$sunucu/prompt" -Method Post -ContentType "application/json; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes($govde))
$id = $yanit.prompt_id
while ($true) {
    $h = Invoke-RestMethod "$sunucu/history/$id"
    if ($h.PSObject.Properties.Name -contains $id) { break }
    Start-Sleep -Milliseconds 500
}
$sonuc = $h.$id
if ($sonuc.status.status_str -ne "success") { "HATA: $($sonuc.status | ConvertTo-Json -Depth 6 -Compress)"; exit 1 }
$dosya = $sonuc.outputs.'13'.images[0]
"süre_sn=$([math]::Round($sw.Elapsed.TotalSeconds,1)) dosya=$($dosya.filename)"
