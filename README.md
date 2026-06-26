# 🚨 911 OS Dispatch 

This project is a comprehensive, interactive Operating Systems simulator themed around a high-stakes 911 Computer Aided Dispatch (CAD) terminal. Developed as a final capstone project for BS Computer Engineering, this application demonstrates the practical, real-world application of core OS resource management algorithms.

Rather than displaying abstract textbook numbers, this system maps traditional OS hardware concepts to physical emergency dispatch logistics in a sleek, DPI-aware 2x2 dark-themed dashboard.

## ⚙️ Core OS Implementations (The 4 Modules)

### 1. CPU Dispatcher (Process Scheduling)
* **Analogy:** Incoming 911 emergencies queued for dispatcher attention.
* **Algorithms:** FCFS, SJF (Preemptive/Non-Preemptive), Priority (Preemptive/Non-Preemptive), Round Robin.
* **Features:** Dynamically generated Matplotlib Gantt charts outlining exact time-unit execution boundaries and context switching.

### 2. Active Memory (RAM Allocation)
* **Analogy:** Deploying continuous blocks of physical emergency responder fleets.
* **Algorithms:** MVT (Variable) and MFT (Fixed) using First Fit, Best Fit, and Worst Fit.
* **Features:** Real-time RAM block visualizations tracking internal/external fragmentation, complete with a manual **Memory Compaction** engine to consolidate free holes.

### 3. Virtual Memory Unit (Demand Paging)
* **Analogy:** Dispatchers caching databank incident files onto a limited number of active monitors (frames).
* **Algorithms:** FIFO, OPT, LRU, LFU, MFU.
* **Features:** Trace-graph analytics tracking Absolute Dispatch Faults vs. Buffer Hits to calculate cache efficiency rates.

### 4. Multi-Disk Router (Mass Storage / Disk Scheduling)
* **Analogy:** Routing autonomous emergency drones across physical city cylinder sectors.
* **Algorithms:** FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK.
* **Features:** Visual flight sweep paths calculating the absolute total track distance/seek time to optimize response vectors.

## 🛠️ Technology Stack
* **Language:** Python 3.8+
* **GUI Framework:** Tkinter (Configured with `ctypes` for crisp Windows High-DPI scaling and custom Segoe UI / Consolas typography).
* **Data Visualization:** Matplotlib / FigureCanvasTkAgg
* **Distribution:** PyInstaller (Standalone `.exe` compilation)

## 🚀 How to Run the Simulator

### Option A: Run the Standalone Executable (No Install Required)
1. Download the `CRISIS_LINK_Dispatch.exe` file from the repository releases/dist folder.
2. Double-click the application to launch. *(Note: Because it is packed with Matplotlib, the initial launch may take 3-8 seconds to unpack into memory).*

### Option B: Run from Source Code
If you wish to modify the algorithms or run the raw Python scripts, follow these steps:

**1. Clone the repository:**
```bash
git clone [https://github.com/yourusername/CRISIS-LINK-OS-Dispatch.git](https://github.com/yourusername/CRISIS-LINK-OS-Dispatch.git)
cd CRISIS-LINK-OS-Dispatch
