# Check that verifyta is in PATH
$verify_ta_version = verifyta.exe -v
if (-not $LASTEXITCODE -eq 0){
    Write-Error "verifyta is not in PATH. Install UPPAAL or make sure it is in the PATH."
    Exit
}

$venv = "venv"

if (-not (Test-Path -Path $venv)) {
    Write-Output "Creating virtual environment"
    & python -m venv "$venv"
}

# Check error
if (-not (Test-Path -Path $venv)) {
    Write-Error "Failed create virtual environment"
    Exit 1
}

Write-Output "Activate virtual env"
& "$venv\Scripts\Activate.ps1"

Write-Output "Upgrade pip"
python -m pip install --upgrade pip

if (-not $LASTEXITCODE -eq 0){
    Write-Error "Pip upgrade failed."
    Exit $LASTEXITCODE
}

Write-Output "Use wheel"
pip install wheel

if (-not $LASTEXITCODE -eq 0){
    Write-Error "Install wheel failed."
    Exit $LASTEXITCODE
}

Write-Output "Install python packages"
pip install -r requirements.txt

# Check error
if (-not $LASTEXITCODE -eq 0){
    Write-Error "Package installation failed."
    Exit $LASTEXITCODE
}

Write-Output "Running tests"
python run_tests.py
