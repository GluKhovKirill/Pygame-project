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
            if not i%5:
                self.c.append([750, i // 5 * (-750)])
            else:
                self.c.append([(i%5)*750,i//5*(-750)])
        return self.c
    def trans(self, c):
        c_append = []
        total = []
        total1 = []
        v = 0
        Flag = True
        for n in c:
            x = n[0]
            y = n[1]
            for i in range(16):
                for k in range(16):

                    if y == n[1] or y == n[1] - 700 or (x == n[0]) or (x == n[0] + 700):
                        if (x == n[0]+700 and y == n[1] - 350 or x == n[0]+700 and y == n[1] - 300 or x == n[0]+700 and y == n[1] - 400) or y == n[1]-700 and x == n[0] + 350 or y == n[1]-700 and x == n[0] + 300 or y == n[1]-700 and x == n[0] + 400:
                            c_append.append([x, y, "grass"])
                        elif v > 0:
                            print(n[0] > c[v-1][0] and (x == n[0] and y == n[1] - 350), x, y, 1, n[0], c[v-1][0])
                            print(n[1] < c[v-1][1] and (y == n[1] and x == n[0] + 350), x, y, 2, n[1], c[v-1][1])
                            if n[0] > c[v-1][0] and (x == n[0] and y == n[1] - 350 or x == n[0] and y == n[1] - 300 or x == n[0] and y == n[1] - 400) or n[1] < c[v-1][1] and (y == n[1] and (x == n[0] + 350 or x == n[0] + 300 or x == n[0] + 400)):
                                c_append.append([x, y, "grass"])
                            else:
                                c_append.append([x, y, "wall"])
                        else:
                            c_append.append([x, y, "wall"])


                    else:
                        if Flag:
                            c_append.append([x, y, "player"])
                            Flag = False
                        else:
                            c_append.append([x, y, random.choice(["grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","grass","hole","wall"])])
                    if x != n[0]+700:
                        x += 50
                    else:
                        x = n[0]
                total.append(c_append)
                c_append = []
                if y != n[1]-700:
                    y -= 50
            v += 1
            total1.append(total)
            total = []
        return total1


for i in Transform().Transformer():
    print(i)


