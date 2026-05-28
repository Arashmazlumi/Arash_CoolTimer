import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import sys

try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

class CoolTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Arash_CoolTimer - Countdown Timer")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg='#1e2c3a')
        
        self.remaining_seconds = 0
        self.is_running = False
        self.paused = False
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        title = tk.Label(self.root, text="✨ Cool Timer ✨", 
                         font=('Segoe UI', 20, 'bold'), 
                         bg='#1e2c3a', fg='#ffd966')
        title.pack(pady=20)
        
        self.time_label = tk.Label(self.root, text="00:00", 
                                   font=('Courier New', 60, 'bold'),
                                   bg='#1e2c3a', fg='#f39c12')
        self.time_label.pack(pady=20)
        
        input_frame = tk.Frame(self.root, bg='#1e2c3a')
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Minutes:", font=('Segoe UI', 12), 
                 bg='#1e2c3a', fg='white').grid(row=0, column=0, padx=5)
        self.min_spinbox = tk.Spinbox(input_frame, from_=0, to=99, width=5, 
                                       font=('Segoe UI', 14), 
                                       command=self.update_from_spinbox)
        self.min_spinbox.grid(row=0, column=1, padx=5)
        self.min_spinbox.delete(0, tk.END)
        self.min_spinbox.insert(0, "0")
        
        tk.Label(input_frame, text="Seconds:", font=('Segoe UI', 12), 
                 bg='#1e2c3a', fg='white').grid(row=0, column=2, padx=5)
        self.sec_spinbox = tk.Spinbox(input_frame, from_=0, to=59, width=5, 
                                       font=('Segoe UI', 14))
        self.sec_spinbox.grid(row=0, column=3, padx=5)
        self.sec_spinbox.delete(0, tk.END)
        self.sec_spinbox.insert(0, "0")
        
        tk.Button(input_frame, text="Set Time", command=self.set_time_from_spinbox,
                  bg='#3498db', fg='white', font=('Segoe UI', 10, 'bold'),
                  padx=10).grid(row=0, column=4, padx=10)
        
        btn_frame = tk.Frame(self.root, bg='#1e2c3a')
        btn_frame.pack(pady=20)
        
        self.start_btn = tk.Button(btn_frame, text="Start", command=self.start_timer,
                                   bg='#2ecc71', fg='white', font=('Segoe UI', 12, 'bold'),
                                   width=10, padx=5)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.pause_btn = tk.Button(btn_frame, text="Pause", command=self.pause_timer,
                                   bg='#e67e22', fg='white', font=('Segoe UI', 12, 'bold'),
                                   width=10, padx=5)
        self.pause_btn.grid(row=0, column=1, padx=5)
        
        self.reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_timer,
                                   bg='#e74c3c', fg='white', font=('Segoe UI', 12, 'bold'),
                                   width=10, padx=5)
        self.reset_btn.grid(row=0, column=2, padx=5)
        
        self.status_label = tk.Label(self.root, text="⏳ Ready", 
                                     font=('Segoe UI', 10), 
                                     bg='#1e2c3a', fg='#bdc3c7')
        self.status_label.pack(pady=10)
        
        info = tk.Label(self.root, text="🔔 Beeps when time is up\n"
                                        "✅ Use 'Set Time' after changing minutes/seconds",
                        font=('Segoe UI', 9), bg='#1e2c3a', fg='#95a5a6', justify=tk.CENTER)
        info.pack(pady=10)
        
        self.update_display()
        
    def update_from_spinbox(self):
        pass
        
    def set_time_from_spinbox(self):
        if self.is_running and not self.paused:
            if messagebox.askyesno("Change time", "Timer is running. Stop and set new time?"):
                self.stop_timer()
            else:
                return
        mins = int(self.min_spinbox.get())
        secs = int(self.sec_spinbox.get())
        self.remaining_seconds = mins * 60 + secs
        self.update_display()
        self.status_label.config(text=f"Time set: {mins:02d}:{secs:02d}")
        
    def update_display(self):
        mins = self.remaining_seconds // 60
        secs = self.remaining_seconds % 60
        self.time_label.config(text=f"{mins:02d}:{secs:02d}")
        if self.remaining_seconds <= 10 and self.remaining_seconds > 0:
            self.time_label.config(fg='#e74c3c')
        else:
            self.time_label.config(fg='#f39c12')
    
    def start_timer(self):
        if self.remaining_seconds <= 0:
            messagebox.showwarning("Error", "Please set a time first!")
            return
        if self.is_running:
            if self.paused:
                self.paused = False
                self.status_label.config(text="▶ Running...")
                self.run_timer()
            else:
                messagebox.showinfo("Info", "Timer is already running!")
        else:
            self.is_running = True
            self.paused = False
            self.status_label.config(text="▶ Running...")
            self.run_timer()
    
    def run_timer(self):
        if not self.is_running or self.paused:
            return
        if self.remaining_seconds <= 0:
            self.timer_finished()
            return
        self.root.after(1000, self.tick)
    
    def tick(self):
        if not self.is_running or self.paused:
            return
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_display()
            self.run_timer()
        else:
            self.timer_finished()
    
    def timer_finished(self):
        self.is_running = False
        self.paused = False
        self.status_label.config(text="✅ Time's up!")
        self.play_sound()
        messagebox.showinfo("Timer", "Time is up!")
    
    def play_sound(self):
        if SOUND_AVAILABLE:
            for _ in range(3):
                winsound.Beep(1000, 300)
                time.sleep(0.2)
        else:
            print('\a')
            threading.Thread(target=lambda: print('\a'*3)).start()
    
    def pause_timer(self):
        if self.is_running and not self.paused:
            self.paused = True
            self.status_label.config(text="⏸ Paused")
        else:
            if not self.is_running:
                messagebox.showinfo("Info", "Timer is not running!")
            elif self.paused:
                messagebox.showinfo("Info", "Timer already paused!")
    
    def reset_timer(self):
        if self.is_running:
            self.is_running = False
            self.paused = False
        mins = int(self.min_spinbox.get())
        secs = int(self.sec_spinbox.get())
        self.remaining_seconds = mins * 60 + secs
        self.update_display()
        self.status_label.config(text="🔄 Reset")
    
    def stop_timer(self):
        self.is_running = False
        self.paused = False
        self.status_label.config(text="⏹️ Stopped")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoolTimer(root)
    root.mainloop()
