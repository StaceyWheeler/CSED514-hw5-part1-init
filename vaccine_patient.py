import pymssql

from sql_connection_manager import SqlConnectionManager
from enums import *
from utils import *

class VaccinePatient:

    def __init__(self):
        return

    def ReserveAppointment(CaregiverSchedulingId, Vaccine, cursor):
        sqltext1 = ("SELECT SlotStatus FROM CaregiverSchedule WHERE CaregiverSlotSchedulingId = CaregiverSchedulingId")
        cursor.execute(sqltext1)
        row = cursor.fetchall()

        if row['SlotStatus'] == 'OnHold':
            #carry on with scheduling the appointment
            sqltext2 = ("UPDATE )

        else:
            #cannot schedule this appointment