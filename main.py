from setup import *
from qpsolvers import solve_qp



if __name__ == '__main__':
    A = np.array([[0.8, 0, 0.2],
                  [0.5, 0.5, 0],
                  [0, 0, 0.5]])

    B = np.array([[1],
                  [0],
                  [0]])
    N = 7
    Aeq = Aeq(A, B, N)
#from numpy import array, dot
#from qpsolvers import solve_qp

# if __name__ == '__main__':
#     M = array([[1., 2., 0.], [-8., 3., 2.], [0., 1., 1.]])
#     P = dot(M.T, M)  # quick way to build a symmetric matrix
#     q = dot(array([3., 2., 3.]), M).reshape((3,))
#     G = array([[1., 2., 1.], [2., 0., 1.], [-1., 2., -1.]])
#     h = array([3., 2., -2.]).reshape((3,))
#     A = array([1., 1., 1.])
#     b = array([1.])
#
#     x = solve_qp(P, q, G, h, A, b)
#     print("QP solution: x = {}".format(x))