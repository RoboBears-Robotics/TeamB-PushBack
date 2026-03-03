$ErrorActionPreference = 'Stop'

$watchDir = (Get-Location).Path
Write-Host "Monitoring folder for a single modification: $watchDir"
Write-Host "Press Ctrl+C to stop."

# Get initial last write times
$lastWriteTimes = @{}
$files = Get-ChildItem -LiteralPath $watchDir -Filter "*.v5python" -File
foreach ($file in $files) {
    $lastWriteTimes[$file.FullName] = $file.LastWriteTime
}

function Wait-FileReady($filePath) {
    for ($i=0; $i -lt 30; $i++) {
        try {
            $stream = [System.IO.File]::Open($filePath, 'Open', 'ReadWrite', 'None')
            $stream.Close()
            return $true
        } catch {
            Start-Sleep -Milliseconds 200
        }
    }
    return $false
}

function Wait-ForVEXExit {
    $vexProcesses = Get-Process -Name "VEXcode V5" -ErrorAction SilentlyContinue
    if ($vexProcesses) {
        Write-Host "Detected running VEXcode V5.exe processes. Waiting for them to exit..."
        Wait-Process -Id $vexProcesses.Id
        Write-Host "All VEXcode V5.exe processes have exited."
    }
}

# Infinite loop until a modification is detected
while ($true) {

    $files = Get-ChildItem -LiteralPath $watchDir -Filter "*.v5python" -File

    foreach ($file in $files) {

        $filePath = $file.FullName
        $currentWrite = $file.LastWriteTime

        if (-not $lastWriteTimes.ContainsKey($filePath)) {
            $lastWriteTimes[$filePath] = $currentWrite
            continue
        }

        if ($lastWriteTimes[$filePath] -ne $currentWrite) {

            Write-Host "Detected modification: $filePath"

            # Wait until the file is ready
            if (-not (Wait-FileReady $filePath)) {
                Write-Host "Skipped (file locked): $filePath"
                exit 1
            }

            # Wait for VEXcode to exit
            Wait-ForVEXExit

            # Run Python conversion once
            Write-Host "Running Python script on: $filePath"
            Start-Process -FilePath "python" `
                          -ArgumentList @("convert_v5python.py", $filePath) `
                          -Wait -NoNewWindow

            Write-Host "Done. Exiting."
            exit 0
        }
    }

    Start-Sleep -Milliseconds 500
}