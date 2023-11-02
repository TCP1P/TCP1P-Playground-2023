-- Create the "notedb" database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS notedb;

-- Switch to the "notedb" database
USE notedb;

-- Create the "notes" table with a "value" column
CREATE TABLE IF NOT EXISTS notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    value TEXT,
    isAdmin BOOLEAN DEFAULT FALSE
);

INSERT INTO notes (value)
VALUES
    ('This is a sample note.'),
    ('Here is another random note.'),
    ('Don\'t forget to buy groceries.'),
    ('Call John about the meeting.'),
    ('Write a report on the project.'),
    ('Study for the upcoming exam.'),
    ('Pick up the kids from school.'),
    ('Plan a weekend trip with family.');

-- Create the "secret" table
CREATE TABLE IF NOT EXISTS secret (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag VARCHAR(255) NOT NULL
);

-- Insert a CTF flag into the "secret" table
INSERT INTO secret (flag)
    VALUES ('fake{flag}');

