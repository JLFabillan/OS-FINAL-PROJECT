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
        pending_locations = incident_locations.copy()
        
        print("\n--- Initiating SSTF Drone Routing Protocol ---")
        print(f"Initial Drone Position: Sector {self.current_position}")
        
        while pending_locations:
            closest_location = min(pending_locations, key=lambda loc: abs(loc - self.current_position))
            distance = abs(closest_location - self.current_position)
            self.total_track_count += distance
            
            self.current_position = closest_location
            self.route_history.append(closest_location)
            pending_locations.remove(closest_location)
            
            print(f"Dispatched to Sector {closest_location} | Distance: {distance} units")
            
        print("-" * 45)
        print("Routing Complete.")
        print(f"Final Path Traversed: {' -> '.join(map(str, self.route_history))}")
        print(f"Total Track Count: {self.total_track_count} units\n")
        
        return self.route_history, self.total_track_count