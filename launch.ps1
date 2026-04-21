# Launch script for TradingPenguin
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BuildDir = Join-Path $ScriptDir "build"
$CacheDir = Join-Path $ScriptDir "build\pycache"

# Verify build exists
if (-not (Test-Path (Join-Path $BuildDir "tradingpenguin"))) {
    Write-Error "Build not found. Run 'python build.py' first."
    exit 1
}

# Redirect runtime cache writes
if (-not (Test-Path $CacheDir)) {
    New-Item -ItemType Directory -Path $CacheDir | Out-Null
}

$env:PYTHONPYCACHEPREFIX = $CacheDir
$env:PYTHONPATH = $BuildDir

# Run
python -m tradingpenguin.main @args
if ($LASTEXITCODE -ne 0) {
    Write-Error "TradingPenguin exited with code $LASTEXITCODE"
    exit $LASTEXITCODE
}