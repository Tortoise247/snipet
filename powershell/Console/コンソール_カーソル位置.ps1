# コンソールをクリアする
Clear-Host

$count = 0

# カーソルの初期位置を取得する
$pos_org = $host.ui.rawui.CursorPosition

# ループする
while ($true) {
    # カーソル位置を取得する
    $pos = $host.ui.rawui.CursorPosition

    # 1行をクリアする
    $host.ui.rawui.CursorPosition = New-Object System.Management.Automation.Host.Coordinates(0, $pos.Y)

    # カーソル位置を表示する
    Write-Host $count $pos.X $pos.Y
    # 1秒待つ
    Start-Sleep -Seconds 1
    $count++

    if($pos.Y -gt 30)
    {
        # カーソル位置を初期位置に戻す
        $host.ui.rawui.CursorPosition = $pos_org
    }
}