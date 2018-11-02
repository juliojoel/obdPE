from DB import DB

class ObdDAO(object):

    def __init__(self):
        self.db = DB()
        self.conn = self.db.conn
        self.createTable()

    def createTable(self):

        try:
            c = self.conn.cursor()

            c.execute("""CREATE TABLE IF NOT EXISTS obd (
                        timestamp	DATE DEFAULT (datetime('now', 'localtime')),
                        speed	        NUMERIC,
                        rpm	        NUMERIC,
                        position	NUMERIC,
                        temperature	NUMERIC)""")
            self.conn.commit()
            
            c.close()

            return
        except:
            print("Error: createTable")
            return

    def logData(self, speed, rpm, pos, temp):

        try:
            c = self.conn.cursor()
            c.execute("insert into obd values (datetime('now','localtime'),'%f','%f','%f','%f')" % (speed, rpm, pos, temp))
            self.conn.commit()
            c.close()

            return
        except:
            print("Error: logData")
            return

    def selectData(self):

        try:
            c = self.conn.cursor()
            c.execute("select timestamp, speed, rpm, position, temperature from obd order by timestamp desc limit 50")
            data = c.fetchall()
            c.close()

            dates = []
            speeds = []
            rpms = []
            positions = []
            temperatures = []

            for row in reversed(data):
                dates.append(row[0])
		speeds.append(row[1])
		rpms.append(row[2])
		positions.append(row[3])
		temperatures.append(row[4])

            return dates, speeds, rpms, positions, temperatures
        except:
            print("Error: selectData")
            return

        
