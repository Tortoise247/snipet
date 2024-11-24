param (
    [string]$folderName
)
# Check if $folderName is empty and prompt for input if it is
if ([string]::IsNullOrEmpty($folderName)) {
    $folderName = Read-Host "フォルダ名を入力してください"
}


$rootPath = "E:\@snipet"  # Replace with your desired root directory

# Recursively search for folders with the specified name
$folders = Get-ChildItem -Path $rootPath -Directory -Recurse | Where-Object { $_.Name -eq $folderName }

# Output the matching folders
$folders | ForEach-Object {
    Write-Output $_.FullName
}