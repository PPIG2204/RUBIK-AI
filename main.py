import pygame
import sys

GREEN = 0  # F
WHITE = 1  # U
ORANGE = 2 # L
YELLOW = 3 # D
RED = 4    # R
BLUE = 5   # B
color = [(0,221,0),(255,255,255),(255,170,0),(255,255,0),(255,0,0),(0,0,255)]

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
    
    def rotate_L_prime(self):
        for _ in range(3):
            self.rotate_L()
    def rotate_U(self):
        self.rotate_face_cw("U")

        temp = self.get_row("B", 0)

        self.set_row("B", 0, self.get_row("R", 0))
        self.set_row("R", 0, self.get_row("F", 0))
        self.set_row("F", 0, self.get_row("L", 0))
        self.set_row("L", 0, temp)

    def rotate_U_prime(self):
        for _ in range(3):
            self.rotate_U()

    def rotate_D(self):
        self.rotate_face_cw("D")

        temp = self.get_row("F", 2)

        self.set_row("F", 2, self.get_row("R", 2))
        self.set_row("R", 2, self.get_row("B", 2))
        self.set_row("B", 2, self.get_row("L", 2))
        self.set_row("L", 2, temp)
    
    def rotate_D_prime(self):
        for _ in range(3):
            self.rotate_D()

    def rotate_F(self):
        self.rotate_face_cw("F")

        temp = self.get_row("U", 2)

        self.set_row("U", 2, self.get_col("L", 2)[::-1])
        self.set_col("L", 2, self.get_row("D", 0))
        self.set_row("D", 0, self.get_col("R", 0)[::-1])
        self.set_col("R", 0, temp)

    def rotate_F_prime(self):
        for _ in range(3):
            self.rotate_F()

    def rotate_B(self):
        self.rotate_face_cw("B")

        temp = self.get_row("U", 0)

        self.set_row("U", 0, self.get_col("R", 2))
        self.set_col("R", 2, self.get_row("D", 2)[::-1])
        self.set_row("D", 2, self.get_col("L", 0))
        self.set_col("L", 0, temp[::-1])

    def rotate_B_prime(self):    
        for _ in range(3):
            self.rotate_B()
    # ========================
    # DEBUG / PRINT
    # ========================

    def print_cube(self):
        for face in ["U", "F", "R", "L", "D", "B"]:
            print(f"{face}:")
            for row in self.cube[face]:
                print(row)
            print()
a = RubikCube()

WIDTH = 600
HEIGHT = 450
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("rubik-ai")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r:
                if mods & pygame.KMOD_SHIFT:
                    a.rotate_R_prime()  # Xoay ngược nếu có Shift
                    print("Đã xoay R' (Shift + R)")
                else:
                    a.rotate_R()        # Xoay xuôi nếu không có Shift
                    print("Đã xoay R")
            if event.key == pygame.K_l:
                if mods & pygame.KMOD_SHIFT:
                    a.rotate_L_prime()  # Xoay ngược nếu có Shift
                    print("Đã xoay L' (Shift + L)")
                else:
                    a.rotate_L()        # Xoay xuôi nếu không có Shift
                    print("Đã xoay L")
            if event.key == pygame.K_u:
                if mods & pygame.KMOD_SHIFT:
                    a.rotate_U_prime()  # Xoay ngược nếu có Shift
                    print("Đã xoay U' (Shift + U)")
                else:
                    a.rotate_U()        # Xoay xuôi nếu không có Shift
                    print("Đã xoay U")
            if event.key == pygame.K_d:
                if mods & pygame.KMOD_SHIFT:
                    a.rotate_D_prime()  # Xoay ngược nếu có Shift
                    print("Đã xoay D' (Shift + D)")
                else:
                    a.rotate_D()        # Xoay xuôi nếu không có Shift
                    print("Đã xoay D")
            if event.key == pygame.K_f:
                if mods & pygame.KMOD_SHIFT:
                    a.rotate_F_prime()  # Xoay ngược nếu có Shift
                    print("Đã xoay F' (Shift + F)")
                else:
                    a.rotate_F()        # Xoay xuôi nếu không có Shift
                    print("Đã xoay F")
            if event.key == pygame.K_b:
                if mods & pygame.KMOD_SHIFT:
                    a.rotate_B_prime()  # Xoay ngược nếu có Shift
                    print("Đã xoay B' (Shift + B)")
                else:
                    a.rotate_B()        # Xoay xuôi nếu không có Shift
                    print("Đã xoay B")
            if event.key == pygame.K_p:
                a = RubikCube()  # Reset về trạng thái solved
                print("Đã reset về trạng thái solved")
    screen.fill((100, 100, 100))
    for face in ["U","L","F","D","R","B"]:
        j=0
        for row in a.cube[face]:
            spacew = 0
            spaceh = 0
            if face == "U" or face == "F" or face == "D":
                spacew = 150
            if face == "R":
                spacew = 300
            if face == "B":
                spacew = 450
            if face == "L" or face == "F" or face == "R" or face == "B":
                spaceh = 150
            if face == "D":
                spaceh = 300
            for i in range(0,3):
                rect = (spacew+i*50,spaceh+j*50,50,50)
                pygame.draw.rect(screen, color[row[i]],rect)
            j+=1
    for i in range(0, int(WIDTH/50)):
        pygame.draw.line(screen, (50, 50, 50), (i*50, 0), (i*50, HEIGHT), 2)
    for j in range(0, int(HEIGHT/50)):
        pygame.draw.line(screen, (50, 50, 50), (0, j*50), (WIDTH, j*50), 2)
    pygame.display.flip()
    clock.tick(30)