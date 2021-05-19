from datetime import datetime
from datetime import timedelta
import pymssql



class VaccinePatient:

    def __init__(self, name, cursor):
        """
        Adds new Patient to Patients table
        """
        self.sqltext = "INSERT INTO Patients (PatientName, VaccineStatus) VALUES ('" + name + ", 0')"
        self.patientid = 0
        self.apptids = []
        try:
            cursor.execute(self.sqltext)
            cursor.connection.commit()
            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.patientid = _identityRow['Identity']
            print('Query executed successfully. Patient : ' + name 
            +  ' added to the database using Patient ID = ' + str(self.patientid))
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Patients! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext)
        cursor.connection.commit()



    def ReserveAppointment(self, CaregiverScheduleID, Vaccine, cursor):

        def get_caregiver_item(SlotId, cursor, col_name = None):
            """
            Helper to return sql query
            """
            sqltext = "'SELECT * FROM CareGiverSchedule WHERE CaregiverSlotSchedulingId = " + str(SlotId) + "'"
            cursor.execute(sqltext)
            row = cursor.fetchone()
            
            if all:
                res = row
            else:
                res = row[col_name]
        
            return res

        def check_is_hold(SlotId, cursor):
            """
            Helper to check whether CareGiverSlotID == Hold
            """
            slot_status = get_caregiver_item(SlotId, cursor, col_name='SlotStatus')

            return slot_status == 1

        # First check that SlotID == Hold
        slotids = []
        appt_days = []
        is_hold = check_is_hold(CaregiverScheduleID, cursor)
        if is_hold:
            slotids.append(CaregiverScheduleID)
        appt_day = get_caregiver_item(CaregiverScheduleID, cursor, col_name='WorkDay')
        appt_days.append(appt_day)

        # Check the dosage needed for this vaccine

        vaccineSqlText = "'SELECT * FROM Vaccines WHERE VaccineName = " + Vaccine + "'"
        cursor.execute(vaccineSqlText)
        vaccineRow = cursor.fetchone()
        dosage = vaccineRow['DosesPerPatient']
        dates_avail = False

        if dosage > 1:

            # Need to verify second appointment

            days_out = timedelta(days = vaccineRow['DaysBetweenDoses'])
            appt_day_2 = datetime.strptime(appt_day) + days_out # Probably need to fix this to account for datetime
            cgSqlText = "'SELECT * FROM CareGiverSchedule WHERE WorkDay = " + appt_day_2 + "'"
            cursor.execute(cgSqlText)
            cgRows = cursor.fetchall()
            second_avail = False
            for cgRow in cgRows:
                if cgRow['SlotStatus'] == 0:
                    cg_slot_2 = cgRow['CaregiverSlotScheduleingId']
                    second_avail = True
                    slotids.append(cg_slot_2)
                    appt_days.append(appt_day_2)
                    break
            
            # Both dates are available
            dates_avail = is_hold * second_avail

        
        else:
            # Just first date is available
            dates_avail = is_hold
        
        if dates_avail:

            for i, slotid in enumerate(slotids):
                sql_res = get_caregiver_item(slotid, cursor)
                careGiverID = sql_res['CaregiverId']
                VaccineName = Vaccine
                PatientId = self.patientid
                ReservationDate = appt_days[i]
                ReservationStartHour = sql_res['SlotHour']
                ReservationStartMinute = sql_res['SlotMinute']
                AppointmentDuration = 15
                SlotStatus = i*3 + 1 # 0 if i = 0; 4 if i = 1
                sqltext_cols = "'INSERT INTO VaccineAppointments(VaccineName, PatientId, CaregiverId, ReservationDate, ReservationStartHour, ReservationStartMinute, AppointmentDuration, SlotStatus)"
                sqltext_vals = "VALUES("+ VaccineName + "," + PatientId + "," + careGiverID + "," + ReservationDate + "," + ReservationStartHour + "," + ReservationStartMinute + "," + AppointmentDuration + "," + SlotStatus + ")'"
                cursor.execute(sqltext_cols + sqltext_vals)
                cursor.connection.commit()
                cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
                _identityRow = cursor.fetchone()
                self.apptids.append(_identityRow['Identity'])


    def ScheduleAppointment(self, cursor):

        return None