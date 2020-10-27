import numpy as np

def test():
    x = 0
    for i in range(7):
        x += 1
    print(x)


x = np.array([[0, 0],
              [1, 0],
              [1, 1]])
print(x[1,0])