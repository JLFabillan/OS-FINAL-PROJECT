import random

class DiskBlock:
    def __init__(self, block_id):
        self.block_id = block_id
        self.is_free = True
        self.incident_id = None
        self.next_block = None  # Used for Linked Allocation

    def __repr__(self):
        if self.is_free:
            return f"[{self.block_id}: FREE]"
        return f"[{self.block_id}: Inc-{self.incident_id}]"

class PoliceDatabaseArchive:
    def __init__(self, total_blocks=50):
        self.total_blocks = total_blocks
        self.disk = [DiskBlock(i) for i in range(total_blocks)]
        self.index_tables = {}  # Used for Indexed Allocation

    def display_disk(self):
        print("\n--- Current Database Disk Status ---")
        # Print the disk in rows of 10 for easy reading
        for i in range(0, self.total_blocks, 10):
            row = self.disk[i:i+10]
            print(" ".join(str(block) for block in row))
        print("-" * 35 + "\n")

    # ==========================================
    # 1. CONTIGUOUS ALLOCATION
    # ==========================================
    def allocate_contiguous(self, incident_id, file_size_blocks):
        print(f"Attempting Contiguous Archive for Incident {incident_id} (Size: {file_size_blocks} blocks)...")
        
        # Search for a continuous streak of free blocks
        streak = 0
        start_index = -1
        
        for i, block in enumerate(self.disk):
            if block.is_free:
                if streak == 0:
                    start_index = i
                streak += 1
                if streak == file_size_blocks:
                    # We found a big enough chunk! Save the file.
                    for j in range(start_index, start_index + file_size_blocks):
                        self.disk[j].is_free = False
                        self.disk[j].incident_id = incident_id
                    print(f"SUCCESS: Saved Contiguously from block {start_index} to {start_index + file_size_blocks - 1}.")
                    return True
            else:
                streak = 0 # Reset streak if we hit an occupied block
                
        print(f"FAILED: Not enough contiguous space. Disk fragmentation is too high.")
        return False

    # ==========================================
    # 2. LINKED ALLOCATION
    # ==========================================
    def allocate_linked(self, incident_id, file_size_blocks):
        print(f"Attempting Linked Archive for Incident {incident_id} (Size: {file_size_blocks} blocks)...")
        
        free_blocks = [b for b in self.disk if b.is_free]
        if len(free_blocks) < file_size_blocks:
            print("FAILED: Not enough total free space on disk.")
            return False
            
        # Take exactly the amount of scattered blocks we need
        allocated_blocks = free_blocks[:file_size_blocks]
        
        for i in range(len(allocated_blocks)):
            current_block = allocated_blocks[i]
            current_block.is_free = False
            current_block.incident_id = incident_id
            
            # Link to the next block, unless it's the last one
            if i < len(allocated_blocks) - 1:
                current_block.next_block = allocated_blocks[i+1].block_id
                
        start = allocated_blocks[0].block_id
        end = allocated_blocks[-1].block_id
        print(f"SUCCESS: Saved via Linked Allocation. File starts at Block {start} and ends at Block {end}.")
        return True

    # ==========================================
    # 3. INDEXED ALLOCATION
    # ==========================================
    def allocate_indexed(self, incident_id, file_size_blocks):
        print(f"Attempting Indexed Archive for Incident {incident_id} (Size: {file_size_blocks} blocks)...")
        
        # We need space for the file PLUS 1 block for the Master Index Card
        required_space = file_size_blocks + 1
        free_blocks = [b for b in self.disk if b.is_free]
        
        if len(free_blocks) < required_space:
            print("FAILED: Not enough total free space on disk (including index block).")
            return False
            
        # The first free block becomes the Index Block
        index_block = free_blocks[0]
        index_block.is_free = False
        index_block.incident_id = f"IDX-{incident_id}"
        
        # The rest become the actual data file blocks
        data_blocks = free_blocks[1:required_space]
        data_block_ids = []
        
        for block in data_blocks:
            block.is_free = False
            block.incident_id = incident_id
            data_block_ids.append(block.block_id)
            
        # Save the master list to our system
        self.index_tables[incident_id] = {
            "index_block_location": index_block.block_id,
            "data_pointers": data_block_ids
        }
        
        print(f"SUCCESS: Saved via Indexed Allocation. Master Index is at Block {index_block.block_id}.")
        print(f"Index Card Pointers: {data_block_ids}")
        return True

# ==========================================
# TEST EXECUTION
# ==========================================
if __name__ == "__main__":
    db = PoliceDatabaseArchive(total_blocks=40)
    
    # 1. Test Contiguous (Will fill blocks 0 through 4)
    db.allocate_contiguous(incident_id=101, file_size_blocks=5)
    
    # Let's manually simulate some disk fragmentation by marking random blocks as taken
    db.disk[6].is_free = False
    db.disk[8].is_free = False
    db.disk[12].is_free = False
    
    db.display_disk()
    
    # 2. Test Linked (Will weave around the fragmented blocks)
    db.allocate_linked(incident_id=102, file_size_blocks=6)
    
    # 3. Test Indexed (Will grab one block for the index, and the rest for data)
    db.allocate_indexed(incident_id=103, file_size_blocks=4)
    
    db.display_disk()