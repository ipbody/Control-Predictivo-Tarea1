import numpy as np

# Funcion que crea la matriz de H a utilizar en quadProg
# Q es una matriz cuadrada de (NxN)
# P es una matriz cuadrada de (NxN)
# R_i valor asociado a u
# N es el horizonte de prediccion
def Hqp(Q, P, R_1, R_2, N):

    # Se consigue el tamano de las matrices
    size_Q = np.shape(Q)[0]
    size_P = np.shape(P)[0]

    # Matriz de ceros de (NxN)
    zeros_matriz = np.zeros((size_Q, size_Q))
    zeros_columna = np.zeros((size_Q, 1))
    zeros_fila = np.zeros((1 ,size_Q))

    # Crear parte Q de la matriz H
    H_q = 0
    for i in range(N):
        zeros_izq = np.tile(zeros_matriz, i)
        zeros_der = np.tile(zeros_matriz, N-i)
        fila = np.concatenate((zeros_izq, Q, zeros_der), axis=1)
        if (np.isscalar(H_q)):
            H_q = fila
        else:
            H_q = np.concatenate((H_q, fila), axis=0)

    # Extender H_q para incluir matriz P

    H_p = np.concatenate((np.tile(zeros_matriz, N), P), axis=1)
    H_qp = np.concatenate((H_q, H_p), axis=0)

    # Extender H_qp para incluir R_1 y R_2
    # R_1
    for i in range(N):
        columna = np.tile(np.array([[0]]), (np.shape(H_qp)[0], 1))
        H_qp = np.concatenate((H_qp, columna), axis=1)
        fila_zeros = np.tile(np.array([[0]]), (1, np.shape(H_qp)[0]))
        fila = np.concatenate((fila_zeros, np.array([[R_1]])), axis=1)
        H_qp = np.concatenate((H_qp, fila), axis=0)

    # R_2
    for i in range(N):
        columna = np.tile(np.array([[0]]), (np.shape(H_qp)[0], 1))
        H_qp = np.concatenate((H_qp, columna), axis=1)
        fila_zeros = np.tile(np.array([[0]]), (1, np.shape(H_qp)[0]))
        fila = np.concatenate((fila_zeros, np.array([[R_2]])), axis=1)
        H_qp = np.concatenate((H_qp, fila), axis=0)
    H_qp = 2*H_qp
    return H_qp

# Funcion que crea el vector f a utilizar en quadProg
# Hqp es la matriz H a ingresar en quadProg
def f(Hqp):
    tamano = np.shape(Hqp)[0]
    f = np.tile(np.array([[0]]), (tamano, 1))
    return f

# Funcion que crea la matriz A a ingresar en quadProg
def Aqp(F, G, H, N):

    # Se consigue el tamano de las matrices
    size_F = np.shape(F)[0]
    size_G= np.shape(G)[0]
    size_H = np.shape(H)

    # Matriz de ceros de (NxN)
    zeros_matriz = np.zeros((size_F, size_F))
    zeros_matriz_H = np.zeros(size_H)
    zeros_columna = np.zeros((size_F, 1))
    zeros_fila = np.zeros((1 ,size_F))

    # Crear parte Fde la matriz Aqp
    A_f = 0
    for i in range(N):
        zeros_izq = np.tile(zeros_matriz, i)
        zeros_der = np.tile(zeros_matriz, N-i)
        fila = np.concatenate((zeros_izq, F, zeros_der), axis=1)
        if (np.isscalar(A_f)):
            A_f = fila
        else:
            A_f = np.concatenate((A_f, fila), axis=0)

    # Extender A_f para incluir matriz H

    A_h = np.concatenate((np.tile(zeros_matriz_H, N), H), axis=1)
    A_fh = np.concatenate((A_f, A_h), axis=0)

    # Extender A_fh para incluir G
    for i in range(N):
        columna = np.tile(np.array([[0]]), (np.shape(A_fh)[0], 1))
        A_fh = np.concatenate((A_fh, columna), axis=1)
        fila_zeros = np.tile(zeros_columna, (1, np.shape(A_fh)[1]-1))
        fila = np.concatenate((fila_zeros, G), axis=1)
        A_fh = np.concatenate((A_fh, fila), axis=0)
        columna_zeros = np.tile(np.array([[0]]), (np.shape(A_fh)[0], 1))
        A_fh = np.concatenate((A_fh, columna_zeros), axis=1)

    # Agregar ceros para condiciones de duk
    # for i in range(N):
    #     columna = np.tile(np.array([[0]]), (np.shape(A_fh)[0], 1))
    #     A_fh = np.concatenate((A_fh, columna), axis=1)

    return A_fh

# Funcion que crea el vector b a utilizar en quadProg
# f, g, h son vectores columna
def bqp(f, g, h, N):
    f = np.tile(f, (N, 1))
    g = np.tile(g, (N, 1))
    bqp = np.concatenate((f, h, g), axis=0)
    return bqp

# Funcion que crea la matriz Aeq a utilizar en quadProg
# A es una matriz cuadrada de (NxN)
# B es un vector de (Nx1)
# N es el horizonte de prediccion
def Aeq(A, B, N):
    # Se consigue el tamano de las matrices
    size_A = np.shape(A)[0]
    size_B = np.shape(B)[0]

    # Creacion de matrices
    I = np.identity(size_A)

    zeros_matrix = np.zeros((size_A, size_A))
    zeros_vector = np.zeros((size_B, 1))

    # Primera mitad de la matriz Aeq
    Aeq_izquierda = np.concatenate((I, zeros_matrix), axis=1)
    Aeq_izquierda = np.concatenate((Aeq_izquierda, np.concatenate((A, -I), axis=1)), axis=0)

    for i in range(N - 1):
        fila = np.concatenate((np.tile(zeros_matrix, i + 1), A), axis=1)
        columna = np.concatenate((np.tile(zeros_matrix, (i + 2, 1)), -I))
        Aeq_izquierda = np.concatenate((Aeq_izquierda, fila), axis=0)
        Aeq_izquierda = np.concatenate((Aeq_izquierda, columna), axis=1)

    # Segunda mitad de la matriz Aeq
    Aeq_derecha = np.concatenate((zeros_vector, B), axis=0)

    for i in range(N - 1):
        fila = np.tile(zeros_vector, i + 1)
        columna = np.concatenate((np.tile(zeros_vector, (i + 2, 1)), B), axis=0)
        Aeq_derecha = np.concatenate((Aeq_derecha, fila), axis=0)
        Aeq_derecha = np.concatenate((Aeq_derecha, columna), axis=1)

    # Se crea la matriz completa
    Aeq = np.concatenate((Aeq_izquierda, Aeq_derecha), axis=1)

    # Extension de Aeq para considerar duk

    columna = np.tile(zeros_vector, (N+1, N))
    Aeq = np.concatenate((Aeq, columna), axis=1)

    fila_izq = np.tile(np.transpose(zeros_vector), N+1)
    fila_cent = np.array([[-1, 1]])
    fila_der = np.tile(np.array([[0]]), 2*N-2)
    fila = np.concatenate((fila_izq, fila_cent, fila_der), axis=1)
    Aeq = np.concatenate((Aeq, fila), axis=0)

    # Iteracion para horizonte N
    for i in range(N-1):
        zeros_izq = np.tile(np.transpose(zeros_vector), N+1)
        zeros_cent = np.tile(np.array([[0]]), 2*i)
        seq = np.array([[1, 0, -1, 1]])
        pre_fila = np.concatenate((zeros_izq, zeros_cent, seq), axis=1)
        zeros_der = np.tile(np.array([[0]]), np.shape(Aeq)[1] - np.shape(pre_fila)[1])
        fila = np.concatenate((pre_fila, zeros_der), axis=1)
        Aeq = np.concatenate((Aeq, fila), axis=0)

    return Aeq

# Funcion que crea el vector beq a utilizar en quadProg
def beq(x_eq, Aeq):
    columna_zeros = np.tile(np.array([[0]]), (np.shape(Aeq)[0]-np.shape(x_eq)[0], 1))
    beq = np.concatenate((x_eq, columna_zeros), axis=0)
    return beq

# Funcion que crea lb a utilizar en quadProg
def lb(lb_xk, lb_uk, lb_duk, N):
    xk = np.tile(lb_xk, (N+1, 1))
    uk = np.tile(lb_uk, (N, 1))
    duk = np.tile(lb_duk, (N, 1))
    lb = np.concatenate((xk, uk, duk), axis=0)
    return lb

# Funcion que crea ub a utilizar en quadProg
def ub(ub_xk, ub_uk, ub_duk, N):
    xk = np.tile(ub_xk, (N+1, 1))
    uk = np.tile(ub_uk, (N, 1))
    duk = np.tile(ub_duk, (N, 1))
    ub = np.concatenate((xk, uk, duk), axis=0)
    return ub



