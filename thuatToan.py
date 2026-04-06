import main

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

if __name__ == "__main__":
    cube = main.RubikCube()
    print(is_goal(cube.cube))  # Should print True for a solved cube
    cube.rotate_R()
    print(is_goal(cube.cube))  # Should print False after a move