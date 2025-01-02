from tkinter import *

class yardsaleData():
    def __init__(self, username, address, dates, timeStart, timeEnd, description):
        self.username = username #string
        self.address = address #string
        self.dates = dates #array of strings
        self.timeStart = timeStart #int
        self.timeEnd = timeEnd #int
        self.description = description #string

class controller(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        container = Frame()
        container.pack()
        
        self.screens = {}
        pages = [viewScreen, uploadScreen]
        
        for f in pages:
            screen = f(container, self)
            
            self.screens[f] = screen
            
            screen.grid(row = 0, column = 0, sticky = "nsew")
        
        self.showScreen(viewScreen)
            
    def showScreen(self, screen): #used to switch screens
        (self.screens[screen]).tkraise()
    
class viewScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        canvas = Canvas(self)
        #makes the canvas to hold the text
        
        #add stuff here for viewScreen
    
class uploadScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)


main = controller()
main.geometry(str(int(main.winfo_screenwidth() / 2)) + "x" + str(int(main.winfo_screenheight() / 2)))
main.title("Yardsales")


main.mainloop()