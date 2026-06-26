import tkinter as tk
from tkinter import ttk, messagebox
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DiskRouterModule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0f171e")
        self.drone_start_sector = 50
        self.drone_targets_queue = []
        self.drone_flight_history = [50]
        self.total_air_seek_distance = 0
        self.math_computation_steps = []
        self.setup_ui()

    def setup_ui(self):
        form_frame = tk.LabelFrame(self, text=" 911 EN-ROUTE DISPATCH DRONE SECTORS (DISK HEAD SCHEDULING INTERNALS) ", bg="#0f171e", fg="#ffcc00", font=("Segoe UI", 10, "bold"))
        form_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(form_frame, text="Caller Cylinder Sector (0-199):", bg="#0f171e", fg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        self.disk_track_ent = tk.Entry(form_frame, bg="#16222f", fg="white", insertbackground="white", width=8)
        self.disk_track_ent.pack(side=tk.LEFT, padx=5)
        self.disk_track_ent.insert(0, "65")

        tk.Label(form_frame, text="Routing Protocol:", bg="#0f171e", fg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        self.disk_algo_var = tk.StringVar(value="SSTF")
        self.disk_algo_box = ttk.Combobox(form_frame, textvariable=self.disk_algo_var, values=["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"], width=10, state="readonly")
        self.disk_algo_box.pack(side=tk.LEFT, padx=5)

        queue_btn = tk.Button(form_frame, text="Queue Distress Call", bg="#1c2d3d", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", bd=0, command=self.queue_drone_sector, width=22)
        queue_btn.pack(side=tk.LEFT, padx=5)
        
        rand_disk_btn = tk.Button(form_frame, text="🎲 Add 4 Random Incident Locations", bg="#1c2d3d", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", bd=0, command=self.randomize_drone_targets)
        rand_disk_btn.pack(side=tk.LEFT, padx=2)

        queue_btn.bind("<Enter>", lambda e: queue_btn.config(bg="#293f54"))
        queue_btn.bind("<Leave>", lambda e: queue_btn.config(bg="#1c2d3d"))
        rand_disk_btn.bind("<Enter>", lambda e: rand_disk_btn.config(bg="#293f54"))
        rand_disk_btn.bind("<Leave>", lambda e: rand_disk_btn.config(bg="#1c2d3d"))

        table_frame = tk.Frame(self, bg="#0f171e")
        table_frame.pack(fill=tk.X, pady=5)
        
        self.disk_tree = ttk.Treeview(table_frame, columns=("Queue", "Pending Sectors", "Total Distance Covered"), show='headings', height=10)
        self.disk_tree.heading("Queue", text="CAD DRONE ROUTER STATUS")
        self.disk_tree.heading("Pending Sectors", text="Unresolved Distress Location Array")
        self.disk_tree.heading("Total Distance Covered", text="Accumulated Flight Seek Tracks")
        self.disk_tree.pack(fill=tk.X, expand=True)

        bottom_workspace = tk.Frame(self, bg="#0f171e")
        bottom_workspace.pack(fill=tk.BOTH, expand=True, pady=5)
        
        left_ctrls = tk.Frame(bottom_workspace, bg="#0f171e")
        left_ctrls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        action_row = tk.Frame(left_ctrls, bg="#0f171e")
        action_row.pack(fill=tk.X, anchor="w", pady=2)

        optimize_btn = tk.Button(action_row, text="⚡ Optimize Drone Response Flight ⚡", bg="#229954", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", bd=0, command=self.execute_disk_scheduling)
        optimize_btn.pack(side=tk.LEFT, padx=5)
        
        view_math_btn = tk.Button(action_row, text="📊 View Analytical Flight Computations 📊", bg="#8e44ad", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", bd=0, command=self.open_math_computation_page)
        view_math_btn.pack(side=tk.LEFT, padx=5)
        
        reset_router_btn = tk.Button(action_row, text="Reset Router", bg="#d35400", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", bd=0, command=self.reset_drone_router)
        reset_router_btn.pack(side=tk.LEFT, padx=2)

        optimize_btn.bind("<Enter>", lambda e: optimize_btn.config(bg="#2cc771"))
        optimize_btn.bind("<Leave>", lambda e: optimize_btn.config(bg="#229954"))
        view_math_btn.bind("<Enter>", lambda e: view_math_btn.config(bg="#9b59b6"))
        view_math_btn.bind("<Leave>", lambda e: view_math_btn.config(bg="#8e44ad"))
        reset_router_btn.bind("<Enter>", lambda e: reset_router_btn.config(bg="#e67e22"))
        reset_router_btn.bind("<Leave>", lambda e: reset_router_btn.config(bg="#d35400"))

        tk.Label(left_ctrls, text="911 Drone Flight Sched Engine Logs", bg="#0f171e", fg="#3498db", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(8,2))
        self.disk_log_txt = tk.Text(left_ctrls, bg="#111111", fg="#ffffff", font=("Segoe UI", 10), height=15, width=45)
        self.disk_log_txt.pack(fill=tk.BOTH, expand=True)

        right_graph = tk.Frame(bottom_workspace, bg="#16222f", relief="solid", bd=1)
        right_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.disk_fig = Figure(figsize=(6, 4), dpi=95, facecolor='#16222f')
        self.disk_ax = self.disk_fig.add_subplot(111)
        self.disk_canvas = FigureCanvasTkAgg(self.disk_fig, master=right_graph)
        self.disk_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.sync_disk_table_ui()
        self.repaint_drone_vector_path()

    def sync_disk_table_ui(self):
        for item in self.disk_tree.get_children(): self.disk_tree.delete(item)
        status_str = f"🚁 EN-ROUTE [{self.disk_algo_var.get()}] OPTIMIZED" if len(self.drone_flight_history) > 1 else "💤 EN-BASE STANDBY"
        self.disk_tree.insert("", tk.END, values=(status_str, str(self.drone_targets_queue), f"{self.total_air_seek_distance} Track Units"))

    def repaint_drone_vector_path(self):
        self.disk_ax.clear()
        self.disk_ax.set_facecolor('#0f171e')
        self.disk_ax.set_title(f"911 Responder Sweep Path Map ({self.disk_algo_var.get()} Engine)", color="white", fontname="Courier New", fontsize=11, fontweight="bold")
        self.disk_ax.set_xlabel("Physical City Cylinder Tracks (0-199 Grid Belt)", color="white", fontname="Courier New")
        self.disk_ax.set_ylabel("Dispatch Timeline Sequence Index", color="white", fontname="Courier New")
        self.disk_ax.tick_params(colors='white')
        self.disk_ax.set_xlim(-5, 205)
        
        if len(self.drone_flight_history) > 1:
            steps = list(range(len(self.drone_flight_history)))
            self.disk_ax.plot(self.drone_flight_history, steps, marker="o", color="#3498db", linewidth=2, markersize=6)
            for idx, txt in enumerate(self.drone_flight_history):
                self.disk_ax.annotate(f"  Pos:{txt}", (self.drone_flight_history[idx], idx), color="white", fontsize=8, fontweight="bold")
        else:
            self.disk_ax.text(100, 0.5, "Awaiting Dispatch Navigation Engine Initialization", color="white", ha="center", va="center", fontname="Segoe UI")
            
        self.disk_ax.xaxis.grid(True, linestyle="--", alpha=0.2, color="#ffffff")
        self.disk_canvas.draw()

    def queue_drone_sector(self):
        try:
            sector = int(self.disk_track_ent.get())
            if sector < 0 or sector > 199: raise ValueError
            self.drone_targets_queue.append(sector)
            self.disk_log_txt.insert(tk.END, f"[ALERT QUEUED] Emergency responder target cylinder sector {sector} added to live buffer queue.\n")
            self.sync_disk_table_ui()
        except ValueError:
            messagebox.showerror("Error", "Cylinder parameters must fall strictly within valid track limits (0 - 199).")

    def randomize_drone_targets(self):
        for _ in range(4):
            rand_sector = random.randint(10, 190)
            self.drone_targets_queue.append(rand_sector)
            self.disk_log_txt.insert(tk.END, f"[ALERT QUEUED] Emergency response localized at track sector {rand_sector}.\n")
        self.sync_disk_table_ui()

    def execute_disk_scheduling(self):
        if not self.drone_targets_queue:
            messagebox.showwarning("Warning", "The execution pool array stack is currently empty. Add target cylinders.")
            return
            
        algo = self.disk_algo_var.get()
        self.disk_log_txt.insert(tk.END, f"--- Activating 911 Flight Optimization Engine via [{algo}] ---\n")
        
        head = self.drone_start_sector
        reqs = list(self.drone_targets_queue)
        path = [head]
        self.math_computation_steps = []
        
        if algo == "FCFS":
            for r in reqs: path.append(r)
        elif algo == "SSTF":
            tmp_reqs = list(reqs)
            curr = head
            while tmp_reqs:
                closest = min(tmp_reqs, key=lambda x: abs(x - curr))
                path.append(closest)
                tmp_reqs.remove(closest)
                curr = closest
        elif algo == "SCAN":
            left = sorted([r for r in reqs if r < head], reverse=True)
            right = sorted([r for r in reqs if r >= head])
            path.extend(left)
            if left: path.append(0)
            path.extend(right)
        elif algo == "C-SCAN":
            right = sorted([r for r in reqs if r >= head])
            left = sorted([r for r in reqs if r < head])
            path.extend(right)
            if right or left:
                path.append(199)
                path.append(0)
            path.extend(left)
        elif algo == "LOOK":
            left = sorted([r for r in reqs if r < head], reverse=True)
            right = sorted([r for r in reqs if r >= head])
            path.extend(left)
            path.extend(right)
        elif algo == "C-LOOK":
            right = sorted([r for r in reqs if r >= head])
            left = sorted([r for r in reqs if r < head])
            path.extend(right)
            path.extend(left)

        total_seek = 0
        self.disk_log_txt.insert(tk.END, f"Optimized CAD Flight Path Matrix: {path}\n")
        
        for i in range(len(path) - 1):
            curr_p = path[i]
            next_p = path[i+1]
            diff = abs(next_p - curr_p)
            total_seek += diff
            self.math_computation_steps.append({"from": curr_p, "to": next_p, "cost": diff})
            self.disk_log_txt.insert(tk.END, f" Flight leg [{i+1}]: Track {curr_p} -> Track {next_p} (Tracks: {diff})\n")
            
        self.total_air_seek_distance = total_seek
        self.drone_flight_history = path
        
        # FIXED: Tell the drone to remember its last physical location!
        self.drone_start_sector = path[-1] 
        
        self.disk_log_txt.insert(tk.END, f"[SUCCESS] Navigation lock complete. Total aerial traversal track latency: {total_seek} steps.\n")
        self.drone_targets_queue.clear()
        self.sync_disk_table_ui()
        self.repaint_drone_vector_path()

    def open_math_computation_page(self):
        math_win = tk.Toplevel(self)
        math_win.title("📐 911 CAD GEOMETRIC FLIGHT SEEK BREAKDOWN")
        math_win.geometry("700x550")
        math_win.configure(bg="#0b1116")
        
        title_lbl = tk.Label(math_win, text=f"911 COORD VECTOR SCHEDULING COMPUTATION DETAILS ({self.disk_algo_var.get()})", 
                             bg="#0b1116", fg="#8e44ad", font=("Segoe UI", 12, "bold"), pady=15)
        title_lbl.pack()
        
        content_box = tk.Frame(math_win, bg="#111c24", relief="solid", bd=1)
        content_box.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scroll = tk.Scrollbar(content_box)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        txt_display = tk.Text(content_box, bg="#111c24", fg="#ffffff", font=("Segoe UI", 10), yscrollcommand=scroll.set, wrap=tk.WORD, bd=0)
        txt_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scroll.config(command=txt_display.yview)
        
        if not self.math_computation_steps:
            txt_display.insert(tk.END, ">> Execution log sequence blank. Trigger mathematical parsing by pressing 'Execute Route Path' first.")
        else:
            txt_display.insert(tk.END, "="*60 + "\n")
            txt_display.insert(tk.END, "STEP-BY-STEP EMERGENCY VEHICLE HEAD TRAVERSAL MATHEMATICAL TRACE\n")
            txt_display.insert(tk.END, "="*60 + "\n\n")
            
            formula_string_parts = []
            for idx, trace in enumerate(self.math_computation_steps):
                line = f"Sector leg {idx+1:02d}: |{trace['to']:3d} - {trace['from']:3d}| = {trace['cost']} Tracks Traversed\n"
                txt_display.insert(tk.END, line)
                formula_string_parts.append(f"|{trace['to']} - {trace['from']}|")
                
            txt_display.insert(tk.END, "\n" + "-"*60 + "\n")
            txt_display.insert(tk.END, "COMPLETE RESPONSE FLIGHT EQUATION VECTOR:\n")
            txt_display.insert(tk.END, " + ".join(formula_string_parts) + "\n")
            txt_display.insert(tk.END, "-"*60 + "\n\n")
            
            sum_parts = [str(x['cost']) for x in self.math_computation_steps]
            txt_display.insert(tk.END, f"Summation Cost Breakdown:\n  = " + " + ".join(sum_parts) + "\n")
            txt_display.insert(tk.END, f"  = {self.total_air_seek_distance} Absolute Cylinder Tracks covered by response drones.\n\n")
            txt_display.insert(tk.END, ">> End of 911 Sched Storage Navigation Kernel.")
            
        txt_display.config(state=tk.DISABLED)
        tk.Button(math_win, text="Dismiss View Screen", bg="#1c2d3d", fg="white", font=("Segoe UI", 9, "bold"), command=math_win.destroy, pady=5).pack(pady=10)

    def reset_drone_router(self):
        self.drone_targets_queue.clear()
        self.drone_flight_history = [50]
        self.drone_start_sector = 50
        self.total_air_seek_distance = 0
        self.math_computation_steps = []
        self.disk_log_txt.delete("1.0", tk.END)
        self.sync_disk_table_ui()
        self.repaint_drone_vector_path()