import os

class Drive_Manager(object):
    ''' Removable drive manager '''

    image_extensions = ['.jpg', '.jpeg', '.png']
    movie_extensions = ['.mp4', '.mov']

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

        elif os.name == 'posix':
            drives = []
            # Get all users
            paths = self.get_path_contents('/media/', 'Dir')
            # Get all devices
            for path in paths:
                full_path = path[0] + path[1] + '/'
                path_drives = self.get_path_contents(full_path, 'Dir')
                for drive in path_drives:
                    drives.append(drive[0] + drive[1])

            return drives

        else:
            raise OSError('Sorry, this application is incompatible with the ' + os.name + ' operating system.')


    def get_path_contents(self, dir, content, media_only=False):
        ''' Get the contents of a directory
            @dir - The directory to map
            @content - A string: Either 'All', 'Dir', or 'File' depending on what type to retrieve
                        'All' returns a tuple of directories and files
            @media_only - True if only media and directories should be collected '''

        contents = []

        # Collect all top-level files and directories
        if content == 'All':
            for root, dirs, files in os.walk(dir):
                for d in dirs:
                    if d[0] != '.' and d[0] != '$':
                        add_dir = (root, d, 'Directory')
                        contents.append(add_dir)
                for f in files:
                    f_type = self.determine_file_type(f)
                    if not media_only or (media_only and f_type == "Image") or (media_only and f_type == "Video"):
                        add_file = (root, f, f_type)
                        contents.append(add_file)
                break

        # Collect all top-level directories
        if content == 'Dir':
            for root, dirs, files in os.walk(dir):
                for d in dirs:
                    if d[0] != '.' and d[0] != '$':
                        add_dir = (root, d, 'Directory')
                        contents.append(add_dir)

                break

        # Collect all top-level files
        if content == 'File':
            for root, dirs, files in os.walk(dir):
                for f in files:
                    f_type = self.determine_file_type(f)
                    if not media_only or (media_only and f_type == "Image") or (media_only and f_type == "Video"):
                        add_file = (root, f, f_type)
                        contents.append(add_file)

                break

        return contents

    def determine_file_type(self, file_t):
        ''' Determine and return the file type
            @file_t - The file to determine type '''

        # Find the index of the extension
        ext_index = file_t.rfind('.')

        # Handle no extension
        if ext_index == -1:
            return "File"

        # Parse extension
        ext = file_t[ext_index::]

        # Check if photo
        if ext in self.image_extensions:
            return "Image"

        # Check if video
        if ext in self.movie_extensions:
            return "Video"

        return "File"
