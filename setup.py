import numpy as np

# Funcion que crea la matriz Aeq a utilizar en quadProg
# A es una matriz cuadrada de (NxN)
# B es un vector de (Nx1)
# N es numero de pasos en el futuro a considerar
def Aeq(A, B, N):
    # Se consigue el tamaño de las matrices
    size_A = np.shape(A)[0]
    size_B = np.shape(B)[0]

    # Creación de matrices
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
    return Aeq

# Funcion que crea la matriz de H a utilizar en quadProg
# Q es una matriz cuadrada de (NxN)
# P es una matriz cuadrada de (NxN)
# R es un vector de (Mx1) donde en cada fila se guarda el valor R_i
def Hqp(Q, P, R):

    # Se consigue el tamaño de las matrices
    size_Q = np.shape(Q)[0]
    size_P = np.shape(P)[0]
    size_R = np.shape(R)[0]



    return
