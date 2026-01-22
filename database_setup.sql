-- Database Creation
CREATE DATABASE IF NOT EXISTS aqi_project;
USE aqi_project;

-- Table Structure
CREATE TABLE IF NOT EXISTS aqi_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(50) NOT NULL,
    reading_date DATE NOT NULL,
    aqi INT,
    pollutant VARCHAR(20),
    status VARCHAR(50)
);

-- (Optional) Insert some dummy data for testing
INSERT INTO aqi_data (city_name, reading_date, aqi, pollutant, status) VALUES 
('New Delhi', '2025-12-08', 352, 'pm2.5', 'Very Unhealthy'),
('Tokyo', '2025-12-08', 25, 'pm10', 'Good');
