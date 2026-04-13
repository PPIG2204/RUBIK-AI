from numpy import sin
import pygame
import sys
import math
import time
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

        temp = self.get_row("F", 0)
        self.set_row("F", 0, self.get_row("R", 0))
        self.set_row("R", 0, self.get_row("B", 0))
        self.set_row("B", 0, self.get_row("L", 0))
        self.set_row("L", 0, temp)
    def rotate_U_prime(self):
        for _ in range(3):
            self.rotate_U()

    def rotate_D(self):
        self.rotate_face_cw("D")

        temp = self.get_row("F", 2)

        self.set_row("F", 2, self.get_row("L", 2))
        self.set_row("L", 2, self.get_row("B", 2))
        self.set_row("B", 2, self.get_row("R", 2))
        self.set_row("R", 2, temp)
    
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
    # WHOLE CUBE ROTATIONS
    # ========================

    def rotate_whole_y(self):
        """Xoay toàn bộ khối sang phải (Mặt Trái L chuyển thành mặt Trước F)"""
        temp = self.cube["F"]
        self.cube["F"] = self.cube["L"]
        self.cube["L"] = self.cube["B"]
        self.cube["B"] = self.cube["R"]
        self.cube["R"] = temp
        
        # Khi xoay khối dọc theo trục Y, mặt U và D cũng phải tự xoay để khớp viền
        self.rotate_face_ccw("U")
        self.rotate_face_cw("D")

    def rotate_whole_y_prime(self):
        """Xoay toàn bộ khối sang trái (Mặt Phải R chuyển thành mặt Trước F)"""
        temp = self.cube["F"]
        self.cube["F"] = self.cube["R"]
        self.cube["R"] = self.cube["B"]
        self.cube["B"] = self.cube["L"]
        self.cube["L"] = temp
        
        self.rotate_face_cw("U")
        self.rotate_face_ccw("D")

    def rotate_whole_x(self):
        """Xoay toàn bộ khối lên trên (Mặt Dưới D chuyển thành mặt Trước F)"""
        temp_F = self.cube["F"]
        temp_U = self.cube["U"]
        temp_B = self.cube["B"]
        temp_D = self.cube["D"]

        self.cube["F"] = temp_D
        self.cube["U"] = temp_F
        
        # Khi vòng qua đỉnh/đáy, mặt B và D bị lật ngược 180 độ
        self.cube["B"] = [list(row) for row in temp_U]
        self.rotate_face_cw("B")
        self.rotate_face_cw("B")
        
        self.cube["D"] = [list(row) for row in temp_B]
        self.rotate_face_cw("D")
        self.rotate_face_cw("D")

        # Mặt R và L chỉ xoay tại chỗ
        self.rotate_face_cw("R")
        self.rotate_face_ccw("L")

    def rotate_whole_x_prime(self):
        """Xoay toàn bộ khối xuống dưới (Mặt Trên U chuyển thành mặt Trước F)"""
        temp_F = self.cube["F"]
        temp_U = self.cube["U"]
        temp_B = self.cube["B"]
        temp_D = self.cube["D"]

        self.cube["F"] = temp_U
        self.cube["D"] = temp_F

        self.cube["U"] = [list(row) for row in temp_B]
        self.rotate_face_cw("U")
        self.rotate_face_cw("U")

        self.cube["B"] = [list(row) for row in temp_D]
        self.rotate_face_cw("B")
        self.rotate_face_cw("B")

        self.rotate_face_ccw("R")
        self.rotate_face_cw("L")

    # ========================
    # APPLY MOVE
    # ========================
    
    def apply_move(self, move):
        """Áp dụng một move dựa trên tên (R, R', L, L', U, U', D, D', F, F', B, B')"""
        moves = {
            "R": self.rotate_R,
            "R'": self.rotate_R_prime,
            "L": self.rotate_L,
            "L'": self.rotate_L_prime,
            "U": self.rotate_U,
            "U'": self.rotate_U_prime,
            "D": self.rotate_D,
            "D'": self.rotate_D_prime,
            "F": self.rotate_F,
            "F'": self.rotate_F_prime,
            "B": self.rotate_B,
            "B'": self.rotate_B_prime,
        }

        if move in moves:
            moves[move]()   # gọi function tương ứng
        else:
            print(f"Move không hợp lệ: {move}")

    # ========================
    # DEBUG / PRINT
    # ========================

    def print_cube(self):
        for face in ["U", "F", "R", "L", "D", "B"]:
            print(f"{face}:")
            for row in self.cube[face]:
                print(row)
            print()

def rhombus(x,y,idx):
    global dx,dy
    if idx == 0:         #trên
        top_points = [
            (x,y),       #trung tâm
            (x-dy,y-dx), #trái
            (x,y-dx*2),  #trên cùng
            (x+dy,y-dx)  #phải
            
        ]
        return top_points
    if idx == 1:         #trái
        top_points = [
            (x,y),       #trung tâm
            (x-dy,y-dx), #trên-trái
            (x-dy,y+dx), #dưới-trái
            (x,y+dx*2)   #dưới cùng
        ]
        return top_points
    if idx == 2:         #phải
        top_points = [
            (x,y),       #trung tâm
            (x+dy,y-dx), #trên-phải
            (x+dy,y+dx), #dưới-phải
            (x,y+dx*2)   #dưới cùng
        ]
        return top_points
   
a = RubikCube()
scramble = input("Nhap scramble: ").split()
WIDTH = 600
HEIGHT = 450
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("rubik-ai")
clock = pygame.time.Clock()
viewpoint = 1
sizev1 = 75
dx=sizev1/2
dy=int(sizev1*pow(3,0.5)/2)
midx=WIDTH/2
midy=HEIGHT/2
for c in scramble:
    if c in ["R","R'","L","L'","U","U'","D","D'","F","F'","B","B'"]:
        a.apply_move(c)
    elif c in ["R2","L2","U2","D2","F2","B2"]:
        a.apply_move(c[0])
        a.apply_move(c[0])

if __name__ == "__main__":
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
                if event.key == pygame.K_o:
                    viewpoint = (viewpoint + 1) & 1
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
                
                # BỔ SUNG PHÍM MŨI TÊN Ở ĐÂY
                if event.key == pygame.K_RIGHT:
                    a.rotate_whole_y()
                    print("Xoay toàn bộ khối sang phải")
                if event.key == pygame.K_LEFT:
                    a.rotate_whole_y_prime()
                    print("Xoay toàn bộ khối sang trái")
                if event.key == pygame.K_UP:
                    a.rotate_whole_x()
                    print("Xoay toàn bộ khối lên trên")
                if event.key == pygame.K_DOWN:
                    a.rotate_whole_x_prime()
                    print("Xoay toàn bộ khối xuống dưới")
        if viewpoint == 0:
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
        else:
            screen.fill((100,100,100))
            for i in range (0,3):
                for j in range(0,3):
                    rx = midx - (2-i)*dy + j*dy
                    ry = midy - (2-i)*dx - j*dx
                    pygame.draw.polygon(screen,color[a.cube["U"][2-j][i]],rhombus(rx,ry,0))
                    pygame.draw.polygon(screen,(0,0,0),rhombus(rx,ry,0),2)
            for i in range (0,3):
                for j in range(0,3):
                    rx = midx - (2-j)*dy
                    ry = midy + i*2*dx +j*dx -2*dx 
                    pygame.draw.polygon(screen,color[a.cube["F"][i][j]],rhombus(rx,ry,1))
                    pygame.draw.polygon(screen,(0,0,0),rhombus(rx,ry,1),2)
            for i in range (0,3):
                for j in range(0,3):
                    rx = midx + j*dy
                    ry = midy + i*2*dx - j*dx 
                    pygame.draw.polygon(screen,color[a.cube["R"][i][j]],rhombus(rx,ry,2))
                    pygame.draw.polygon(screen,(0,0,0),rhombus(rx,ry,2),2)
            
            
        pygame.display.flip()
        clock.tick(30)