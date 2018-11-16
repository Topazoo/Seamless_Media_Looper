from Tkinter import *
import ttk
from drive_manager import Drive_Manager
from collections import OrderedDict


class Player_GUI(object):
    ''' Media player GUI '''

    def __init__(self):
        # Create main window
        self.mw = self.create_main_window()

        # Display drives as tabs and get dictionary of all tabs with drives as keys
        self.tabs = self.display_drives()

        # Populate the first tab
        self.populate_tab(self.tabs.items()[0])

        # Show the main window
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

        # Dictionary of tabs
        tab_dict = OrderedDict()

        # Create a tab manager
        tabs = ttk.Notebook(self.mw)

        # Callback for changing tabs
        tabs.bind("<<NotebookTabChanged>>", self.tab_changed_callback)

        # Instantiate the drive manager
        drive_manager = Drive_Manager()

        # Collect drives
        drives = drive_manager.get_drives()

        # Display drives as tabs
        for drive in drives:
            # Create a new tab
            new_tab = ttk.Frame(tabs)
            # Add it to a dictionary
            tab_dict[drive] = new_tab
            # Add it to the main window
            tabs.add(new_tab, text='      {}      '.format(drive))

        tabs.pack(expand=1, fill='both')

        return tab_dict

    def populate_tab(self, tab):
        ''' Populate tabs based on drive contents
            @ tab - A (drive, tab) tuple where drive is the drive name string and tab is the tab object '''

        # Instantiate the drive manager
        drive_manager = Drive_Manager()

        # Get contents of the drive referred to by the tab
        contents = drive_manager.get_path_contents(tab[0], 'All')

        # List all contents in tab
        for content in enumerate(contents):
            if content[1][2] == 'd':
                new_label = Label(tab[1], text=content[1][1] + '/')
            else:
                new_label = Label(tab[1], text=content[1][1])

            new_label.grid(column=0, row=content[0])

    def tab_changed_callback(self, event):
        ''' Callback to run when a tab is changed '''

        # Get tab that was clicked
        selection = event.widget.select()

        # Get the tab name
        tab_name = event.widget.tab(selection, "text").strip()

        # Get the tab
        tab_value = self.tabs[tab_name]

        # Populate the tab
        self.populate_tab((tab_name,tab_value))
