CREATE PROCEDURE InitDataModel AS

    Create Table Caregivers(
        CaregiverId int IDENTITY PRIMARY KEY,
        CaregiverName varchar(50)
        );

    Create Table Patients(
        PatientID int PRIMARY KEY,
        PatientName varchar(150)
        );

    Create Table CaregiverSchedule(
        SlotID int Identity PRIMARY KEY, 
        CaregiverId int DEFAULT 0 NOT NULL
            CONSTRAINT FK_CareGiverScheduleCaregiverId FOREIGN KEY (caregiverId)
                REFERENCES Caregivers(CaregiverId),
        WorkDay date,
        SlotHour int DEFAULT 0 NOT NULL,
        SlotMinute int DEFAULT 0 NOT NULL,
        );

    Create Table Vaccines(
        VaccineID int PRIMARY KEY,
        VaccineBrand varchar(50), --Moderna, Pfizer, etc. 
        SlotStatus varchar(50)
        );  

    Create Table VaccineAppointment(
        VaccineAppointmentID int PRIMARY KEY,
        PatientID int  DEFAULT 0 NOT NULL
            CONSTRAINT FK_VaccineAppointmentPatientID FOREIGN KEY (PatientID) 
                REFERENCES Patients(PatientID),
        SlotID int DEFAULT 0 NOT NULL
            CONSTRAINT FK_VaccineAppointmentSlotID FOREIGN KEY (SlotID) 
                REFERENCES CaregiverSchedule(SlotID),
        VaccineID int NOT NULL
            CONSTRAINT FK_VaccineAppointmentVaccineID FOREIGN KEY (VaccineID)
                REFERENCES Vaccines(VaccineID)
        );


