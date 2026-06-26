import tkinter as tk
from tkinter import ttk, messagebox
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VirtualMemoryModule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0f171e")
        self.VM_FRAMES_COUNT = 3  
        self.vm_slots = [None] * self.VM_FRAMES_COUNT
        self.vm_incident_stream = []
        self.page_fault_count = 0
        self.page_hit_count = 0
        self.vm_historical_requests = []
        self.setup_ui()

    def setup_ui(self):
        form_frame = tk.LabelFrame(self, text=" 911 DISPATCH DATABANK CACHING (VIRTUAL MEMORY UNIT) ", bg="#0f171e", fg="#ffcc00", font=("Segoe UI", 10, "bold"))
        form_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(form_frame, text="Incident Code / Page ID:", bg="#0f171e", fg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        self.vm_page_ent = tk.Entry(form_frame, bg="#16222f", fg="white", insertbackground="white", width=6)
        self.vm_page_ent.pack(side=tk.LEFT, padx=5)
        self.vm_page_ent.insert(0, "7")

        tk.Label(form_frame, text="Active Cache Frames:", bg="#0f171e", fg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        self.vm_frame_size_var = tk.StringVar(value=str(self.VM_FRAMES_COUNT))
        self.vm_frame_size_box = ttk.Combobox(form_frame, textvariable=self.vm_frame_size_var, values=["3", "4", "5", "6", "7"], width=4, state="readonly")
        self.vm_frame_size_box.pack(side=tk.LEFT, padx=5)
        self.vm_frame_size_box.bind("<<ComboboxSelected>>", self.handle_frame_size_change)

        tk.Label(form_frame, text="Eviction Protocol:", bg="#0f171e", fg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        self.vm_algo_var = tk.StringVar(value="LRU")
        self.vm_algo_box = ttk.Combobox(form_frame, textvariable=self.vm_algo_var, values=["FIFO", "OPT", "LRU", "LFU", "MFU"], width=8, state="readonly")
        self.vm_algo_box.pack(side=tk.LEFT, padx=5)

        fetch_btn = tk.Button(form_frame, text="Fetch Incident Records", bg="#1c2d3d", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", bd=0, command=self.access_virtual_page_suite, width=22)
        fetch_btn.pack(side=tk.LEFT, padx=5)
        
        rand_vm_btn = tk.Button(form_frame, text="Log 4 Random Calls", bg="#1c2d3d", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", bd=0, command=self.randomize_vm_stream_suite)
        rand_vm_btn.pack(side=tk.LEFT, padx=2)

        fetch_btn.bind("<Enter>", lambda e: fetch_btn.config(bg="#293f54"))
        fetch_btn.bind("<Leave>", lambda e: fetch_btn.config(bg="#1c2d3d"))
        rand_vm_btn.bind("<Enter>", lambda e: rand_vm_btn.config(bg="#293f54"))
        rand_vm_btn.bind("<Leave>", lambda e: rand_vm_btn.config(bg="#1c2d3d"))

        table_frame = tk.Frame(self, bg="#0f171e")
        table_frame.pack(fill=tk.X, pady=5)
        
        self.vm_tree = ttk.Treeview(table_frame, columns=("Step", "Algo", "Request ID", "Frame State", "Status Outcome"), show='headings', height=10)
        self.vm_tree.heading("Step", text="CAD LOOKUP STEP")
        self.vm_tree.heading("Algo", text="CACHE STRATEGY")
        self.vm_tree.heading("Request ID", text="Incident Code (Page)")
        self.vm_tree.heading("Frame State", text="Active Databank RAM Slots")
        self.vm_tree.heading("Status Outcome", text="CAD Cache Status")
        self.vm_tree.pack(fill=tk.X, expand=True)

        bottom_workspace = tk.Frame(self, bg="#0f171e")
        bottom_workspace.pack(fill=tk.BOTH, expand=True, pady=5)
        
        left_ctrls = tk.Frame(bottom_workspace, bg="#0f171e")
        left_ctrls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        action_row = tk.Frame(left_ctrls, bg="#0f171e")
        action_row.pack(fill=tk.X, anchor="w", pady=2)

        matrix_btn = tk.Button(action_row, text="📊 Open 911 Databank Analytics Matrix 📊", bg="#8e44ad", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", bd=0, command=self.open_paging_analytics_page)
        matrix_btn.pack(side=tk.LEFT, padx=5)
        
        wipe_btn = tk.Button(action_row, text="Wipe Core Cache Server Data", bg="#d35400", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", bd=0, command=self.clear_vm_simulation)
        wipe_btn.pack(side=tk.LEFT, padx=2)

        matrix_btn.bind("<Enter>", lambda e: matrix_btn.config(bg="#9b59b6"))
        matrix_btn.bind("<Leave>", lambda e: matrix_btn.config(bg="#8e44ad"))
        wipe_btn.bind("<Enter>", lambda e: wipe_btn.config(bg="#e67e22"))
        wipe_btn.bind("<Leave>", lambda e: wipe_btn.config(bg="#d35400"))

        tk.Label(left_ctrls, text="911 Dispatch Mainframe Cache Terminal Logs", bg="#0f171e", fg="#e74c3c", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(8,2))
        self.vm_log_txt = tk.Text(left_ctrls, bg="#111111", fg="#ffffff", font=("Segoe UI", 10), height=15, width=45)
        self.vm_log_txt.pack(fill=tk.BOTH, expand=True)

        right_graph = tk.Frame(bottom_workspace, bg="#16222f", relief="solid", bd=1)
        right_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.vm_fig = Figure(figsize=(6, 4), dpi=95, facecolor='#16222f')
        self.vm_ax = self.vm_fig.add_subplot(111)
        self.vm_canvas = FigureCanvasTkAgg(self.vm_fig, master=right_graph)
        self.vm_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.sync_vm_table_ui()
        self.repaint_vm_ratio_chart()

    def handle_frame_size_change(self, event):
        new_size = int(self.vm_frame_size_var.get())
        self.VM_FRAMES_COUNT = new_size
        self.clear_vm_simulation()
        self.vm_log_txt.insert(tk.END, f"[CAD SYSTEM] Mainframe RAM split into {new_size} emergency buffer slots.\n")

    def sync_vm_table_ui(self):
        for item in self.vm_tree.get_children(): self.vm_tree.delete(item)
        for idx, entry in enumerate(self.vm_incident_stream):
            self.vm_tree.insert("", tk.END, values=(idx + 1, entry["algo"], f"Code {entry['page']}", str(entry["frames"]), entry["status"]))

    def repaint_vm_ratio_chart(self):
        self.vm_ax.clear()
        self.vm_ax.set_facecolor('#0f171e')
        self.vm_ax.set_title(f"911 CAD Call Stream Reference String ({self.vm_algo_var.get()})", color="white", fontname="Segoe UI", fontsize=11, fontweight="bold")
        
        if not self.vm_incident_stream:
            self.vm_ax.text(0.5, 0.5, "Awaiting 911 Databank Requests.\nLog an incident code to trace cache frame grids.", color="white", ha="center", va="center", fontname="Segoe UI")
            self.vm_ax.get_yaxis().set_visible(False)
            self.vm_ax.get_xaxis().set_visible(False)
            for spine in self.vm_ax.spines.values(): spine.set_visible(False)
            self.vm_canvas.draw()
            return
            
        self.vm_ax.get_yaxis().set_visible(False)
        self.vm_ax.get_xaxis().set_visible(False)
        for spine in self.vm_ax.spines.values(): spine.set_visible(False)
            
        n_steps = len(self.vm_incident_stream)
        
        for idx, step in enumerate(self.vm_incident_stream):
            x = idx * 1.3
            is_fault = "FAULT" in step["status"]
            
            self.vm_ax.text(x + 0.5, 4.5, f"C:{step['page']}", color="white", weight="bold", ha="center", va="center", fontname="Segoe UI", fontsize=9,
                             bbox=dict(boxstyle="square,pad=0.4", fc="#16222f", ec="#ffffff", lw=1.5))
            
            for slot_idx in range(self.VM_FRAMES_COUNT):
                val = step["frames"][slot_idx]
                val_str = str(val) if val is not None else ""
                text_color = "#ff4a4a" if is_fault and val_str != "" else "#ffffff"
                
                y = 3.2 - (slot_idx * 0.8)
                self.vm_ax.text(x + 0.5, y, val_str, color=text_color, weight="bold", ha="center", va="center", fontname="Segoe UI", fontsize=10,
                                 bbox=dict(boxstyle="square,pad=0.4", fc="#111c24", ec="#ffffff", lw=1.2))
                                 
        self.vm_ax.set_xlim(-0.2, n_steps * 1.3 + 0.2)
        self.vm_ax.set_ylim(-3.5, 5.5)
        self.vm_canvas.draw()

    def access_virtual_page_suite(self):
        try:
            page = int(self.vm_page_ent.get())
            if page < 0: raise ValueError
            self.vm_historical_requests.append(page)
            self.evaluate_paging_step(page)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid positive integer.")

    def randomize_vm_stream_suite(self):
        for _ in range(4):
            rand_page = random.randint(0, 7)
            self.vm_historical_requests.append(rand_page)
            self.evaluate_paging_step(rand_page)

    def evaluate_paging_step(self, incoming_page):
        algo = self.vm_algo_var.get()
        current_frames = list(self.vm_slots)
        
        if incoming_page in current_frames:
            status = "✅ CAD HIT"
            self.page_hit_count += 1
            self.vm_log_txt.insert(tk.END, f"[HIT] 911 Incident Code {incoming_page} pulled from rapid-access buffer logic [{algo}].\n")
        else:
            status = "❌ DISPATCH FAULT"
            self.page_fault_count += 1
            
            if None in current_frames:
                empty_idx = current_frames.index(None)
                current_frames[empty_idx] = incoming_page
                self.vm_log_txt.insert(tk.END, f"[FAULT] Initialized blank core sector with Incident File Code {incoming_page}.\n")
            else:
                evict_page = None
                if algo == "FIFO":
                    evict_page = current_frames[0]
                    current_frames.pop(0)
                    current_frames.append(incoming_page)
                elif algo == "OPT":
                    future_stream = self.vm_historical_requests[len(self.vm_incident_stream)+1:]
                    farthest_idx = -1
                    target_to_evict = current_frames[0]
                    for f in current_frames:
                        if f not in future_stream:
                            target_to_evict = f
                            break
                        else:
                            f_idx = future_stream.index(f)
                            if f_idx > farthest_idx:
                                farthest_idx = f_idx
                                target_to_evict = f
                    evict_page = target_to_evict
                    c_idx = current_frames.index(evict_page)
                    current_frames[c_idx] = incoming_page
                elif algo == "LRU":
                    past_stream = self.vm_historical_requests[:len(self.vm_incident_stream)]
                    past_stream.reverse()
                    least_recent_idx = -1
                    target_to_evict = current_frames[0]
                    for f in current_frames:
                        f_idx = past_stream.index(f)
                        if f_idx > least_recent_idx:
                            least_recent_idx = f_idx
                            target_to_evict = f
                    evict_page = target_to_evict
                    c_idx = current_frames.index(evict_page)
                    current_frames[c_idx] = incoming_page
                elif algo in ["LFU", "MFU"]:
                    past_stream = self.vm_historical_requests[:len(self.vm_incident_stream)]
                    freq = {x: past_stream.count(x) for x in current_frames}
                    if algo == "LFU":
                        evict_page = min(current_frames, key=lambda x: freq[x])
                    else:
                        evict_page = max(current_frames, key=lambda x: freq[x])
                    c_idx = current_frames.index(evict_page)
                    current_frames[c_idx] = incoming_page

                if evict_page is not None:
                    self.vm_log_txt.insert(tk.END, f"[SWAP OUT] Databank full. Archive Incident File Code {evict_page} to persistent disk storage.\n")

        self.vm_slots = list(current_frames)
        self.vm_incident_stream.append({
            "algo": algo,
            "page": incoming_page,
            "frames": list(self.vm_slots),
            "status": status
        })
        self.sync_vm_table_ui()
        self.repaint_vm_ratio_chart()

    def open_paging_analytics_page(self):
        page_win = tk.Toplevel(self)
        page_win.title("📊 911 DATABANK MAIN FRAMEWORK ANALYTICS")
        page_win.geometry("950x700")
        page_win.configure(bg="#0b1116")
        
        title_lbl = tk.Label(page_win, text=f"911 COMPUTER AIDED DISPATCH DEMAND PAGING RECORD TRACE-GRAPH // STRATEGY: {self.vm_algo_var.get()}", 
                             bg="#0b1116", fg="#e74c3c", font=("Segoe UI", 11, "bold"), pady=10)
        title_lbl.pack()

        graph_box = tk.Frame(page_win, bg="#16222f")
        graph_box.pack(fill=tk.X, padx=15, pady=5)
        
        fig = Figure(figsize=(9.0, 3.8), dpi=95, facecolor='#16222f')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#0f171e')
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().set_visible(False)
        for spine in ax.spines.values(): spine.set_visible(False)
        
        if self.vm_incident_stream:
            for idx, step in enumerate(self.vm_incident_stream):
                x = idx * 1.3
                is_fault = "FAULT" in step["status"]
                ax.text(x + 0.5, 4.5, f"Call:{step['page']}", color="#ffcc00", weight="bold", ha="center", va="center", fontname="Segoe UI")
                
                for slot_idx in range(self.VM_FRAMES_COUNT):
                    if slot_idx < len(step["frames"]):
                        val = step["frames"][slot_idx]
                    else:
                        val = None
                    val_str = str(val) if val is not None else "-"
                    text_color = "#ff4a4a" if is_fault and val is not None else "#ffffff"
                    
                    y = 3.2 - (slot_idx * 0.8)
                    ax.text(x + 0.5, y, f"[{val_str}]", color=text_color, weight="bold", ha="center", va="center", fontname="Segoe UI")
            ax.set_xlim(-0.2, len(self.vm_incident_stream) * 1.3 + 0.2)
            ax.set_ylim(-3.5, 5.5)
        else:
            ax.text(0.5, 0.5, "Awaiting Virtual Paging Execution Streams", color="white", ha="center", va="center", fontname="Segoe UI")
            
        canvas = FigureCanvasTkAgg(fig, master=graph_box)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        data_box = tk.Frame(page_win, bg="#111c24", relief="solid", bd=1)
        data_box.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        scr = tk.Scrollbar(data_box)
        scr.pack(side=tk.RIGHT, fill=tk.Y)
        
        grid_txt = tk.Text(data_box, bg="#111c24", fg="#ffffff", font=("Segoe UI", 10), yscrollcommand=scr.set, wrap=tk.NONE)
        grid_txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scr.config(command=grid_txt.yview)

        if not self.vm_incident_stream:
            grid_txt.insert(tk.END, ">> Server pipeline registry contains no metrics. Request pages on dashboard terminal interface first.")
        else:
            grid_txt.insert(tk.END, f"CAD SYSTEM COUNTERS: ABSOLUTE DISPATCH FAULTS = {self.page_fault_count} // BUFFER HITS = {self.page_hit_count}\n")
            grid_txt.insert(tk.END, f"MAINFRAME HIT CACHE EFFICIENCY RATE: {(self.page_hit_count / max(1, self.page_hit_count+self.page_fault_count))*100:.1f}%\n")
            grid_txt.insert(tk.END, "="*95 + "\n")
            
            header_slots = " | ".join([f"BUFFER SLOT {x+1}" for x in range(self.VM_FRAMES_COUNT)])
            grid_txt.insert(tk.END, f"STEP RECORD || REQUEST CODE ||  {header_slots}  ||\n")
            grid_txt.insert(tk.END, "="*95 + "\n")
            
            for idx, item in enumerate(self.vm_incident_stream):
                slot_strings = []
                for s_idx in range(self.VM_FRAMES_COUNT):
                    if s_idx < len(item['frames']):
                        v = item['frames'][s_idx]
                    else:
                        v = None
                    slot_strings.append(f"[{str(v) if v is not None else '-':^3s}]")
                
                joined_slots = "   |   ".join(slot_strings)
                outcome = "HIT" if "HIT" in item["status"] else "FAULT"
                
                line = f" Step {idx+1:02d}    ||    Code ({item['page']})   ||   {joined_slots}   ||  ({outcome})\n"
                grid_txt.insert(tk.END, line)
                
            grid_txt.insert(tk.END, "="*95 + "\n>> End of Core Matrix Trace Log Ledger Execution Frame.")
            
        grid_txt.config(state=tk.DISABLED)
        tk.Button(page_win, text="Dismiss Analytics View", bg="#1c2d3d", fg="white", font=("Segoe UI", 9, "bold"), command=page_win.destroy).pack(pady=5)

    def clear_vm_simulation(self):
        self.vm_slots = [None] * self.VM_FRAMES_COUNT
        self.vm_incident_stream.clear()
        self.vm_historical_requests.clear()
        self.page_fault_count = 0
        self.page_hit_count = 0
        self.vm_log_txt.delete("1.0", tk.END)
        self.sync_vm_table_ui()
        self.repaint_vm_ratio_chart()