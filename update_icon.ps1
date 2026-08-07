$src = "C:\Users\vinod kumar\.gemini\antigravity\brain\5d91328b-235e-4c12-8a83-4d05535f9916\skysense_app_icon_1784728843723.jpg"
$res = "C:\Users\vinod kumar\OneDrive\Documents\PDD\web\android\app\src\main\res"

Get-ChildItem -Path $res -Directory -Filter "mipmap-*" | ForEach-Object {
    $target1 = Join-Path $_.FullName "ic_launcher.png"
    $target2 = Join-Path $_.FullName "ic_launcher_round.png"
    Copy-Item -Path $src -Destination $target1 -Force
    Copy-Item -Path $src -Destination $target2 -Force
    Write-Host "Updated app icon in: "$_.Name
}
