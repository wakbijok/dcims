#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit
fi

# System update and dependencies
apt update
apt install -y python3-pip python3-venv mariadb-server mariadb-client default-libmysqlclient-dev python3-dev build-essential pkg-config

# Create and copy application files
mkdir -p /opt/dcims/{app,scripts,logs}
cp -r app/* /opt/dcims/app/
cp scripts/* /opt/dcims/scripts/
cp requirements.txt /opt/dcims/

# Set permissions
chown -R www-data:www-data /opt/dcims
chmod -R 755 /opt/dcims
chmod -R 760 /opt/dcims/logs

# MySQL setup
mysql -e "CREATE DATABASE IF NOT EXISTS dcims;"
mysql -e "CREATE USER IF NOT EXISTS 'dcims'@'localhost' IDENTIFIED BY 'dcims_password';"
mysql -e "GRANT ALL PRIVILEGES ON dcims.* TO 'dcims'@'localhost';"
mysql -e "FLUSH PRIVILEGES;"

# Python environment
cd /opt/dcims
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create service file
cat > /etc/systemd/system/dcims.service << EOF
[Unit]
Description=DCIMS Web Application
After=network.target mysql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/dcims
Environment="PATH=/opt/dcims/venv/bin"
ExecStart=/opt/dcims/venv/bin/python app/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start services
systemctl daemon-reload
systemctl enable mysql dcims
systemctl start mysql dcims

# Create admin user
cd /opt/dcims
source venv/bin/activate
python3 scripts/create_admin.py

echo "Installation complete! Service running at http://localhost:8080"
echo "Login with username: admin, password: admin123"