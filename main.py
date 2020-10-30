from setup import *
from qpsolvers import solve_qp
#from oct2py import octave

#octave.addpath('~/Documentos/Ucosas/Control Predictivo/Control-Predictivo-Tarea1/')


if __name__ == '__main__':
    A = np.array([[0.8, 0, 0.2],
                  [0.5, 0.5, 0],
                  [0, 0, 0.5]])

    B = np.array([[1],
                  [0],
                  [0]])
    N = 7

    x_0 = np.array([[0],
                    [0],
                    [0.5]])

    x_eq = np.array([[2.5],
                     [2.5],
                     [0]])

    u_0 = 0
    u_eq = 0.5

    Q = np.array([[1, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]])

    P = np.array([[1.0585, 0, 0.0151],
                  [0, 0, 0],
                  [0.0151, 0, 0.0052]])

    R_1 = 0.1
    R_2 = 0.1

    F = np.zeros((3, 3))
    G = np.zeros((3, 1))

    H_modelo = np.concatenate((np.identity(3), -np.identity(3)), axis=0)

    f_modelo = np.zeros((3, 1))
    g_modelo = np.zeros((3, 1))
    h_modelo = np.tile(0.2, (6, 1)) + np.matmul(H_modelo, x_eq)

    lb_xk = np.zeros((3, 1))
    ub_xk = 5*np.ones((3, 1))

    lb_uk = -1.5
    ub_uk = 1.5

    lb_duk = -0.5
    ub_duk = 0.5

    Hqp = Hqp(Q, P, R_1, R_2, N)
    f = f(Hqp)
    Aqp = Aqp(F, G, H_modelo, N)
    bqp = bqp(f_modelo, g_modelo, h_modelo, N)
    Aeq = Aeq(A, B, N)
    beq = beq(x_0, Aeq)
    lb = lb(lb_xk, lb_uk, lb_duk, N)
    ub = ub(ub_xk, ub_uk, ub_duk, N)

    # Implementacion de lazo de control

    uk = np.array([u_0])
    xk = x_0
    iteraciones = 100
    #solucion = octave.quadprog(Hqp, f, Aqp, bqp, Aeq, beq, lb, ub)
    #solucion2 = octave.quadprog(Hqp, f, Aqp, bqp, Aeq, beq, lb, ub)
    f = np.double(f)
    for i in range(iteraciones):
        solucion = solve_qp(Hqp, f, Aqp, bqp, Aeq, beq, lb, ub, solver='cvxopt')
        uk_1 = np.array([solucion[((N+1)*np.shape(x_eq)[0]+1)]])
        uk = np.concatenate((uk, uk_1), axis=0)
        xk_1 = np.matmul(A, np.row_stack(np.take(xk, [0, 1, 2]))) + B*uk_1
        xk = np.concatenate((xk_1, xk), axis=0)
        beq = np.delete(beq, [0, 1, 2])
        beq = np.reshape(beq, (np.shape(beq)[0], 1))
        beq = np.concatenate((xk_1, beq), axis=0)


