$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$propertiesDir = $scriptDir + "\properties.json"
$mainDir = $scriptDir + "\main.py"
$Properties = Get-Content -Raw -Path $propertiesDir | ConvertFrom-Json
$python_path = $Properties.python_path
& $python_path
python $mainDir
deactivate