import random
class Transform():
    def __init__(self):
        self.dim_x = 5
        self.dim_y = 5
        self.c = []
        self.grid = [[0 for i in range(self.dim_x)] for j in range(self.dim_y)]
        self.visited = [1]
    
    def valid(self,nb):
        if nb >= 1 and nb <= self.dim_x * self.dim_y:
            return True
        return False
    
    def list_moves(self,nb):
        moves = []
        nb = int(nb)
        if self.valid(nb + self.dim_y) and self.visited.count(nb + self.dim_y) < 1:
            moves.append(nb + self.dim_y)
        if self.valid(nb - self.dim_y) and self.visited.count(nb - self.dim_y) < 1:
            moves.append(nb - self.dim_y)
        if self.valid(nb + 1) and self.visited.count(nb + 1) < 1 and nb % self.dim_x != 0:
            moves.append(nb + 1)
        if self.valid(nb - 1) and self.visited.count(nb - 1) < 1 and nb % self.dim_x != 1:
            moves.append(nb - 1)
        return moves
    
    def gen(self):
        pos = len(self.visited) - 1
        while len(self.list_moves(self.visited[pos])) < 1:
            pos -= 1
        next_visit = random.choice(self.list_moves(self.visited[pos]))
        self.visited.append(next_visit)
    def generator(self):
        while len(self.visited) != self.dim_x * self.dim_y:
            self.gen()
        return self.visited
    def Transformer(self):
        visit = self.generator()
        for i in self.visited:
            self.c.append([i%5*700,i//5*(-700)])
        return self.c
    def trans(self, c):
        c_append = []
        total = []
        total1 = []
        Flag = True
        for n in c:
            x = n[0]
            y = n[1]
            for i in range(15):
                for k in range(15):
                    if y == n[1] or y == n[1] - 700 or (x == n[0]) or (x == n[0] + 700):
                        c_append.append([x, y, "wall"])
                    else:
                        if Flag:
                            c_append.append([x, y, "player"])
                            Flag = False
                        else:
                            c_append.append([x, y, random.choice(["grass","hole","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","wall"])])
                    if x != n[0]+700:
                        x += 50
                    else:
                        x = n[0]
                total.append(c_append)
                c_append = []
                if y != n[1]-700:
                    y -= 50
            total1.append(total)
            total = []
        return total1


for i in Transform().Transformer():
    print(i)


