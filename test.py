import random

class Tst(object):
    def __init__(self):
        self.smart_range = [random.choice(self.smart_x), random.choice(self.smart_y)]

    def check_hit(self, x, y):
        smart_x = range(x-1, x+2)
        smart_y = range(y-1, y+2)
        return self.smart_range

if __name__ == '__main__':
    tst = Tst()