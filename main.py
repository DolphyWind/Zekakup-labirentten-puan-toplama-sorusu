"""
Her sayıyı en fazla bir kez kullanmak koşulu ile bir sayı turu yapacaksınız.
Dilediğiniz kareden başlayarak sağ, sol, aşağı ya da yukarı yönde hareket edebilirsiniz.
Turu başladığınız karede bitireceksiniz.
Hedef tur boyunca kullandığınız sayıların toplamının maksimum olması.

    {9,  13, 15, 7,  15},
    {8,  8,  15, 5,  8},
    {13, 13, 12, 7,  10},
    {9,  11, 10, 6,  12},
    {7,  9,  5,  14, 14}
"""

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

matrix = [
    [-1, -1, -1, -1, -1, -1, -1],
    [-1, 9,  13, 15, 7,  15, -1],
    [-1, 8,  8,  15, 5,  8,  -1],
    [-1, 13, 13, 12, 7,  10, -1],
    [-1, 9,  11, 10, 6,  12, -1],
    [-1, 7,  9,  5,  14, 14, -1],
    [-1, -1, -1, -1, -1, -1, -1],
]

sumList = []
pathList = []

debug_messages = False

class MemoryCell:
    def __init__(self, pos: list, previouslySeen: set, cameFrom: int, possibleToGo: list, sumOfNumbers: int):
        self.pos = pos
        self.previouslySeen = previouslySeen
        self.cameFrom = cameFrom
        self.possibleToGo = possibleToGo
        self.sumOfNumbers = sumOfNumbers


    def printDebugMessage(self):
        print(f"pos: {self.pos}\n"
              f"previouslySeen: {self.previouslySeen}\n"
              f"cameFrom: {self.cameFrom}\n"
              f"possibleToGo: {self.possibleToGo}\n"
              f"sumOfNumbers: {self.sumOfNumbers}\n")

class Traveller:
    def __init__(self):
        self.memory = []
        self.startingPos = []

    # İlk adımı at
    def start(self, pos: list):
        self.startingPos = pos.copy()
        x = pos[0]
        y = pos[1]
        m = MemoryCell(pos.copy(), {-1, matrix[y][x]}, -1, [], matrix[y][x])
        m.possibleToGo = self.calcPossibleToGo(m)
        if debug_messages:
            m.printDebugMessage()
        self.memory.append(m)

        self.travel()

    # Bir önceki adımın pozisyonu
    def getPreviousPos(self, m: MemoryCell):
        p = m.pos
        x = p[0]
        y = p[1]
        cameFrom = m.cameFrom

        if cameFrom == UP: # Yukarı
            y -= 1
        elif cameFrom == LEFT: # Sol
            x -= 1
        elif cameFrom == DOWN: # Aşağı
            y += 1
        elif cameFrom == RIGHT: # Sağ
            x += 1
        return [x,y]

    def canGoStartingPos(self, m: MemoryCell):
        x = m.pos[0]
        y = m.pos[1]
        if x == self.startingPos[0] and y - 1 == self.startingPos[1] and m.cameFrom != UP:
            return True
        if x - 1 == self.startingPos[0] and y == self.startingPos[1] and m.cameFrom != LEFT:
            return True
        if x == self.startingPos[0] and y + 1 == self.startingPos[1] and m.cameFrom != DOWN:
            return True
        if x + 1 == self.startingPos[0] and y == self.startingPos[1] and m.cameFrom != RIGHT:
            return True
        return False

    # Son hafıza hücresini kullanarak ilerle
    def travel(self):
        # Eğer hafıza hücresi kalmadıysa imkansızdır
        if len(self.memory) == 0:
            if debug_messages:
                print(f"{self.startingPos} noktasından sonuç bulmak imkansız")

        m = self.memory[-1]
        if self.canGoStartingPos(m):
            if debug_messages:
                print(f"{self.startingPos} noktasından başlayarak bir sonuç bulundu! Toplamlar: {m.sumOfNumbers}")
            pos_list = []
            for q in self.memory:
                pos_list.append(q.pos)

            sumList.append(m.sumOfNumbers)
            pathList.append(pos_list)
        if len(m.possibleToGo) == 0:
            self.memory.pop()
        else:
            self.goToDirection(m, m.possibleToGo[0])
        if debug_messages:
            self.memory[-1].printDebugMessage()

    def goToDirection(self, m: MemoryCell, dir: int):
        m.possibleToGo.remove(dir)
        p = m.pos
        x = p[0]
        y = p[1]

        new_sum = m.sumOfNumbers
        new_cameFrom = 0
        new_prevSeen = m.previouslySeen.copy()

        if dir == UP:    # Yukarı
            y -= 1
            new_cameFrom = DOWN
        elif dir == LEFT:  # Sol
            x -= 1
            new_cameFrom = RIGHT
        elif dir == DOWN:  # Aşağı
            y += 1
            new_cameFrom = UP
        elif dir == RIGHT:  # Sağ
            x += 1
            new_cameFrom = LEFT

        new_p = [x,y]

        new_prevSeen.add(matrix[y][x])
        new_sum += matrix[y][x]

        m2 = MemoryCell(new_p, new_prevSeen, new_cameFrom, [], new_sum)
        m2.possibleToGo = self.calcPossibleToGo(m2)
        self.memory.append(m2)

    # Gidilbilecek yerleri hesapla
    def calcPossibleToGo(self, m: MemoryCell):
        x = m.pos[0]
        y = m.pos[1]
        ptg = []

        # Yukarıyı kontrol et
        if matrix[y - 1][x] not in m.previouslySeen:
            ptg.append(UP)
        # Solu kontrol et
        if matrix[y][x - 1] not in m.previouslySeen:
            ptg.append(LEFT)
        # Aşağıyı kontrol et
        if matrix[y + 1][x] not in m.previouslySeen:
            ptg.append(DOWN)
        # Sağı kontrol et
        if matrix[y][x + 1] not in m.previouslySeen:
            ptg.append(RIGHT)
        return ptg



def main():
    for y in range(1, 6):
        for x in range(1, 6):
            t = Traveller()
            t.start([x, y])
            temp = True
            while temp:
                try:
                    t.travel()
                except:
                    temp = False
    maxVal = max(sumList)
    for i in range(len(sumList)):
        if sumList[i] == maxVal:
            print(pathList[i])
    print("Max:", maxVal)

if __name__ == '__main__':
    main()

