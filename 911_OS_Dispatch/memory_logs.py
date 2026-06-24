class MemoryBlock:
    def __init__(self, start_address, size, is_free=True, incident_id=None):
        self.start_address = start_address
        self.size = size
        self.is_free = is_free
        self.incident_id = incident_id

    def __repr__(self):
        status = "FREE" if self.is_free else f"INCIDENT-{self.incident_id}"
        return f"[{self.start_address}k - {self.start_address + self.size}k] : {status} ({self.size}k)"


class DispatchMemoryManager:
    def __init__(self, total_memory_kb=1024, mode="MVT", mft_partitions=None):
        self.total_memory = total_memory_kb
        self.mode = mode # "MFT" or "MVT"
        
        if self.mode == "MFT":
            # Initialize fixed rigid blocks based on the provided partition sizes
            self.memory_map = []
            address = 0
            # Default partitions if none are provided
            mft_partitions = mft_partitions or [100, 200, 300, 400] 
            for size in mft_partitions:
                self.memory_map.append(MemoryBlock(address, size))
                address += size
        else:
            # MVT starts with one giant block
            self.memory_map = [MemoryBlock(0, total_memory_kb)]

    def allocate(self, incident_id, required_size, algorithm="First Fit"):
        """Routes the allocation request based on the system mode."""
        if self.mode == "MFT":
            return self._allocate_mft(incident_id, required_size, algorithm)
        else:
            return self._allocate_mvt(incident_id, required_size, algorithm)

    def _allocate_mvt(self, incident_id, required_size, algorithm):
        # 1. Gather all free blocks that are large enough
        valid_holes = [b for b in self.memory_map if b.is_free and b.size >= required_size]
        
        if not valid_holes:
            print(f"MVT Allocation Failed: Not enough contiguous space for Incident {incident_id} ({required_size}k).")
            return False 
            
        target_block = None
        
        # 2. Apply the specific algorithm logic
        if algorithm == "First Fit":
            target_block = valid_holes[0]
            
        elif algorithm == "Best Fit":
            # Sort by smallest leftover space
            valid_holes.sort(key=lambda b: b.size - required_size)
            target_block = valid_holes[0]
            
        elif algorithm == "Worst Fit":
            # Sort by largest leftover space (descending)
            valid_holes.sort(key=lambda b: b.size, reverse=True)
            target_block = valid_holes[0]

        # 3. Split the block dynamically (MVT characteristic)
        self._split_and_assign(target_block, incident_id, required_size)
        return True

    def _split_and_assign(self, block, incident_id, required_size):
        """Helper function for MVT to carve out exactly what is needed."""
        print(f"Allocating {required_size}k for Incident {incident_id}...")
        if block.size == required_size:
            block.is_free = False
            block.incident_id = incident_id
        else:
            # Calculate leftovers
            leftover_size = block.size - required_size
            new_start_address = block.start_address + required_size
            leftover_block = MemoryBlock(new_start_address, leftover_size)
            
            # Modify current block
            block.size = required_size
            block.is_free = False
            block.incident_id = incident_id
            
            # Insert the leftover gap into the memory map
            index = self.memory_map.index(block)
            self.memory_map.insert(index + 1, leftover_block)

    def _allocate_mft(self, incident_id, required_size, algorithm):
        """Assigns incidents to pre-existing fixed partitions."""
        valid_blocks = [b for b in self.memory_map if b.is_free and b.size >= required_size]
        
        if not valid_blocks:
            print(f"MFT Allocation Failed: No fixed partition large enough for Incident {incident_id}.")
            return False
            
        target_block = None
        
        if algorithm == "First Fit":
            target_block = valid_blocks[0]
            
        elif algorithm in ["Best Fit", "Best Available Fit"]:
            valid_blocks.sort(key=lambda b: b.size - required_size)
            target_block = valid_blocks[0]
            
        elif algorithm == "Worst Fit": # Usually applied to MVT, but can technically apply to MFT
            valid_blocks.sort(key=lambda b: b.size, reverse=True)
            target_block = valid_blocks[0]

        print(f"Allocating fixed partition ({target_block.size}k) for Incident {incident_id} ({required_size}k)...")
        # In MFT, we do NOT split. The whole partition is taken (Internal Fragmentation).
        target_block.is_free = False
        target_block.incident_id = incident_id
        return True

    def deallocate(self, incident_id):
        """Frees the memory block when an emergency is resolved."""
        for block in self.memory_map:
            if not block.is_free and block.incident_id == incident_id:
                print(f"Freeing memory from resolved Incident {incident_id}...")
                block.is_free = True
                block.incident_id = None
                return
        print(f"Incident {incident_id} not found in active memory.")

    def compact_memory(self):
        """
        Pushes all active MVT blocks to the front, creating one massive free block at the end.
        This solves External Fragmentation.
        """
        if self.mode == "MFT":
            print("Compaction failed: Compaction is not applicable to fixed MFT partitions.")
            return

        print("\n--- Initiating System Memory Compaction (MVT) ---")
        
        active_blocks = [b for b in self.memory_map if not b.is_free]
        self.memory_map = []
        current_address = 0 
        
        for block in active_blocks:
            block.start_address = current_address 
            self.memory_map.append(block)
            current_address += block.size         
            
        leftover_space = self.total_memory - current_address
        
        if leftover_space > 0:
            self.memory_map.append(MemoryBlock(current_address, leftover_space))
            
        print("Compaction Complete. All free space successfully merged.")

    def display_status(self):
        print(f"\n--- Current Bandwidth Map ({self.mode}) ---")
        for block in self.memory_map:
            print(block)
        print("-" * 45 + "\n")


# ==========================================
# TEST EXECUTION
# ==========================================
if __name__ == "__main__":
    # Test 1: MVT (Variable Tasks) with Compaction
    print(">>> TESTING MVT MODE <<<")
    mvt_sys = DispatchMemoryManager(total_memory_kb=500, mode="MVT")
    
    mvt_sys.allocate(incident_id=101, required_size=100, algorithm="First Fit")
    mvt_sys.allocate(incident_id=102, required_size=200, algorithm="First Fit")
    mvt_sys.allocate(incident_id=103, required_size=50, algorithm="First Fit")
    mvt_sys.display_status()
    
    mvt_sys.deallocate(incident_id=102) # Creates a 200k gap
    mvt_sys.display_status()
    
    # Try to fit 250k into the scattered space (will fail)
    mvt_sys.allocate(incident_id=104, required_size=250, algorithm="Best Fit")
    
    # Run compaction to merge the space, then try again
    mvt_sys.compact_memory()
    mvt_sys.display_status()
    mvt_sys.allocate(incident_id=104, required_size=250, algorithm="Best Fit")
    mvt_sys.display_status()

    # Test 2: MFT (Fixed Tasks)
    print("\n\n>>> TESTING MFT MODE <<<")
    mft_sys = DispatchMemoryManager(mode="MFT", mft_partitions=[100, 200, 300])
    
    # Needs 80k, but will take the whole 100k partition
    mft_sys.allocate(incident_id=201, required_size=80, algorithm="First Fit") 
    mft_sys.display_status()
    
    # Try to run compaction (will be blocked)
    mft_sys.compact_memory()