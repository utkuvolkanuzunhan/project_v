# Aynı istemden N görseli TEK çağrıda üretir (batch) ve görsel başına süreyi ölçer.
#   uret_toplu.ps1 -Istem "..." -Adet 4 -Tohum 5 -Genislik 1024 -Yukseklik 1024 -Onek hiz
param(
    [Parameter(Mandatory)][string]$Istem,
    [int]$Adet = 4,
    [int]$Tohum = 1,
    [int]$Genislik = 1024,
    [int]$Yukseklik = 1024,
    [string]$Onek = "hiz"
)
$sunucu = "http://127.0.0.1:8188"
$akis = Get-Content -LiteralPath "$PSScriptRoot\klein_hizli.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$akis.'4'.inputs.text = $Istem
$akis.'10'.inputs.noise_seed = $Tohum
$akis.'8'.inputs.width = $Genislik;  $akis.'8'.inputs.height = $Yukseklik
$akis.'9'.inputs.width = $Genislik;  $akis.'9'.inputs.height = $Yukseklik
$akis.'9'.inputs.batch_size = $Adet
$akis.'13'.inputs.filename_prefix = $Onek
$govde = @{ prompt = $akis } | ConvertTo-Json -Depth 12 -Compress
$sw = [Diagnostics.Stopwatch]::StartNew()
$yanit = Invoke-RestMethod "$sunucu/prompt" -Method Post -ContentType "application/json; charset=utf-8" -Body ([Text.Encoding]::UTF8.GetBytes($govde))
$id = $yanit.prompt_id
while ($true) {
    $h = Invoke-RestMethod "$sunucu/history/$id"
    if ($h.PSObject.Properties.Name -contains $id) { break }
    Start-Sleep -Milliseconds 400
}
$sonuc = $h.$id
if ($sonuc.status.status_str -ne "success") { "HATA: $($sonuc.status | ConvertTo-Json -Depth 6 -Compress)"; exit 1 }
$n = $sonuc.outputs.'13'.images.Count
$toplam = $sw.Elapsed.TotalSeconds
"adet=$n boyut=${Genislik}x$Yukseklik toplam_sn=$([math]::Round($toplam,1)) gorsel_basina_sn=$([math]::Round($toplam/$n,2))"
