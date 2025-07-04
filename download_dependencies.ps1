# Cropperview Dependency Downloader
# This script downloads the required executables for Cropperview

Write-Host "=== Cropperview Dependency Downloader ===" -ForegroundColor Green
Write-Host "This script will download HandBrake CLI and Superview CLI executables." -ForegroundColor Yellow
Write-Host ""

# Create directories if they don't exist
if (!(Test-Path "downloads")) {
    New-Item -ItemType Directory -Name "downloads"
}

# Function to download file with progress
function Download-FileWithProgress {
    param(
        [string]$Url,
        [string]$OutFile,
        [string]$Description
    )
    
    Write-Host "Downloading $Description..." -ForegroundColor Cyan
    Write-Host "URL: $Url" -ForegroundColor Gray
    
    try {
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($Url, $OutFile)
        Write-Host "✓ Successfully downloaded $Description" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "✗ Failed to download $Description" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Download HandBrake CLI
Write-Host "=== Downloading HandBrake CLI ===" -ForegroundColor Blue
$handbrakeUrl = "https://github.com/HandBrake/HandBrake/releases/download/1.7.3/HandBrakeCLI-1.7.3-x86_64-Win_GUI.exe"
$handbrakeFile = "downloads\HandBrakeCLI.exe"

if (Download-FileWithProgress -Url $handbrakeUrl -OutFile $handbrakeFile -Description "HandBrake CLI") {
    # Move to root directory
    Move-Item $handbrakeFile "HandBrakeCLI.exe" -Force
    Write-Host "✓ HandBrake CLI installed successfully" -ForegroundColor Green
}

Write-Host ""

# Download Superview CLI
Write-Host "=== Downloading Superview CLI ===" -ForegroundColor Blue
Write-Host "Note: Superview CLI is not available as a direct download." -ForegroundColor Yellow
Write-Host "Please download it manually from: https://github.com/niek/superview/releases" -ForegroundColor Yellow
Write-Host ""

# Alternative: Try to download from a known source (if available)
$superviewUrl = "https://github.com/niek/superview/releases/latest/download/superview-cli.exe"
$superviewFile = "downloads\superview-cli.exe"

Write-Host "Attempting to download Superview CLI from GitHub releases..." -ForegroundColor Cyan
if (Download-FileWithProgress -Url $superviewUrl -OutFile $superviewFile -Description "Superview CLI") {
    # Move to root directory
    Move-Item $superviewFile "superview-cli.exe" -Force
    Write-Host "✓ Superview CLI installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Could not download Superview CLI automatically" -ForegroundColor Red
    Write-Host "Please download it manually:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://github.com/niek/superview/releases" -ForegroundColor White
    Write-Host "2. Download the latest superview-cli.exe" -ForegroundColor White
    Write-Host "3. Place it in this directory" -ForegroundColor White
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green

# Check if files exist
$handbrakeExists = Test-Path "HandBrakeCLI.exe"
$superviewExists = Test-Path "superview-cli.exe"

Write-Host "Dependency Status:" -ForegroundColor Blue
Write-Host "HandBrake CLI: $(if ($handbrakeExists) { '✓ Installed' } else { '✗ Missing' })" -ForegroundColor $(if ($handbrakeExists) { 'Green' } else { 'Red' })
Write-Host "Superview CLI: $(if ($superviewExists) { '✓ Installed' } else { '✗ Missing' })" -ForegroundColor $(if ($superviewExists) { 'Green' } else { 'Red' })

if ($handbrakeExists -and $superviewExists) {
    Write-Host ""
    Write-Host "🎉 All dependencies are installed! You can now run Cropperview." -ForegroundColor Green
    Write-Host "Double-click RUN_cropperview.bat to start the application." -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "⚠️  Some dependencies are missing. Please install them before running Cropperview." -ForegroundColor Yellow
}

# Clean up downloads directory
if (Test-Path "downloads") {
    Remove-Item "downloads" -Recurse -Force
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 