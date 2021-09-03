import tkinter as tk
from tkinter import ttk
from tkinter import Entry
import threading
from urllib.request import urlopen
import json
import time
import os
import detection.py
import telepot

LARGEFONT = ("Verdana", 20)
MEDFONT = ("Verdana", 15)

class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Intelligent Syringe Automation System")
        # creating a container
        container = tk.Frame(self)
        container.pack(expand=1000)

        container.grid_rowconfigure(0, weight=1000)
        container.grid_columnconfigure(0, weight=1000)

        frame = StartPage(container, self)
        frame.grid(row=0, column=0)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        print("Show Frame")
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage
'''''
def thread_function():
    print("Hello")


def thread_openpg(self, parent):
    print("Count")
    time.sleep(5)
    frame = Countdown(parent, self, 1, 0, 1)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.tkraise()

def thread_wash(self, parent):
    print("Wash")
    frame = OpenWash(parent, self)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.tkraise()
'''

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        parent = parent
        timeLabel = ttk.Label(self, text="Press to start", font=MEDFONT)
        timeLabel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=6)
        btn_wash = ttk.Button(self, text="Start Washing", command=lambda: self.OpenWash(parent))
        btn_both = ttk.Button(self, text="Start Full Process", command=lambda: self.OpenBoth(parent))
        btn_wash.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        btn_both.grid(row=2, column=4, padx=10, pady=10, sticky="nsew")

    def OpenWash(self, parent):
        frame = OpenWash(parent, self, 0, 0, 1)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def OpenBoth(self, parent):
        print("Getting suggested timing from ML")
        suggestedTime = detection.run_timeml()
        hourValue = suggestedTime/60
        minsValue = round(suggestedTime - (hourValue*60)/10)
        frame = SelectDry(parent, self, hourValue, minsValue, 3)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

class CoverOpen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        parent = parent
        textVar = "Cover is open"

        label_msg = ttk.Label(self, text=textVar, font=MEDFONT)
        label_msg.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=6)

        app.after(1000, self.CheckClose, parent)

    def CheckClose(self, parent):
        lid_status = 1
        while (lid_status != '1'):
            # to get from TS the status for the lid
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/1/last.json")
            # getting json response and putting them in an array
            response = new_TS.read()
            data = json.loads(response)
            # getting status from field 1
            lid_status = data['field1']
        frame = CoverOpen(parent, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        parent = parent
        label_msg = ttk.Label(self, text="Press to start", font=MEDFONT)
        label_msg.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=6)

        btn_wash = ttk.Button(self, text="Start Washing", command=lambda: self.OpenWash(parent))
        btn_both = ttk.Button(self, text="Start Full Process", command=lambda: self.OpenBoth(parent))
        btn_wash.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        btn_both.grid(row=2, column=4, padx=10, pady=10, sticky="nsew")

        app.after(1000, self.CheckLid, parent)

    def OpenWash(self, parent):
        frame = OpenWash(parent, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def OpenBoth(self, parent):
        #Do ML here to determin suggested time
        frame = SelectDry(parent, self, 1, 0, 3)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def CheckLid(self, parent):
        lid_status = 1
        while (lid_status != '1'):
            # to get from TS the status for the lid
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/1/last.json")
            # getting json response and putting them in an array
            response = new_TS.read()
            data = json.loads(response)
            # getting status from field 1
            lid_status = data['field1']
        frame = CoverOpen(parent, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

class OpenWash(tk.Frame):
    def __init__(self, parent, controller, hourValue, minsValue, option):
        tk.Frame.__init__(self, parent)
        parent = parent
        textVar = "Washing in progress..."

        # label of frame Layout 2
        timeLabel = ttk.Label(self, text=textVar, font=MEDFONT)
        timeLabel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=6)

        btnstyle = ttk.Style()
        btnstyle.configure("button", height=100, width=100)

        btn_stop = ttk.Button(self, text="Stop", command=lambda: self.OpenStop(parent, 1))

        btn_stop.grid(row=3, column=0, padx=10, pady=10, columnspan=6, sticky="nsew")

        app.after(1000, self.startWashing, parent, hourValue, minsValue, option)

    def checkLid(self, parent):
        print("Checking if the lock is locked")
        print("Lid is locked")
        app.after(1000, self.startWashing, parent)

    def startWashing(self, parent, hourValue, minsValue, option):
        print("Starting ultrasonic cleaner")
        # Initialise the dirtysyringe variable to 1 so that it will enter into the washing loop
        dirtySyringe = 1
        # If there are dirty syringes detected, it will enter the washing loop to wash the syringe till it is dry
        while (dirtySyringe != 0):
            print("Starting ultrasonic cleaner")
            # Staring ultrasonic cleaner
            urlopen("https://api.thingspeak.com/update?api_key=HEM4RL1FUXVMJUIT&field3=1")
            # t Checking if ultrasonic cleaner is turned on
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/5/last.json")
            response = new_TS.read()
            data = json.loads(response)
            ultrasonic_status = data['field5']
            while (ultrasonic_status != '1'):
                time.sleep(3)
                print("Untrasonic cleaner not started")
                new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/5/last.json")
                response = new_TS.read()
                data = json.loads(response)
                ultrasonic_status = data['field5']

            # Code will only enter here when ultrasonic cleaner is turned on
            print("Ultrasonic cleaner started")
            print("Waiting for 120 secs")
            time.sleep(120)
            urlopen("https://api.thingspeak.com/update?api_key=HEM4RL1FUXVMJUIT&field3=0")
            print("Ultrasonic cleaner stopped")
            dirtySyringe = detection.run_camml()

            while (ultrasonic_status != '0'):
                time.sleep(3)
                print("Untrasonic cleaner not started")
                new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/5/last.json")
                response = new_TS.read()
                data = json.loads(response)
                ultrasonic_status = data['field5']

        # Code will only enter here will dirtySyringe = 0
        time.sleep(15)
        print("Opening drain valve")
        urlopen("https://api.thingspeak.com/update?api_key=HEM4RL1FUXVMJUIT&field4=1")
        time.sleep(15)
        new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/6/last.json")
        response = new_TS.read()
        data = json.loads(response)
        valve_status = data['field6']
        while (valve_status != '1'):
            time.sleep(3)
            print("Drain valve not opened")
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/6/last.json")
            response = new_TS.read()
            data = json.loads(response)
            valve_status = data['field6']
        print("Drain valve opened")


    if (option==3):
        frame = Prepare(parent, self, hourValue, minsValue, 0, 2)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
    else:
        frame = ProcessEnd(parent, self, 1)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def OpenStop(self, parent, option):
        print("Stop")
        frame = Countdown(parent, self, 0, 0, 0, option, 0)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


class Prepare(tk.Frame):
    def __init__(self, parent, controller, hourValue, minsValue, secsValue, option):
        tk.Frame.__init__(self, parent)
        parent = parent
        textVar = "Washing in progress..."
        if (textVar == 1):
            labelText = "Washing in progress."
        if (option == 2):
            textVar = "Drying in progress."
        if (option == 3):
            textVar = "Washing & Drying in progress."

        label_content = ttk.Label(self, text=textVar, font=LARGEFONT)
        label_content.grid(row=1, column=2, padx=10, pady=10, sticky="nsew", columnspan=4)
        btn_stop = ttk.Button(self, text="Stop", command=lambda: self.Stop(parent))
        btn_stop.grid(row=3, column=0, padx=10, pady=10, columnspan=6, sticky="nsew")

        if (option == 1 or option == 3):
            app.after(1000, self.PrepareWash, parent, hourValue, minsValue, option)
        elif (option == 2):
            app.after(1000, self.PrepareDry, parent, hourValue, minsValue)

    def Stop(self, parent):
        self.destroy()
        frame = Home(parent, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def PrepareWash(self, parent, hourValue, minsValue, option):
        time.sleep(15)
        print("Closing drain valve")
        urlopen("https://api.thingspeak.com/update?api_key=HEM4RL1FUXVMJUIT&field4=0")
        time.sleep(15)
        new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/6/last.json")
        response = new_TS.read()
        data = json.loads(response)
        valve_status = data['field6']
        while (valve_status != '0'):
            time.sleep(3)
            print("Drain valve not closed")
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/6/last.json")
            response = new_TS.read()
            data = json.loads(response)
            valve_status = data['field6']
        print("Drain valve closed")
        # 15sec of waiting for TS data
        time.sleep(15)
        # to get from TS the status for the lid
        new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/1/last.json")
        # getting json response and putting them in an array
        response = new_TS.read()
        data = json.loads(response)
        # getting status from field 1
        lid_status = data['field1']
        print("Checking status of the lid")
        while (lid_status != '1'):
            # checking at intervals of 3 secs
            time.sleep(3)
            print("Lid is open")
            # checking TS again on status of lid
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/1/last.json")
            response = new_TS.read()
            data = json.loads(response)
            lid_status = data['field1']
        # Code will go to here once ths staus of lid is confirmed to be closed
        print("Lid is close")
        print("Locking lid")
        # locking of the lid
        urlopen("https://api.thingspeak.com/update?api_key=HEM4RL1FUXVMJUIT&field1=1")
        time.sleep(15)
        # checking if the lid is locked
        new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/2/last.json")
        response = new_TS.read()
        data = json.loads(response)
        lid_lock = data['field2']
        while (lid_lock != '1'):
            time.sleep(3)
            print("Fail to lock lid")
            # checking TS again to see if the lid is locked
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/2/last.json")
            response = new_TS.read()
            data = json.loads(response)
            lid_lock = data['field2']
        # Code will go to here when the lid is locked
        print("Lid is locked")
        print("Starting wash")
        time.sleep(15)
        # Starting water pump
        urlopen("https://api.thingspeak.com/update?api_key=HEM4RL1FUXVMJUIT&field2=1")
        time.sleep(10)
        # Checking TS for the status of pump
        new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/3/last.json")
        response = new_TS.read()
        data = json.loads(response)
        pump_status = data['field3']
        while (pump_status != '0'):
            time.sleep(3)
            print("Pump not stopped")
            # Checking TS for the status of pump
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/3/last.json")
            response = new_TS.read()
            data = json.loads(response)
            pump_status = data['field3']
        # Code will only go to here when the pump is stopped
        print("Pump stopped")
        time.sleep(15)
        # All checks have been done, and device is ready to wash the syringe
        # Opening of washing frame
        frame = OpenWash(parent, self, hourValue, minsValue, option)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def PrepareDry(self, parent, hourValue, minsValue):
        time.sleep(15)
        print("Opening drain valve")
        urlopen("https://api.thingspeak.com/update?api_key=HEM4RL1FUXVMJUIT&field4=1")
        time.sleep(15)
        new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/6/last.json")
        response = new_TS.read()
        data = json.loads(response)
        valve_status = data['field6']
        while (valve_status != '1'):
            time.sleep(3)
            print("Drain valve not opened")
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/6/last.json")
            response = new_TS.read()
            data = json.loads(response)
            valve_status = data['field6']
        print("Drain valve opened")
        time.sleep(15)
        # Checking if the lid is open
        new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/1/last.json")
        response = new_TS.read()
        data = json.loads(response)
        lid_status = data['field1']
        print("Checking status of the lid")
        while (lid_status != '1'):
            time.sleep(3)
            print("Lid is open")
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/1/last.json")
            response = new_TS.read()
            data = json.loads(response)
            lid_status = data['field1']
        print("Lid is close")
        print("Locking lid")
        # Locking the lid
        urlopen("https://api.thingspeak.com/update?api_key=HEM4RL1FUXVMJUIT&field1=1")
        time.sleep(15)
        # Checking if the lock is locked
        new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/2/last.json")
        response = new_TS.read()
        data = json.loads(response)
        lock_status = data['field2']
        while (lock_status != '1'):
            time.sleep(3)
            print("Fail to lock lid")
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/2/last.json")
            response = new_TS.read()
            data = json.loads(response)
            lock_status = data['field2']
        print("Lid is locked")
        print("Starting dry")
        print("Starting fan")
        time.sleep(15)
        # Turning on the fan
        urlopen("https://api.thingspeak.com/update?api_key=HEM4RL1FUXVMJUIT&field5=1")
        # Checking if the fan is turned on
        new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/7/last.json")
        response = new_TS.read()
        data = json.loads(response)
        fan_status = data['field7']
        while (fan_status != '1'):
            time.sleep(3)
            print("Fan not started")
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/7/last.json")
            response = new_TS.read()
            data = json.loads(response)
            fan_status = data['field7']
        # Code goes to here when the fan is started
        print("Fan started")
        frame = Countdown(parent, self, hourValue, minsValue, 0, 2)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

class Countdown(tk.Frame):
    def __init__(self, parent, controller, hourValue, minsValue, secsValue, option, count):
        tk.Frame.__init__(self, parent)
        labelText = ""
        if (option == 1):
            labelText = "Washing in progress."
        if (option == 2):
            labelText = "Drying in progress."
        if (option == 3):
            labelText = "Washing & Drying in progress."
        if (option > 3):
            app.after(1000, self.OpenStop, parent)

        # label of frame
        timeLabel = ttk.Label(self, text=labelText, font=MEDFONT)
        hour = ttk.Label(self, text=hourValue, font=LARGEFONT)
        mins = ttk.Label(self, text=minsValue, font=LARGEFONT)
        secs = ttk.Label(self, text=secsValue, font=LARGEFONT)
        space1 = ttk.Label(self, text=":", font=LARGEFONT)
        space2 = ttk.Label(self, text=":", font=LARGEFONT)
        hourLabel = ttk.Label(self, text="hour")
        minsLabel = ttk.Label(self, text="mins")
        secsLabel = ttk.Label(self, text="secs")

        timeLabel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=6)
        hour.grid(row=3, column=1, padx=10, pady=10, columnspan=1)
        space1.grid(row=3, column=2, padx=10, pady=10, columnspan=1)
        mins.grid(row=3, column=3, padx=10, pady=10, columnspan=1)
        space2.grid(row=3, column=4, padx=10, pady=10, columnspan=1)
        secs.grid(row=3, column=5, padx=10, pady=10, columnspan=1)
        hourLabel.grid(row=4, column=1, padx=10, pady=10, columnspan=1)
        minsLabel.grid(row=4, column=3, padx=10, pady=10, columnspan=1)
        secsLabel.grid(row=4, column=5, padx=10, pady=10, columnspan=1)

        btn_stop = ttk.Button(self, text="Stop", command=lambda: self.Stop(parent))
        btn_stop.grid(row=6, column=0, padx=10, pady=10, sticky="nsew", columnspan=6)

        app.after(1000, self.countdownAnimation, parent, hourValue, minsValue, secsValue, option, count)

    def Stop(self, parent):
        self.destroy()
        frame = Home(parent, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def countdownAnimation(self, parent, hour, mins, secs, option, count):
        secs = secs - 1
        if (secs < 0 and hour == 0 and mins == 0):
            print("Timer end")
            # Stopping fans
            urlopen("https://api.thingspeak.com/update?api_key=HEM4RL1FUXVMJUIT&field5=0")
            # time.sleep(3)
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/7/last.json")
            response = new_TS.read()
            data = json.loads(response)
            fan_status = data['field7']
            while (fan_status != '0'):
                time.sleep(3)
                print("Fan not stopped")
                new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/7/last.json")
                response = new_TS.read()
                data = json.loads(response)
                fan_status data['field7']
            print("Fan stopped")
            time.sleep(15)
            print("Closing drain valve")
            urlopen("https://api.thingspeak.com/update?api_key=HEM4RL1FUXVMJUIT&field4=0")
            time.sleep(15)
            new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/6/last.json")
            response = new_TS.read()
            data = json.loads(response)
            drain_status = data['field6']
            while (drain_status != '0'):
                time.sleep(3)
                print("Drain valve not closed")
                new_TS = urlopen("https://api.thingspeak.com/channels/1481771/fields/6/last.json")
                response = new_TS.read()
                data = json.loads(response)
                drain_status = data['field6']
            print("Drain valve closed")
            time.sleep(5)

            frame = ProcessEnd(parent, self, option)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()
            return
        if (secs < 0):
            mins = mins - 1
            secs = 59
        if (mins < 0):
            print("here")
            hour = hour - 1
            mins = 59
        if (option == 3):
            count = count + 1
        if (count == 120):
            print("Ending wash, starting dry")
        frame = Countdown(parent, self, hour, mins, secs, option, count)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

class ProcessEnd(tk.Frame):
    def __init__(self, parent, controller, option):
        tk.Frame.__init__(self, parent)
        btn_dry = ttk.Button(self, text="Start Drying", command=lambda: self.OpenDry(parent))
        if (option == 1):
            labelText = "Washing complete"
            btn_dry.grid(row=6, column=0, padx=10, pady=10, sticky="nsew", columnspan=6)
            bot = telepot.Bot('1959248925:AAFwEF9z_vTgmfATP9bsQ_cLAuxCewWxrFY')
            bot.sendMessage("95635875", "Washing is complete")
        elif (option == 2):
            labelText = "Drying complete"
            bot = telepot.Bot('1959248925:AAFwEF9z_vTgmfATP9bsQ_cLAuxCewWxrFY')
            bot.sendMessage("95635875", "Drying is complete")
        elif (option == 3):
            labelText = "Washing & Drying complete"
            bot = telepot.Bot('1959248925:AAFwEF9z_vTgmfATP9bsQ_cLAuxCewWxrFY')
            bot.sendMessage("95635875", "Washing & Drying is complete")

        timeLabel = ttk.Label(self, text=labelText, font=MEDFONT)
        timeLabel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=6)

        btn_home = ttk.Button(self, text="Home", command=lambda: self.OpenHome(parent))
        btn_home.grid(row=7, column=0, padx=10, pady=10, sticky="nsew", columnspan=6)

    def OpenHome(self, parent):
        frame = Home(parent, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

# Driver Code
app = tkinterApp()
#app.geometry('960x540')
app.geometry('2000x2000')
app.rowconfigure(3, weight=100)
app.columnconfigure(2, weight=100)
app.mainloop()
