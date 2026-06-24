class Incident:
    def __init__(self, incident_id, description, priority, burst_time, arrival_time):
        self.incident_id = incident_id
        self.description = description
        self.priority = priority             # Lower number = higher urgency (1 is critical)
        self.burst_time = burst_time         # Total time required
        self.arrival_time = arrival_time
        
        # Tracking variables
        self.remaining_time = burst_time     # Crucial for preemptive algorithms
        self.is_completed = False
        self.completion_time = 0
        self.turnaround_time = 0             # Completion Time - Arrival Time
        self.waiting_time = 0                # Turnaround Time - Burst Time

    def __repr__(self):
        return f"[ID:{self.incident_id} | {self.description} | Arrival:{self.arrival_time} | Burst:{self.burst_time} | Priority:{self.priority}]"


class Dispatcher:
    def __init__(self, incidents):
        self.incidents = incidents           # Master list of all calls for the day
        self.completed = []                  # Log of finished calls
        self.current_time = 0                # The Master Simulation Clock

    def reset_system(self):
        """Resets the simulation clock and incident states between algorithm runs."""
        self.current_time = 0
        self.completed = []
        for inc in self.incidents:
            inc.remaining_time = inc.burst_time
            inc.is_completed = False
            inc.completion_time = 0

    def get_available_incidents(self):
        """Helper function: Returns incidents that have arrived and aren't finished."""
        return [i for i in self.incidents if i.arrival_time <= self.current_time and not i.is_completed]

    # ==========================================
    # 1. NON-PREEMPTIVE ALGORITHMS
    # ==========================================

    def run_fcfs(self):
        self.reset_system()
        print("\n--- Running FCFS (First Come, First Served) ---")
        
        # Sort master list purely by arrival time
        queue = sorted(self.incidents, key=lambda x: x.arrival_time)
        
        for inc in queue:
            # If the unit is idle waiting for the next call to arrive
            if self.current_time < inc.arrival_time:
                self.current_time = inc.arrival_time
                
            print(f"Time {self.current_time}: Dispatching to {inc.description}")
            
            # Non-preemptive: Jump the clock forward by the full burst time
            self.current_time += inc.burst_time
            inc.completion_time = self.current_time
            inc.is_completed = True
            self.completed.append(inc)

    def run_sjf_non_preemptive(self):
        self.reset_system()
        print("\n--- Running SJF (Non-Preemptive) ---")
        
        while len(self.completed) < len(self.incidents):
            available = self.get_available_incidents()
            
            if not available:
                self.current_time += 1 # Idle tick
                continue
                
            # Sort by burst time, then by arrival time if there's a tie
            available.sort(key=lambda x: (x.burst_time, x.arrival_time))
            current_inc = available[0]
            
            print(f"Time {self.current_time}: Dispatching to {current_inc.description} (Burst: {current_inc.burst_time})")
            
            self.current_time += current_inc.burst_time
            current_inc.completion_time = self.current_time
            current_inc.is_completed = True
            self.completed.append(current_inc)

    def run_priority_non_preemptive(self):
        self.reset_system()
        print("\n--- Running Priority (Non-Preemptive) ---")
        
        while len(self.completed) < len(self.incidents):
            available = self.get_available_incidents()
            
            if not available:
                self.current_time += 1
                continue
                
            # Sort by Priority (lowest number first), then arrival time
            available.sort(key=lambda x: (x.priority, x.arrival_time))
            current_inc = available[0]
            
            print(f"Time {self.current_time}: Priority {current_inc.priority} Dispatch to {current_inc.description}")
            
            self.current_time += current_inc.burst_time
            current_inc.completion_time = self.current_time
            current_inc.is_completed = True
            self.completed.append(current_inc)

    # ==========================================
    # 2. PREEMPTIVE ALGORITHMS
    # ==========================================

    def run_srtf(self):
        self.reset_system()
        print("\n--- Running SRTF (Preemptive SJF) ---")
        
        last_incident_id = None # Used to track if we switched tasks
        
        while len(self.completed) < len(self.incidents):
            available = self.get_available_incidents()
            
            if not available:
                self.current_time += 1
                continue
                
            # Sort by shortest remaining time
            available.sort(key=lambda x: (x.remaining_time, x.arrival_time))
            current_inc = available[0]
            
            # Print only when a preemptive switch occurs
            if last_incident_id != current_inc.incident_id:
                print(f"Time {self.current_time}: Preempting/Switching to {current_inc.description} (Remaining: {current_inc.remaining_time})")
                last_incident_id = current_inc.incident_id
            
            # Tick the clock by 1 unit
            self.current_time += 1
            current_inc.remaining_time -= 1
            
            if current_inc.remaining_time == 0:
                current_inc.completion_time = self.current_time
                current_inc.is_completed = True
                self.completed.append(current_inc)
                print(f"Time {self.current_time}: Incident Resolved -> {current_inc.description}")

    def run_priority_preemptive(self):
        self.reset_system()
        print("\n--- Running Priority (Preemptive) ---")
        
        last_incident_id = None
        
        while len(self.completed) < len(self.incidents):
            available = self.get_available_incidents()
            
            if not available:
                self.current_time += 1
                continue
                
            # Sort by Priority (lowest number first)
            available.sort(key=lambda x: (x.priority, x.arrival_time))
            current_inc = available[0]
            
            if last_incident_id != current_inc.incident_id:
                print(f"Time {self.current_time}: High Priority Override to {current_inc.description} (Priority: {current_inc.priority})")
                last_incident_id = current_inc.incident_id
            
            self.current_time += 1
            current_inc.remaining_time -= 1
            
            if current_inc.remaining_time == 0:
                current_inc.completion_time = self.current_time
                current_inc.is_completed = True
                self.completed.append(current_inc)

    def run_round_robin(self, time_quantum):
        self.reset_system()
        print(f"\n--- Running Round Robin (Quantum: {time_quantum}) ---")
        
        queue = []
        # Sort master list to know when things arrive
        sorted_incidents = sorted(self.incidents, key=lambda x: x.arrival_time)
        index = 0
        
        # Push initial arrivals into the queue
        while index < len(sorted_incidents) and sorted_incidents[index].arrival_time <= self.current_time:
            queue.append(sorted_incidents[index])
            index += 1
            
        while len(self.completed) < len(self.incidents):
            if not queue:
                self.current_time += 1
                # Check for new arrivals while idle
                while index < len(sorted_incidents) and sorted_incidents[index].arrival_time <= self.current_time:
                    queue.append(sorted_incidents[index])
                    index += 1
                continue
                
            current_inc = queue.pop(0)
            
            # Determine how long we work on this incident right now
            work_time = min(time_quantum, current_inc.remaining_time)
            print(f"Time {self.current_time}: Working on {current_inc.description} for {work_time} units.")
            
            self.current_time += work_time
            current_inc.remaining_time -= work_time
            
            # While working, did new incidents arrive? Add them to the queue BEFORE pushing the current one back.
            while index < len(sorted_incidents) and sorted_incidents[index].arrival_time <= self.current_time:
                queue.append(sorted_incidents[index])
                index += 1
                
            if current_inc.remaining_time > 0:
                queue.append(current_inc) # Go to the back of the line
            else:
                current_inc.completion_time = self.current_time
                current_inc.is_completed = True
                self.completed.append(current_inc)
                print(f"Time {self.current_time}: Incident Resolved -> {current_inc.description}")


# ==========================================
# TEST EXECUTION
# ==========================================
if __name__ == "__main__":
    calls = [
        Incident(1, "Noise Complaint", priority=3, burst_time=5, arrival_time=0),
        Incident(2, "Traffic Accident", priority=2, burst_time=8, arrival_time=2),
        Incident(3, "Armed Robbery", priority=1, burst_time=3, arrival_time=4),
        Incident(4, "Medical Emergency", priority=1, burst_time=4, arrival_time=5)
    ]
    
    dispatch_center = Dispatcher(calls)
    
    dispatch_center.run_fcfs()
    dispatch_center.run_sjf_non_preemptive()
    dispatch_center.run_priority_non_preemptive()
    dispatch_center.run_srtf()
    dispatch_center.run_priority_preemptive()
    dispatch_center.run_round_robin(time_quantum=3)