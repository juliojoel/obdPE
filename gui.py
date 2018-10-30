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

import obd

LARGE_FONT= ("Verdana", 12)
#style.use("ggplot")

f = Figure(figsize=(10,6), dpi=100)
a = f.add_subplot(111)

port = ""

def animate(i):
    pullData = open('sampleText.txt','r').read()
    dataArray = pullData.split('\n')
    xar=[]
    yar=[]
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    a.clear()
    a.plot(xar,yar)

    title = "title\n"
    a.set_title(title)   

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
                            command=lambda: [self.connect("/dev/ttys003")])
        button1.pack()

        button2 = ttk.Button(self, text="Connect to ELM327",
                            command=lambda: [self.connect()])
        button2.pack()

        self.status = tk.Label(self, text="", font=LARGE_FONT)
        self.status.pack(pady=10,padx=10)

    def connect(self, port):

        if port=="":            
            self.status["text"] = "Connecting to ELM327..."
            self.update()
            conn = obd.OBD()
            
        else:
            self.status["text"] = "Connecting to simulator..."
            self.update()
            conn = obd.OBD(portstr=port)

        if obd.OBD.is_connected(conn):
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

                
class SpeedGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Speed Graph", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Dashboard",
                            command=lambda: controller.show_frame(Dashboard))
        button1.pack()




class RPMGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="RPM Graph", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Dashboard",
                            command=lambda: controller.show_frame(Dashboard))
        button1.pack()



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
        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = obdGUI()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
