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
            drives = ['%s:' % drive for drive in possible_drives if os.path.exists('%s:' % drive)]
            return drives

        #TODO - Raspbian drives

