# 🚨 911 OS Dispatch Simulator

A comprehensive, interactive Operating Systems simulator themed around a 911 Emergency Dispatch Center. This desktop application was developed as a final project for BS Computer Engineering to demonstrate the practical, real-world application of core OS resource management algorithms.

Instead of abstract numbers, this system maps traditional OS concepts to physical dispatch logistics:
* **Processes** $\rightarrow$ Incoming 911 Emergencies
* **CPU** $\rightarrow$ Emergency Response Units
* **RAM** $\rightarrow$ Dispatcher Radio/Video Bandwidth
* **Virtual Pages** $\rightarrow$ Active Dispatcher Dashboard Monitors
* **Disk Head** $\rightarrow$ Drone/Patrol Car Routing

## ⚙️ Core OS Implementations

The dashboard features five dynamic modules:

1. **CPU Scheduling:** Preemptive and non-preemptive task management with live Gantt chart generation. *(FCFS, SJF, SRTF, Round Robin)*
2. **Memory Management:** Dynamic bandwidth allocation and fragmentation resolution. *(MVT/MFT, First/Best/Worst Fit, Compaction)*
3. **Virtual Memory:** Page replacement simulation for limited dispatcher monitors. *(FIFO, LRU, Optimal, Second Chance/Clock, LFU, MFU)*
4. **Disk Scheduling (Virtual Memory):** Optimal physical routing paths for response units, calculating total track count. *(SSTF)*
5. **Mass Storage Management:** Permanent archiving of resolved case files into physical disk blocks. *(Contiguous, Linked, Indexed Allocation)*

## 🛠️ Prerequisites

To run this application, you will need the following installed on your machine:
* **Python 3.8+**
* **Tkinter** (Usually comes pre-installed with Python. Linux users may need to run `sudo apt-get install python3-tk`)
* **Matplotlib** (For rendering the dynamic Gantt charts and memory/routing graphs)

## 🚀 Installation & Setup

Follow these steps to get the simulator running on your local machine:

**1. Clone the repository:**
```bash
git clone [https://github.com/yourusername/911-OS-Dispatch.git](https://github.com/yourusername/911-OS-Dispatch.git)
cd 911-OS-Dispatch
