$ErrorActionPreference = "Stop"

$cvBasename = "CV_Gaston_Bujia"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

function Test-Command {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Missing required command: $Name"
    }
}

Set-Location $root

Test-Command -Name "python"
Test-Command -Name "pandoc"

Write-Host "Construyendo archivos Markdown desde cv_data.yaml..."
python src\build_cv.py

Write-Host "Generando CVs en progreso..."

pandoc "src\$cvBasename.md" `
    -H "assets\disable_hyphens.tex" `
    -V "geometry:margin=1in" `
    -o "output\${cvBasename}_ES.pdf"

pandoc "src\english\${cvBasename}_EN.md" `
    -H "assets\disable_hyphens.tex" `
    -V "geometry:margin=1in" `
    -o "output\${cvBasename}_EN.pdf"

Write-Host "PDFs generados exitosamente en la carpeta 'output/':"
Write-Host "  - output\${cvBasename}_ES.pdf"
Write-Host "  - output\${cvBasename}_EN.pdf"
