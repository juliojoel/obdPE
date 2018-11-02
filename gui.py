import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

import Tkinter as tk
import ttk

import pandas as pd
import numpy as np

from time import sleep
from ObdDAO import ObdDAO
from ObdData import ObdData
from ScadaBR import updateScada

from obd import OBD

connOBD = ""
connDB = ObdDAO()
connected = False

LARGE_FONT= ("Verdana", 18)
TITLE_FONT= ("Verdana", 30)


fig = Figure(figsize=(10,8), dpi=100)

plotSpeed = fig.add_subplot(411)
plotRPM = fig.add_subplot(412)
plotPos = fig.add_subplot(413)
plotTemp = fig.add_subplot(414)

title = "Live Graph\n"
fig.suptitle(title)

def animate(i):

    dates, speeds, rpms, positions, temperatures = connDB.selectData()

    plotSpeed.clear()
    plotRPM.clear()
    plotPos.clear()
    plotTemp.clear()
    
    plotSpeed.plot(dates,speeds)
    plotRPM.plot(dates,rpms)
    plotPos.plot(dates,positions)
    plotTemp.plot(dates,temperatures)
    
    plotSpeed.set_xticks([])
    plotRPM.set_xticks([])
    plotPos.set_xticks([])
    plotTemp.set_xticks([])

    plotSpeed.set_title("Speed")
    plotRPM.set_title("RPM")
    plotPos.set_title("Throttle Position")
    plotTemp.set_title("Coolant Temperature")
    

class obdGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "OBD Dashboard")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Dashboard, LiveGraph):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Choose working mode:", font=LARGE_FONT)
        label.grid(row=1,columnspan=4,pady=10)

        entry1 = ttk.Entry(self, justify="center")
        entry1.insert(0, '/dev/ttys006')
        entry1.grid(row=2,column=1)
        


        button1 = ttk.Button(self, text="OBDSim",
                            command=lambda: [self.connect(entry1.get())])
        button1.grid(row=2,column=2)

        button2 = ttk.Button(self, text="Connect to ELM327",
                            command=lambda: [self.connect("")])
        button2.grid(row=3,columnspan=4,pady=10)

        self.status = tk.Label(self, text="", font=LARGE_FONT)
        self.status.grid(row=4,columnspan=4)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)


    def connect(self, port):

        global connected
        global connOBD

        if port=="":            
            self.status["text"] = "Connecting to ELM327..."
            self.update()
            connOBD = ObdData("")

            
        else:
            self.status["text"] = "Connecting to simulator..."
            self.update()
            connOBD = ObdData(port)

        if OBD.is_connected(connOBD.conn):
            connected = True
            app.show_frame(Dashboard)
        else:
            self.status["text"] = "Error!!"
            self.update()

        
class Dashboard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        button1 = ttk.Button(self, text="Exit",
                            command=quit)
        button1.grid(row=1,column=0,pady=10)

        button2 = ttk.Button(self, text="LiveGraph",
                            command=lambda: controller.show_frame(LiveGraph))
        button2.grid(row=1,column=2)
        
        label = tk.Label(self, text=("""OBD Dashboard"""), font=TITLE_FONT)
        label.grid(row=2,columnspan=5,pady=20)

        

        labelSpeed = tk.Label(self, text="Speed", font=TITLE_FONT)
        labelSpeed.grid(row=3,column=1,pady=50)

        labelRPM = tk.Label(self, text="RPM", font=TITLE_FONT)
        labelRPM.grid(row=3,column=3)

        self.valSpeed = tk.Label(self, text="", font=LARGE_FONT)
        self.valSpeed.grid(row=4,column=1)

        self.valRPM = tk.Label(self, text="", font=LARGE_FONT)
        self.valRPM.grid(row=4,column=3)

        labelPos = tk.Label(self, text="Throttle Pos", font=TITLE_FONT)
        labelPos.grid(row=6,column=1,pady=50)

        xspace = tk.Label(self, text="          ", font=TITLE_FONT)
        xspace.grid(row=6,column=2)

        labelTemp = tk.Label(self, text="Coolant Temp", font=TITLE_FONT)
        labelTemp.grid(row=6,column=3)

        self.valPos = tk.Label(self, text="", font=LARGE_FONT)
        self.valPos.grid(row=7,column=1)

        self.valTemp = tk.Label(self, text="", font=LARGE_FONT)
        self.valTemp.grid(row=7,column=3)

        

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.update_values()


    def update_values(self):

        if connected:
            speed, rpm, pos, temp = connOBD.getData()
            
            res2 = connDB.logData(speed, rpm, pos, temp)

            res3 = updateScada(speed, rpm, pos, temp)

            self.valSpeed["text"] = ("%d km/h" % speed)
            self.valRPM["text"] = ("%d rpm" % rpm)
            self.valPos["text"] = ("%d %%" % pos)
            self.valTemp["text"] = ("%d degC" % temp)

            self.update()

        self.after(500, self.update_values)

                
class LiveGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = ttk.Button(self, text="Back to Dashboard",
                            command=lambda: controller.show_frame(Dashboard))
        button1.grid(row=1,pady=10)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2)

        canvas._tkcanvas.grid(row=2)



app = obdGUI()
ani = animation.FuncAnimation(fig, animate, blit=False, interval=3000, repeat=False)
app.mainloop()


