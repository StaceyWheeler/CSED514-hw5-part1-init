import unittest
import os
import time
import pymssql
from utils import *
from sql_connection_manager import SqlConnectionManager as SCM
from vaccine_patient import db_opp_err_handler
from vaccine_caregiver import VaccineCaregiver

class TestException(unittest.TestCase):
    
    def test_operational_exception(self):
        
        def raise_opp_err():
            raise pymssql.OperationalError()

        with SCM(Server=os.getenv("Server"),
                DBname=os.getenv("DBName"),
                UserId=os.getenv("UserID"),
                Password=os.getenv("Password")) as sqlClient:

            with sqlClient.cursor(as_dict=True) as cursor:
                clear_tables(sqlClient)
                
                _try = 0
                while _try < 3:
                    try:
                        raise_opp_err()
                    except pymssql.OperationalError as db_opp_err:
                        db_opp_err_handler('TableName')
                        _try += 1
        

if __name__ == '__main__':
    unittest.main()