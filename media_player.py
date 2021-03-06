import vlc
import os
import Tkinter as tk
from PIL import ImageTk, Image

class VLC_Player(object):
    ''' Window to display videos '''

    def __init__(self, path, video_label_id):
        ''' @path - The path of the file to load
            @video_label_id - The id of the window to attach to
            @loop - True if the media should be looped'''

        self.path = path

        # Instantiate video player
        self.vlc_root = vlc.Instance()
        self.player = self.vlc_root.media_player_new()

        # Assign to window
        if os.name == "nt":
            self.player.set_hwnd(video_label_id)
        elif os.name == "posix":
            self.player.set_xwindow(video_label_id)

        self.load_video(path)

    def load_video(self, path):
        # Load video
        video = self.vlc_root.media_new(path)
        self.player.set_media(video)

    def play(self, loop):
        ''' Play video '''

        if loop:
            # Create and bind events
            player_events = self.player.event_manager()
            player_events.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.video_playing_callback)

        self.player.play()

    def stop(self):
        ''' Stop video '''

        self.player.stop()

    def video_playing_callback(self, event):
        ''' Reset position if within 1/5 of a second of the end '''

        diff = self.player.get_length() - self.player.get_time()

        if diff <= 200 or self.player.get_time() >= self.player.get_length():
            self.player.set_position(0)

class Image_Viewer(object):
    ''' Image viewer'''

    def resize_image(self, raw_image, base_width, base_height):
        ''' Resize an image to fit a width and height maintaining aspect-ratio
            @raw_image - The image to resize
            @base_width - The width to resize to
            @base_height - The height to resize to '''

        # If the original image is too wide
        if base_width < raw_image.size[0]:
            # Get the percentage to scale the width down by
            width_percentage = base_width / float(raw_image.size[0])
            # Get the height scaled down by that percentage
            new_height = int(width_percentage * float(raw_image.size[1]))
            # Resize the image
            raw_image = raw_image.resize((base_width, new_height), Image.ANTIALIAS)

        # If the original image or new image is too tall
        if base_height < raw_image.size[1]:
            # Get the percentage to scale the height down by
            height_percentage = base_height / float(raw_image.size[1])
            # Get the width scaled down by that percentage
            new_width = int(height_percentage * float(raw_image.size[0]))
            # Resize the image
            raw_image = raw_image.resize((new_width, base_height), Image.ANTIALIAS)

        return raw_image

    def display_image(self, path):
        ''' Display an image in fullscreen
            @path - The path to the image '''

        # Create a fullscreen image window
        window = tk.Toplevel()
        window.wm_attributes('-fullscreen', 'true')

        # Load the image with tk
        raw_image = Image.open(path)
        raw_image = self.resize_image(raw_image, window.winfo_screenwidth(), window.winfo_screenheight())
        img = ImageTk.PhotoImage(raw_image)

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

class Video_Player(object):
    def __init__(self, path):

        # Create the video window
        self.window_id = self.create_video_window()
        self.vlc_player = VLC_Player(path, self.window_id)

    def create_video_window(self):
        ''' Create the player window in the GUI '''

        # Create a fullscreen video window
        window = tk.Toplevel()
        window.wm_attributes('-fullscreen', 'true')

        # Add the video to the window
        video_label = tk.Label(window)
        video_label.configure(bg='black')

        # The Pack geometry manager packs widgets in rows or columns.
        video_label.pack(side="bottom", fill="both", expand="yes")

        # Set focus on the window
        window.focus_set()

        # Bind escape key to quit the window
        window.bind("<Escape>", self.video_exit_callback)

        video_label_id = video_label.winfo_id()

        return video_label_id

    def play_video(self, loop=False):
        ''' Play a video in fullscreen
            @loop - True if media should be looped '''

        # Play media
        self.vlc_player.play(loop)

    def video_exit_callback(self, event):
        ''' Callback when window is destroyed '''

        # Stop the playing video
        self.vlc_player.stop()

        # Quit the window
        event.widget.destroy()