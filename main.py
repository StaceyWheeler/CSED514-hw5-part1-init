import sql_connection_manager
from COVID19_vaccine import COVID19Vaccine as covid
import vaccine_caregiver
import pymssql
import os

#connections

server = os.getenv('Server')
dbname = os.getenv('DBname')
userid = os.getenv('userid')
pswd =  os.getenv('Password')

SCM = sql_connection_manager.SqlConnectionManager(server, dbname, userid, pswd)
conn = pymssql.connect(server, userid, pswd, dbname)
cursor = SCM.cursor(as_dict=True)
#jj = COVID19_vaccine.COVID19Vaccine('JJ', cursor)
#jj.AddDoses(5, cursor)

# Testing out adding rows to Vaccines and AddDoses:
covid_obj_Moderna = covid('Moderna', 2, 28, cursor)
# covid_obj_Moderna.AddDoses('Moderna', 20, dbcursor)
# covid_obj_Pfizer = covid('Pfizer', 2, 21, dbcursor)
# covid_obj_Pfizer.AddDoses('Pfizer', 5, dbcursor)
# covid_obj_Pfizer.AddDoses('Pfizer', 10, dbcursor)

#Testing out ReserveDoses:
covid_obj_Moderna = covid('Moderna', 2, 28, cursor)
covid_obj_Moderna.ReserveDoses('Moderna', cursor)