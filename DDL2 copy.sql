-- Drop existing tables if they exist
DROP TABLE IF EXISTS Payment, Billing, Equipment, Room, ClassSchedule, Session, Availability, AdminStaff, Trainer, Member CASCADE;

-- Create tables in the correct order of dependency
CREATE TABLE Member (
    MemberID SERIAL PRIMARY KEY,
    FullName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Weight_goal TEXT,
    Weight TEXT
);

CREATE TABLE Trainer (
    TrainerID SERIAL PRIMARY KEY,
    FullName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL
);

CREATE TABLE AdminStaff (
    StaffID SERIAL PRIMARY KEY,
    FullName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL
);

CREATE TABLE Room (
    RoomID SERIAL PRIMARY KEY,
    RoomName VARCHAR(255) NOT NULL,
    Capacity INTEGER NOT NULL
);

CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    MaintenanceSchedule DATE
);

CREATE TABLE Session (
    SessionID SERIAL PRIMARY KEY,
    MemberID INTEGER REFERENCES Member(MemberID),
    TrainerID INTEGER REFERENCES Trainer(TrainerID),
    DateTime TIMESTAMP NOT NULL,
    Duration INTERVAL,
    Status VARCHAR(50) CHECK (Status IN ('Scheduled', 'Completed', 'Cancelled'))
);

CREATE TABLE Billing (
    BillID SERIAL PRIMARY KEY,
    MemberID INTEGER REFERENCES Member(MemberID),
    Amount DECIMAL(10, 2) NOT NULL,
    DueDate DATE NOT NULL,
    SessionID INTEGER REFERENCES Session(SessionID)  -- Link to Session table
);

CREATE TABLE Payment (
    PaymentID SERIAL PRIMARY KEY,
    BillID INTEGER UNIQUE REFERENCES Billing(BillID),
    PaymentMethod VARCHAR(255) NOT NULL,
    PaymentDate TIMESTAMP NOT NULL
);

CREATE TABLE ClassSchedule (
    ClassID SERIAL PRIMARY KEY,
    ClassName VARCHAR(255) NOT NULL,
    TrainerID INTEGER NOT NULL REFERENCES Trainer(TrainerID),
    RoomID INTEGER NOT NULL REFERENCES Room(RoomID),
    Day VARCHAR(10) NOT NULL,
    StartTime TIME NOT NULL,
    EndTime TIME NOT NULL,
    CONSTRAINT chk_day CHECK (Day IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))
);

CREATE TABLE Availability (
    AvailabilityID SERIAL PRIMARY KEY,
    TrainerID INTEGER NOT NULL REFERENCES Trainer(TrainerID),
    Day VARCHAR(10) NOT NULL CHECK (Day IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))
);
