import main
import heapq
import time


def heuristic(state):
    """
    Improved heuristic: max(misplaced_corners, misplaced_edges)
    - Corners at positions [0,0], [0,2], [2,0], [2,2] on each face
    - Edges at positions [0,1], [1,0], [1,2], [2,1] on each face
    Mapping:
      - Each corner piece touches 3 faces (8 corners total)
      - Each edge piece touches 2 faces (12 edges total)
    Returns: max count to get better bound
    """
    misplaced_corners = 0
    misplaced_edges = 0
    
    for face in state.values():
        center_color = face[1][1]  # center color of the face
        
        # Check corners: [0,0], [0,2], [2,0], [2,2]
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for r, c in corners:
            if face[r][c] != center_color:
                misplaced_corners += 1
        
        # Check edges: [0,1], [1,0], [1,2], [2,1]
        edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
        for r, c in edges:
            if face[r][c] != center_color:
                misplaced_edges += 1
    
    # Each corner piece touches 3 faces, so divide by 3
    # Each edge piece touches 2 faces, so divide by 2
    corners_count = misplaced_corners // 3
    edges_count = misplaced_edges // 2
    
    # Return max for better A* bound
    return max(corners_count, edges_count)

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