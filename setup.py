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

    # Extensión de Aeq para considerar duk
    columna = np.tile(zeros_vector, (N+1, N))
    Aeq = np.concatenate((Aeq, columna), axis=1)
    vector_aux1 = np.tile(np.transpose(zeros_vector), N+1)
    vector_aux2 = np.array([[-1, 0, 1, 0]])
    fila = np.concatenate((vector_aux1, vector_aux2), axis=1)
    print(Aeq)
    Aeq = np.concatenate((Aeq, fila), axis=0)


    return Aeq

# Funcion que crea la matriz de H a utilizar en quadProg
# Q es una matriz cuadrada de (NxN)
# P es una matriz cuadrada de (NxN)
# R_i valor asociado a u

def Hqp(Q, P, R_1, R_2):


    # Se consigue el tamaño de las matrices
    size_Q = np.shape(Q)[0]
    size_P = np.shape(P)[0]
    size_R = np.shape(R)[0]

    # Matriz de ceros de (NxN)
    zeros_matriz = np.zeros(size_Q, size_Q)





    return
