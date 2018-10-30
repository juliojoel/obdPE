import sqlite3
import obd
import sys
import requests as req
import time

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

    print(rawSpeed)
    print(rawRPM)
    print(rawPos)
    print(rawTemp)

    resSpeed = rawSpeed.messages[0].data[0]
    resRPM1 = rawRPM.messages[0].data[0]
    resRPM2 = rawRPM.messages[0].data[1]
    resPos = rawPos.messages[0].data[0]
    resTemp = rawTemp.messages[0].data[0]

    resRPM = (resRPM1 * 256.00 + resRPM2 ) / 4.00
    resPos = resPos * 100.00 / 255.00
    resTemp = resTemp - 40.00
    
    return resSpeed, resRPM, resPos, resTemp

def logData (speed, rpm, pos, temp):
    try:
        connDB = sqlite3.connect('obdPE.db')
        c = connDB.cursor()
        c.execute("insert into obd values (datetime('now'),'%f','%f','%f','%f')" % (speed, rpm, pos, temp))
        connDB.commit()
        c.close()

        return "ok!"
    except:
        return "error!"
    
while True:

    speed, rpm, pos, temp = getData()

    res2 = logData(speed, rpm, pos, temp)
    print(res2)

    payload = {'obd.speed': speed, 'obd.rpm': rpm, 'obd.pos': pos, 'obd.temp': temp}
    print(payload)
    resp = req.get("http://150.162.6.111/ScadaBRy/httpds", params=payload)
    print(resp)
    time.sleep(5)
