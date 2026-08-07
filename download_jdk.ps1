$url = "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.2%2B13/OpenJDK21U-jdk_x64_windows_hotspot_21.0.2_13.zip"
$output = "$env:TEMP\jdk21.zip"
$target = "C:\Users\vinod kumar\.jdk21"

Write-Host "Downloading OpenJDK 21 for Android Gradle compilation..."
Invoke-WebRequest -Uri $url -OutFile $output
Write-Host "Extracting to $target..."
if (-not (Test-Path $target)) { New-Item -ItemType Directory -Path $target }
Expand-Archive -Path $output -DestinationPath $target -Force
Write-Host "JDK 21 setup complete!"
