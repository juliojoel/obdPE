import Tkinter as tk
import ttk
import leather
from PIL import Image, ImageTk

import cairo
import rsvg


import obd

LARGE_FONT= ("Verdana", 12)

port = ""

filename = "lines.svg"

data = [(0, 3),
    (4, 5),
    (7, 9),
    (8, 4)
]

def svgPhotoImage(self,file_path_name):
        import Image,ImageTk,rsvg,cairo
        "Returns a ImageTk.PhotoImage object represeting the svg file" 
        # Based on pygame.org/wiki/CairoPygame and http://bit.ly/1hnpYZY        
        svg = rsvg.Handle(file=file_path_name)
        width, height = svg.get_dimension_data()[:2]
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))
        context = cairo.Context(surface)
        #context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        svg.render_cairo(context)
        tk_image=ImageTk.PhotoImage('RGBA')
        image=Image.frombuffer('RGBA',(width,height),surface.get_data(),'raw','BGRA',0,1)
        tk_image.paste(image)
        return(tk_image)

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
                            command=lambda: [self.connect("/dev/ttys001")])
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
        

        chart = leather.Chart('Line')
        chart.add_line(data)

        svg = chart.to_svg()

        
        img = cairo.ImageSurface(cairo.FORMAT_ARGB32, 640,480)

        ctx = cairo.Context(img)

        #handle = rsvg.Handle(filename)
        handle= rsvg.Handle(None, str(svg))

        handle.render_cairo(ctx)

        img.write_to_png("svg.png")

        imgg = ImageTk.PhotoImage(Image.open("svg.png"))
        lbl = tk.Label(window, image = imgg).pack()

app = obdGUI()
app.mainloop()
