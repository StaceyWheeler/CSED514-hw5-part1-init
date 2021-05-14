from datetime import datetime
from datetime import timedelta
import pymssql


class COVID19Vaccine:
    ''' Adds a row to the Vaccines table '''
    def __init__(self, name, doses_per_patient, days_between_doses, cursor):

        sqltext1 = "SELECT * FROM Vaccines"
        cursor.execute(sqltext1)
        rows = cursor.fetchall()
        #print('rows: ', rows)
        found = False
        for row in rows:
            #print(type(row))
            if row['VaccineName'] == name:
                #break out. We don't want to add this vaccine to the table bc it already exists.
                found = True
                break 
            #else:
             #   do nothing
    
        if not found:
            self.sqltext = "INSERT INTO Vaccines (VaccineName, DosesPerPatient, DaysBetweenDoses) VALUES (%s, %s, %s)" 

            try: 
                cursor.execute(self.sqltext, ((name), (str(doses_per_patient)), (str(days_between_doses))))
                cursor.connection.commit()
                print('Query executed successfully. Vaccine : ' + name 
                +  ' added to the database')
            except pymssql.Error as db_err:
                print("Database Programming Error in SQL Query processing for Caregivers! ")
                print("Exception code: " + str(db_err.args[0]))
                if len(db_err.args) > 1:
                    print("Exception message: " + str(db_err.args[1]))
                print("SQL text that resulted in an Error: " + self.sqltext)

        cursor.connection.commit()

    def AddDoses(self, name, num_doses, cursor):

        self.sqltext = "UPDATE Vaccines SET AvailableDoses = AvailableDoses + %s, TotalDoses = TotalDoses + %s WHERE VaccineName = %s"

        try: 
                cursor.execute(self.sqltext, ((str(num_doses)), (str(num_doses)), (name)))
                cursor.connection.commit()
                print('Query executed successfully. Quantity : ' + str(num_doses)
                +  ' added to the inventory')
        except pymssql.Error as db_err:
                print("Database Programming Error in SQL Query processing for Caregivers! ")
                print("Exception code: " + str(db_err.args[0]))
                if len(db_err.args) > 1:
                    print("Exception message: " + str(db_err.args[1]))
                print("SQL text that resulted in an Error: " + self.sqltext)

        cursor.connection.commit()

    def ReserveDoses(self, name, cursor):

        sqltext2 = "SELECT * FROM Vaccines"
        cursor.execute(sqltext2)
        rows = cursor.fetchall()

        for row in rows:
            if row['VaccineName'] == name:
                doses_per_patient = row['DosesPerPatient']
        
        if row['AvailableDoses'] >= doses_per_patient:
            self.sqltext = "UPDATE Vaccines SET AvailableDoses = AvailableDoses - 2, ReservedDoses = ReservedDoses + 2 WHERE VaccineName = %s"
            try: 
                cursor.execute(self.sqltext, ((name)))
                cursor.connection.commit()
                print('Query executed successfully. ' + str(doses_per_patient) + ' doses reserved.')
            except pymssql.Error as db_err:
                print("Database Programming Error in SQL Query processing for Caregivers! ")
                print("Exception code: " + str(db_err.args[0]))
                if len(db_err.args) > 1:
                    print("Exception message: " + str(db_err.args[1]))
                print("SQL text that resulted in an Error: " + self.sqltext)     

        else:
            print("Not enough doses available to complete this reservation.")

        

        