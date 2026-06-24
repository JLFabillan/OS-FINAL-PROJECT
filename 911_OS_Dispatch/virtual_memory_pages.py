class PageReplacementSimulator:
    def __init__(self, num_frames=3):
        self.num_frames = num_frames  # Number of monitors the dispatcher has

    # ==========================================
    # 1. STANDARD ALGORITHMS
    # ==========================================

    def run_fifo(self, reference_string):
        """First-In, First-Out (FIFO)"""
        print("\n--- Running FIFO Page Replacement ---")
        frames = []
        page_faults = 0

        for page in reference_string:
            if page not in frames:
                page_faults += 1
                if len(frames) >= self.num_frames:
                    removed = frames.pop(0)
                    print(f"Monitor full. Evicted oldest Incident {removed}.")
                
                frames.append(page)
                print(f"Loaded Incident {page} -> Screens: {frames}")
            else:
                print(f"Incident {page} is already on screen.")

        print(f"Total FIFO Page Faults: {page_faults}")

    def run_lru(self, reference_string):
        """Least Recently Used (LRU)"""
        print("\n--- Running LRU Page Replacement ---")
        frames = []
        page_faults = 0

        for page in reference_string:
            if page not in frames:
                page_faults += 1
                if len(frames) >= self.num_frames:
                    removed = frames.pop(0) # Index 0 is the least recently used
                    print(f"Monitor full. Evicted idle Incident {removed}.")
                
                frames.append(page)
                print(f"Loaded Incident {page} -> Screens: {frames}")
            else:
                # Move accessed page to the back (most recently used)
                frames.remove(page)
                frames.append(page)
                print(f"Viewed Incident {page} again -> Screens: {frames}")

        print(f"Total LRU Page Faults: {page_faults}")

    def run_optimal(self, reference_string):
        """Optimal Page Replacement (Look-ahead)"""
        print("\n--- Running Optimal Page Replacement ---")
        frames = []
        page_faults = 0

        for i, page in enumerate(reference_string):
            if page not in frames:
                page_faults += 1
                if len(frames) >= self.num_frames:
                    future_uses = []
                    for frame in frames:
                        if frame in reference_string[i+1:]:
                            future_uses.append(reference_string[i+1:].index(frame))
                        else:
                            future_uses.append(float('inf'))
                    
                    evict_index = future_uses.index(max(future_uses))
                    removed = frames.pop(evict_index)
                    print(f"Monitor full. Evicted Incident {removed} (not needed soon).")
                
                frames.append(page)
                print(f"Loaded Incident {page} -> Screens: {frames}")
            else:
                print(f"Incident {page} is already on screen.")

        print(f"Total Optimal Page Faults: {page_faults}")

    # ==========================================
    # 2. LRU APPROXIMATION ALGORITHMS
    # ==========================================

    def run_second_chance_clock(self, reference_string):
        """Second Chance (Clock) Algorithm"""
        print("\n--- Running Second Chance (Clock) Algorithm ---")
        frames = [] 
        clock_hand = 0
        page_faults = 0

        for page in reference_string:
            found = False
            for frame in frames:
                if frame["id"] == page:
                    frame["ref_bit"] = 1
                    print(f"Incident {page} accessed. Reference bit set to 1.")
                    found = True
                    break
            
            if not found:
                page_faults += 1
                if len(frames) < self.num_frames:
                    frames.append({"id": page, "ref_bit": 1})
                    print(f"Empty monitor found. Loaded Incident {page}.")
                else:
                    while True:
                        current_frame = frames[clock_hand]
                        if current_frame["ref_bit"] == 1:
                            print(f"Clock hand at {current_frame['id']} (Bit 1) -> Giving second chance, clearing to 0.")
                            current_frame["ref_bit"] = 0
                            clock_hand = (clock_hand + 1) % self.num_frames
                        else:
                            print(f"Clock hand at {current_frame['id']} (Bit 0) -> Evicting!")
                            frames[clock_hand] = {"id": page, "ref_bit": 1}
                            clock_hand = (clock_hand + 1) % self.num_frames
                            break
                
                layout = [f"{f['id']}(bit:{f['ref_bit']})" for f in frames]
                print(f"Current Monitors Layout: {layout}")
                    
        print(f"Total Second Chance Page Faults: {page_faults}")

    # ==========================================
    # 3. COUNTING-BASED ALGORITHMS
    # ==========================================

    def run_lfu(self, reference_string):
        """Least Frequently Used (LFU)"""
        print("\n--- Running LFU Algorithm ---")
        frames = []       
        frequencies = {}  
        page_faults = 0

        for page in reference_string:
            frequencies[page] = frequencies.get(page, 0) + 1
            
            if page not in frames:
                page_faults += 1
                if len(frames) >= self.num_frames:
                    # Find incident with the lowest frequency
                    victim = min(frames, key=lambda f: frequencies[f])
                    frames.remove(victim)
                    print(f"Monitors full. Evicted LFU Incident {victim} (Used {frequencies[victim]} times).")
                
                frames.append(page)
                print(f"Loaded Incident {page} -> Screens: {frames}")
            else:
                print(f"Incident {page} viewed again. Frequency count updated to {frequencies[page]}.")

        print(f"Total LFU Page Faults: {page_faults}")

    def run_mfu(self, reference_string):
        """Most Frequently Used (MFU)"""
        print("\n--- Running MFU Algorithm ---")
        frames = []       
        frequencies = {}  
        page_faults = 0

        for page in reference_string:
            frequencies[page] = frequencies.get(page, 0) + 1
            
            if page not in frames:
                page_faults += 1
                if len(frames) >= self.num_frames:
                    # Find incident with the highest frequency
                    victim = max(frames, key=lambda f: frequencies[f])
                    frames.remove(victim)
                    print(f"Monitors full. Evicted MFU Incident {victim} (Used {frequencies[victim]} times).")
                
                frames.append(page)
                print(f"Loaded Incident {page} -> Screens: {frames}")
            else:
                print(f"Incident {page} viewed again. Frequency count updated to {frequencies[page]}.")

        print(f"Total MFU Page Faults: {page_faults}")




class DroneRouter:
    def __init__(self, initial_position):
        self.initial_position = initial_position
        self.current_position = initial_position
        self.route_history = [initial_position]
        self.total_track_count = 0

    def calculate_sstf(self, incident_locations):
        """
        Takes a list of pending emergency sectors and calculates the optimal 
        SSTF path, tracking the total distance traveled.
        """
        # Create a copy of the list so we don't destroy the original data
        pending_locations = incident_locations.copy()
        
        print("\n--- Initiating SSTF Drone Routing Protocol ---")
        print(f"Initial Drone Position: Sector {self.current_position}")
        
        while pending_locations:
            # 1. Find the location with the absolute shortest distance from our current spot
            closest_location = min(pending_locations, key=lambda loc: abs(loc - self.current_position))
            
            # 2. Calculate the tracks traversed (distance traveled)
            distance = abs(closest_location - self.current_position)
            self.total_track_count += distance
            
            # 3. Move the drone to the new location
            self.current_position = closest_location
            self.route_history.append(closest_location)
            
            # 4. Remove the resolved location from the pending list
            pending_locations.remove(closest_location)
            
            print(f"Dispatched to Sector {closest_location} | Distance: {distance} units")
            
        print("-" * 45)
        print("Routing Complete.")
        print(f"Final Path Traversed: {' -> '.join(map(str, self.route_history))}")
        print(f"Total Track Count: {self.total_track_count} units\n")
        
        # Return the data so the UI can draw the graph later
        return self.route_history, self.total_track_count

# ==========================================
# TEST EXECUTION
# ==========================================
if __name__ == "__main__":
    # The drone starts at sector 50
    dispatch_drone = DroneRouter(initial_position=50)
    
    # A list of active 911 emergencies at various map coordinates
    active_emergencies = [82, 170, 43, 140, 24, 16, 190]
    
    # Calculate the route
    route, total_distance = dispatch_drone.calculate_sstf(active_emergencies)