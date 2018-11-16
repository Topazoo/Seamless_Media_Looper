import os

class Drive_Manager(object):
    ''' Removable drive manager '''

    def __init__(self):

        # Detect connected drives
        self.drives = self.get_drives()

    def get_drives(self):
        ''' Collect connected removable storage '''

        # Handle Windows drives
        if os.name == 'nt':
            possible_drives = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            drives = ['%s:\\' % drive for drive in possible_drives if os.path.exists('%s:' % drive)]
            return drives

        #TODO - Raspbian drives


    def get_path_contents(self, dir, content):
        ''' Get the contents of a directory
            @dir - The directory to map
            @content - A string: Either 'All', 'Dir', or 'File' depending on what type to retrieve
                        'All' returns a tuple of directories and files '''

        contents = []

        # Collect all top-level files and directories
        if content == 'All':
            for root, dirs, files in os.walk(dir):
                for d in dirs:
                    if d[0] != '.' and d[0] != '$':
                        add_dir = (root, d, 'd')
                        contents.append(add_dir)
                for f in files:
                    add_file = (root, f, 'f')
                    contents.append(add_file)

                break

        # Collect all top-level directories
        if content == 'Dir':
            for root, dirs, files in os.walk(dir):
                for d in dirs:
                    if d[0] != '.' and d[0] != '$':
                        add_dir = (root, d, 'd')
                        contents.append(add_dir)

                break

        # Collect all top-level files
        if content == 'File':
            for root, dirs, files in os.walk(dir):
                for f in files:
                    add_file = (root, f, 'f')
                    contents.append(add_file)

                break

        return contents
