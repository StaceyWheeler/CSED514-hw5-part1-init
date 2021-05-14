import unittest
import os

from sql_connection_manager import SqlConnectionManager
from enums import *
from utils import *
from COVID19_vaccine import COVID19Vaccine as covid


class TestCOVID19_vaccine(unittest.TestCase):
    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Moderna Vaccine object
                    self.moderna = covid('Moderna', 2, 28, cursor)
                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM Vaccines
                               WHERE VaccineName = 'Moderna'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    # print(rows)
                    if len(rows) < 1:
                        self.fail("Creating vaccines failed")
                    # clear the tables after testing, just in-case
                    # clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating vaccines failed")
    
    def test_add_dose(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Moderna Vaccine object
                    self.moderna = covid('Moderna', 2, 28, cursor)
                    sqlQuery = '''
                               SELECT AvailableDoses
                               FROM Vaccines
                               WHERE VaccineName = 'Moderna'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    # add doses to Moderna
                    self.moderna.AddDoses('Moderna', 3, cursor)
                    # check if doeses are added
                    sqlQuery2 = '''
                               SELECT AvailableDoses
                               FROM Vaccines
                               WHERE VaccineName = 'Moderna'
                               '''
                    cursor.execute(sqlQuery2)
                    rows2 = cursor.fetchall()
                    before_add = rows[0]
                    after_add = rows2[0]
                    if before_add['AvailableDoses'] != after_add['AvailableDoses'] - 3:
                        self.fail("Failed to verify added doses")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Failed to verify added doses")
    
    def test_reserve_dose(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                DBname=os.getenv("DBName"),
                                UserId=os.getenv("UserID"),
                                Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Moderna Vaccine object
                    self.moderna = covid('Moderna', 2, 28, cursor)
                    sqlQuery = '''
                            SELECT AvailableDoses
                            FROM Vaccines
                            WHERE VaccineName = 'Moderna'
                            '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    # Add 3 doses of Moderna
                    self.moderna.AddDoses('Moderna', 3, cursor)
                    # Reserve 2 doses of Moderna
                    self.moderna.ReserveDoses('Moderna', cursor)
                    # check if doses are reserved
                    sqlQuery2 = '''
                            SELECT AvailableDoses
                            FROM Vaccines
                            WHERE VaccineName = 'Moderna'
                            '''
                    cursor.execute(sqlQuery2)
                    rows2 = cursor.fetchall()
                    before_reserve = rows[0]
                    after_reserve = rows2[0]
                    print('before: ', before_reserve)
                    print('after: ', after_reserve)
                    if before_reserve['AvailableDoses'] != after_reserve['AvailableDoses'] - 1:
                        self.fail("Failed to verify reserved doses")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Failed to verify reserved doses")

    def test_reserve_dose_insufficient(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                DBname=os.getenv("DBName"),
                                UserId=os.getenv("UserID"),
                                Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Moderna Vaccine object
                    self.moderna = covid('Moderna', 2, 28, cursor)
                    sqlQuery = '''
                            SELECT AvailableDoses
                            FROM Vaccines
                            WHERE VaccineName = 'Moderna'
                            '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    # Add 1 dose of Moderna
                    self.moderna.AddDoses('Moderna', 1, cursor)
                    # Reserve 2 doses of Moderna -- this does not execute
                    self.moderna.ReserveDoses('Moderna', cursor)
                    # check if doses are reserved
                    sqlQuery2 = '''
                            SELECT AvailableDoses
                            FROM Vaccines
                            WHERE VaccineName = 'Moderna'
                            '''
                    cursor.execute(sqlQuery2)
                    rows2 = cursor.fetchall()
                    before_reserve = rows[0]
                    after_reserve = rows2[0]
                    print('before: ', before_reserve)
                    print('after: ', after_reserve)
                    if before_reserve['AvailableDoses'] == after_reserve['AvailableDoses']:
                        self.fail("Failed to verify reserved doses")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Failed to verify reserved doses")

if __name__ == '__main__':
    unittest.main()