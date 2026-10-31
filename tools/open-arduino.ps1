$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$tools = Join-Path $root '.tools'
$ide = Join-Path $tools 'arduino-1.8.19'
$exe = Join-Path $ide 'arduino.exe'
if (-not (Test-Path $exe)) {
    Expand-Archive -LiteralPath (Join-Path $tools 'arduino-ide-windows.zip') -DestinationPath $tools -Force
}
$portable = Join-Path $ide 'portable'
$tempDir = Join-Path $portable 'tmp'
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
$prefs = Join-Path $portable 'preferences.txt'
if (-not (Test-Path $prefs)) {
    @(
        'board=uno'
        'target_package=arduino'
        'target_platform=avr'
        'update.check=false'
        ('sketchbook.path=' + (Join-Path $portable 'sketchbook').Replace('\','/'))
    ) | Set-Content -LiteralPath $prefs -Encoding ASCII
}
$env:TEMP = $tempDir
$env:TMP = $tempDir
$sketch = Join-Path $root 'firmware\acoustic_levitator\acoustic_levitator.ino'
$process = Start-Process -FilePath $exe -ArgumentList ('"' + $sketch + '"') -WorkingDirectory $ide -PassThru
Start-Sleep -Seconds 10
Get-Process -Name arduino,javaw -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,MainWindowTitle,Path | Format-List
Write-Output ('Launcher PID: ' + $process.Id)
