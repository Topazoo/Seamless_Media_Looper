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

        # Remove any existing content
        for widget in tab[1].winfo_children():
            widget.destroy()

        # Instantiate the drive manager
        drive_manager = Drive_Manager()

        # Get contents of the drive referred to by the tab
        contents = drive_manager.get_path_contents(tab[0], 'All')

        # Create the file viewer
        tree = ttk.Treeview(tab[1], columns=("Files", "Type"))
        tree['show'] = 'headings'
        tree.heading("Files", text="Contents")
        tree.heading("Type", text="Type")
        tree.pack(fill=BOTH, expand=1)

        for content in enumerate(contents):
            item_text = 'item_' + str(content[0])
            f_type = self.determine_file_type(content[1])
            tree.insert('', 'end', text=item_text, values=('"{}" {}'.format(content[1][1], f_type)))

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

    def determine_file_type(self, file):
        ''' Determine and return the file type
            @file - a (root, name, type) 3-tuple '''

        # TODO - Check for image and video extensions

        if file[2] == 'd':
            return "Directory"
        elif file[2] == 'f':
            return "File"
        else:
            return "Unknown"

