from enum import IntEnum
import os
import pymssql
import traceback

from sql_connection_manager import SqlConnectionManager
from vaccine_caregiver import VaccineCaregiver
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as covid
from vaccine_patient import VaccinePatient as patient


class VaccineReservationScheduler:

    def __init__(self):
        pass

    def PutHoldOnAppointmentSlot(self, cursor):
        ''' Method that reserves a CareGiver appointment slot &
        returns the unique scheduling slotid
        Should return -2 if no slot is available  or -1 if there is a database error'''
        self.slotSchedulingId = -2
        self.getAppointmentSQL = "SELECT TOP (1)* FROM CaregiverSchedule WHERE SlotStatus = 0 ORDER BY WorkDay, SlotHour, SlotMinute ASC"
        try:
            cursor.execute(self.getAppointmentSQL)
            row = cursor.fetchone()
            if row != None:
                self.slotSchedulingId = row['CaregiverSlotSchedulingId']
                cursor.connection.commit()
            else:
                print('Appointment slot unavailable. Please try again later.')
                cursor.connection.rollback()

        
        except pymssql.Error as db_err:
            db_err_handler('CareGiverSchedule', self.getAppointmentSQL, db_err, cursor)
            return -1

        if self.slotSchedulingId != -2:
            putApptOnHoldSqlText = "UPDATE CareGiverSchedule SET SlotStatus = 1 WHERE CaregiverSlotSchedulingId = %s"
            try:
                cursor.execute(putApptOnHoldSqlText, str(self.slotSchedulingId))
                cursor.connection.commit()
                print('Query executed successfully. Appointment has been added to the schedule.')
            except pymssql.Error as db_err:
                db_err_handler('CareGiverSchedule', putApptOnHoldSqlText, db_err, cursor)


        cursor.connection.commit()
        return self.slotSchedulingId

    def ScheduleAppointmentSlot(self, slotid, cursor):
        '''method that marks a slot on Hold with a definite reservation  
        slotid is the slot that is currently on Hold and whose status will be updated 
        returns the same slotid when the database update succeeds 
        returns 0 is there if the database update dails 
        returns -1 the same slotid when the database command fails
        returns -2 if the slotid parm is invalid '''

        if slotid < 1:
            return -2
        self.slotSchedulingId = slotid

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

            # Add 5 doses of Moderna
            
            covid_obj_Moderna = covid('Moderna', 2, 28, dbcursor)
            covid_obj_Moderna.AddDoses('Moderna', 5, dbcursor)

            vrs = VaccineReservationScheduler()
            cgid = vrs.PutHoldOnAppointmentSlot(dbcursor)

            # Add 3 patients

            patient_1 = patient('Snow White', dbcursor)
            patient_2 = patient('Robin Hood', dbcursor)
            patient_3 = patient('Peter Rabbit', dbcursor)

            # Patient3 Will fail- insufficient doses

            for pat in [patient_1, patient_2, patient_3]:
                schedid = vrs.PutHoldOnAppointmentSlot(dbcursor)
                if schedid != -2:
                    pat.ReserveAppointment(schedid, 'Moderna', dbcursor)
                    appt_ids = pat.apptids
                    pat.ScheduleAppointment(appt_ids, dbcursor)

            
            # Test cases done!
            # clear_tables(sqlClient)
