from time import sleep
from ObdDAO import ObdDAO
from ObdData import ObdData
from ScadaBR import updateScada

#connOBD = ObdData("/dev/ttys005")
connOBD = ObdData("")
connDB = ObdDAO()

while True:
    
    speed, rpm, pos, temp = connOBD.getData()

    res2 = connDB.logData(speed, rpm, pos, temp)

    res3 = updateScada(speed, rpm, pos, temp)
    
    sleep(1)
