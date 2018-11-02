from requests import get as getHTTP

def updateScada(speed, rpm, pos, temp):

    payload = {'obd.speed': speed, 'obd.rpm': rpm, 'obd.pos': pos, 'obd.temp': temp}

    try:
        
        response = getHTTP("http://150.162.6.111/ScadaBRy/httpds", params=payload)

        return response
    except:
        print("Error: updateScada")
        return

