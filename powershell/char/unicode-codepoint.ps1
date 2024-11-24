# ユーザーに文字の入力を求める
$inputChar = Read-Host "文字を入力してください"

# 入力された文字のUnicodeコードポイントを取得
$utf32Bytes = [System.Text.Encoding]::UTF32.GetBytes($inputChar)
$unicodeCodePoint = [BitConverter]::ToUInt32($utf32Bytes, 0)

# 結果を表示
Write-Host "文字 '$inputChar' のUnicodeコードポイントは $([Convert]::ToString($unicodeCodePoint, 16).ToUpper()) です。"

# UTF-16BEのコードポイントを取得
$utf16beBytes = [System.Text.Encoding]::BigEndianUnicode.GetBytes($inputChar)
$utf16beCodePoint = [BitConverter]::ToString($utf16beBytes)
Write-Host "文字 '$inputChar' のUTF-16BEコードポイントは $utf16beCodePoint です。"