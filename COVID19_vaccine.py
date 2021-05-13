from datetime import datetime
from datetime import timedelta
import pymssql


class COVID19Vaccine:
    ''' Adds a row to the Vaccines table '''
    def __init__(self, name, doses_per_patient, days_between_doses, cursor):
        
        self.sqltext = "INSERT INTO Vaccines (VaccineName, DosesPerPatient, DaysBetweenDoses) VALUES ('" 
        self.sqltext += name + "', "
        self.sqltext += str(doses_per_patient) + "', "
        self.sqltext += str(days_between_doses) + "')"
        
        try: 
            cursor.execute(self.sqltext)
            cursor.connection.commit()
            #cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            #_identityRow = cursor.fetchone()
            #self.caregiverId = _identityRow['Identity']
            # cursor.connection.commit()
            print('Query executed successfully. Vaccine : ' + name 
            +  ' added to the database')
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Caregivers! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext)

        cursor.connection.commit()

    def AddDoses(name, num_doses, cursor):

        self.sqltext = "UPDATE Vaccines SET AvailableDoses = AvailableDoses + " 
        self.sqltext += str(num_doses)
        self.sqltext += " WHERE name = '"
        self.sqltext += str(name) + "';"
        self.sqltext += "UPDATE Vaccines SET TotalDoses = TotalDoses + " 
        self.sqltext += str(num_doses)
        self.sqltext += " WHERE name = '"
        self.sqltext += str(name) + "'"

        try: 
                cursor.execute(self.sqltext)
                cursor.connection.commit()
                #cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
                #_identityRow = cursor.fetchone()
                #self.caregiverId = _identityRow['Identity']
                # cursor.connection.commit()
                print('Query executed successfully. Quantity : ' + num_doses 
                +  ' added to the inventory')
        except pymssql.Error as db_err:
                print("Database Programming Error in SQL Query processing for Caregivers! ")
                print("Exception code: " + str(db_err.args[0]))
                if len(db_err.args) > 1:
                    print("Exception message: " + db_err.args[1])
                print("SQL text that resulted in an Error: " + self.sqltext)

        cursor.connection.commit()

    def ReserveDoses(self, name, num_appointments, cursor):

        if name == 'Pfizer' or name == 'Moderna':
            self.doses_needed = 2
        else:
            self.doese_needed = 1

        self.sqltext = "INSERT INTO Vaccines (AvalableDoses, TotalDoses) VALUES ('" 
        self.sqltext += str(num_doses) + "', "
        self.sqltext += str(num_doses) + "')"

        