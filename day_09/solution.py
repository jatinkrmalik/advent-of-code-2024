from collections import defaultdict
from typing import List, Dict, Tuple

def parse_disk_map(disk_map: str) -> list:
    """
    Parse the disk map string into a list of blocks where each block
    either contains a file ID (int) or free space ('.')
    """
    blocks = []
    file_id = 0
    for i, length in enumerate(disk_map):
        length = int(length)
        if i % 2 == 0:  # File blocks
            blocks.extend([file_id] * length)
            file_id += 1
        else:  # Free space blocks
            blocks.extend(['.'] * length)
    return blocks

# Bruteforce approach - Part 1
# def find_move_positions(blocks: list) -> tuple[int, int]:
#     """
#     Find the rightmost file block and leftmost free space.
#     Returns (source, destination) positions or (None, None) if no moves possible.
#     """
#     # Find rightmost file (source)
#     source = None
#     for i in range(len(blocks) - 1, -1, -1):
#         if blocks[i] != '.':
#             source = i
#             break
    
#     # Find leftmost free space (destination)
#     destination = None
#     for i in range(len(blocks)):
#         if blocks[i] == '.':
#             destination = i
#             break
    
#     # If either position not found or destination >= source, no valid moves
#     if source is None or destination is None or destination >= source:
#         return None, None
    
#     return source, destination

# def compact_disk(blocks: list) -> None:
#     """
#     Compact the disk by moving files one at a time from right to left
#     into the leftmost available free space.
#     """
#     while True:
#         source, destination = find_move_positions(blocks)
#         if source is None:  # No more valid moves
#             break
#         # Move the file block
#         blocks[destination] = blocks[source]
#         blocks[source] = '.'

# Optimised approach - Part 1 (2 pointer approach)
def compact_disk_part1(blocks: list) -> None:
    """
    Optimize disk compaction using two pointers for Part 1
    """
    left = 0
    right = len(blocks) - 1
    
    while left < right:
        # Find leftmost free space
        while left < right and blocks[left] != '.':
            left += 1
            
        # Find rightmost file
        while left < right and blocks[right] == '.':
            right -= 1
            
        # If pointers are valid, swap the blocks
        if left < right:
            blocks[left], blocks[right] = blocks[right], blocks[left]
            left += 1
            right -= 1

# Bruteforce approach - Part 2
# def get_file_info(blocks: List) -> Dict[int, List[int]]:
#     """
#     Get information about each file's position and size
#     Returns: Dict[file_id, List[positions]]
#     """
#     file_positions = defaultdict(list)
#     for pos, block in enumerate(blocks):
#         if block != '.':
#             file_positions[block].append(pos)
#     return file_positions

# def find_free_space(blocks: List, start: int, size_needed: int) -> int:
#     """
#     Find the leftmost position of a contiguous free space of required size
#     Returns: starting position of free space or -1 if not found
#     """
#     count = 0
#     pos = start
#     start_pos = -1
    
#     while pos < len(blocks):
#         if blocks[pos] == '.':
#             if count == 0:
#                 start_pos = pos
#             count += 1
#             if count == size_needed:
#                 return start_pos
#         else:
#             count = 0
#             start_pos = -1
#         pos += 1
    
#     return -1

# def move_file(blocks: List, file_id: int, file_positions: List[int], new_start: int) -> None:
#     """
#     Move a file to a new position as a single unit
#     """
#     file_size = len(file_positions)
    
#     # First clear the old positions
#     for pos in file_positions:
#         blocks[pos] = '.'
    
#     # Then place the file in its new position
#     for i in range(file_size):
#         blocks[new_start + i] = file_id

# def compact_disk_part2(blocks: List) -> None:
#     """
#     Compact disk by moving whole files left-to-right, processing files
#     in decreasing order of file IDs. Each file can only move once.
#     """
#     file_info = get_file_info(blocks)
    
#     # Process files in decreasing order of file IDs
#     for file_id in sorted(file_info.keys(), reverse=True):
#         positions = file_info[file_id]
#         file_size = len(positions)
#         file_start = min(positions)
        
#         # Look for free space before the file's current position
#         new_pos = find_free_space(blocks, 0, file_size)
        
#         # Only move if we found a valid space that's before the current position
#         if new_pos != -1 and new_pos < file_start:
#             move_file(blocks, file_id, positions, new_pos)

# Optimised approach - Part 2 (2 pointer approach)
def compact_disk_part2_optimised(blocks: List) -> None:
    """
    Optimize disk compaction for Part 2 using two pointers and on-the-fly file detection.
    """
    right = len(blocks) - 1
    current_file_id = max(block for block in blocks if block != '.')
    
    while current_file_id >= 0:
        # Find rightmost position of current file
        while right >= 0 and blocks[right] != current_file_id:
            right -= 1
            
        if right < 0:
            current_file_id -= 1
            right = len(blocks) - 1
            continue
            
        # Count file size from right pointer
        file_size = 0
        file_positions = []
        temp_right = right
        while temp_right >= 0 and blocks[temp_right] == current_file_id:
            file_size += 1
            file_positions.append(temp_right)
            temp_right -= 1
        
        file_start = min(file_positions)
        
        # Find leftmost valid space
        left = 0
        while left < file_start:
            count = 0
            pos = left
            
            # Check contiguous space
            while pos < file_start and blocks[pos] == '.':
                count += 1
                pos += 1
                
            if count >= file_size:
                # Move the file
                for i, old_pos in enumerate(reversed(file_positions)):
                    blocks[left + i] = current_file_id
                    blocks[old_pos] = '.'
                break
                
            left = pos + 1
            
        current_file_id -= 1
        right = len(blocks) - 1

def calculate_checksum(blocks: list) -> int:
    """
    Calculate filesystem checksum by summing position * file_id
    for each block containing a file
    """
    return sum(pos * file_id for pos, file_id in enumerate(blocks) if file_id != '.')

def run_tests():
    """
    Run test cases from the puzzle description
    """
    # Test Part 1
    test1 = "12345"
    blocks1 = parse_disk_map(test1)
    compact_disk_part1(blocks1)
    checksum1 = calculate_checksum(blocks1)
    assert checksum1 == 60, f"Part 1 Test 1 failed: got {checksum1}, expected 60"

    test2 = "2333133121414131402"
    blocks2 = parse_disk_map(test2)
    compact_disk_part1(blocks2)
    checksum2 = calculate_checksum(blocks2)
    assert checksum2 == 1928, f"Part 1 Test 2 failed: got {checksum2}, expected 1928"

    # Test Part 2
    test3 = "2333133121414131402"
    blocks3 = parse_disk_map(test3)
    compact_disk_part2_optimised(blocks3)
    checksum3 = calculate_checksum(blocks3)
    assert checksum3 == 2858, f"Part 2 Test failed: got {checksum3}, expected 2858"

    print("All test cases passed!")


if __name__ == "__main__":
    # Run the tests
    run_tests()

    with open("day_9/input.txt") as f:
        disk_map = f.read().strip()
    
    # Solve Part 1
    blocks1 = parse_disk_map(disk_map)
    compact_disk_part1(blocks1)
    part1_result = calculate_checksum(blocks1)
    print(f"Part 1 solution: {part1_result}")    
    
    # Solve Part 2
    blocks2 = parse_disk_map(disk_map)
    compact_disk_part2_optimised(blocks2)
    part2_result = calculate_checksum(blocks2)
    print(f"Part 2 solution: {part2_result}")