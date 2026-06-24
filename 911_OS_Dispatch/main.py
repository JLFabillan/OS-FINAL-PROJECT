import tkinter as tk
from tkinter import ttk, messagebox
import sys
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
import copy

# --- Import Backend Modules ---
try:
    from dispatcher_cpu import Incident, Dispatcher
    from memory_logs import DispatchMemoryManager
    from sstf_routing import DroneRouter
    from virtual_memory_pages import PageReplacementSimulator
    from storage_archive import PoliceDatabaseArchive
except ImportError as e:
    print(f"Error importing modules. Make sure all files are in the same folder.\nDetails: {e}")
    sys.exit(1)

# --- UI Text Redirector ---
class PrintLogger:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.configure(state="disabled")

    def write(self, message):
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state="disabled")

    def flush(self):
        pass

class DispatchDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("911 OS Dispatch System - Full Interactive Dashboard")
        self.geometry("1300x900") # Made the window slightly larger to fit the new text
        self.configure(bg="#2c3e50")

        # --- Master UI Font Styling ---
        style = ttk.Style()
        style.configure(".", font=("Arial", 14))
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        style.configure("Treeview", font=("Arial", 14), rowheight=35) # Taller rows
        style.configure("TLabelframe.Label", font=("Arial", 14, "bold"))
        style.configure("TButton", font=("Arial", 14))

        # Global States
        self.user_incidents = []
        self.incident_counter = 1
        self.memory_manager = DispatchMemoryManager(total_memory_kb=1000, mode="MVT")
        self.storage_db = PoliceDatabaseArchive(total_blocks=50)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Initialize All Tabs
        self.init_cpu_tab()
        self.init_memory_tab()
        self.init_virtual_mem_tab()
        self.init_sstf_tab()
        self.init_storage_tab()

    # ==========================================
    # TAB 1: CPU SCHEDULING
    # ==========================================
    def init_cpu_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="1. CPU Dispatcher")

        input_frame = ttk.LabelFrame(frame, text="Log New 911 Incident")
        input_frame.pack(fill='x', padx=10, pady=5)

        input_font = ("Arial", 14)
        ttk.Label(input_frame, text="Desc:", font=input_font).grid(row=0, column=0, padx=5)
        self.entry_desc = ttk.Entry(input_frame, width=15, font=input_font)
        self.entry_desc.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Arrival:", font=input_font).grid(row=0, column=2, padx=5)
        self.entry_arrival = ttk.Entry(input_frame, width=6, font=input_font)
        self.entry_arrival.grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="Burst:", font=input_font).grid(row=0, column=4, padx=5)
        self.entry_burst = ttk.Entry(input_frame, width=6, font=input_font)
        self.entry_burst.grid(row=0, column=5, padx=5)

        ttk.Label(input_frame, text="Priority (1=High):", font=input_font).grid(row=0, column=6, padx=5)
        self.entry_priority = ttk.Entry(input_frame, width=6, font=input_font)
        self.entry_priority.grid(row=0, column=7, padx=5)

        ttk.Button(input_frame, text="Add", command=self.add_incident).grid(row=0, column=8, padx=5)
        ttk.Button(input_frame, text="🎲 Randomize", command=self.random_cpu).grid(row=0, column=9, padx=10)

        cols = ("ID", "Description", "Arrival Time", "Burst Time", "Priority")
        self.cpu_table = ttk.Treeview(frame, columns=cols, show="headings", height=4)
        for col in cols: self.cpu_table.heading(col, text=col)
        self.cpu_table.pack(fill='x', padx=10, pady=5)

        ctrl_frame = ttk.Frame(frame)
        ctrl_frame.pack(fill='x', padx=10, pady=5)
        ttk.Label(ctrl_frame, text="Algorithm:", font=input_font).pack(side='left')
        self.cpu_algo = ttk.Combobox(ctrl_frame, values=["FCFS", "SJF (Non-Preemptive)", "SRTF (Preemptive)", "Round Robin"], font=input_font)
        self.cpu_algo.set("FCFS")
        self.cpu_algo.pack(side='left', padx=5)
        ttk.Button(ctrl_frame, text="Run Dispatch", command=self.run_cpu_sim).pack(side='left', padx=5)
        ttk.Button(ctrl_frame, text="Clear Queue", command=self.clear_cpu).pack(side='left', padx=5)

        bot_frame = ttk.Frame(frame)
        bot_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        log_frame = ttk.LabelFrame(bot_frame, text="System Execution Log")
        log_frame.pack(side='left', expand=True, fill='both', padx=(0, 5))
        
        # Increased Text Box Font to 14
        self.cpu_log = tk.Text(log_frame, bg="#1e1e1e", fg="#e0e0e0", font=("Consolas", 14), width=45, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(log_frame, command=self.cpu_log.yview)
        self.cpu_log.configure(yscrollcommand=scrollbar.set)
        
        self.cpu_log.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')

        self.cpu_fig, self.cpu_ax = plt.subplots()
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=bot_frame)
        self.cpu_canvas.get_tk_widget().pack(side='right', expand=True, fill='both')

    def random_cpu(self):
        emergencies = ["Bank Robbery", "House Fire", "Traffic Stop", "Heart Attack", "Noise Complaint", "Assault", "Missing Person", "Fender Bender"]
        self.entry_desc.delete(0, tk.END); self.entry_desc.insert(0, random.choice(emergencies))
        self.entry_arrival.delete(0, tk.END); self.entry_arrival.insert(0, str(random.randint(0, 15)))
        self.entry_burst.delete(0, tk.END); self.entry_burst.insert(0, str(random.randint(2, 12)))
        self.entry_priority.delete(0, tk.END); self.entry_priority.insert(0, str(random.randint(1, 3)))

    def add_incident(self):
        try:
            desc = self.entry_desc.get() or f"Inc-{self.incident_counter}"
            arr = int(self.entry_arrival.get())
            brst = int(self.entry_burst.get())
            pri = int(self.entry_priority.get())
            self.user_incidents.append(Incident(self.incident_counter, desc, pri, brst, arr))
            self.cpu_table.insert("", "end", values=(self.incident_counter, desc, arr, brst, pri))
            self.incident_counter += 1
            for e in (self.entry_desc, self.entry_arrival, self.entry_burst, self.entry_priority): e.delete(0, tk.END)
        except ValueError: messagebox.showerror("Error", "Numerical fields require integers.")

    def clear_cpu(self):
        self.user_incidents.clear()
        self.incident_counter = 1
        for item in self.cpu_table.get_children(): self.cpu_table.delete(item)
        self.cpu_ax.clear()
        self.cpu_canvas.draw()
        
        self.cpu_log.configure(state="normal")
        self.cpu_log.delete(1.0, tk.END)
        self.cpu_log.configure(state="disabled")

    def run_cpu_sim(self):
        if not self.user_incidents: return messagebox.showwarning("Warning", "Queue is empty.")
        
        self.cpu_log.configure(state="normal")
        self.cpu_log.delete(1.0, tk.END)
        self.cpu_log.configure(state="disabled")
        
        sys.stdout = PrintLogger(self.cpu_log)
        
        dispatcher = Dispatcher(copy.deepcopy(self.user_incidents))
        algo = self.cpu_algo.get()
        if algo == "FCFS": dispatcher.run_fcfs()
        elif algo == "SJF (Non-Preemptive)": dispatcher.run_sjf_non_preemptive()
        elif algo == "SRTF (Preemptive)": dispatcher.run_srtf()
        elif algo == "Round Robin": dispatcher.run_round_robin(time_quantum=3)
        sys.stdout = sys.__stdout__
        
        self.cpu_ax.clear()
        dispatcher.completed.sort(key=lambda x: x.completion_time)
        
        x_ticks = set() 
        x_ticks.add(0)  
        
        for i, inc in enumerate(dispatcher.completed):
            start = max(inc.completion_time - inc.burst_time, inc.arrival_time)
            self.cpu_ax.barh(i, inc.burst_time, left=start, color='#4A90E2', edgecolor='black')
            
            # Matplotlib font size 14
            self.cpu_ax.text(start + (inc.burst_time/2), i, f"ID:{inc.incident_id}", 
                             ha='center', va='center', color='white', fontweight='bold', fontsize=14)
            
            x_ticks.add(start)
            x_ticks.add(inc.completion_time)
        
        self.cpu_ax.set_yticks(range(len(dispatcher.completed)))
        
        # Applied fontsize=14 to all Matplotlib elements
        self.cpu_ax.set_yticklabels([inc.description for inc in dispatcher.completed], fontsize=14)
        self.cpu_ax.set_xlabel("Time Units", fontsize=14, fontweight='bold')
        self.cpu_ax.set_title("Dispatch Timeline (Gantt Chart)", fontsize=16, fontweight='bold')
        
        sorted_ticks = sorted(list(x_ticks))
        self.cpu_ax.set_xticks(sorted_ticks)
        self.cpu_ax.set_xticklabels(sorted_ticks, fontsize=14)
        
        self.cpu_ax.grid(axis='x', linestyle='--', alpha=0.5)
        
        # Ensure the layout doesn't cut off the larger text
        self.cpu_fig.tight_layout()
        self.cpu_canvas.draw()

# ==========================================
    # TAB 2: MEMORY MANAGEMENT (MVT & MFT)
    # ==========================================
    def init_memory_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="2. Active Memory (MVT/MFT)")

        input_frame = ttk.LabelFrame(frame, text="Memory Allocation Control (Total: 1000KB)")
        input_frame.pack(fill='x', padx=10, pady=5)

        # --- Row 0: Inputs ---
        ttk.Label(input_frame, text="System Mode:").grid(row=0, column=0, padx=5, pady=5)
        self.mem_mode = ttk.Combobox(input_frame, values=["MVT (Variable)", "MFT (Fixed)"], width=14)
        self.mem_mode.set("MVT (Variable)")
        self.mem_mode.grid(row=0, column=1, padx=5, pady=5)
        self.mem_mode.bind("<<ComboboxSelected>>", self.change_memory_mode) # Triggers function on change

        ttk.Label(input_frame, text="Incident ID:").grid(row=0, column=2, padx=5, pady=5)
        self.mem_id = ttk.Entry(input_frame, width=8)
        self.mem_id.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Size (KB):").grid(row=0, column=4, padx=5, pady=5)
        self.mem_size = ttk.Entry(input_frame, width=8)
        self.mem_size.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(input_frame, text="Algorithm:").grid(row=0, column=6, padx=5, pady=5)
        self.mem_algo = ttk.Combobox(input_frame, values=["First Fit", "Best Fit", "Worst Fit"], width=10)
        self.mem_algo.set("First Fit")
        self.mem_algo.grid(row=0, column=7, padx=5, pady=5)

        # --- Row 1: Buttons ---
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=1, column=0, columnspan=8, pady=5)
        
        ttk.Button(btn_frame, text="Allocate", command=self.alloc_mem).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Deallocate ID", command=self.dealloc_mem).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Run Compaction", command=self.compact_mem).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🎲 Randomize", command=self.random_mem).pack(side='left', padx=15)

        # --- Graphics & Logs ---
        bot_frame = ttk.Frame(frame)
        bot_frame.pack(expand=True, fill='both', padx=10, pady=5)
        self.mem_log = tk.Text(bot_frame, bg="black", fg="cyan", font=("Consolas", 10), width=45)
        self.mem_log.pack(side='left', expand=True, fill='both')
        self.mem_fig, self.mem_ax = plt.subplots(figsize=(6, 2))
        self.mem_canvas = FigureCanvasTkAgg(self.mem_fig, master=bot_frame)
        self.mem_canvas.get_tk_widget().pack(side='right', expand=True, fill='both')
        self.draw_memory_map()

    def change_memory_mode(self, event=None):
        """Reboots the memory map when the user switches between MVT and MFT."""
        mode = self.mem_mode.get()
        self.mem_log.delete(1.0, tk.END)
        sys.stdout = PrintLogger(self.mem_log)
        
        if "MFT" in mode:
            print("--- System Reboot: Switching to MFT Mode ---")
            print("Establishing fixed hardware partitions: [100k, 150k, 250k, 500k]")
            # We pass specific hardwired partitions for MFT
            self.memory_manager = DispatchMemoryManager(mode="MFT", mft_partitions=[100, 150, 250, 500])
        else:
            print("--- System Reboot: Switching to MVT Mode ---")
            print("Establishing unified dynamic pool: 1000k")
            # We pass the full 1000k pool for MVT
            self.memory_manager = DispatchMemoryManager(total_memory_kb=1000, mode="MVT")
            
        sys.stdout = sys.__stdout__
        self.draw_memory_map()

    def random_mem(self):
        self.mem_id.delete(0, tk.END); self.mem_id.insert(0, str(random.randint(400, 499)))
        self.mem_size.delete(0, tk.END); self.mem_size.insert(0, str(random.randint(30, 250)))

    def alloc_mem(self):
        try:
            sys.stdout = PrintLogger(self.mem_log)
            self.memory_manager.allocate(int(self.mem_id.get()), int(self.mem_size.get()), self.mem_algo.get())
            sys.stdout = sys.__stdout__
            self.draw_memory_map()
        except ValueError: messagebox.showerror("Error", "Enter valid integers.")

    def dealloc_mem(self):
        try:
            sys.stdout = PrintLogger(self.mem_log)
            self.memory_manager.deallocate(int(self.mem_id.get()))
            sys.stdout = sys.__stdout__
            self.draw_memory_map()
        except ValueError: messagebox.showerror("Error", "Enter Incident ID.")

    def compact_mem(self):
        sys.stdout = PrintLogger(self.mem_log)
        self.memory_manager.compact_memory()
        sys.stdout = sys.__stdout__
        self.draw_memory_map()

    def draw_memory_map(self):
        self.mem_ax.clear()
        for block in self.memory_manager.memory_map:
            color = 'lightgrey' if block.is_free else 'crimson'
            self.mem_ax.barh(0, block.size, left=block.start_address, color=color, edgecolor='black')
            
            # Add grid lines for MFT so the user can easily see the fixed walls
            if self.memory_manager.mode == "MFT":
                self.mem_ax.axvline(block.start_address, color='black', linewidth=2)
                self.mem_ax.axvline(block.start_address + block.size, color='black', linewidth=2)

            if block.size > 40: 
                label = "FREE" if block.is_free else f"ID:{block.incident_id}"
                self.mem_ax.text(block.start_address + (block.size/2), 0, label, ha='center', va='center', rotation=90)
        
        self.mem_ax.set_yticks([])
        self.mem_ax.set_xlabel("Memory Address (KB)")
        mode_text = "Variable Pool" if self.memory_manager.mode == "MVT" else "Fixed Partitions"
        self.mem_ax.set_title(f"Live RAM Bandwidth Allocation ({mode_text})")
        self.mem_canvas.draw()

    # ==========================================
    # TAB 3: VIRTUAL MEMORY
    # ==========================================
    def init_virtual_mem_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="3. Virtual Pages")

        input_frame = ttk.LabelFrame(frame, text="Page Replacement Configuration")
        input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(input_frame, text="Reference String (comma separated):").grid(row=0, column=0, padx=5)
        self.entry_ref = ttk.Entry(input_frame, width=30)
        self.entry_ref.insert(0, "1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5")
        self.entry_ref.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Frames (Monitors):").grid(row=0, column=2, padx=5)
        self.entry_frames = ttk.Entry(input_frame, width=5)
        self.entry_frames.insert(0, "3")
        self.entry_frames.grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="Algorithm:").grid(row=0, column=4, padx=5)
        self.page_algo = ttk.Combobox(input_frame, values=["FIFO", "LRU", "Optimal", "Second Chance", "LFU", "MFU"])
        self.page_algo.set("FIFO")
        self.page_algo.grid(row=0, column=5, padx=5)

        ttk.Button(input_frame, text="Simulate", command=self.run_page_sim).grid(row=0, column=6, padx=5)
        ttk.Button(input_frame, text="🎲 Randomize", command=self.random_pages).grid(row=0, column=7, padx=10)

        self.page_log = tk.Text(frame, bg="black", fg="yellow", font=("Consolas", 11))
        self.page_log.pack(expand=True, fill='both', padx=10, pady=5)

    def random_pages(self):
        # Generate a string of 12-15 random numbers between 1 and 8
        seq_length = random.randint(12, 15)
        random_sequence = [str(random.randint(1, 8)) for _ in range(seq_length)]
        self.entry_ref.delete(0, tk.END)
        self.entry_ref.insert(0, ", ".join(random_sequence))
        self.entry_frames.delete(0, tk.END)
        self.entry_frames.insert(0, str(random.randint(3, 5)))

    def run_page_sim(self):
        try:
            self.page_log.delete(1.0, tk.END)
            sys.stdout = PrintLogger(self.page_log)
            
            ref_str = [int(x.strip()) for x in self.entry_ref.get().split(",")]
            frames = int(self.entry_frames.get())
            
            sim = PageReplacementSimulator(num_frames=frames)
            algo = self.page_algo.get()
            
            if algo == "FIFO": sim.run_fifo(ref_str)
            elif algo == "LRU": sim.run_lru(ref_str)
            elif algo == "Optimal": sim.run_optimal(ref_str)
            elif algo == "Second Chance": sim.run_second_chance_clock(ref_str)
            elif algo == "LFU": sim.run_lfu(ref_str)
            elif algo == "MFU": sim.run_mfu(ref_str)
            
            sys.stdout = sys.__stdout__
        except ValueError:
            sys.stdout = sys.__stdout__
            messagebox.showerror("Error", "Reference string must be integers separated by commas.")

    # ==========================================
    # TAB 4: SSTF ROUTING
    # ==========================================
    def init_sstf_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="4. SSTF Drone Routing")

        input_frame = ttk.LabelFrame(frame, text="Drone Sector Routing")
        input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(input_frame, text="Initial Position:").grid(row=0, column=0, padx=5)
        self.entry_initial = ttk.Entry(input_frame, width=8)
        self.entry_initial.insert(0, "50")
        self.entry_initial.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Emergencies (comma separated):").grid(row=0, column=2, padx=5)
        self.entry_sectors = ttk.Entry(input_frame, width=40)
        self.entry_sectors.insert(0, "82, 170, 43, 140, 24, 16, 190")
        self.entry_sectors.grid(row=0, column=3, padx=5)

        ttk.Button(input_frame, text="Map Route", command=self.run_sstf).grid(row=0, column=4, padx=5)
        ttk.Button(input_frame, text="🎲 Randomize", command=self.random_sstf).grid(row=0, column=5, padx=10)

        bot_frame = ttk.Frame(frame)
        bot_frame.pack(expand=True, fill='both', padx=10, pady=5)
        self.sstf_log = tk.Text(bot_frame, bg="black", fg="white", font=("Consolas", 10), width=40)
        self.sstf_log.pack(side='left', expand=True, fill='both')
        self.sstf_fig, self.sstf_ax = plt.subplots()
        self.sstf_canvas = FigureCanvasTkAgg(self.sstf_fig, master=bot_frame)
        self.sstf_canvas.get_tk_widget().pack(side='right', expand=True, fill='both')

    def random_sstf(self):
        self.entry_initial.delete(0, tk.END)
        self.entry_initial.insert(0, str(random.randint(0, 199)))
        
        # Generate 6 to 9 random sectors between 0 and 199
        num_sectors = random.randint(6, 9)
        random_sectors = [str(random.randint(0, 199)) for _ in range(num_sectors)]
        self.entry_sectors.delete(0, tk.END)
        self.entry_sectors.insert(0, ", ".join(random_sectors))

    def run_sstf(self):
        try:
            self.sstf_log.delete(1.0, tk.END)
            sys.stdout = PrintLogger(self.sstf_log)
            
            initial = int(self.entry_initial.get())
            sectors = [int(x.strip()) for x in self.entry_sectors.get().split(",")]
            
            drone = DroneRouter(initial)
            route, dist = drone.calculate_sstf(sectors)
            sys.stdout = sys.__stdout__

            self.sstf_ax.clear()
            y_order = list(range(len(route))) 
            self.sstf_ax.plot(route, y_order, marker='o', linestyle='-', color='red', markersize=8)
            self.sstf_ax.set_title(f"SSTF Routing Path (Total Tracks: {dist})")
            self.sstf_ax.set_xlabel("Sector Location")
            self.sstf_ax.set_ylabel("Sequence")
            self.sstf_ax.invert_yaxis() 
            self.sstf_ax.grid(True, linestyle='--', alpha=0.6)
            for i, txt in enumerate(route):
                self.sstf_ax.annotate(txt, (route[i], y_order[i]), textcoords="offset points", xytext=(0,10), ha='center')
            self.sstf_canvas.draw()
        except ValueError:
            sys.stdout = sys.__stdout__
            messagebox.showerror("Error", "Inputs must be comma-separated integers.")

    # ==========================================
    # TAB 5: STORAGE ARCHIVE
    # ==========================================
    def init_storage_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="5. Storage Archive")

        input_frame = ttk.LabelFrame(frame, text="Permanent Database Archiving")
        input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(input_frame, text="Incident ID:").grid(row=0, column=0, padx=5)
        self.store_id = ttk.Entry(input_frame, width=8)
        self.store_id.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="File Size (Blocks):").grid(row=0, column=2, padx=5)
        self.store_size = ttk.Entry(input_frame, width=8)
        self.store_size.grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="Method:").grid(row=0, column=4, padx=5)
        self.store_algo = ttk.Combobox(input_frame, values=["Contiguous", "Linked", "Indexed"])
        self.store_algo.set("Contiguous")
        self.store_algo.grid(row=0, column=5, padx=5)

        ttk.Button(input_frame, text="Save to Disk", command=self.run_storage).grid(row=0, column=6, padx=5)
        ttk.Button(input_frame, text="🎲 Randomize", command=self.random_storage).grid(row=0, column=7, padx=10)

        bot_frame = ttk.Frame(frame)
        bot_frame.pack(expand=True, fill='both', padx=10, pady=5)
        self.store_log = tk.Text(bot_frame, bg="black", fg="orange", font=("Consolas", 10), width=45)
        self.store_log.pack(side='left', expand=True, fill='both')
        
        self.store_fig, self.store_ax = plt.subplots(figsize=(6, 4))
        self.store_canvas = FigureCanvasTkAgg(self.store_fig, master=bot_frame)
        self.store_canvas.get_tk_widget().pack(side='right', expand=True, fill='both')
        self.draw_disk_grid()

    def random_storage(self):
        self.store_id.delete(0, tk.END)
        self.store_id.insert(0, str(random.randint(800, 999)))
        self.store_size.delete(0, tk.END)
        self.store_size.insert(0, str(random.randint(2, 9)))

    def run_storage(self):
        try:
            sys.stdout = PrintLogger(self.store_log)
            inc_id = int(self.store_id.get())
            size = int(self.store_size.get())
            method = self.store_algo.get()

            if method == "Contiguous": self.storage_db.allocate_contiguous(inc_id, size)
            elif method == "Linked": self.storage_db.allocate_linked(inc_id, size)
            elif method == "Indexed": self.storage_db.allocate_indexed(inc_id, size)
            
            sys.stdout = sys.__stdout__
            self.draw_disk_grid()
        except ValueError: messagebox.showerror("Error", "ID and Size must be integers.")

    def draw_disk_grid(self):
        self.store_ax.clear()
        self.store_ax.set_xlim(-0.5, 9.5)
        self.store_ax.set_ylim(-0.5, 4.5)
        
        for block in self.storage_db.disk:
            x = block.block_id % 10
            y = 4 - (block.block_id // 10) 
            
            color = '#2ecc71' if block.is_free else '#e74c3c'
            rect = patches.Rectangle((x-0.45, y-0.45), 0.9, 0.9, linewidth=1, edgecolor='black', facecolor=color)
            self.store_ax.add_patch(rect)
            
            label = str(block.block_id) if block.is_free else f"I-{block.incident_id}"
            self.store_ax.text(x, y, label, ha='center', va='center', fontsize=8, color='black' if block.is_free else 'white')

        self.store_ax.set_title("Physical Hard Drive Array (50 Blocks)")
        self.store_ax.axis('off') 
        self.store_canvas.draw()

if __name__ == "__main__":
    app = DispatchDashboard()
    app.mainloop()