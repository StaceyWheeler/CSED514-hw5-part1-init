from datetime import datetime
from datetime import timedelta
import pymssql



class VaccinePatient:

    def __init__(self, name, cursor):
        """
        Adds new Patient to Patients table
        """
        self.name = name
        self.sqltext = "INSERT INTO Patients (PatientName, VaccineStatus) VALUES ('" + name + "', 0)"
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



    def ReserveAppointment(self, CaregiverScheduleID, vaccine_name, cursor):

        def get_caregiver_item(SlotId, cursor, col_name = None):
            """
            Helper to return sql query
            """
            sqltext = "SELECT * FROM CareGiverSchedule WHERE CaregiverSlotSchedulingId = " + str(SlotId)
            cursor.execute(sqltext)
            row = cursor.fetchone()
            
            if col_name:
                res = row[col_name]
            else:
                res = row
        
            return res

        def check_is_hold(SlotId, cursor):
            """
            Helper to check whether CareGiverSlotID == Hold
            """
            slot_status = get_caregiver_item(SlotId, cursor, col_name='SlotStatus')

            return slot_status == 1
        
        def check_dose_avail(vaccine, n, cursor):
            """
            Helper to check whether vaccine inventory is available
            """

            sqltext = "SELECT * FROM Vaccines WHERE VaccineName = " + "'" + vaccine + "'"
            cursor.execute(sqltext)
            row = cursor.fetchone()

            return row['AvailableDoses'] >= n

        # First check that SlotID == Hold
        slotids = []
        appt_days = []
        is_hold = check_is_hold(CaregiverScheduleID, cursor)
        if is_hold:
            slotids.append(CaregiverScheduleID)
        appt_day = get_caregiver_item(CaregiverScheduleID, cursor, col_name='WorkDay')
        appt_days.append(appt_day)

        # Check the dosage needed for this vaccine

        vaccineSqlText = "SELECT * FROM Vaccines WHERE VaccineName = %s"
        cursor.execute(vaccineSqlText, (vaccine_name))
        vaccineRow = cursor.fetchone()
        dosage = vaccineRow['DosesPerPatient']
        dates_avail = False

        # Check whether dosage inventory is sufficient

        if check_dose_avail(vaccine_name, dosage, cursor):

            if dosage > 1:

                # Need to verify second appointment

                days_out = timedelta(days = vaccineRow['DaysBetweenDoses'])
                appt_day_2 = (datetime.strptime(appt_day, '%Y-%m-%d') + days_out) # keep this in datetime
                cgSqlText = "SELECT * FROM CareGiverSchedule WHERE WorkDay = '" + appt_day_2.strftime('%Y-%m-%d') + "'"
                cursor.execute(cgSqlText)
                cgRows = cursor.fetchall()
                second_avail = False
                for cgRow in cgRows:
                    if cgRow['SlotStatus'] == 0:
                        cg_slot_2 = cgRow['CaregiverSlotSchedulingId']
                        second_avail = True
                        slotids.append(cg_slot_2)
                        appt_days.append(appt_day_2)
                        break
                
                # Both dates are available
                dates_avail = is_hold * second_avail
                # print('is_hold: ', is_hold)
                # print('dates_avail: ', dates_avail)

            
            else:
                # Just first date is available
                dates_avail = is_hold
        
            if dates_avail:

                try:

                    for i, slotid in enumerate(slotids):
                        sql_res = get_caregiver_item(slotid, cursor)
                        careGiverID = str(sql_res['CaregiverId'])
                        VaccineName = vaccine_name
                        PatientId = str(self.patientid)
                        ReservationDate = str(appt_days[i])
                        # print('ReservationDate: ', ReservationDate)
                        ReservationStartHour = str(sql_res['SlotHour'])
                        ReservationStartMinute = str(sql_res['SlotMinute'])
                        AppointmentDuration = str(15)
                        SlotStatus = str(i*3 + 1)# 0 if i = 0; 4 if i = 1
                        self.sqltext_reserve = """
                        INSERT INTO VaccineAppointments(
                            VaccineName, 
                            PatientId, 
                            CaregiverId, 
                            ReservationDate, 
                            ReservationStartHour, 
                            ReservationStartMinute, 
                            AppointmentDuration, 
                            SlotStatus) VALUES(
                            """
                        self.sqltext_reserve += "'" + VaccineName + "'" + "," + PatientId + "," + careGiverID + ","
                        self.sqltext_reserve += "'" + ReservationDate + "'" + "," + ReservationStartHour + "," + ReservationStartMinute + ","
                        self.sqltext_reserve +=  AppointmentDuration + "," + SlotStatus + ")"
                        cursor.execute(self.sqltext_reserve)
                        cursor.connection.commit()
                        cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
                        _identityRow = cursor.fetchone()
                        self.apptids.append(_identityRow['Identity'])
                
                except pymssql.Error as db_err:
                    print("Database Programming Error in SQL Query processing for VaccinePatients! ")
                    print("Exception code: " + str(db_err.args[0]))
                    if len(db_err.args) > 1:
                        print("Exception message: " + str(db_err.args[1]))
                    print("SQL text that resulted in an Error: " + self.sqltext_reserve)
            
            else:
                print("Unable to reserve appointment for Patient ", self.name, ". Caregiver unavailable.")
        
        else:
            print("Unable to reserve appointment for Patient ", self.name, ". Unable to reserve sufficient doses.")

    def ScheduleAppointment(self, VaccineAppointmentId, cursor):
        # ScheduleAppointment() marks the appointments as “Scheduled” -> VaccineAppointments (SlotStatus) to 2 
        # update the Patient’s VaccineStatus field -> Patients (VaccineStatus) to 2
        # maintain the Vaccine inventory -> Vaccines (AvailableDoses) -= 1, Vaccines (ReservedDoses) -= 1
        # update the CaregiverSchedule Table -> CaregiverSchedule (SlotStatus) to 2
        # and any additional tasks required to schedule the appointments for the Caregiver  to administer the vaccine doses to the Patient, ensuring that the database properly reflects the Scheduling Actions.
        
        for i, slotid in enumerate(VaccineAppointmentId):
            
            slotstatus = str(i*3 + 2) # 2 if 0, 5 if 1
            apptSqlText = "SELECT * FROM VaccineAppointments WHERE VaccineAppointmentId = %s"
            cursor.execute(apptSqlText, str(slotid))
            appt_info = cursor.fetchone()
            # print(appt_info)
            appt_id = str(self.apptids[i])
            patient_id = str(appt_info['PatientId'])
            vaccine_name = appt_info['VaccineName']
            caregiver_id = str(appt_info['CaregiverId'])
            vaccineApptSqlText = "UPDATE VaccineAppointments SET SlotStatus = 2 WHERE VaccineAppointmentId = " + appt_id
            patientSqlText = "UPDATE Patients SET VaccineStatus = " + slotstatus + "WHERE PatientId = " + patient_id
            vaccineInventorySqlText = "UPDATE Vaccines SET AvailableDoses = AvailableDoses - 1, ReservedDoses = ReservedDoses + 1 WHERE VaccineName = " + "'" + vaccine_name + "'"
            cgSchedSqlText = "UPDATE CaregiverSchedule SET SlotStatus = 2 WHERE VaccineAppointmentId = " + appt_id

            for sqltext in [vaccineApptSqlText, patientSqlText, vaccineInventorySqlText, cgSchedSqlText]:
                try:
                    cursor.execute(sqltext)
                    cursor.connection.commit()
                    print('Updated ', sqltext.split(" ")[1], "table for Appointment ", i+1, "for Patient ", self.name)
                except pymssql.Error as db_err:
                    print("Database Programming Error in SQL Query processing!")
                    print("Exception code: " + str(db_err.args[0]))
                    if len(db_err.args) > 1:
                        print("Exception message: " + str(db_err.args[1]))
                    print("SQL text that resulted in an Error: " + sqltext)


        cursor.connection.commit()