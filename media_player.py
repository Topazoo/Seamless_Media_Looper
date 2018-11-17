import Tkinter as tk
from PIL import ImageTk, Image

class Media_Player(object):
    ''' Media player '''

    def display_image(self, path):

        # Create a fullscreen image window
        window = tk.Toplevel()
        window.wm_attributes('-fullscreen', 'true')

        # Load the image with tk
        img = ImageTk.PhotoImage(Image.open(path))

        # Add the image to the window
        image_label = tk.Label(window, image=img)
        image_label.configure(bg='black')

        # The Pack geometry manager packs widgets in rows or columns.
        image_label.pack(side="bottom", fill="both", expand="yes")

        # Set focus on the window
        window.focus_set()

        # Bind escape key to quit the window
        window.bind("<Escape>", lambda quit_window: quit_window.widget.destroy())

        # Start the GUI
        window.mainloop()