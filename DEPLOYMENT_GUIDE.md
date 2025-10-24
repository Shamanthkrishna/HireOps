# HireOps Deployment Guide

## Overview
This guide provides comprehensive instructions for deploying HireOps in production environments. HireOps is a modern recruitment tracking system built with FastAPI, PostgreSQL, and Redis.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Prerequisites](#prerequisites)
3. [Installation Methods](#installation-methods)
4. [Configuration](#configuration)
5. [Production Deployment](#production-deployment)
6. [Security Configuration](#security-configuration)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **CPU**: 2 cores, 2.4GHz
- **RAM**: 4GB
- **Storage**: 20GB SSD
- **OS**: Ubuntu 20.04 LTS, CentOS 8, or RHEL 8
- **Network**: 1Gbps ethernet

### Recommended for Production
- **CPU**: 4 cores, 3.0GHz
- **RAM**: 8GB
- **Storage**: 100GB SSD
- **OS**: Ubuntu 22.04 LTS
- **Network**: Load balancer with SSL termination

### Supported Platforms
- **Docker**: Recommended deployment method
- **Kubernetes**: For scalable deployments
- **Traditional**: Direct installation on Linux servers
- **Cloud**: AWS, Azure, GCP compatible

---

## Prerequisites

### Docker Installation (Recommended)

**Ubuntu/Debian:**
```bash
# Update package index
sudo apt update

# Install Docker
sudo apt install -y docker.io docker-compose

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
```

**CentOS/RHEL:**
```bash
# Install Docker
sudo yum install -y docker docker-compose

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
```

### Manual Installation Prerequisites

**System Packages:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3.11 python3.11-pip python3.11-venv
sudo apt install -y postgresql-14 postgresql-contrib
sudo apt install -y redis-server
sudo apt install -y nginx

# CentOS/RHEL
sudo yum install -y python311 python311-pip
sudo yum install -y postgresql14-server postgresql14-contrib
sudo yum install -y redis
sudo yum install -y nginx
```

**Python Dependencies:**
```bash
# Create virtual environment
python3.11 -m venv /opt/hireops/venv
source /opt/hireops/venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

---

## Installation Methods

### Method 1: Docker Deployment (Recommended)

#### Quick Start
```bash
# Clone repository
git clone https://github.com/your-org/hireops.git
cd hireops

# Copy production environment
cp .env.production.example .env.production

# Edit configuration
nano .env.production

# Deploy
chmod +x deploy.sh
./deploy.sh
```

#### Manual Docker Setup
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Method 2: Kubernetes Deployment

#### Kubernetes Manifests

**Namespace:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: hireops
```

**ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: hireops-config
  namespace: hireops
data:
  DATABASE_URL: "postgresql://user:pass@postgres:5432/hireops"
  REDIS_URL: "redis://redis:6379"
  ENVIRONMENT: "production"
```

**Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hireops-app
  namespace: hireops
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hireops-app
  template:
    metadata:
      labels:
        app: hireops-app
    spec:
      containers:
      - name: hireops
        image: hireops:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: hireops-config
```

**Service:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: hireops-service
  namespace: hireops
spec:
  selector:
    app: hireops-app
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Method 3: Manual Installation

#### Database Setup
```bash
# PostgreSQL setup
sudo -u postgres createuser hireops_user
sudo -u postgres createdb hireops_db
sudo -u postgres psql -c "ALTER USER hireops_user PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE hireops_db TO hireops_user;"
```

#### Application Setup
```bash
# Create application user
sudo useradd -m -s /bin/bash hireops

# Create directories
sudo mkdir -p /opt/hireops/{app,logs,uploads}
sudo chown -R hireops:hireops /opt/hireops

# Install application
sudo -u hireops cp -r . /opt/hireops/app/
```

#### Systemd Service
```ini
[Unit]
Description=HireOps Recruitment System
After=network.target postgresql.service redis.service

[Service]
Type=exec
User=hireops
Group=hireops
WorkingDirectory=/opt/hireops/app
Environment=PATH=/opt/hireops/venv/bin
ExecStart=/opt/hireops/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## Configuration

### Environment Variables

#### Required Settings
```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/database
SECRET_KEY=your-super-secret-jwt-key-minimum-32-chars
ALGORITHM=HS256

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@company.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@company.com

# Application Settings
APP_NAME=HireOps
ENVIRONMENT=production
DEBUG=false
```

#### Optional Settings
```bash
# Redis Configuration
REDIS_URL=redis://localhost:6379

# File Upload Settings
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=pdf,doc,docx,txt

# Security Settings
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["https://yourdomain.com"]

# Feature Flags
ENABLE_ANALYTICS=true
ENABLE_NOTIFICATIONS=true
ENABLE_CALENDAR_INTEGRATION=true
```

### Database Configuration

#### Connection Settings
```python
# Production database URL format
DATABASE_URL = "postgresql://username:password@hostname:port/database_name"

# SSL Configuration (recommended for production)
DATABASE_URL = "postgresql://user:pass@host:5432/db?sslmode=require"

# Connection pooling
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 20,
    "max_overflow": 0,
    "pool_pre_ping": True,
    "pool_recycle": 3600
}
```

#### Database Initialization
```bash
# Run migrations
alembic upgrade head

# Create admin user
python scripts/create_admin.py

# Seed sample data (optional)
python scripts/seed_data.py
```

### Nginx Configuration

#### Production Nginx Config
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/yourdomain.com.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    # Application Proxy
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Static Files
    location /static {
        alias /opt/hireops/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # File Uploads
    location /uploads {
        alias /opt/hireops/uploads;
        internal;  # Only accessible through application
    }
}
```

---

## Production Deployment

### Pre-Deployment Checklist

#### Security Review
- [ ] Change default passwords
- [ ] Generate secure JWT secret
- [ ] Configure SSL certificates
- [ ] Set up firewall rules
- [ ] Enable audit logging
- [ ] Configure backup system

#### Performance Optimization
- [ ] Database indexing
- [ ] Connection pooling
- [ ] Caching configuration
- [ ] Load balancing setup
- [ ] CDN configuration
- [ ] Monitoring setup

#### High Availability Setup

**Load Balancer Configuration:**
```nginx
upstream hireops_backend {
    server 10.0.1.10:8000;
    server 10.0.1.11:8000;
    server 10.0.1.12:8000;
    
    # Health check
    keepalive 32;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://hireops_backend;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Database Clustering:**
```bash
# PostgreSQL Master-Slave setup
# Master server configuration
echo "wal_level = replica" >> /etc/postgresql/14/main/postgresql.conf
echo "max_wal_senders = 3" >> /etc/postgresql/14/main/postgresql.conf
echo "wal_keep_segments = 64" >> /etc/postgresql/14/main/postgresql.conf

# Slave server setup
pg_basebackup -h master-ip -D /var/lib/postgresql/14/main -U replication -v -P -W
```

### Deployment Scripts

#### Zero-Downtime Deployment
```bash
#!/bin/bash
# deploy-production.sh

set -e

echo "Starting zero-downtime deployment..."

# Pull latest code
git fetch origin
git checkout $1  # Version tag

# Build new Docker image
docker build -t hireops:$1 .

# Run database migrations
docker run --rm --env-file .env.production \
    --network hireops_default \
    hireops:$1 alembic upgrade head

# Update docker-compose with new image
sed -i "s/hireops:latest/hireops:$1/" docker-compose.yml

# Rolling update
docker-compose up -d --no-deps app

# Health check
sleep 30
curl -f http://localhost/health || exit 1

# Cleanup old images
docker image prune -f

echo "Deployment completed successfully!"
```

#### Rollback Script
```bash
#!/bin/bash
# rollback.sh

PREVIOUS_VERSION=$1

echo "Rolling back to version: $PREVIOUS_VERSION"

# Update compose file
sed -i "s/hireops:.*/hireops:$PREVIOUS_VERSION/" docker-compose.yml

# Deploy previous version
docker-compose up -d --no-deps app

# Health check
sleep 30
curl -f http://localhost/health || exit 1

echo "Rollback completed!"
```

---

## Security Configuration

### SSL/TLS Setup

#### Let's Encrypt (Free SSL)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

#### Commercial SSL Certificate
```bash
# Generate private key
openssl genrsa -out yourdomain.com.key 2048

# Generate CSR
openssl req -new -key yourdomain.com.key -out yourdomain.com.csr

# Install certificate files
sudo cp yourdomain.com.crt /etc/ssl/certs/
sudo cp yourdomain.com.key /etc/ssl/private/
sudo chmod 600 /etc/ssl/private/yourdomain.com.key
```

### Firewall Configuration

#### UFW (Ubuntu Firewall)
```bash
# Enable firewall
sudo ufw enable

# Allow SSH
sudo ufw allow ssh

# Allow HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Allow database (internal only)
sudo ufw allow from 10.0.0.0/8 to any port 5432

# Deny all other traffic
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

#### iptables Rules
```bash
# Basic firewall rules
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -j DROP

# Save rules
iptables-save > /etc/iptables/rules.v4
```

### Application Security

#### JWT Configuration
```python
# Strong JWT configuration
SECRET_KEY = os.urandom(32).hex()  # Generate secure random key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Additional security headers
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'"
}
```

#### Input Validation
```python
# File upload security
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# SQL injection prevention (automatically handled by SQLAlchemy)
# XSS prevention (automatically handled by FastAPI/Pydantic)
# CSRF protection
CSRF_SECRET_KEY = os.urandom(32).hex()
```

---

## Monitoring and Maintenance

### Health Monitoring

#### Application Health Checks
```python
# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "database": await check_database_health(),
        "redis": await check_redis_health()
    }
```

#### System Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# System resource monitoring
#!/bin/bash
# monitor.sh
while true; do
    echo "=== $(date) ==="
    echo "CPU Usage:"
    top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}'
    
    echo "Memory Usage:"
    free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }'
    
    echo "Disk Usage:"
    df -h | awk '$NF=="/"{printf "Disk Usage: %d/%dGB (%s)\n", $3,$2,$5}'
    
    sleep 60
done
```

### Log Management

#### Log Configuration
```python
# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": "/opt/hireops/logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
    },
}
```

#### Log Rotation
```bash
# Logrotate configuration
cat > /etc/logrotate.d/hireops << EOF
/opt/hireops/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
}
EOF
```

### Backup Strategy

#### Database Backup
```bash
#!/bin/bash
# backup-db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/database"
DB_NAME="hireops_db"

mkdir -p $BACKUP_DIR

# Create backup
pg_dump $DB_NAME | gzip > $BACKUP_DIR/hireops_backup_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "hireops_backup_*.sql.gz" -mtime +30 -delete

# Upload to S3 (optional)
aws s3 cp $BACKUP_DIR/hireops_backup_$DATE.sql.gz s3://your-backup-bucket/database/
```

#### File Backup
```bash
#!/bin/bash
# backup-files.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/files"
SOURCE_DIR="/opt/hireops/uploads"

mkdir -p $BACKUP_DIR

# Create backup
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz -C $SOURCE_DIR .

# Keep only last 7 days
find $BACKUP_DIR -name "files_backup_*.tar.gz" -mtime +7 -delete
```

#### Automated Backup Schedule
```bash
# Add to crontab
0 2 * * * /opt/hireops/scripts/backup-db.sh
0 3 * * * /opt/hireops/scripts/backup-files.sh
```

---

## Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check logs
docker-compose logs app

# Common solutions
1. Check environment variables
2. Verify database connectivity
3. Check port conflicts
4. Verify file permissions
```

#### Database Connection Issues
```bash
# Test database connection
psql -h localhost -U hireops_user -d hireops_db

# Common solutions
1. Check PostgreSQL service status
2. Verify connection string
3. Check firewall rules
4. Verify user permissions
```

#### Performance Issues
```bash
# Check system resources
htop
iotop
nethogs

# Database performance
# Check slow queries
SELECT * FROM pg_stat_activity WHERE state = 'active';

# Application performance
# Enable debug logging
DEBUG=true docker-compose restart app
```

### Diagnostic Commands

#### System Health
```bash
# Check all services
docker-compose ps

# Check resource usage
docker stats

# Check network connectivity
netstat -tulpn | grep :8000
curl -I http://localhost/health

# Check database
docker-compose exec db psql -U hireops_user -d hireops_db -c "SELECT version();"
```

#### Log Analysis
```bash
# Application logs
docker-compose logs -f app

# Database logs
docker-compose logs -f db

# Nginx logs
docker-compose logs -f nginx

# Search for errors
grep -i error /opt/hireops/logs/*.log
```

### Recovery Procedures

#### Database Recovery
```bash
# Stop application
docker-compose stop app

# Restore from backup
gunzip -c /opt/backups/database/hireops_backup_YYYYMMDD_HHMMSS.sql.gz | psql -U hireops_user -d hireops_db

# Start application
docker-compose start app
```

#### File Recovery
```bash
# Extract backup
tar -xzf /opt/backups/files/files_backup_YYYYMMDD_HHMMSS.tar.gz -C /opt/hireops/uploads/

# Fix permissions
chown -R 1000:1000 /opt/hireops/uploads/
```

---

## Support and Resources

### Documentation
- **API Reference**: https://your-domain.com/docs
- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)

### Monitoring URLs
- **Application**: https://your-domain.com/health
- **Database**: Check via application health endpoint
- **API Docs**: https://your-domain.com/docs

### Support Contacts
- **Technical Support**: support@hireops.com
- **Emergency**: +1-800-HIRE-OPS
- **Documentation**: docs@hireops.com

---

*This deployment guide is regularly updated. For the latest version and additional resources, visit our documentation portal.*

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Maintained by**: HireOps DevOps Team