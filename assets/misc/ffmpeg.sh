# Define URLs and paths
$ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
$zipPath = "$env:TEMP\ffmpeg.zip"
$installPath = "C:\ffmpeg"

# Download FFmpeg ZIP
Invoke-WebRequest -Uri $ffmpegUrl -OutFile $zipPath

# Create install directory if it doesn't exist
New-Item -ItemType Directory -Path $installPath -Force | Out-Null

# Unzip the contents
Expand-Archive -Path $zipPath -DestinationPath $installPath -Force

# Move files up if nested
$extractedFolder = Get-ChildItem $installPath | Where-Object {$_.PSIsContainer} | Select-Object -First 1
Move-Item "$($extractedFolder.FullName)\*" $installPath -Force
Remove-Item $extractedFolder.FullName -Recurse -Force

# Add FFmpeg bin directory to system PATH
$ffmpegBin = "$installPath\bin"
$envPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::Machine)

if ($envPath -notlike "*$ffmpegBin*") {
    [Environment]::SetEnvironmentVariable("Path", "$envPath;$ffmpegBin", [EnvironmentVariableTarget]::Machine)
    Write-Output "FFmpeg path added to system PATH. You may need to restart your terminal or PC."
} else {
    Write-Output "FFmpeg path is already in PATH."
}
