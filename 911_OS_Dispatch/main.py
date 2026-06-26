import tkinter as tk
from tkinter import ttk
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

from cpu_dispatcher import CPUModule
from memory_mvt import MemoryModule
from virtual_memory import VirtualMemoryModule
from disk_router import DiskRouterModule

class ComprehensiveOSCADApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRISIS-LINK // Unified 4-in-1 OS Capstone Dashboard")
        self.root.geometry("1400x850")
        self.root.state('zoomed')  
        
        self.bg_main = "#0B192C"
        self.root.configure(bg=self.bg_main)

        self.setup_styles()
        self.build_navigation_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure(".", font=("Segoe UI", 11))
        
        style.configure("Treeview", 
                        background="#112844", 
                        foreground="#ffffff", 
                        rowheight=35, 
                        fieldbackground="#112844",
                        font=("Consolas", 11)) 

        style.configure("Treeview.Heading",
                        background="#1a365d",
                        foreground="#ffffff",
                        font=("Segoe UI", 12, "bold"),
                        padding=6)
        
        style.map("Treeview", background=[('selected', '#3182ce')], foreground=[('selected', '#ffffff')])

    def build_navigation_layout(self):
        # ==========================================
        # TOP HEADER SECTION
        # ==========================================
        self.top_frame = tk.Frame(self.root, bg=self.bg_main)
        self.top_frame.pack(fill=tk.X, side=tk.TOP, pady=10, padx=10)

        # FIX: Enforce a strict 3:1 ratio (75% Banner, 25% Menu) so they never squish each other
        self.top_frame.columnconfigure(0, weight=3) 
        self.top_frame.columnconfigure(1, weight=1) 

        # 3/4 Banner Layout
        banner_frame = tk.Frame(self.top_frame, bg=self.bg_main)
        banner_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # FIX: Stacked the title into two lines and reduced font to 18 to save horizontal space
        banner_text = "🚨 SYSTEM INTERNALS CORE DASHBOARD 🚨\n// 911 COMPUTER AIDED DISPATCH TERMINAL //"
        top_banner = tk.Label(banner_frame, text=banner_text,
                              bg="#1a365d", fg="#ff4a4a", font=("Segoe UI", 18, "bold"), pady=15, relief="raised", bd=2)
        top_banner.pack(fill=tk.BOTH, expand=True)

        # 1/4 Navigation Grid (2x2)
        nav_frame = tk.Frame(self.top_frame, bg=self.bg_main)
        nav_frame.grid(row=0, column=1, sticky="nsew")
        
        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=1)
        nav_frame.rowconfigure(0, weight=1)
        nav_frame.rowconfigure(1, weight=1)

        self.nav_buttons = []
        modules = [
            ("1. CPU Dispatch", self.show_cpu_module),
            ("2. Active Mem", self.show_memory_module),
            ("3. Virtual Mem", self.show_vm_module),
            ("4. Disk Router", self.show_storage_module)
        ]
        
        for i, (name, callback) in enumerate(modules):
            btn = tk.Button(nav_frame, text=name, font=("Segoe UI", 12, "bold"), relief="flat", bd=0, 
                            command=lambda c=callback, idx=i: self.handle_tab_switch(c, idx))
            
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
            self.nav_buttons.append(btn)

        # ==========================================
        # MODULE CONTAINER SECTION
        # ==========================================
        self.container_panel = tk.Frame(self.root, bg=self.bg_main)
        self.container_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.cpu_frame = CPUModule(self.container_panel)
        self.memory_frame = MemoryModule(self.container_panel)
        self.vm_frame = VirtualMemoryModule(self.container_panel)
        self.disk_frame = DiskRouterModule(self.container_panel)

        # Default initialization
        self.handle_tab_switch(self.show_cpu_module, 0)
    def handle_tab_switch(self, callback, active_index):
        """Highlights the active tab and shadows out the idle ones."""
        active_bg = "#3182ce"
        active_fg = "#ffffff"
        idle_bg = "#060f1c"  
        idle_fg = "#4a6282" 
        
        for i, btn in enumerate(self.nav_buttons):
            if i == active_index:
                btn.configure(bg=active_bg, fg=active_fg)
            else:
                btn.configure(bg=idle_bg, fg=idle_fg)
        
        callback()

    # =========================================================================
    # MODULE DISPLAY SWITCHERS
    # =========================================================================
    def show_cpu_module(self):
        self.memory_frame.pack_forget()
        self.vm_frame.pack_forget()
        self.disk_frame.pack_forget()
        self.cpu_frame.pack(fill=tk.BOTH, expand=True)

    def show_memory_module(self):
        self.cpu_frame.pack_forget()
        self.vm_frame.pack_forget()
        self.disk_frame.pack_forget()
        self.memory_frame.pack(fill=tk.BOTH, expand=True)

    def show_vm_module(self):
        self.cpu_frame.pack_forget()
        self.memory_frame.pack_forget()
        self.disk_frame.pack_forget()
        self.vm_frame.pack(fill=tk.BOTH, expand=True)

    def show_storage_module(self):
        self.cpu_frame.pack_forget()
        self.memory_frame.pack_forget()
        self.vm_frame.pack_forget()
        self.disk_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ComprehensiveOSCADApp(root)
    root.mainloop()