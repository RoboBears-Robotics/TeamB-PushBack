$folder = "C:\Users\robobears\Documents\Github\TeamB-PushBack"
$script = "C:\Users\robobears\Documents\Github\TeamB-PushBack\convert_v5python.py"

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $folder
$watcher.EnableRaisingEvents = $true

$action = {
    $file = $Event.SourceEventArgs.FullPath
    python $script $file
}

Register-ObjectEvent $watcher "Changed" -Action $action

Write-Host "Watching $folder... Press Ctrl+C to stop."
while ($true) { Start-Sleep 1 }