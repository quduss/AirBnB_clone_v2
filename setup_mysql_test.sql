-- Create a new user hbnb_test and database hbnb_test_db
-- Grant select privilege on performance_schema to hbnb_test
-- Grant all privileges on hbnb_test_db to hbnb_test

CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
