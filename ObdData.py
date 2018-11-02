import obd
import math

class ObdData(object):

    def truncate(self, number, digits):
        stepper = pow(10.0, digits)
        return math.trunc(stepper * number) / stepper

    def __init__(self, port):
        
        if port=="":
            self.conn = obd.OBD()
        else:
            self.conn = obd.OBD(portstr=port)
        
        self.cmdSpeed = obd.commands.SPEED
        self.cmdRPM = obd.commands.RPM
        self.cmdPos = obd.commands.THROTTLE_POS
        self.cmdTemp = obd.commands.COOLANT_TEMP
        
    def getData(self):

        try:
            
            rawSpeed = self.conn.query(self.cmdSpeed)
            rawRPM   = self.conn.query(self.cmdRPM)
            rawPos   = self.conn.query(self.cmdPos)
            rawTemp  = self.conn.query(self.cmdTemp)


        except:
            print("Error: getData.query")
            return

        resSpeed = rawSpeed.messages[0].data[0]
        resRPM1 = rawRPM.messages[0].data[0]
        resRPM2 = rawRPM.messages[0].data[1]
        resPos = rawPos.messages[0].data[0]
        resTemp = rawTemp.messages[0].data[0]

        resRPM = (resRPM1 * 256 + resRPM2 ) / 4
        resPos = resPos * 100.0 / 255.0
        resPos = self.truncate(resPos, 2)
        resTemp = resTemp - 40
        
        return resSpeed, resRPM, resPos, resTemp


