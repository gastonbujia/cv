$ErrorActionPreference = "Stop"

# Thin wrapper: build_cv.py renders the Markdown files AND invokes Pandoc for
# every CV (academic EN/ES plus one industry CV per language for each profile
# in src/profiles/). To add a CV, drop a new file in src/profiles/ -- no script
# changes needed.

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

function Test-Command {
    param([Parameter(Mandatory = $true)][string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Missing required command: $Name"
    }
}

Test-Command -Name "python"
Test-Command -Name "pandoc"

Write-Host "Construyendo CVs (Markdown + PDF) desde cv_data.yaml y src/profiles/..."
python src\build_cv.py

Write-Host "PDFs generados exitosamente en la carpeta 'output/'."
