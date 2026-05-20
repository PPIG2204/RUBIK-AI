import main
import heapq
import time

CORNERS = [
    # Tên: vị trí trên cube
    [("U", 0, 0), ("L", 0, 0), ("B", 0, 2)],  # ULB
    [("U", 0, 2), ("B", 0, 0), ("R", 0, 2)],  # UBR
    [("U", 2, 0), ("F", 0, 0), ("L", 0, 2)],  # UFL
    [("U", 2, 2), ("R", 0, 0), ("F", 0, 2)],  # URF
    [("D", 0, 0), ("F", 2, 0), ("L", 2, 2)],  # DFL
    [("D", 0, 2), ("R", 2, 0), ("F", 2, 2)],  # DRF
    [("D", 2, 0), ("L", 2, 0), ("B", 2, 2)],  # DLB
    [("D", 2, 2), ("B", 2, 0), ("R", 2, 2)],  # DBR
]
 
# ============================================
# ĐỊNH NGHĨA 12 EDGE PIECES
# Mỗi edge là list 2 tuple (face, row, col)
# ============================================
EDGES = [
    [("U", 0, 1), ("B", 0, 1)],  # UB
    [("U", 1, 0), ("L", 0, 1)],  # UL
    [("U", 1, 2), ("R", 0, 1)],  # UR
    [("U", 2, 1), ("F", 0, 1)],  # UF
    [("D", 0, 1), ("F", 2, 1)],  # DF
    [("D", 1, 0), ("L", 2, 1)],  # DL
    [("D", 1, 2), ("R", 2, 1)],  # DR
    [("D", 2, 1), ("B", 2, 1)],  # DB
    [("F", 1, 0), ("L", 1, 2)],  # FL
    [("F", 1, 2), ("R", 1, 0)],  # FR
    [("B", 1, 0), ("R", 1, 2)],  # BR
    [("B", 1, 2), ("L", 1, 0)],  # BL
]
# ============================================
# SOLVED STATE - Trạng thái hoàn chỉnh của cube
# Màu sắc: F=0(GREEN), U=1(WHITE), L=2(ORANGE), D=3(YELLOW), R=4(RED), B=5(BLUE)
# ============================================
SOLVED_STATE = {
    "F": [[0]*3 for _ in range(3)],  # GREEN
    "U": [[1]*3 for _ in range(3)],  # WHITE
    "L": [[2]*3 for _ in range(3)],  # ORANGE
    "D": [[3]*3 for _ in range(3)],  # YELLOW
    "R": [[4]*3 for _ in range(3)],  # RED
    "B": [[5]*3 for _ in range(3)],  # BLUE
}
def heuristic(state):
    """
    Improved heuristic: max(misplaced_corners, misplaced_edges)
    
    Args:
        state: dict với keys "F", "U", "L", "D", "R", "B"
               mỗi value là list 3x3 chứa số từ 0-5 (màu)
    
    Returns:
        max(corners_wrong, edges_wrong) - lower bound cho số move còn lại
    """
    
    corners_wrong = 0
    edges_wrong = 0
    
    # ============================================
    # ĐẾM CORNER SẢI VỊ TRÍ
    # ============================================
    for corner_positions in CORNERS:
        # Lấy tập màu của corner hiện tại
        current_colors = set()
        for face, row, col in corner_positions:
            current_colors.add(state[face][row][col])
        
        # Lấy tập màu của corner trong trạng thái solved
        solved_colors = set()
        for face, row, col in corner_positions:
            solved_colors.add(SOLVED_STATE[face][row][col])
        
        # Nếu tập màu không khớp → corner sai vị trí
        if current_colors != solved_colors:
            corners_wrong += 1
    
    # ============================================
    # ĐẾM EDGE SẢI VỊ TRÍ
    # ============================================
    for edge_positions in EDGES:
        # Lấy tập màu của edge hiện tại
        current_colors = set()
        for face, row, col in edge_positions:
            current_colors.add(state[face][row][col])
        
        # Lấy tập màu của edge trong trạng thái solved
        solved_colors = set()
        for face, row, col in edge_positions:
            solved_colors.add(SOLVED_STATE[face][row][col])
        
        # Nếu tập màu không khớp → edge sai vị trí
        if current_colors != solved_colors:
            edges_wrong += 1
    
    # Trả về max để được lower bound tốt hơn
    return max(corners_wrong, edges_wrong)

def is_goal(state):
    for face in state.values():
        color = face[0][0]
        for row in face:
            for cell in row:
                if cell != color:
                    return False
    return True

def hash_state(state):
    return tuple(
        cell
        for face in ["U", "D", "L", "R", "F", "B"]
        for row in state[face]
        for cell in row
    )


def get_all_moves():
    return [
        "R", "R'", "L", "L'", "U", "U'", "D", "D'", "F", "F'", "B", "B'"
    ]

def is_reverse_move(move1, move2):
    """Check if move2 is reverse of move1"""
    return (move1 + "'") == move2 or (move2 + "'") == move1

def get_face_from_move(move):
    """Extract face letter from move (e.g., 'R' from 'R' or 'R'')"""
    return move[0]

def is_valid_move(current_move, last_move, move_history):
    """
    Pruning rules:
    1. Don't do reverse move immediately
    2. Don't rotate same face 3 times in a row
    """
    # Rule 1: No reverse move
    if last_move and is_reverse_move(last_move, current_move):
        return False
    
    # Rule 2: No same face 3 times in a row
    if len(move_history) >= 2:
        face = get_face_from_move(current_move)
        if (get_face_from_move(move_history[-1]) == face and 
            get_face_from_move(move_history[-2]) == face):
            return False
    
    return True

def apply_move(state, move):
    new_state = {face: [row[:] for row in state[face]] for face in state}
    cube = main.RubikCube()
    cube.cube = new_state
    if move == "R":
        cube.rotate_R()
    elif move == "R'":
        cube.rotate_R_prime()
    elif move == "L":
        cube.rotate_L()
    elif move == "L'":
        cube.rotate_L_prime()
    elif move == "U":
        cube.rotate_U()
    elif move == "U'":
        cube.rotate_U_prime()
    elif move == "D":
        cube.rotate_D()
    elif move == "D'":
        cube.rotate_D_prime()
    elif move == "F":
        cube.rotate_F()
    elif move == "F'":
        cube.rotate_F_prime()
    elif move == "B":
        cube.rotate_B()
    elif move == "B'":
        cube.rotate_B_prime()
    return cube.cube

class Node:
    def __init__(self, state, parent=None, move=None, g=0, h=0, last_move=None):
        self.state = state      # trạng thái cube (tuple / list)
        self.parent = parent    # node trước
        self.move = move        # hành động đã thực hiện
        self.last_move = last_move  # hành động trước đó (để pruning)
        self.g = g              # cost đã đi
        self.h = h              # heuristic
        self.f = g + h          # tổng cost

    def __lt__(self, other):
        return self.f < other.f
    
def reconstruct_path(node):
    path = []
    while node.parent is not None:
        path.append(node.move)
        node = node.parent
    return path[::-1]  # đảo ngược đường đi

def astar(start_state):
    """
    A* search with:
    - Improved heuristic: max(misplaced_corners, misplaced_edges)
    - Pruning: no reverse moves, no same face 3 times
    - h_cache: heuristic caching to avoid recalculation
    - Profiling: nodes_expanded count and runtime measurement
    """
    start_node = Node(
        state=start_state,
        g=0,
        h=heuristic(start_state),
        last_move=None
    )

    open_list = []
    heapq.heappush(open_list, start_node)

    visited = set()
    h_cache = {}  # Cache for heuristic values
    
    nodes_expanded = 0
    start_time = time.perf_counter()

    global step

    while open_list:
        current = heapq.heappop(open_list)
        nodes_expanded += 1

        step += 1

        # Goal check
        if current.h == 0:
            elapsed_time = time.perf_counter() - start_time
            print(f"\n✓ Solution found!")
            print(f"  Nodes expanded: {nodes_expanded}")
            print(f"  Time elapsed: {elapsed_time:.6f}s")
            return reconstruct_path(current), nodes_expanded, elapsed_time

        # state_key = tuple(current.state) # This was wrong
        state_key = hash_state(current.state)

        if state_key in visited:
            continue
        visited.add(state_key)

        # Reconstruct path to get move history for pruning
        path = reconstruct_path(current)
        
        # Expand neighbors
        for move in get_all_moves():
            # Apply pruning rules
            if not is_valid_move(move, current.move, path):
                continue
            
            new_state = apply_move(current.state, move)
            new_state_key = hash_state(new_state)
            
            # Skip if already visited
            if new_state_key in visited:
                continue
            
            # Get or compute heuristic with caching
            if new_state_key in h_cache:
                h_value = h_cache[new_state_key]
            else:
                h_value = heuristic(new_state)
                h_cache[new_state_key] = h_value

            new_node = Node(
                state=new_state,
                parent=current,
                move=move,
                g=current.g + 1,
                h=h_value,
                last_move=current.move
            )

            heapq.heappush(open_list, new_node)

    elapsed_time = time.perf_counter() - start_time
    print(f"\n✗ No solution found!")
    print(f"  Nodes expanded: {nodes_expanded}")
    print(f"  Time elapsed: {elapsed_time:.6f}s")
    return None, nodes_expanded, elapsed_time


step = 0

if __name__ == "__main__":
    
    a = main.RubikCube()
    sc = input("Nhap scramble: ").split()   
    main.use_scramble(a, sc)
    result = astar(a.cube)
    if result:
        astar_solution, nodes_expanded, elapsed_time = result
        print("A* solution:", astar_solution)
        print("Number of steps:", step)
    else:
        print("No solution found")
        print("Number of steps:", step)