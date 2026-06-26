import tkinter as tk
from tkinter import ttk, messagebox
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CPUModule(tk.Frame):
    def __init__(self, parent):
        self.bg_main = "#0B192C"
        self.bg_elevated = "#112844"
        super().__init__(parent, bg=self.bg_main)
        self.cpu_incidents = []  
        self.setup_ui()

    def setup_ui(self):
        form_frame = tk.LabelFrame(self, text=" LOG NEW 911 INCIDENT ", bg=self.bg_main, fg="#ffcc00", font=("Segoe UI", 10, "bold"))
        form_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(form_frame, text="Desc:", bg=self.bg_main, fg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.cpu_desc_ent = tk.Entry(form_frame, bg=self.bg_elevated, fg="white", insertbackground="white", width=15, font=("Segoe UI", 10))
        self.cpu_desc_ent.pack(side=tk.LEFT, padx=5)
        self.cpu_desc_ent.insert(0, "Assault")

        tk.Label(form_frame, text="Arrival:", bg=self.bg_main, fg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.cpu_arr_ent = tk.Entry(form_frame, bg=self.bg_elevated, fg="white", insertbackground="white", width=6, font=("Segoe UI", 10))
        self.cpu_arr_ent.pack(side=tk.LEFT, padx=5)
        self.cpu_arr_ent.insert(0, "0")

        tk.Label(form_frame, text="Burst:", bg=self.bg_main, fg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.cpu_burst_ent = tk.Entry(form_frame, bg=self.bg_elevated, fg="white", insertbackground="white", width=6, font=("Segoe UI", 10))
        self.cpu_burst_ent.pack(side=tk.LEFT, padx=5)
        self.cpu_burst_ent.insert(0, "10")

        tk.Label(form_frame, text="Priority (1=High):", bg=self.bg_main, fg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)
        self.cpu_prio_ent = tk.Entry(form_frame, bg=self.bg_elevated, fg="white", insertbackground="white", width=6, font=("Segoe UI", 10))
        self.cpu_prio_ent.pack(side=tk.LEFT, padx=5)
        self.cpu_prio_ent.insert(0, "1")

        # Removed redundant top algorithm dropdown

        add_btn = tk.Button(form_frame, text="Add Incident", bg="#1c2d3d", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", bd=0, command=self.add_incident_to_table, width=12)
        add_btn.pack(side=tk.LEFT, padx=20)

        rand_btn = tk.Button(form_frame, text="🎲 Randomize 4", bg="#1c2d3d", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", bd=0, command=self.randomize_cpu_incidents)
        rand_btn.pack(side=tk.LEFT, padx=2)

        add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#293f54"))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg="#1c2d3d"))
        rand_btn.bind("<Enter>", lambda e: rand_btn.config(bg="#293f54"))
        rand_btn.bind("<Leave>", lambda e: rand_btn.config(bg="#1c2d3d"))

        table_frame = tk.Frame(self, bg=self.bg_main)
        table_frame.pack(fill=tk.X, pady=5)
        
        self.cpu_tree = ttk.Treeview(table_frame, columns=("ID", "Description", "Arrival Time", "Burst Time", "Priority"), show='headings', height=10)
        self.cpu_tree.heading("ID", text="ID")
        self.cpu_tree.heading("Description", text="Description")
        self.cpu_tree.heading("Arrival Time", text="Arrival Time")
        self.cpu_tree.heading("Burst Time", text="Burst Time")
        self.cpu_tree.heading("Priority", text="Priority")
        self.cpu_tree.pack(fill=tk.X, expand=True)

        bottom_workspace = tk.Frame(self, bg=self.bg_main)
        bottom_workspace.pack(fill=tk.BOTH, expand=True, pady=5)
        
        left_ctrls = tk.Frame(bottom_workspace, bg=self.bg_main)
        left_ctrls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        algo_row = tk.Frame(left_ctrls, bg=self.bg_main)
        algo_row.pack(fill=tk.X, anchor="w", pady=2)
        
        tk.Label(algo_row, text="Algorithm:", bg=self.bg_main, fg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=2)
        
        algo_list = ["FCFS", "SJF (Non-Preemptive)", "SJF (Preemptive/SRTF)", "Priority (Non-Preemptive)", "Priority (Preemptive)", "Round Robin (RR)"]
        self.algo_var = tk.StringVar(value="FCFS")
        self.algo_box = ttk.Combobox(algo_row, textvariable=self.algo_var, values=algo_list, width=22, state="readonly", font=("Segoe UI", 10))
        self.algo_box.pack(side=tk.LEFT, padx=5)
        self.algo_box.bind("<<ComboboxSelected>>", self.toggle_quantum_visibility)

        # Repositioned Quantum Box
        self.quantum_frame = tk.Frame(algo_row, bg=self.bg_main)
        tk.Label(self.quantum_frame, text="Q:", bg=self.bg_main, fg="#ffcc00", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=2)
        self.quantum_ent = tk.Entry(self.quantum_frame, bg=self.bg_elevated, fg="#ffffff", insertbackground="white", width=3, font=("Segoe UI", 10))
        self.quantum_ent.insert(0, "4")
        self.quantum_ent.pack(side=tk.LEFT)

        run_btn = tk.Button(algo_row, text="Run Dispatch", bg="#229954", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", bd=0, command=self.execute_cpu_dispatcher)
        run_btn.pack(side=tk.LEFT, padx=10)
        
        clear_btn = tk.Button(algo_row, text="Clear Queue", bg="#d35400", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", bd=0, command=self.clear_cpu_queue)
        clear_btn.pack(side=tk.LEFT, padx=2)

        run_btn.bind("<Enter>", lambda e: run_btn.config(bg="#2cc771"))
        run_btn.bind("<Leave>", lambda e: run_btn.config(bg="#229954"))
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#e67e22"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg="#d35400"))

        tk.Label(left_ctrls, text="System Execution Log", bg=self.bg_main, fg="#52be80", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(8,2))
        self.cpu_log_txt = tk.Text(left_ctrls, bg="#08101C", fg="#ffffff", font=("Consolas", 11), height=15, width=45)
        self.cpu_log_txt.pack(fill=tk.BOTH, expand=True)

        right_graph = tk.Frame(bottom_workspace, bg=self.bg_elevated, relief="solid", bd=1)
        right_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.cpu_fig = Figure(figsize=(6, 4), dpi=95, facecolor=self.bg_elevated)
        self.cpu_ax = self.cpu_fig.add_subplot(111)
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=right_graph)
        self.cpu_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.sync_cpu_table_ui()
        self.render_empty_gantt()

    def toggle_quantum_visibility(self, event=None):
        if self.algo_var.get() == "Round Robin (RR)":
            self.quantum_frame.pack(side=tk.LEFT, padx=5, before=self.algo_box.master.pack_slaves()[2]) # Packs right next to dropdown
        else:
            self.quantum_frame.pack_forget()

    def log_to_terminal(self, msg):
        self.cpu_log_txt.insert(tk.END, msg + "\n")
        self.cpu_log_txt.see(tk.END)

    def add_incident_to_table(self):
        try:
            desc = self.cpu_desc_ent.get().strip()
            arr = int(self.cpu_arr_ent.get())
            burst = int(self.cpu_burst_ent.get())
            prio = int(self.cpu_prio_ent.get())
            if arr < 0 or burst <= 0 or prio <= 0 or not desc: raise ValueError
            
            nid = len(self.cpu_incidents) + 1
            self.cpu_incidents.append({"id": nid, "desc": desc, "arrival": arr, "burst": burst, "priority": prio})
            self.sync_cpu_table_ui()
        except ValueError:
            messagebox.showerror("Error", "Verify item metrics are valid positive numbers.")

    def randomize_cpu_incidents(self):
        sample_pool = ["Traffic Stop", "Assault", "Heart Attack", "Structure Fire", "Robbery", "MVA Accident", "Noise Complaint", "Burglary"]
        self.cpu_incidents.clear()
        for i in range(1, 5):
            desc = random.choice(sample_pool)
            arr = random.randint(0, 15)
            burst = random.randint(3, 20)
            prio = random.randint(1, 4)
            self.cpu_incidents.append({"id": i, "desc": f"{desc} (p{i})", "arrival": arr, "burst": burst, "priority": prio})
        self.sync_cpu_table_ui()

    def clear_cpu_queue(self):
        self.cpu_incidents.clear()
        self.sync_cpu_table_ui()
        self.cpu_log_txt.delete("1.0", tk.END)
        self.render_empty_gantt()

    def sync_cpu_table_ui(self):
        for item in self.cpu_tree.get_children(): self.cpu_tree.delete(item)
        for i in self.cpu_incidents:
            self.cpu_tree.insert("", tk.END, values=(i["id"], i["desc"], i["arrival"], i["burst"], i["priority"]))

    def render_empty_gantt(self):
        self.cpu_ax.clear()
        self.cpu_ax.set_facecolor(self.bg_main)
        self.cpu_ax.set_title("Dispatch Timeline (Gantt Chart)", fontsize=13, fontweight="bold", color="white", fontname="Segoe UI")
        self.cpu_ax.set_xlabel("Time Units", fontsize=11, fontweight="bold", color="white", fontname="Segoe UI")
        self.cpu_ax.tick_params(colors='white')
        self.cpu_fig.subplots_adjust(bottom=0.25, left=0.15, right=0.95, top=0.85)
        self.cpu_canvas.draw()

    def execute_cpu_dispatcher(self):
        if not self.cpu_incidents:
            messagebox.showwarning("Warning", "Add some dispatch vectors into the simulation registry first.")
            return
        
        self.cpu_log_txt.delete("1.0", tk.END)
        algo = self.algo_var.get()
        self.log_to_terminal(f"📡 INITIALIZING DISPATCHER CORE // ENGINE ALGORITHM: {algo}")
        
        queue = [[i["id"], i["desc"], i["arrival"], i["burst"], i["priority"]] for i in self.cpu_incidents]
        current_time = 0
        gantt_data = []
        
        # FCFS
        if algo == "FCFS":
            queue.sort(key=lambda x: x[2])
            for job in queue:
                if current_time < job[2]: current_time = job[2]
                gantt_data.append({"id": job[0], "desc": job[1], "start": current_time, "duration": job[3]})
                self.log_to_terminal(f"[TIME {current_time}]: Dispatching '{job[1]}' (Burst: {job[3]})")
                current_time += job[3]

        # SJF (NON-PRE)    
        elif algo == "SJF (Non-Preemptive)":
            while queue:
                available_jobs = [job for job in queue if job[2] <= current_time]
                if not available_jobs:
                    current_time = min(job[2] for job in queue)
                    continue
                next_job = min(available_jobs, key=lambda x: x[3])
                queue.remove(next_job)
                gantt_data.append({"id": next_job[0], "desc": next_job[1], "start": current_time, "duration": next_job[3]})
                self.log_to_terminal(f"[TIME {current_time}]: Dispatching '{next_job[1]}' (Burst: {next_job[3]})")
                current_time += next_job[3]

        # SJF (PRE)
        elif algo == "SJF (Preemptive/SRTF)":
            current_job = None
            job_start_time = 0
            while queue or current_job:
                available_jobs = [job for job in queue if job[2] <= current_time]
                if not available_jobs and not current_job:
                    current_time = min(job[2] for job in queue)
                    continue
                if available_jobs:
                    best_arrival_job = min(available_jobs, key=lambda x: x[3])
                    if current_job is None or best_arrival_job[3] < current_job[3]:
                        if current_job:
                            duration = current_time - job_start_time
                            if duration > 0:
                                gantt_data.append({"id": current_job[0], "desc": current_job[1], "start": job_start_time, "duration": duration})
                            queue.append(current_job)
                        current_job = best_arrival_job
                        queue.remove(best_arrival_job)
                        job_start_time = current_time
                        self.log_to_terminal(f"[TIME {current_time}]: ⚠️ PREEMPTING context to shorter unit '{current_job[1]}'")
                current_time += 1
                current_job[3] -= 1
                if current_job[3] == 0:
                    gantt_data.append({"id": current_job[0], "desc": current_job[1], "start": job_start_time, "duration": current_time - job_start_time})
                    self.log_to_terminal(f"💥 [TIME {current_time}]: Completed tracking for '{current_job[1]}'.")
                    current_job = None

        # PRIORITY (NON-PRE)
        elif algo == "Priority (Non-Preemptive)":
            while queue:
                available_jobs = [job for job in queue if job[2] <= current_time]
                if not available_jobs:
                    current_time = min(job[2] for job in queue)
                    continue
                next_job = min(available_jobs, key=lambda x: x[4])
                queue.remove(next_job)
                gantt_data.append({"id": next_job[0], "desc": next_job[1], "start": current_time, "duration": next_job[3]})
                self.log_to_terminal(f"[TIME {current_time}]: Dispatching High Priority '{next_job[1]}' (Rank: {next_job[4]})")
                current_time += next_job[3]

        # PRIORITY (PRE-EMP)
        elif algo == "Priority (Preemptive)":
            current_job = None
            job_start_time = 0
            while queue or current_job:
                available_jobs = [job for job in queue if job[2] <= current_time]
                if not available_jobs and not current_job:
                    current_time = min(job[2] for job in queue)
                    continue
                if available_jobs:
                    best_arrival_job = min(available_jobs, key=lambda x: x[4])
                    if current_job is None or best_arrival_job[4] < current_job[4]:
                        if current_job:
                            duration = current_time - job_start_time
                            if duration > 0:
                                gantt_data.append({"id": current_job[0], "desc": current_job[1], "start": job_start_time, "duration": duration})
                            queue.append(current_job)
                        current_job = best_arrival_job
                        queue.remove(best_arrival_job)
                        job_start_time = current_time
                        self.log_to_terminal(f"[TIME {current_time}]: ⚠️ PREEMPTING context to critical priority task '{current_job[1]}'")
                current_time += 1
                current_job[3] -= 1
                if current_job[3] == 0:
                    gantt_data.append({"id": current_job[0], "desc": current_job[1], "start": job_start_time, "duration": current_time - job_start_time})
                    self.log_to_terminal(f"💥 [TIME {current_time}]: Completed tracking for critical task '{current_job[1]}'.")
                    current_job = None

        # ROUND ROBIN
        elif algo == "Round Robin (RR)":
            try:
                quantum = int(self.quantum_ent.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer for Time Quantum.")
                return
            queue.sort(key=lambda x: x[2])
            ready_queue = []
            while queue or ready_queue:
                while queue and queue[0][2] <= current_time:
                    ready_queue.append(queue.pop(0))
                if not ready_queue:
                    current_time = queue[0][2]
                    continue
                current_job = ready_queue.pop(0)
                execute_time = min(current_job[3], quantum)
                gantt_data.append({"id": current_job[0], "desc": current_job[1], "start": current_time, "duration": execute_time})
                current_time += execute_time
                current_job[3] -= execute_time
                while queue and queue[0][2] <= current_time:
                    ready_queue.append(queue.pop(0))
                if current_job[3] > 0:
                    ready_queue.append(current_job)
                else:
                    self.log_to_terminal(f"💥 [TIME {current_time}]: Completed tracking for '{current_job[1]}'.")
            
        self.cpu_ax.clear()
        self.cpu_ax.set_facecolor(self.bg_main)
        self.cpu_ax.set_title("Dispatch Timeline (Gantt Chart)", fontsize=13, fontweight="bold", color="white", fontname="Segoe UI")
        self.cpu_ax.set_xlabel("Time Units", fontsize=11, fontweight="bold", color="white", fontname="Segoe UI")
        self.cpu_ax.tick_params(colors='white')
        
        all_unique_descriptions = list(dict.fromkeys([p["desc"] for p in sorted(self.cpu_incidents, key=lambda x: x["arrival"])]))
        self.cpu_ax.set_yticks(range(len(all_unique_descriptions)))
        self.cpu_ax.set_yticklabels(all_unique_descriptions, fontname="Segoe UI", color="white", fontsize=10)
        
        x_ticks_positions = [0]
        for block in gantt_data:
            y_position_index = all_unique_descriptions.index(block["desc"])
            self.cpu_ax.barh(y=y_position_index, width=block["duration"], left=block["start"], height=0.6, color="#4aa3df", edgecolor="#ffffff", align="center")
            self.cpu_ax.text(block["start"] + block["duration"]/2, y_position_index, f"ID:{block['id']}", ha="center", va="center", color="white", fontsize=10, fontweight="bold")
            end_time = block["start"] + block["duration"]
            if end_time not in x_ticks_positions: x_ticks_positions.append(end_time)
                
        x_ticks_positions.sort()
        self.cpu_ax.set_xticks(x_ticks_positions)
        self.cpu_ax.xaxis.grid(True, linestyle="--", alpha=0.3, color="#ffffff")
        self.cpu_ax.set_axisbelow(True)
        self.cpu_fig.subplots_adjust(bottom=0.25, left=0.15, right=0.95, top=0.85)
        self.cpu_canvas.draw()