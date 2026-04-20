import main
import heapq



def heuristic(state):
    # Heuristic: count the number of misplaced edges and corners
    # Corners are at positions [0,0], [0,2], [2,0], [2,2]
    # Edges are at positions [0,1], [1,0], [1,2], [2,1]
    misplaced = 0
    
    for face in state.values():
        center_color = face[1][1]  # center color of the face
        
        # Check corners: [0,0], [0,2], [2,0], [2,2]
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for r, c in corners:
            if face[r][c] != center_color:
                misplaced += 1
        
        # Check edges: [0,1], [1,0], [1,2], [2,1]
        edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
        for r, c in edges:
            if face[r][c] != center_color:
                misplaced += 1
    
    return misplaced

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
    def __init__(self, state, parent=None, move=None, g=0, h=0):
        self.state = state      # trạng thái cube (tuple / list)
        self.parent = parent    # node trước
        self.move = move        # hành động đã thực hiện
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

step = 0

def astar(start_state):
    start_node = Node(
        state=start_state,
        g=0,
        h=heuristic(start_state)
    )

    open_list = []
    heapq.heappush(open_list, start_node)

    visited = set()

    global step

    while open_list:
        current = heapq.heappop(open_list)

        step += 1

        # Goal check
        if is_goal(current.state):
            return reconstruct_path(current)

        # state_key = tuple(current.state) # This was wrong
        state_key = hash_state(current.state)

        if state_key in visited:
            continue
        visited.add(state_key)

        # Expand neighbors
        for move in get_all_moves():
            new_state = apply_move(current.state, move)

            new_node = Node(
                state=new_state,
                parent=current,
                move=move,
                g=current.g + 1,
                h=heuristic(new_state)
            )

            heapq.heappush(open_list, new_node)

    return None

a = main.RubikCube()
sc = input("Nhap scramble: ").split()   
main.use_scramble(a, sc)
astar_solution = astar(a.cube)
print("A* solution:", astar_solution)
print("Number of steps:", step)


if __name__ == "__main__":
    # Test with a simple scramble
    initial_cube = main.RubikCube()
    initial_cube.rotate_R()
    initial_cube.rotate_U()
    
    print("Starting A* search...")
    solution = astar(initial_cube.cube)
    print("Solution found:", solution)

    cube = main.RubikCube()
    print("Is solved cube goal?", is_goal(cube.cube))
    cube.rotate_R()
    print("Is cube after R move goal?", is_goal(cube.cube))