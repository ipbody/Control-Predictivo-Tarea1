from setup import *

if __name__ == '__main__':
    A = np.array([[0.8, 0, 0.2],
                  [0.5, 0.5, 0],
                  [0, 0, 0.5]])

    B = np.array([[1],
                  [0],
                  [0]])
    N = 2
    Aeq = Aeq(A, B, N)
    print(Aeq)
