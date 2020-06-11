class Ant:
    def __init__(self, x, y, dx, dy, size):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = 2 * size

    def update_xy(self):
        self.x += self.dx
        self.y += self.dy
