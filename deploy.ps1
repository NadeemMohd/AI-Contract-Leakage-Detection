# AI Contract Leakage Detection - Windows PowerShell Deployment Script
# This script automates the deployment process on Windows

param(
    [switch]$Production,
    [switch]$GenerateSamples,
    [switch]$Help
)

if ($Help) {
    Write-Host "AI Contract Leakage Detection - Deployment Script" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\deploy.ps1                    # Development deployment"
    Write-Host "  .\deploy.ps1 -Production        # Production deployment with Gunicorn"
    Write-Host "  .\deploy.ps1 -GenerateSamples   # Generate sample contracts"
    Write-Host "  .\deploy.ps1 -Help              # Show this help"
    Write-Host ""
    exit 0
}

Write-Host "🚀 Starting deployment of AI Contract Leakage Detection System..." -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "app.py")) {
    Write-Host "❌ Error: app.py not found. Please run this script from the project root directory." -ForegroundColor Red
    exit 1
}

# Function to check if command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

if (-not (Test-Command "python")) {
    Write-Host "❌ Python is required but not installed." -ForegroundColor Red
    exit 1
}

if (-not (Test-Command "pip")) {
    Write-Host "❌ pip is required but not installed." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Prerequisites check passed" -ForegroundColor Green

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "🔧 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "📦 Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create necessary directories
Write-Host "📁 Creating directories..." -ForegroundColor Yellow
$directories = @(
    "uploads\azure-nadcomms",
    "uploads\nadcomms-customerA", 
    "uploads\nadcomms-customerB",
    "uploads\nadcomms-customerC",
    "models",
    "analysis_results"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# Generate sample contracts if requested
if ($GenerateSamples -or (-not $Production)) {
    $generate = Read-Host "🎯 Generate sample contracts for testing? (y/n)"
    if ($generate -eq "y" -or $generate -eq "Y") {
        Write-Host "📄 Generating sample contracts..." -ForegroundColor Yellow
        python sample_contracts.py
    }
}

# Configure Windows Firewall
Write-Host "🔒 Configuring Windows Firewall..." -ForegroundColor Yellow
try {
    netsh advfirewall firewall add rule name="Contract Leakage Detection" dir=in action=allow protocol=TCP localport=5000 | Out-Null
    Write-Host "✅ Firewall rule added for port 5000" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not configure firewall. You may need to run as Administrator." -ForegroundColor Yellow
}

# Start application
if ($Production) {
    Write-Host "🏭 Installing Gunicorn..." -ForegroundColor Yellow
    pip install gunicorn
    
    Write-Host "🚀 Starting application with Gunicorn..." -ForegroundColor Green
    Write-Host "📍 Application will be available at http://localhost:5000" -ForegroundColor Cyan
    Write-Host "🛑 Press Ctrl+C to stop the server" -ForegroundColor Yellow
    
    # Start with Gunicorn
    gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
} else {
    Write-Host "🧪 Starting development server..." -ForegroundColor Green
    Write-Host "📍 Application will be available at http://localhost:5000" -ForegroundColor Cyan
    Write-Host "🛑 Press Ctrl+C to stop the server" -ForegroundColor Yellow
    
    # Start development server
    python app.py
}
