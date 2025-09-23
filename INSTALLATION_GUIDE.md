# 🚀 Fresh Server Installation Guide
## AI-Powered Smart Contract Leakage Detection System

This guide provides complete step-by-step instructions for installing the system on a fresh server from GitHub.

---

## 📋 Prerequisites

### System Requirements
- **OS**: Windows Server 2019+, Ubuntu 18.04+, or CentOS 7+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space
- **Network**: Internet connection for package downloads

### Software Requirements
- Python 3.8 or higher
- Git
- Web browser (for accessing the interface)

---

## 🖥️ Windows Server Installation

### Step 1: Install Python
```powershell
# Download Python from https://python.org
# Choose "Add Python to PATH" during installation
# Verify installation
python --version
pip --version
```

### Step 2: Install Git
```powershell
# Download Git from https://git-scm.com
# Install with default settings
# Verify installation
git --version
```

### Step 3: Clone Repository
```powershell
# Navigate to desired directory
cd C:\
git clone https://github.com/YOUR_USERNAME/AI-Contract-Leakage-Detection.git
cd AI-Contract-Leakage-Detection
```

### Step 4: Setup Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (should show (venv) in prompt)
```

### Step 5: Install Dependencies
```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 6: Create Directory Structure
```powershell
# Create upload directories
mkdir uploads\azure-nadcomms
mkdir uploads\nadcomms-customerA
mkdir uploads\nadcomms-customerB
mkdir uploads\nadcomms-customerC

# Create other required directories
mkdir models
mkdir analysis_results
```

### Step 7: Generate Sample Data (Optional)
```powershell
# Generate sample contracts for testing
python sample_contracts.py
```

### Step 8: Start Application
```powershell
# Start the Flask application
python app.py

# Application will be available at http://localhost:5000
```

### Step 9: Configure Windows Firewall (If needed)
```powershell
# Allow inbound connections on port 5000
netsh advfirewall firewall add rule name="Contract Leakage Detection" dir=in action=allow protocol=TCP localport=5000
```

---

## 🐧 Linux/Ubuntu Server Installation

### Step 1: Update System
```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install software-properties-common -y
```

### Step 2: Install Python and Git
```bash
# Install Python 3.8+, pip, venv, and git
sudo apt install python3 python3-pip python3-venv git -y

# Verify installations
python3 --version
pip3 --version
git --version
```

### Step 3: Clone Repository
```bash
# Navigate to desired directory
cd /opt

# Clone repository (may need sudo for /opt)
sudo git clone https://github.com/YOUR_USERNAME/AI-Contract-Leakage-Detection.git
cd AI-Contract-Leakage-Detection

# Change ownership to current user
sudo chown -R $USER:$USER /opt/AI-Contract-Leakage-Detection
```

### Step 4: Setup Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show (venv) in prompt)
```

### Step 5: Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install additional system dependencies if needed
sudo apt install python3-dev build-essential -y
```

### Step 6: Create Directory Structure
```bash
# Create upload directories
mkdir -p uploads/{azure-nadcomms,nadcomms-customerA,nadcomms-customerB,nadcomms-customerC}

# Create other required directories
mkdir -p models analysis_results

# Set proper permissions
chmod -R 755 uploads/ models/ analysis_results/
```

### Step 7: Generate Sample Data (Optional)
```bash
# Generate sample contracts for testing
python sample_contracts.py
```

### Step 8: Start Application
```bash
# Start the Flask application
python app.py

# Application will be available at http://localhost:5000
```

### Step 9: Configure Firewall (If needed)
```bash
# Allow inbound connections on port 5000
sudo ufw allow 5000/tcp
sudo ufw reload
```

---

## 🐳 Docker Installation

### Step 1: Install Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Windows: Download Docker Desktop from docker.com
```

### Step 2: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-Contract-Leakage-Detection.git
cd AI-Contract-Leakage-Detection
```

### Step 3: Build and Run
```bash
# Build Docker image
docker build -t contract-leakage-detection .

# Run container
docker run -d -p 5000:5000 --name contract-app contract-leakage-detection

# Check container status
docker ps
```

### Step 4: Access Application
```bash
# Application available at http://localhost:5000
# View logs
docker logs contract-app
```

---

## 🔧 Production Deployment

### Using Gunicorn (Recommended)
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or with more options
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --max-requests 1000 app:app
```

### Using Nginx (Reverse Proxy)
```nginx
# /etc/nginx/sites-available/contract-leakage
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Systemd Service (Linux)
```ini
# /etc/systemd/system/contract-leakage.service
[Unit]
Description=Contract Leakage Detection System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/AI-Contract-Leakage-Detection
Environment=PATH=/opt/AI-Contract-Leakage-Detection/venv/bin
ExecStart=/opt/AI-Contract-Leakage-Detection/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable contract-leakage
sudo systemctl start contract-leakage
sudo systemctl status contract-leakage
```

---

## 🧪 Verification & Testing

### Step 1: Access Web Interface
```bash
# Open browser to http://localhost:5000
# Should see the main dashboard
```

### Step 2: Test File Upload
```bash
# Generate sample contracts
python sample_contracts.py

# Upload PDFs from sample_contracts/ folder
# Test different contract types
```

### Step 3: Test Analysis
```bash
# Click "Retrain & Analyze" button
# Should complete within 2-3 minutes
# Check results dashboard
```

### Step 4: Verify API Endpoints
```bash
# Test API endpoints
curl http://localhost:5000/contracts
curl http://localhost:5000/results
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Python/Pip Not Found
```bash
# Windows
# Add Python to PATH environment variable
# Or reinstall Python with "Add to PATH" option

# Linux
sudo apt install python3 python3-pip
```

#### 2. Permission Denied Errors
```bash
# Windows
icacls uploads /grant Users:F /T

# Linux
sudo chown -R $USER:$USER .
chmod -R 755 uploads/ models/ analysis_results/
```

#### 3. Port Already in Use
```bash
# Find process using port 5000
# Windows
netstat -ano | findstr :5000

# Linux
sudo lsof -i :5000

# Kill process or change port in app.py
```

#### 4. Module Import Errors
```bash
# Ensure virtual environment is activated
# Windows
venv\Scripts\activate

# Linux
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

#### 5. PDF Processing Errors
```bash
# Install additional dependencies
pip install PyPDF2 reportlab

# Check file permissions
ls -la sample_contracts/
```

---

## 📊 Performance Optimization

### For High-Volume Deployments
```bash
# Increase worker processes
gunicorn -w 8 -b 0.0.0.0:5000 app:app

# Add Redis for caching
pip install redis
# Configure Redis in app.py

# Use PostgreSQL for production
pip install psycopg2-binary
# Update database configuration
```

### Memory Optimization
```python
# In app.py, add memory limits
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

---

## 🔒 Security Configuration

### Basic Security
```bash
# Change default Flask secret key
export SECRET_KEY='your-secret-key-here'

# Disable debug mode in production
export FLASK_ENV=production
export FLASK_DEBUG=False
```

### SSL/HTTPS Setup
```bash
# Generate SSL certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with SSL
python app.py --ssl-context=adhoc
```

---

## 📈 Monitoring & Logging

### Application Logs
```python
# Add to app.py
import logging
logging.basicConfig(level=logging.INFO)
```

### System Monitoring
```bash
# Monitor system resources
htop
df -h
free -m

# Monitor application logs
tail -f /var/log/contract-leakage.log
```

---

## 🆘 Support & Maintenance

### Regular Maintenance
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Clean up old files
find uploads/ -type f -mtime +30 -delete

# Backup data
tar -czf backup-$(date +%Y%m%d).tar.gz uploads/ models/ analysis_results/
```

### Getting Help
- **Documentation**: Check `SOLUTION_DOCUMENT.md`
- **GitHub Issues**: Create issue with error details
- **Logs**: Check application and system logs
- **Community**: Stack Overflow with tag `contract-leakage-detection`

---

**Installation Complete! 🎉**

Your AI-Powered Contract Leakage Detection System is now ready to help prevent revenue loss through intelligent contract analysis.
