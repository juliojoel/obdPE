import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
#from matplotlib import style

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

LARGE_FONT= ("Verdana", 12)

figSpeed = Figure(figsize=(10,6), dpi=100)
figRPM = Figure(figsize=(10,6), dpi=100)
figPos = Figure(figsize=(10,6), dpi=100)
figTemp = Figure(figsize=(10,6), dpi=100)

plotSpeed = figSpeed.add_subplot(111)
plotRPM = figRPM.add_subplot(111)
plotPos = figPos.add_subplot(111)
plotTemp = figTemp.add_subplot(111)

def animate(i):
    dates, speeds = connDB.selectSpeed()
    plotSpeed.clear()
    plotSpeed.plot(dates,speeds)

    plotSpeed.set_xticklabels([])

    title = "Speeds\n"
    plotSpeed.set_title(title)   

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

        for F in (StartPage, Dashboard, SpeedGraph, RPMGraph, ThrottleGraph, CoolantGraph):

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
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="OBDSim",
                            command=lambda: [self.connect("/dev/ttys005")])
        button1.pack()

        button2 = ttk.Button(self, text="Connect to ELM327",
                            command=lambda: [self.connect("")])
        button2.pack()

        self.status = tk.Label(self, text="", font=LARGE_FONT)
        self.status.pack(pady=10,padx=10)

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
        label = tk.Label(self, text=("""OBD Dashboard"""), font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Speed",
                            command=lambda: controller.show_frame(SpeedGraph))
        button1.pack()

        button2 = ttk.Button(self, text="RPM",
                            command=lambda: controller.show_frame(RPMGraph))
        button2.pack()

        button3 = ttk.Button(self, text="Throttle Pos",
                            command=lambda: controller.show_frame(ThrottleGraph))
        button3.pack()
        button4 = ttk.Button(self, text="Coolant Temp",
                            command=lambda: controller.show_frame(CoolantGraph))
        button4.pack()

        button5 = ttk.Button(self, text="Exit",
                            command=quit)
        button5.pack()

        self.update_values()


    def update_values(self):

        if connected:
            speed, rpm, pos, temp = connOBD.getData()
            res2 = connDB.logData(speed, rpm, pos, temp)

        self.after(1000, self.update_values)

                
class SpeedGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Speed Graph", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Dashboard",
                            command=lambda: controller.show_frame(Dashboard))
        button1.pack()

        canvas = FigureCanvasTkAgg(figSpeed, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class RPMGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="RPM Graph", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Dashboard",
                            command=lambda: controller.show_frame(Dashboard))
        button1.pack()

##        canvas = FigureCanvasTkAgg(figRPM, self)
##        canvas.draw()
##        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
##
##        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class ThrottleGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Throttle Position Graph", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Dashboard",
                            command=lambda: controller.show_frame(Dashboard))
        button1.pack()



class CoolantGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Coolant Temperature Graph", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Dashboard",
                            command=lambda: controller.show_frame(Dashboard))
        button1.pack()

app = obdGUI()
ani = animation.FuncAnimation(figSpeed, animate, interval=1000)
app.mainloop()


