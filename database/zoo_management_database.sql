-- Zoo Management System Database Schema


CREATE DATABASE IF NOT EXISTS zoo_management;
USE zoo_management;

-- 1. Users/Staff Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('Admin', 'Senior Staff', 'Staff') NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    join_date DATE NOT NULL,
    status ENUM('Active', 'On Leave', 'Inactive') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Enclosures Table
CREATE TABLE IF NOT EXISTS enclosures (
    enclosure_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type ENUM('Outdoor', 'Indoor', 'Aquatic', 'Aviary') NOT NULL,
    capacity INT NOT NULL,
    current_occupancy INT DEFAULT 0,
    condition_status ENUM('Excellent', 'Good', 'Needs Repair', 'Under Maintenance') DEFAULT 'Good',
    last_maintenance DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. Animals Table
CREATE TABLE IF NOT EXISTS animals (
    animal_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    species VARCHAR(100) NOT NULL,
    age INT,
    gender ENUM('Male', 'Female') NOT NULL,
    enclosure_id VARCHAR(20),
    health_status VARCHAR(50) DEFAULT 'Healthy',
    arrival_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (enclosure_id) REFERENCES enclosures(enclosure_id) ON DELETE SET NULL
);

-- 4. Health Records Table
CREATE TABLE IF NOT EXISTS health_records (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    animal_id INT NOT NULL,
    check_date DATE NOT NULL,
    condition_desc VARCHAR(255),
    treatment TEXT,
    vet_notes TEXT,
    vet_name VARCHAR(100) NOT NULL,
    next_checkup DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(animal_id) ON DELETE CASCADE
);

-- 5. Feeding Schedule Table
CREATE TABLE IF NOT EXISTS feeding_schedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    animal_id INT NOT NULL,
    feed_time TIME NOT NULL,
    food_type VARCHAR(100) NOT NULL,
    quantity VARCHAR(50) NOT NULL,
    staff_id INT NOT NULL,
    schedule_date DATE NOT NULL,
    status ENUM('Pending', 'Completed', 'Missed') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (animal_id) REFERENCES animals(animal_id) ON DELETE CASCADE,
    FOREIGN KEY (staff_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 6. Tasks Table
CREATE TABLE IF NOT EXISTS tasks (
    task_id INT PRIMARY KEY AUTO_INCREMENT,
    staff_id INT NOT NULL,
    task_description TEXT NOT NULL,
    due_date DATE,
    priority ENUM('Low', 'Medium', 'High', 'Urgent') DEFAULT 'Medium',
    status ENUM('Pending', 'In Progress', 'Completed') DEFAULT 'Pending',
    assigned_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (staff_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(user_id) ON DELETE SET NULL
);

-- 7. System Logs Table (optional - for tracking changes)
CREATE TABLE IF NOT EXISTS system_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(255) NOT NULL,
    table_name VARCHAR(50),
    record_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- Insert Sample Data

-- Sample Users (password: 'password123' - you should hash these in production)
INSERT INTO users (username, password, full_name, role, email, phone, join_date, status) VALUES
('admin', 'password123', 'Admin User', 'Admin', 'admin@zoo.com', '+1234567890', '2020-01-01', 'Active'),
('johnd', 'password123', 'John Doe', 'Staff', 'john@zoo.com', '+1234567891', '2020-01-15', 'Active'),
('janes', 'password123', 'Jane Smith', 'Staff', 'jane@zoo.com', '+1234567892', '2019-06-20', 'Active'),
('mikej', 'password123', 'Mike Johnson', 'Senior Staff', 'mike@zoo.com', '+1234567893', '2018-03-10', 'Active'),
('sarahw', 'password123', 'Sarah Williams', 'Staff', 'sarah@zoo.com', '+1234567894', '2021-08-05', 'Active');

-- Sample Enclosures
INSERT INTO enclosures (enclosure_id, name, type, capacity, current_occupancy, condition_status, last_maintenance) VALUES
('E-001', 'Lion Habitat', 'Outdoor', 5, 2, 'Good', '2024-01-01'),
('E-002', 'Elephant Sanctuary', 'Outdoor', 10, 3, 'Excellent', '2023-12-15'),
('E-003', 'Zebra Plains', 'Outdoor', 15, 8, 'Good', '2024-01-05'),
('E-004', 'Monkey Island', 'Outdoor', 20, 12, 'Needs Repair', '2023-11-20'),
('E-005', 'Penguin Pool', 'Aquatic', 30, 15, 'Excellent', '2024-01-08');

-- Sample Animals
INSERT INTO animals (name, species, age, gender, enclosure_id, health_status, arrival_date) VALUES
('Leo', 'Lion', 5, 'Male', 'E-001', 'Healthy', '2020-01-15'),
('Ellie', 'Elephant', 12, 'Female', 'E-002', 'Healthy', '2018-05-20'),
('Zara', 'Zebra', 3, 'Female', 'E-003', 'Under Treatment', '2021-03-10'),
('Max', 'Monkey', 7, 'Male', 'E-004', 'Healthy', '2019-08-25'),
('Penny', 'Penguin', 2, 'Female', 'E-005', 'Healthy', '2022-02-14');

-- Sample Health Records
INSERT INTO health_records (animal_id, check_date, condition_desc, treatment, vet_notes, vet_name, next_checkup) VALUES
(1, '2024-01-05', 'Healthy', 'Routine checkup', 'Lion is in excellent condition', 'Dr. Smith', '2024-04-05'),
(2, '2024-01-08', 'Healthy', 'Dental care', 'Dental cleaning completed', 'Dr. Johnson', '2024-03-08'),
(3, '2024-01-09', 'Under Treatment', 'Leg injury treatment', 'Minor leg injury, applying medication', 'Dr. Williams', '2024-01-16');

-- Sample Feeding Schedule
INSERT INTO feeding_schedule (animal_id, feed_time, food_type, quantity, staff_id, schedule_date, status) VALUES
(1, '09:00:00', 'Raw Meat', '15 kg', 2, '2024-01-10', 'Completed'),
(2, '08:00:00', 'Hay & Vegetables', '50 kg', 3, '2024-01-10', 'Completed'),
(3, '10:30:00', 'Grass & Grains', '20 kg', 4, '2024-01-10', 'Pending'),
(4, '11:00:00', 'Fruits & Nuts', '5 kg', 5, '2024-01-10', 'Pending'),
(5, '14:00:00', 'Fish', '8 kg', 2, '2024-01-10', 'Pending');

-- Sample Tasks
INSERT INTO tasks (staff_id, task_description, due_date, priority, status, assigned_by) VALUES
(2, 'Feed the lions at 9:00 AM', '2024-01-10', 'High', 'Completed', 1),
(2, 'Clean elephant enclosure', '2024-01-10', 'Medium', 'Pending', 1),
(4, 'Health check for zebras', '2024-01-10', 'High', 'Pending', 1),
(3, 'Update feeding records', '2024-01-10', 'Low', 'Completed', 1),
(5, 'Prepare food for penguins', '2024-01-10', 'Medium', 'Pending', 1);
USE zoo_management;

