
function Clear-Line {
    param (
        [int]$line
    )
    $currentPosition = [Console]::CursorTop
    [Console]::SetCursorPosition(0, $line)
    [Console]::Write(" " * [Console]::WindowWidth)
    [Console]::SetCursorPosition(0, $line)
}

function write-string($str) {
    [Console]::Write($str)
    Start-Sleep -Seconds 1
}

write-host "進捗表示"

while($true)
{
    write-string( "a")
    write-string( "b")
    write-string( "c")
    write-string( "d")
    write-string( "e")
    write-string( "f")
    write-string( "g")
    write-string( "h")
    write-string( "i")
    write-string( "j")
    write-string( "k")
    Clear-line 
}

