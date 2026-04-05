GREEN = 0  # F
WHITE = 1  # U
ORANGE = 2 # L
YELLOW = 3 # D
RED = 4    # R
BLUE = 5   # B


class RubikCube:
    def __init__(self, state=None):
        self.cube = state if state else self._init_solved()

    def _init_solved(self):
        return {
            "F": [[GREEN]*3 for _ in range(3)],
            "U": [[WHITE]*3 for _ in range(3)],
            "L": [[ORANGE]*3 for _ in range(3)],
            "D": [[YELLOW]*3 for _ in range(3)],
            "R": [[RED]*3 for _ in range(3)],
            "B": [[BLUE]*3 for _ in range(3)],
        }

    # ========================
    # HELPER FUNCTIONS
    # ========================

    def rotate_face_cw(self, face):
        """Xoay mặt 90 độ theo chiều kim đồng hồ"""
        self.cube[face] = [list(row) for row in zip(*self.cube[face][::-1])]

    def rotate_face_ccw(self, face):
        """Xoay mặt 90 độ ngược chiều kim đồng hồ"""
        self.cube[face] = [list(row) for row in zip(*self.cube[face])]
        self.cube[face].reverse()

    def get_col(self, face, col):
        return [self.cube[face][i][col] for i in range(3)]

    def set_col(self, face, col, values):
        for i in range(3):
            self.cube[face][i][col] = values[i]

    def get_row(self, face, row):
        return self.cube[face][row][:]

    def set_row(self, face, row, values):
        self.cube[face][row] = values[:]

    # ========================
    # MOVES
    # ========================

    def rotate_R(self):
        self.rotate_face_cw("R")

        U, F, D, B = self.cube["U"], self.cube["F"], self.cube["D"], self.cube["B"]

        temp = self.get_col("U", 2)

        self.set_col("U", 2, self.get_col("F", 2))
        self.set_col("F", 2, self.get_col("D", 2))
        self.set_col("D", 2, self.get_col("B", 0)[::-1])
        self.set_col("B", 0, temp[::-1])

    def rotate_R_prime(self):
        for _ in range(3):
            self.rotate_R()

    def rotate_L(self):
        self.rotate_face_cw("L")

        temp = self.get_col("U", 0)

        self.set_col("U", 0, self.get_col("B", 2)[::-1])
        self.set_col("B", 2, self.get_col("D", 0)[::-1])
        self.set_col("D", 0, self.get_col("F", 0))
        self.set_col("F", 0, temp)

    def rotate_U(self):
        self.rotate_face_cw("U")

        temp = self.get_row("B", 0)

        self.set_row("B", 0, self.get_row("R", 0))
        self.set_row("R", 0, self.get_row("F", 0))
        self.set_row("F", 0, self.get_row("L", 0))
        self.set_row("L", 0, temp)

    def rotate_D(self):
        self.rotate_face_cw("D")

        temp = self.get_row("F", 2)

        self.set_row("F", 2, self.get_row("R", 2))
        self.set_row("R", 2, self.get_row("B", 2))
        self.set_row("B", 2, self.get_row("L", 2))
        self.set_row("L", 2, temp)

    def rotate_F(self):
        self.rotate_face_cw("F")

        temp = self.get_row("U", 2)

        self.set_row("U", 2, self.get_col("L", 2)[::-1])
        self.set_col("L", 2, self.get_row("D", 0))
        self.set_row("D", 0, self.get_col("R", 0)[::-1])
        self.set_col("R", 0, temp)

    def rotate_B(self):
        self.rotate_face_cw("B")

        temp = self.get_row("U", 0)

        self.set_row("U", 0, self.get_col("R", 2))
        self.set_col("R", 2, self.get_row("D", 2)[::-1])
        self.set_row("D", 2, self.get_col("L", 0))
        self.set_col("L", 0, temp[::-1])

    # ========================
    # DEBUG / PRINT
    # ========================

    def print_cube(self):
        for face in ["U", "F", "R", "L", "D", "B"]:
            print(f"{face}:")
            for row in self.cube[face]:
                print(row)
            print()
