$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root ".venv\Scripts\python.exe"

Push-Location (Join-Path $root "..\data_pipeline")
& $python "scripts\fetch_osm_data.py"
& $python "scripts\build_demo_dataset.py"
Pop-Location
