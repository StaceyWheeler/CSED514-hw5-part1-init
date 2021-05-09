-- Given CREATE TABLE statements to start your database

Create Table Caregivers(
	CaregiverId int IDENTITY PRIMARY KEY,
	CaregiverName varchar(50)
	);

Create Table AppointmentStatusCodes(
	StatusCodeId int PRIMARY KEY,
	StatusCode   varchar(30)
	);

INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (0, 'Open');
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (1, 'OnHold');
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (2, 'Scheduled');
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (3, 'Completed');
INSERT INTO AppointmentStatusCodes (statusCodeId, StatusCode)
	VALUES (4, 'Missed');

Create Table VaccineAppointment(
	VaccineAppointmentId int PRIMARY KEY,
	StatusCodeId int  DEFAULT 0 NOT NULL
		CONSTRAINT FK_AppointmentStatusCode FOREIGN KEY (StatusCodeId) 
		     REFERENCES AppointmentStatusCodes(StatusCodeId)
	);

Create Table CareGiverSchedule(
	CaregiverSlotSchedulingId int Identity PRIMARY KEY, 
	CaregiverId int DEFAULT 0 NOT NULL
		CONSTRAINT FK_CareGiverScheduleCaregiverId FOREIGN KEY (caregiverId)
			REFERENCES Caregivers(CaregiverId),
	WorkDay date,
	--SlotTime time,
	SlotHour int DEFAULT 0 NOT NULL,
	SlotMinute int DEFAULT 0 NOT NULL,
	SlotStatus int  DEFAULT 0 NOT NULL
		CONSTRAINT FK_CaregiverStatusCode FOREIGN KEY (SlotStatus) 
		     REFERENCES AppointmentStatusCodes(StatusCodeId),
	VaccineAppointmentId int DEFAULT 0 NOT NULL
		CONSTRAINT FK_CaregiverAppointmentCode FOREIGN KEY (VaccineAppointmentId)
			REFERENCES VaccineAppointment(VaccineAppointmentId)
	);

Create Table Vaccines(
	VaccineId int,
	VaccineName varchar(50),
	VaccineAppointmentId int DEFAULT 0 NOT NULL
		CONSTRAINT FK_VaccineAppointmentCode FOREIGN KEY (VaccineAppointmentId)
			REFERENCES VaccineAppointment(VaccineAppointmentId)
	PRIMARY KEY (VaccineId, VaccineName)
	);
--https://stackoverflow.com/questions/1750335/can-sql-table-have-multiple-columns-with-primary-key/1750347#:~:text=If%20you%20mean%20%22can%20a,%22%2C%20the%20answer%20is%20yes.&text=A%20table%20can%20have%20just,col1%2C%20col2%2C%20col3)%20)%3B

Create Table Patients(
	PatientId int PRIMARY KEY,
	PatientName varchar(150),
	VaccineAppointmentId int DEFAULT 0 NOT NULL
		CONSTRAINT FK_PatientAppointmentCode FOREIGN KEY (VaccineAppointmentId)
			REFERENCES VaccineAppointment(VaccineAppointmentId)
	);

-- Additional helper code for your use if needed

-- --- Drop commands to restructure the DB
-- Drop Table CareGiverSchedule
-- Drop Table AppointmentStatusCodes
-- Drop Table Caregivers
-- Go

-- --- Commands to clear the active database Tables for unit testing
-- Truncate Table CareGiverSchedule
-- DBCC CHECKIDENT ('CareGiverSchedule', RESEED, 0)
-- Delete From Caregivers
-- DBCC CHECKIDENT ('Caregivers', RESEED, 0)
-- GO
