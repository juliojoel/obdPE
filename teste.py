import sqlite3
import obd
import sys

connOBD = obd.OBD(portstr="/dev/ttys003")

cmdSpeed = obd.commands.SPEED
cmdRPM = obd.commands.RPM
cmdPos = obd.commands.THROTTLE_POS
cmdTemp = obd.commands.COOLANT_TEMP

def getData():	
        
    rawSpeed = connOBD.query(cmdSpeed)
    rawRPM = connOBD.query(cmdRPM)
    rawPos = connOBD.query(cmdPos)
    rawTemp = connOBD.query(cmdTemp)

    resSpeed = rawSpeed.messages[0].data[0]
    resRPM = rawRPM.messages[0].data[0]
    resPos = rawPos.messages[0].data[0]
    resTemp = rawTemp.messages[0].data[0]
    
    return resSpeed, resRPM, resPos, resTemp

def logData (speed, rpm, pos, temp):
    try:
        connDB = sqlite3.connect('obdPE.db')
        c = connDB.cursor()
        c.execute("insert into speed values (datetime('now'),'%f')" % speed)
        c.execute("insert into rpm values (datetime('now'),'%f')" % rpm)
        c.execute("insert into position values (datetime('now'),'%f')" % pos)
        c.execute("insert into temperature values (datetime('now'),'%f')" % temp)
        connDB.commit()
        c.close()

        return "ok!"
    except:
        return "erro!"
    

speed, rpm, pos, temp = getData()

res2 = logData(speed, rpm, pos, temp)
print(res2)
