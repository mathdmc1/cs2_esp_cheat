import tkinter as tk
import win32api,win32con,time,random
from win32api import GetSystemMetrics
class ScreenDrawer:
    def __init__(self):
        self.root = tk.Tk()

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        self.transparent_color = "magenta"
        self.root.configure(bg=self.transparent_color)
        self.root.attributes("-transparentcolor", self.transparent_color)
        self.root.bind("<Button-1>", self.on_canvas_click)
        self.canvas = tk.Canvas(
            self.root,
            bg=self.transparent_color,
            highlightthickness=0,takefocus=False
        )
        self.canvas.pack(fill="both", expand=True)
    

    def on_canvas_click(self, event):
            # Check if the click occurred within the region occupied by the drawn elements
            x, y = event.x, event.y
            if self.canvas.find_overlapping(x, y, x, y):
                # release if clicked on overlay so it doesnt hang
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                # Simulate a click at the calculated position to get focus back
                win32api.SetCursorPos((x - 50, y - 2000))
                time.sleep(0.08)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                time.sleep(random.uniform(0.01, 0.03))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            return "break"
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
