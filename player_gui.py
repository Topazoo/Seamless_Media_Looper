from Tkinter import *
from drive_manager import Drive_Manager


class Player_GUI(object):
    ''' Media player GUI '''

    def __init__(self):
        self.mw = self.create_main_window()
        self.display_drives()
        self.mw.mainloop()

    def create_main_window(self):
        ''' Create the main GUI Window '''

        root = Tk()

        # Set title
        root.title("Media Player")

        # Maximize window
        root.state('zoomed')

        return root

    def display_drives(self):
        ''' Display the connected drives '''

        # Instantiate the drive manager
        drive_manager = Drive_Manager()

        # Collect drives
        drives = drive_manager.get_drives()

        # Display drives
        for drive in enumerate(drives):
            lbl = Label(self.mw, text=drive[1])
            lbl.grid(column=0, row=drive[0])
