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
                    self.schedid = vrs.PutHoldOnAppointmentSlot(cursor)
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


        self.sqlClient = SqlConnectionManager(
            Server=os.getenv("Server"),
            DBname=os.getenv("DBName"),
            UserId=os.getenv("UserID"),
            Password=os.getenv("Password"))
        self.cursor = self.sqlClient.cursor(as_dict = True)
        
        clear_tables(self.sqlClient)

        try:

            self.moderna = covid('Moderna', 2, 28, self.cursor)
            self.caregiver1 = caregiver('Annie Wilkes', self.cursor)
            self.schedid = vrs.PutHoldOnAppointmentSlot(self.cursor)
            # clear the tables before testing
            # clear_tables(self.sqlClient)
            # create a new Patient object
            self.patient1 = patient('Hercule Poirot', self.cursor)
            pid = self.patient1.patientid

            # reserve appointment for Patient 1
            self.patient1.ReserveAppointment(self.schedid, 'Moderna', self.cursor)

            sqlQuery = '''
                        SELECT *
                        FROM VaccinesAppointments
                        WHERE PatientId = %s
                        '''
            self.cursor.execute(sqlQuery, str(pid))
            rows = self.cursor.fetchall()
            if len(rows) < 1:
                self.fail("Failed to reserve appointment")
            else:
                for row in rows:
                    slotstatus = row['SlotStatus']
                    if slotstatus not in [1, 4]:
                        self.fail("Failed to reserve appointment")

            # clear the tables after testing, just in-case
            clear_tables(self.sqlClient)
        except Exception:
            # clear the tables if an exception occurred
            clear_tables(self.sqlClient)
            self.fail("Failed to reserve appointment")

            

if __name__ == '__main__':
    unittest.main()