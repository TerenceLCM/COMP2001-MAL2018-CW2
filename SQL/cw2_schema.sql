CREATE DATABASE COMP2001_CW2;

USE COMP2001_CW2;

CREATE SCHEMA CW2;

--User Table
CREATE TABLE CW2.[User] (
    User_ID INT IDENTITY(1,1) PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Role VARCHAR(50) NOT NULL
);

--Lookup Tables
--===Category===
CREATE TABLE CW2.Category (
    Category_ID INT IDENTITY(1,1) PRIMARY KEY,
    Category_Name VARCHAR(255) NOT NULL
);

--===Difficulty===
CREATE TABLE CW2.Difficulty (
    Difficulty_ID INT IDENTITY(1,1) PRIMARY KEY,
    Difficulty_Name VARCHAR(255) NOT NULL
);

--===Route_Type===
CREATE TABLE CW2.Route_Type (
    Route_ID INT IDENTITY(1,1) PRIMARY KEY,
    Route_Type VARCHAR(255) NOT NULL
);

--Trail table (core entity)
CREATE TABLE CW2.Trail (
    Trail_ID INT IDENTITY(1,1) PRIMARY KEY,
    Trail_Name VARCHAR(255) NOT NULL,
    Description TEXT,
    Distance DECIMAL(6,2),
    Elevation_Gain INT,
    Estimate_Time INT,
    Trail_Info TEXT,

    Category_ID INT NOT NULL,
    Difficulty_ID INT NOT NULL,
    Route_ID INT NOT NULL,
    User_ID INT NOT NULL,

    CONSTRAINT FK_Trail_Category FOREIGN KEY (Category_ID)
        REFERENCES CW2.Category(Category_ID),

    CONSTRAINT FK_Trail_Difficulty FOREIGN KEY (Difficulty_ID)
        REFERENCES CW2.Difficulty(Difficulty_ID),

    CONSTRAINT FK_Trail_Route FOREIGN KEY (Route_ID)
        REFERENCES CW2.Route_Type(Route_ID),

    CONSTRAINT FK_Trail_User FOREIGN KEY (User_ID)
        REFERENCES CW2.[User](User_ID)
);

--Trail_Point table (one-to-many)
CREATE TABLE CW2.Trail_Point (
    Point_ID INT IDENTITY(1,1) PRIMARY KEY,
    Trail_ID INT NOT NULL,
    Latitude DECIMAL(9,6) NOT NULL,
    Longitude DECIMAL(9,6) NOT NULL,
    PointOrder INT NOT NULL,

    CONSTRAINT FK_Point_Trail FOREIGN KEY (Trail_ID)
        REFERENCES CW2.Trail(Trail_ID)
        ON DELETE CASCADE
);

--Feature table
CREATE TABLE CW2.Feature (
    Feature_ID INT IDENTITY(1,1) PRIMARY KEY,
    Feature_Name VARCHAR(255) NOT NULL,
    Feature_Description TEXT
);

--Trail_Feature (link table)
CREATE TABLE CW2.Trail_Feature (
    Trail_ID INT NOT NULL,
    Feature_ID INT NOT NULL,

    CONSTRAINT PK_Trail_Feature PRIMARY KEY (Trail_ID, Feature_ID),

    CONSTRAINT FK_TrailFeature_Trail FOREIGN KEY (Trail_ID)
        REFERENCES CW2.Trail(Trail_ID)
        ON DELETE CASCADE,

    CONSTRAINT FK_TrailFeature_Feature FOREIGN KEY (Feature_ID)
        REFERENCES CW2.Feature(Feature_ID)
);

--Insert Sample Data

--Insert Users (simulated Auth users)
INSERT INTO CW2.[User] (Username, Email, Role)
VALUES
('Ada Lovelace', 'ada@plymouth.ac.uk', 'owner'),
('Tim Berners-Lee', 'tim@plymouth.ac.uk', 'viewer');

--Insert lookup data
--===Category===
INSERT INTO CW2.Category (Category_Name)
VALUES ('Nature'), ('Urban');

--===Difficulty===
INSERT INTO CW2.Difficulty (Difficulty_Name)
VALUES ('Easy'), ('Moderate'), ('Hard');

--===Route_Type===
INSERT INTO CW2.Route_Type (Route_Type)
VALUES ('Circular'), ('Out and Back');

--Insert Features
INSERT INTO CW2.Feature (Feature_Name, Feature_Description)
VALUES
('Waterfall', 'Trail includes a waterfall'),
('Scenic View', 'Panoramic viewpoints along the trail');

--Insert a Trail (owned by Ada)
INSERT INTO CW2.Trail (
    Trail_Name,
    Description,
    Distance,
    Elevation_Gain,
    Estimate_Time,
    Trail_Info,
    Category_ID,
    Difficulty_ID,
    Route_ID,
    User_ID
)
VALUES (
    'Plymbridge Circular',
    'A scenic circular trail through woodland.',
    4.50,
    120,
    90,
    'Popular local trail suitable for most users.',
    1, -- Nature
    2, -- Moderate
    1, -- Circular
    1  -- Ada Lovelace
);

--Insert Trail Points
INSERT INTO CW2.Trail_Point (Trail_ID, Latitude, Longitude, PointOrder)
VALUES
(1, 50.4145, -4.0942, 1),
(1, 50.4151, -4.0930, 2),
(1, 50.4160, -4.0915, 3);

️--Link Features to Trail
INSERT INTO CW2.Trail_Feature (Trail_ID, Feature_ID)
VALUES
(1, 1), -- Waterfall
(1, 2); -- Scenic View
