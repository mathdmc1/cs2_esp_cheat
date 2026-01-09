import tkinter as tk
import win32api,win32con,time,random
from win32api import GetSystemMetrics
import ctypes

class ScreenDrawer:
    def __init__(self):
        self.root = tk.Tk()
        self.transparent_color = "white"

        self.root.attributes('-fullscreen', True)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.config(cursor="none")
        self.root.wm_attributes("-transparentcolor", self.transparent_color)
        
        #self.root.configure(bg=self.transparent_color)
       
        
        self.canvas = tk.Canvas(
            self.root,
            bg=self.transparent_color,
            highlightthickness=0,takefocus=False
        )

        self.canvas.pack(fill="both", expand=True )#
        self.root.update_idletasks()
        hwnd = ctypes.windll.user32.FindWindowW(None, self.root.title())
        self.make_window_clickthrough(hwnd)
    

    def make_window_clickthrough(self, hwnd):
        ctypes.windll.user32.ShowCursor(False)
        extended_style = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, extended_style | 0x80000 | 0x20)
    def clear(self):
        self.canvas.delete("all")


    def draw_circle(self, x, y, r=15, color="red"):
        return self.canvas.create_oval(x - r, y - r, x + r, y + r, outline=color, width=2)
    

    def draw_canvas(self, x, y,z):
        
            # Adjust rectangle size based on Z-distance and screen size
            rect_size = 100000 / z
            rect_width = rect_size / 3.3
            rect_height = rect_size / 1.9

            # Calculate rectangle coordinates
            rect_x1 = x - rect_width / 2
            rect_y1 = y
            rect_x2 = x + rect_width / 2
            rect_y2 = y + rect_height * -1

            # Draw rectangle with outline
            self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, outline="#00ff00")
            # Draw line from bottom center to crosshair middle
            bottom_center_x = GetSystemMetrics(0) // 2
            bottom_center_y = GetSystemMetrics(1)
            self.canvas.create_line(bottom_center_x, bottom_center_y, x, y, fill="#0000bb")
  # Replace with the actual health value for each enemy
            
    def run(self):
        self.root.mainloop()
