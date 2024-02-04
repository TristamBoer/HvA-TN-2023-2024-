import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
print("Opdracht 1")
# =============================================================================

def opdracht1(N):
    MATRIX1 = np.zeros((N, N))  # Maak een NxN array met nullen
    for i in range(N):  # Loop over de rijen i van de matrix
        if i % 2 == 0:  # Controleer of i een heel getal is
            for j in range(N):  # Loop over de kolommen j van de matrix
                if j % 2 == 0 and i == j:  # Controleer of j een heel getal is en gelijk staat aan i
                    MATRIX1[i:, j] = 1  # Stel alle elementen in rij i na (inclusief i) en kolom j in op 1
                    MATRIX1[i, j:] = 1  # Stel alle elementen in rij i en na (inclusief j) in op 1
    print(MATRIX1, end='\n\n')
    return MATRIX1

N = 10
opdracht1(N)

N = 5
opdracht1(N)

# =============================================================================
print("Opdracht 2")
# =============================================================================

def opdracht2(M, N):
    MATRIX2 = np.random.randint(0, 1000, size=(M, N))  # Maak een MxN matrix met willekeurige ints van 0 tot 999
    MATRIX3 = np.amax(MATRIX2, axis=1)  # Maak een nieuwe matrix met het maxima van elke rij uit MATRIX2
    print(MATRIX2, end='\n\n')
    print(MATRIX3, end='\n\n')
    return MATRIX3


M = 5
N = 3
opdracht2(M, N)

M = 10
N = 4
opdracht2(M, N)

# =============================================================================
print("Opdracht 3")
# =============================================================================

def opdracht3(M, N, x):
    MATRIX4 = np.random.randint(0, 50, size=(M, N))  # Maak een MxN matrix aan gevuld met willekeurige ints van 0 tot 49
    MATRIX5 = MATRIX4  # Maakt een nieuwe matrix die hetzelfde is als MATRIX4

    for i in range(0, x, 1):  # Voeg MATRIX4 x aantal keer toe aan MATRIX5
        MATRIX5 = np.append(MATRIX5, MATRIX4, axis=1)  # Horizontaal toevoegen van MATRIX4 aan MATRIX5
    print(MATRIX5, end='\n\n')
    return MATRIX5


M = 4
N = 3
x = 3
opdracht3(M, N, x)

M = 4
N = 3
x = 6
opdracht3(M, N, x)

# =============================================================================
print("Opdracht 4")
# =============================================================================

def opdracht4(M, N):
    MATRIX6 = np.random.randint(0, 50, size=(M, N))  # Maak een MxN matrix met willekeurige ints van 0 tot 49
    MATRIX7 = np.fliplr(MATRIX6)  # Maak een nieuwe matrix die een spiegelbeeld is van MATRIX6
    print(MATRIX6, end='\n\n')
    print(MATRIX7, end='\n\n')
    return MATRIX7


M = 4
N = 3
opdracht4(M, N)

M = 2
N = 6
opdracht4(M, N)

# =============================================================================
print("Opdracht 5")
# =============================================================================

def opdracht5(M, N):
    MATRIX8 = np.random.randint(1, 50, size=(M, N))  # Maak een MxN matrix met willekeurige ints van 1 tot 49
    print(MATRIX8, end='\n\n')
    MATRIX8[MATRIX8 < 10] = 10  # Verander alle waarden kleiner dan 10 naar 10 in de matrix
    MATRIX8[MATRIX8 > 30] = 30  # Verander alle waarden groter dan 30 naar 30 in de matrix
    print(MATRIX8, end='\n\n')
    return MATRIX8


M = 6
N = 4
opdracht5(M, N)

M = 10
N = 6
opdracht5(M, N)

# =============================================================================
print("Opdracht 6")
# =============================================================================
# 6a
THETA = np.array([0.88, 1.10, 1.42, 1.77, 2.14])
R = np.array([3.0, 2.3, 1.65, 1.25, 1.01])
VECTOR = np.ones_like(THETA)
R_COS = R * np.cos(THETA)

A = np.array([VECTOR, R_COS])
A = A.transpose()
x = np.linalg.solve(A.transpose() @ A, A.transpose() @ R)
[BETA, EPSILON] = x
THETA_X = np.linspace(0.88, 2.14, num=100)
r = BETA / (1 - EPSILON * np.cos(THETA_X))
THETA1 = 4.6

print('Afstand =', (BETA / (1 - EPSILON * np.cos(THETA1))), 'miljoenen km', end='\n\n')

# 6b
plt.plot(THETA_X, r, color='red')
plt.scatter(THETA, R)
plt.xlabel('Hoek theta [rad]')
plt.ylabel('Afstand r [miljoenen km]')
plt.title("Opdracht 6")
plt.grid()
plt.show()

# =============================================================================
print("Opdracht 7")
# =============================================================================
# 7a
GEWICHT = np.array([22, 30, 40, 56, 65])
BLOEDDRUK = np.array([91, 98, 103, 110, 112])
VECTOR = np.ones_like(GEWICHT)
LN_W = np.log(GEWICHT)

A = np.array([VECTOR, LN_W])
A = A.transpose()
x = np.linalg.solve(A.transpose() @ A, A.transpose() @ BLOEDDRUK)
[BETA0, BETA1] = x
w = np.linspace(0.001, 65, 100)
p = BETA0 + BETA1 * np.log(w)
w1 = 50

print('Bloeddruk =', (BETA0 + BETA1 * np.log(w1)), 'mmHg', end='\n\n')

# 7b
plt.scatter(GEWICHT, BLOEDDRUK)
plt.plot(w, p, color='red')
plt.ylim(bottom=0)
plt.xlabel('Gewicht w [kg]')
plt.ylabel('Bloeddruk p [mmHg]')
plt.title("Opdracht 7")
plt.grid()
plt.show()


# =============================================================================
print("Opdracht 8")
# =============================================================================
# 8a
T = np.linspace(0, 12, num=12)
POSITIE = np.array([8.8, 29.9, 62.0, 104.7, 159.1, 222.0, 294.5, 380.4, 471.1, 571.7, 686.8, 809.2])
VECTOR = np.ones_like(T)

A = np.array([VECTOR, T, T ** 2, T ** 3])
A = A.transpose()
o = np.linalg.solve(A.transpose() @ A, A.transpose() @ POSITIE)
[BETA0, BETA1, BETA2, BETA3] = o
x = BETA0 + BETA1 * T + BETA2 * T ** 2 + BETA3 * T ** 3
T1 = 4.5

print('Horizontale positie =', (BETA0 + BETA1 * T1 + BETA2 * T1 ** 2 + BETA3 * T1 ** 3), 'feet', end='\n\n')

# 8b
plt.scatter(T, POSITIE)
plt.plot(T, x, color='red')
plt.xlabel('Tijd [s]')
plt.ylabel('feet')
plt.title("Opdracht 8")
plt.grid()
plt.show()

# =============================================================================
print("Opdracht 9")
# =============================================================================
# 9a
DATA = np.loadtxt('Data - spectra.txt')
GOLFLENGTE = DATA[:, 0]
SPECTRUM = DATA[:, 1]
a = DATA[:, 2]
b = DATA[:, 3]
c = DATA[:, 4]

A = np.array([a, b, c])
A = A.transpose()
x = np.linalg.solve(A.transpose() @ A, A.transpose() @ SPECTRUM)
[C1, C2, C3] = x
S = C1 * a + C2 * b + C3 * c

print('Concentratie A =', C1, 'mg/L')
print('Concentratie B =', C2, 'mg/L')
print('Concentratie C =', C3, 'mg/L')

# 9b
plt.plot(GOLFLENGTE, SPECTRUM)
plt.plot(GOLFLENGTE, S, color='red')
plt.xlabel('Golflengte [nm]')
plt.ylabel('Extinctie')
plt.title("Opdracht 9")
plt.grid()
plt.show()
