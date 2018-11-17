from Tkinter import *
import ttk
import os
from drive_manager import Drive_Manager
from media_player import Media_Player
from collections import OrderedDict

class View_Tree(object):
    ''' Hierarchy viewer for the GUI '''

    def __init__(self, tab):
        '''@tab - the tab to attach the view to '''

        # Create the file viewer
        self.tree = ttk.Treeview(tab, columns=("Root", "Files", "Type"))

        # Create headers
        self.tree.heading("Files", text="Contents")
        self.tree.heading("Type", text="Type")
        self.tree.column("#0", width=240, stretch=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=0)
        self.tree.column('#3', stretch=NO, minwidth=120, width=120)

        # Set event callback for double click
        self.tree.bind("<Double-1>", self.tree_double_click_callback)
        # Set event callback for enter key press
        self.tree.bind('<Return>', self.tree_double_click_callback)

    def populate_tree(self, contents, element=''):
        ''' Populate the file viewer
            @element - The tree or tree element to attach to
            @contents - A list of contents to populate the viewer with '''

        for content in contents:
            # Insert all contents
            insert = content[0]
            if element == '' and os.name == "nt":
                insert += '\\'
            elif element =='' and os.name == "posix":
                insert += '/'

            content_str = '"{}" "{}" "{}"'.format(insert, content[1], content[2])

            self.tree.insert(element, 'end', text=content[0],
                             values=content_str)

    def tree_double_click_callback(self, event):
        ''' Callback to run when a treeview button is clicked '''

        drive_manager = Drive_Manager()

        # Get ID of selection
        selection = self.tree.selection()
        item = selection[0]
        item_vals = self.tree.item(item, "value")
        item_text = self.tree.item(item, "text")

        # If it's a directory
        if item_vals[2] == 'Directory':
            # Delete children if they exist
            children = self.tree.get_children(item)
            if len(children) > 0:
                self.tree.delete(children)

            if os.name == "nt":
                new_path = item_text + "\\" + item_vals[1]
            elif os.name == "posix":
                new_path = item_text + "/" + item_vals[1]

            # Get contents of the drive referred to by the tab
            contents = drive_manager.get_path_contents(new_path, 'All', media_only=True)

            self.populate_tree(contents, item)

        # TODO - Otherwise play the video
        else:
            media_player = Media_Player()

            # Display image if selected
            if item_vals[2] == "Image":
                if os.name == 'nt':
                    full_path = item_text + '\\' + item_vals[1]
                elif os.name == 'posix':
                    full_path = item_text + '/' + item_vals[1]

                media_player.display_image(full_path)

    def show(self):
        self.tree.pack(fill=BOTH, expand=1)
        self.tree.selection_set(self.tree.get_children()[0])
        self.tree.focus(self.tree.get_children()[0])
        self.tree.focus_set()

class Player_GUI(object):
    ''' Media player GUI '''

    def __init__(self):
        # Create main window
        self.mw = self.create_main_window()

        # Create a tab manager
        self.notebook = ttk.Notebook(self.mw)

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
        if os.name == "nt":
            root.state('zoomed')
        elif os.name == "posix":
            root.attributes('-zoomed', True)

        return root

    def display_drives(self):
        ''' Display the connected drives '''

        # Dictionary of tabs
        tab_dict = OrderedDict()

        # Callbacks for changing tabs
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_changed_callback)
        self.notebook.bind("<Tab>", self.tab_pressed_callback)

        # Instantiate the drive manager
        drive_manager = Drive_Manager()

        # Collect drives
        drives = drive_manager.get_drives()

        # Display drives as tabs
        for drive in drives:
            # Create a new tab
            new_tab = ttk.Frame(self.notebook)
            # Add it to a dictionary
            tab_dict[drive] = new_tab
            # Add it to the main window
            self.notebook.add(new_tab, text='      {}      '.format(drive))

        self.notebook.pack(expand=1, fill='both')

        return tab_dict

    def populate_tab(self, tab):
        ''' Populate tabs based on drive contents
            @ tab - A (drive, tab) tuple where drive is the drive name string and tab is the tab object '''

        # Remove any existing content
        for widget in tab[1].winfo_children():
            widget.destroy()

        # Instantiate the drive manager
        drive_manager = Drive_Manager()

        # Create a tree
        tree = View_Tree(tab[1])

        # Get contents of the drive referred to by the tab
        contents = drive_manager.get_path_contents(tab[0], 'All', media_only=True)

        # Populate the tree
        tree.populate_tree(contents)

        # Place the file viewer
        tree.show()

    def tab_pressed_callback(self, event):
        ''' Callback to run when the tab key is pressed '''

        self.notebook.tab(self.notebook.select())


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

