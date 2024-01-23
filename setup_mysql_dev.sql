-- Create a new user hbnb_dev and database hbnb_dev_db
-- Grant select privilege on performance_schema to hbnb_dev
-- Grant all privileges on hbnb_dev_db to hbnb_dev

CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
