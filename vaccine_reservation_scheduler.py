import datetime
from enum import IntEnum
import os
import pymssql
import traceback

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as covid
from vaccine_patient_wip import VaccinePatient as patient


class VaccineReservationScheduler:

    def __init__(self):
        pass

    def PutHoldOnAppointmentSlot(self, cursor):
        ''' Method that reserves a CareGiver appointment slot &
        returns the unique scheduling slotid
        Should return 0 if no slot is available  or -1 if there is a database error'''
        # Note to students: this is a stub that needs to replaced with your code
        self.slotSchedulingId = 0
        self.getAppointmentSQL = "SELECT TOP (1)* FROM CaregiverSchedule WHERE SlotStatus = 0 ORDER BY WorkDay, SlotHour, SlotMinute"
        try:
            cursor.execute(self.getAppointmentSQL)
            cursor.connection.commit()
            cursor.execute("SELECT @@IDENTITY AS 'Identity';")
            _identityRow = cursor.fetchone()
            self.slotSchedulingId = _identityRow['Identity']
            #print(self.slotSchedulingId)
            cursor.connection.commit()
            #return self.slotSchedulingId
        
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])           
            print("SQL text that resulted in an Error: " + self.getAppointmentSQL)
            cursor.connection.rollback()
            return -1

        if self.slotSchedulingId != 0:
            putApptOnHoldSqlText = "UPDATE CaregiverSchedule SET SlotStatus = 1 WHERE CaregiverId = %s"
            try:
                cursor.execute(putApptOnHoldSqlText, str(self.slotSchedulingId))
                cursor.connection.commit()
                #print(self.slotSchedulingId)
                print('Query executed successfully. Appointment has been added to the schedule.')
            except pymssql.Error as db_err:
                print("Database Programming Error in SQL Query processing for VaccinePatients! ")
                print("Exception code: " + str(db_err.args[0]))
                if len(db_err.args) > 1:
                    print("Exception message: " + str(db_err.args[1]))
                print("SQL text that resulted in an Error: " + self.sqltext)

        cursor.connection.commit()
        return self.slotSchedulingId

    def ScheduleAppointmentSlot(self, slotid, cursor):
        '''method that marks a slot on Hold with a definite reservation  
        slotid is the slot that is currently on Hold and whose status will be updated 
        returns the same slotid when the database update succeeds 
        returns 0 is there if the database update dails 
        returns -1 the same slotid when the database command fails
        returns -2 if the slotid parm is invalid '''
        # Note to students: this is a stub that needs to replaced with your code
        if slotid < 1:
            return -2
        self.slotSchedulingId = slotid
        #getAppointmnetSQL should grab the first available appointment from the CaregiverSchedule.
        #Do we need to do a join on CaregiverSchedule and AppointmentStatusCode? 
        self.getAppointmentSQL = "SELECT TOP 1 * FROM CaregiverSchedule WHERE SlotStatus = "
        try:
            cursor.execute(self.getAppointmentSQL)
            return self.slotSchedulingId
        except pymssql.Error as db_err:    
            print("Database Programming Error in SQL Query processing! ")
            print("Exception code: " + db_err.args[0])
            if len(db_err.args) > 1:
                print("Exception message: " + str(db_err.args[1]))  
            print("SQL text that resulted in an Error: " + self.getAppointmentSQL)
            return -1

        #We still need to mark the appointment OnHold... where to do that? In the select statement?

if __name__ == '__main__':
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            clear_tables(sqlClient)

            # get a cursor from the SQL connection
            dbcursor = sqlClient.cursor(as_dict=True)



            # Iniialize the caregivers, patients & vaccine supply
            caregiversList = []
            caregiversList.append(VaccineCaregiver('Carrie Nation', dbcursor))
            caregiversList.append(VaccineCaregiver('Clare Barton', dbcursor))
            caregivers = {}
            for cg in caregiversList:
                cgid = cg.caregiverId
                caregivers[cgid] = cg

            vrs = VaccineReservationScheduler()
            cgid = vrs.PutHoldOnAppointmentSlot(dbcursor)
            print(cgid)

            patient_obj = patient('Snow White', dbcursor)
            patient_obj.ReserveAppointment(cgid, 'Moderna', dbcursor)
            appt_ids = patient_obj.apptids
            print(appt_ids)
            patient_obj.ScheduleAppointment(appt_ids, dbcursor)

            # Testing out adding rows to Vaccines and AddDoses:
            covid_obj_Moderna = covid('Moderna', 2, 28, dbcursor)
            covid_obj_Moderna.AddDoses('Moderna', 20, dbcursor)
            
            # Testing out ReserveDoses:
            # covid_obj_Moderna = covid('Moderna', 2, 28, dbcursor)
            # covid_obj_Moderna.ReserveDoses('Moderna', dbcursor)

            # Vaccines table is populated with Moderna vaccines. Let's reserve one
            #new_patient=patient('John Doe', dbcursor) # Adds John Doe to the Patients table with VaccineStatus=0
            #new_patient.ReserveAppointment(1, 'Moderna', dbcursor)

            
            # Test cases done!
            clear_tables(sqlClient)
