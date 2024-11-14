while ($true) {
    $cpu = Get-Counter '\Processor(_Total)\% Processor Time'
    $memory = Get-WmiObject Win32_OperatingSystem
    $disk = Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Used -gt 0 }

    Clear-Host
    Write-Output "System Dashboard"
    Write-Output "-----------------"
    Write-Output "CPU Usage: {0:N2} %" -f $cpu.CounterSamples.CookedValue
    Write-Output "Memory Available: {0:N2} MB" -f ($memory.FreePhysicalMemory / 1024)
    Write-Output "Disk Space:"
    foreach ($d in $disk) {
        Write-Output "  Drive {0}: {1:N2} GB free" -f $d.Name, ($d.Free / 1GB)
    }
    Start-Sleep -Seconds 1
}
