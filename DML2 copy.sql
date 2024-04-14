-- Insert Members
INSERT INTO Member (FullName, Email, Password, Weight_goal, Weight) VALUES
('John Doe', 'john.doe@example.com', 'johnsSecurePassword123', 'Lose 20 pounds', '200 pounds'),
('Alice Johnson', 'alice.johnson@example.com', 'alicesSecurePassword123', 'Run a marathon', '150 pounds');

-- Insert Trainers
INSERT INTO Trainer (FullName, Email, Password) VALUES
('Bob Smith', 'bob.smith@example.com', 'bobSecurePassword123'),
('Carol Taylor', 'carol.taylor@example.com', 'carolSecurePassword123');

-- Insert Admin Staff
INSERT INTO AdminStaff (FullName, Email, Password) VALUES
('David Admin', 'david.admin@example.com', 'davidSecurePassword123');

-- Insert Rooms
INSERT INTO Room (RoomName, Capacity) VALUES
('Room A', 20),
('Room B', 30);

-- Insert Equipment
INSERT INTO Equipment (Name, MaintenanceSchedule) VALUES
('Treadmill', '2023-12-01'),
('Elliptical', '2023-12-15');

-- Insert Billing (Initially no PaymentID)
INSERT INTO Billing (MemberID, Amount, DueDate) VALUES
(1, 100.00, '2023-12-01'),
(2, 150.00, '2023-12-15');

-- Insert Payments (Initially no link to Billing)
INSERT INTO Payment (BillID, PaymentMethod, PaymentDate) VALUES
(1, 'Credit Card', '2023-01-02 12:34:56');

-- Link Payment to Billing
UPDATE Billing SET PaymentID = 1 WHERE BillID = 1;

-- Insert Sessions
INSERT INTO Session (MemberID, TrainerID, DateTime, Duration, Status) VALUES
(1, 1, '2023-10-03 10:00:00', INTERVAL '1 hour', 'Scheduled'),
(2, 2, '2023-10-04 14:00:00', INTERVAL '2 hours', 'Scheduled');

-- Insert Class Schedules
INSERT INTO ClassSchedule (ClassName, TrainerID, RoomID, Day, StartTime, EndTime) VALUES
('Yoga Basics', 1, 1, 'Monday', '08:00:00', '09:00:00'),
('Advanced Pilates', 2, 2, 'Tuesday', '15:00:00', '16:30:00');

-- Insert Availability for Trainers
INSERT INTO Availability (TrainerID, Day) VALUES
(1, 'Monday'),
(1, 'Wednesday'),
(1, 'Friday'),
(2, 'Tuesday'),
(2, 'Thursday');
