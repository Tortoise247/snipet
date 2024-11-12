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