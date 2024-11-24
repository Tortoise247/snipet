# Define an array in PowerShell
$array = @("item1", "item2", "item3", "item4")

# Output the array
$array

# JSONに変換
$json = $array | ConvertTo-Json

# Output the JSON
$json

# XMLに変換
$xml = $array | ConvertTo-Xml -As String

# Output the XML
$xml

# sample.xml ファイルを読み込む
$xmlPath = "sample.xml"
$xmlData = [xml](Get-Content -Path $xmlPath)

# すべての author 要素を取得する
$authorElements = $xmlData.SelectNodes("//author")

# 各 author 要素のテキストを取得する
$authors = @()
foreach ($author in $authorElements) {
    $authors += $author.InnerText
}

# author 要素のテキストを表示する
$authors


# author 要素のテキストを JSON に変換する
$jsonData = $authors | ConvertTo-Json -Depth 10

# JSON データを表示する
$jsonData