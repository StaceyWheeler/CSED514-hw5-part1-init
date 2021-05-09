# This is a copy of vaccine_caregiver to use as a template
# You will design and build the Python code to instantiate instances of the 
# COVID19Vaccine class associated with each type of vaccine the health organization 
# maintains a supply of and wants to distribute to its patients. 
# This code file must be named COVID19_vaccine.py. In addition to its __init__ routine 
# that inserts an entry into the Vaccine Table for each particular brand of vaccine the 
# health organization maintains an inventory for, your COVID19Vaccine needs to support 
# the following methods
# AddDoses() which is called to add doses to the vaccine inventory for a particular vaccine
# ReserveDoses() which is called to reserve the vaccine doses associated with a 
# specific patient who is being scheduled for vaccine administration.

from datetime import datetime
from datetime import timedelta
import pymssql


class COVID19Vaccine:
    ''' Adds the Vaccine to the DB '''
    def __init__(self, VaccineBrand, cursor):
        self.sqltext = "INSERT INTO Vaccines (VaccineBrand) VALUES ('" + VaccineBrand + "')"
        self.VaccineId = 0
        try: 
            cursor.execute(self.sqltext)
            cursor.connection.commit()
            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.VaccineId = _identityRow['Identity']
            # cursor.connection.commit()
            print('Query executed successfully. Vaccine : ' + name 
            +  ' added to the database using Vaccine ID = ' + str(self.caregiverId))
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Vaccines! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext)

# Below here is all template code, not edited for COVID19Vaccine class
        _weeks_to_schedule = []
        _now = datetime.now()
        _weeks_to_schedule.append(_now)
        _one_week_time_delta = timedelta(days=7)
        _weeks_ahead = 4
        _lcv = 0
        while _lcv < _weeks_ahead:
            _now = _now + _one_week_time_delta
            _weeks_to_schedule.append(_now)
            _lcv = _lcv + 1

        _formatstring = "%Y-%m-%d"

        for _day in _weeks_to_schedule:
            _formattedDate = _day.strftime(_formatstring)
            # print (_formattedDate)

            for _hr in _hoursToSchedlue:
                _startTime = 0
                while _startTime < 60:
                    _sqltext2 = ("INSERT INTO CareGiverSchedule (caregiverid, WorkDay, SlotHour, SlotMinute) VALUES (") 
                    _sqltext2 += str(self.caregiverId) + ", '" + _formattedDate + "', " 
                    _sqltext2 += str(_hr) + ", "  
                    _sqltext2 += str(_startTime) + ")" 
                    try:
                        cursor.execute(_sqltext2)
                        _startTime = _startTime + _appointmentDuration
                    except pymssql.Error as db_err:
                        print("Database Programming Error in SQL Query processing for CareGiver scheduling slots! ")
                        print("Exception code: " + str(db_err.args[0]))
                        if len(db_err.args) > 1:
                            print("Exception message: " + db_err.args[1]) 
                        print("SQL text that resulted in an Error: " + _sqltext2)
        cursor.connection.commit()

 #Methods to fill in for COVID19Vaccine class   
    def AddDoses(self, cursor):
        return None

    def ReserveDoses(self, cursor):
        return None