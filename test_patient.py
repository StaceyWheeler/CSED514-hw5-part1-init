import unittest
import os
import pymssql
from sql_connection_manager import SqlConnectionManager
from enums import *
from utils import *
from vaccine_patient_wip import VaccinePatient as patient
from COVID19_vaccine import COVID19Vaccine as covid
from vaccine_caregiver import VaccineCaregiver as caregiver
from vaccine_reservation_scheduler import VaccineReservationScheduler as vrs


class TestVaccinePatient(unittest.TestCase):

    def test_init(self):

        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                clear_tables(sqlClient)

                try:
                    self.moderna = covid('Moderna', 2, 28, cursor)
                    self.caregiver1 = caregiver('Annie Wilkes', cursor)
                    vrs_obj = vrs()
                    self.schedid = vrs_obj.PutHoldOnAppointmentSlot(cursor)
                    # clear the tables before testing
                    # clear_tables(self.sqlClient)
                    # create a new Patient object
                    self.patient1 = patient('Hercule Poirot', cursor)
                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                                SELECT *
                                FROM Patients
                                WHERE PatientName = 'Hercule Poirot'
                                '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail('Creating patient object failed')
                    # clear the tables 
                    clear_tables(sqlClient)
        
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating patient object failed")
    
    def test_reserve_appointment(self):


        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
        
                clear_tables(sqlClient)

                try:

                    self.moderna = covid('Moderna', 2, 28, cursor)
                    self.moderna.AddDoses('Moderna', 5, cursor)
                    self.caregiver1 = caregiver('Annie Wilkes', cursor)
                    vrs_obj = vrs()
                    self.schedid = vrs_obj.PutHoldOnAppointmentSlot(cursor)
                    # clear the tables before testing
                    # clear_tables(self.sqlClient)
                    # create a new Patient object
                    self.patient1 = patient('Hercule Poirot', cursor)
                    #pid = self.patient1.patientid

                    # reserve appointment for Patient 1
                    self.patient1.ReserveAppointment(self.schedid, 'Moderna', cursor)

                    sqlQuery = "SELECT v.* FROM VaccineAppointments v, Patients p WHERE v.PatientId = p.PatientId"
                    #cursor.execute(sqlQuery, (str(pid)))
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Failed to reserve appointment")
                    else:
                        for row in rows:
                            slotstatus = row['SlotStatus']
                            if slotstatus not in [1, 4]:
                                self.fail("Failed to reserve appointment")

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Failed to reserve appointment")


    def test_schedule_appointment(self):

        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
        
                clear_tables(sqlClient)

                try:

                    self.moderna = covid('Moderna', 2, 28, cursor)
                    self.moderna.AddDoses('Moderna', 5, cursor)
                    self.caregiver1 = caregiver('Annie Wilkes', cursor)
                    vrs_obj = vrs()
                    self.schedid = vrs_obj.PutHoldOnAppointmentSlot(cursor)
                    # clear the tables before testing
                    # clear_tables(self.sqlClient)
                    # create a new Patient object
                    self.patient1 = patient('Hercule Poirot', cursor)
                    #pid = self.patient1.patientid

                    # reserve and schedule appointment for Patient 1
                    self.patient1.ReserveAppointment(self.schedid, 'Moderna', cursor)
                    appt_ids = self.patient1.apptids
                    self.patient1.ScheduleAppointment(appt_ids, cursor)

                    sqlQuery = "SELECT v.* FROM VaccineAppointments v, Patients p WHERE v.PatientId = p.PatientId"
                    #cursor.execute(sqlQuery, (str(pid)))
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Failed to reserve appointment")
                    else:
                        for row in rows:
                            slotstatus = row['SlotStatus']
                            if slotstatus not in [2]:
                                self.fail("Failed to reserve appointment")

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Failed to reserve appointment")


    def test_insufficient_doses(self):

        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
        
                clear_tables(sqlClient)

                try:

                    self.moderna = covid('Moderna', 2, 28, cursor)
                    self.moderna.AddDoses('Moderna', 5, cursor)
                    self.caregiver1 = caregiver('Annie Wilkes', cursor)
                    vrs_obj = vrs()
                    self.schedid = vrs_obj.PutHoldOnAppointmentSlot(cursor)
                    # clear the tables before testing
                    # clear_tables(self.sqlClient)
                    # create a new Patient object
                    self.patient_1 = patient('Snow White', cursor)
                    self.patient_2 = patient('Robin Hood', cursor)
                    self.patient_3 = patient('Peter Rabbit', cursor)
                    #pid = self.patient1.patientid

                    for pat in [self.patient_1, self.patient_2, self.patient_3]:
                        schedid = vrs_obj.PutHoldOnAppointmentSlot(cursor)
                        if schedid != -2:
                            pat.ReserveAppointment(schedid, 'Moderna', cursor)
                            appt_ids = pat.apptids
                            pat.ScheduleAppointment(appt_ids, cursor)

                    sqlQuery = "SELECT * FROM VaccineAppointments"
                    #cursor.execute(sqlQuery, (str(pid)))
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Failed to reserve appointment")
                    else:
                        for row in rows:
                            scheduled_patientid = row['PatientId']
                            if scheduled_patientid == 3:
                                self.fail("Failed due to scheduling appointment despite insufficient doses.")

                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Failed to reserve appointment")
            

if __name__ == '__main__':
    unittest.main()