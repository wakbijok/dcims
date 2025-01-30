CREATE DATABASE IF NOT EXISTS dcims;
USE dcims;

CREATE TABLE datacenters (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hardware (
    id INT PRIMARY KEY AUTO_INCREMENT,
    datacenter_id INT,
    equipment VARCHAR(100),
    serial_number VARCHAR(100) UNIQUE,
    function_desc TEXT,
    brand_model VARCHAR(100),
    ip_address VARCHAR(45) UNIQUE,
    username VARCHAR(50),
    password VARCHAR(255),
    ilo_login VARCHAR(100),
    FOREIGN KEY (datacenter_id) REFERENCES datacenters(id),
    INDEX idx_serial (serial_number),
    INDEX idx_ip (ip_address)
);

CREATE TABLE virtual_machines (
    id INT PRIMARY KEY AUTO_INCREMENT,
    datacenter_id INT,
    ip_address VARCHAR(45) UNIQUE,
    hostname VARCHAR(255),
    tech_stack VARCHAR(100),
    description TEXT,
    environment ENUM('Production', 'Staging', 'Development'),
    FOREIGN KEY (datacenter_id) REFERENCES datacenters(id),
    INDEX idx_ip (ip_address),
    INDEX idx_hostname (hostname)
);

CREATE TABLE networks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    datacenter_id INT,
    description VARCHAR(255),
    network_address VARCHAR(45),
    gateway VARCHAR(45),
    broadcast VARCHAR(45),
    vlan_id INT,
    FOREIGN KEY (datacenter_id) REFERENCES datacenters(id)
);

CREATE TABLE urls (
    id INT PRIMARY KEY AUTO_INCREMENT,
    description TEXT,
    url VARCHAR(255),
    is_public BOOLEAN,
    environment VARCHAR(50),
    ip_address VARCHAR(45) UNIQUE,
    protocol VARCHAR(10),
    port INT,
    remarks TEXT,
    FOREIGN KEY (ip_address) REFERENCES virtual_machines(ip_address),
    INDEX idx_url (url)
);