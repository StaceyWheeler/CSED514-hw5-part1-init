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
    # There will be an instance of COVID19Vaccine for each brand
    def __init__(self, VaccineBrand, cursor):
        self.VaccineBrand = VaccineBrand

    # For adding new inventory to the table, user can call AddDoses with the instance corresponding to the brand 
    # (e.g. Moderna.AddDoses(500) will add 500 rows of Moderna vaccines with status default to Available)
    def AddDoses(self, num_doses, cursor):
    
        self.sqltext = "INSERT INTO Vaccines (VaccineBrand) VALUES ('" + self.VaccineBrand + "')"
        self.VaccineId = 0
        
        for _ in range(0, num_doses):
            try: 
                cursor.execute(self.sqltext)
                cursor.connection.commit()
                cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
                _identityRow = cursor.fetchone()
                self.VaccineId = _identityRow['Identity']
                # cursor.connection.commit()
                print('Query executed successfully. Vaccine : ' +  self.VaccineBrand
                +  ' added to the database using Vaccine ID = ' + str(self.VaccineId))
            except pymssql.Error as db_err:
                print("Database Programming Error in SQL Query processing for Vaccines! ")
                print("Exception code: " + str(db_err.args[0]))
                if len(db_err.args) > 1:
                    print("Exception message: " + db_err.args[1])
                print("SQL text that resulted in an Error: " + self.sqltext)


    def ReserveDoses(self, cursor):
        return None