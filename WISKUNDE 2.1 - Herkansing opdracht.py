import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-dark')


def Opdracht_1(M, N):
    # Maken van een lege matrix
    matrix = np.zeros((M, N))

    # Patroon in matrix vullen
    for i in range(M):
        for j in range(N):
            matrix[i, j] = i + j
    return print(matrix, end='\n\n')

Opdracht_1(5, 8)



def Opdracht_2(M, N):
    matrix = np.zeros((M, N))

    for i in range(M):
        for j in range(N):
            matrix[i, j] = j

    for i in range(M):
        for j in range(i):
            matrix[i, j] = 0
    return print(matrix, end='\n\n')

Opdracht_2(6, 10)



def Opdracht_3(M, N):
    # Maken van matrix en verschillende vectoren
    matrix = np.zeros((M, N))
    vector1 = np.zeros(N)
    vector2 = np.zeros(N)

    # Elke oneven element veranderen van vector1
    for i in range(1, len(vector1), 2):
        vector1[i] = 1

    # Maken van patroon in matrix
    for i in range(M):
        if i % 3 == 0:
            matrix[i] = vector1
        else:
            matrix[i] = vector2
    return print(matrix, end='\n\n')

Opdracht_3(10, 12)
Opdracht_3(8, 6)



# Opdracht 4
# Inlezen data
data = np.loadtxt('slinger.txt')
lengte = np.array(data[:, 0])
slingertijd = np.array(data[:, 1])

# Uitvoeren kleinste kwadraten oplossing
A = np.array([lengte])
A = A.transpose()
[g] = np.linalg.solve(A.transpose() @ A, A.transpose() @ slingertijd)
g = 2*np.pi*np.sqrt(g)

# Maken fit vergelijking
x_data = np.linspace(0, lengte[-1], num=1000)
y_data = 2*np.pi*np.sqrt(x_data/g)

# Plotten data en fit
plt.scatter(lengte, slingertijd, color='tab:red', label='data')
plt.plot(x_data, y_data, color='blue', label='fit', alpha=0.8)
plt.xlabel('L [m]')
plt.ylabel('T [s]')
plt.title(f"Slingertijd bij verschillende slinger lengtes met g={round(g,2)}")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()



# Opdracht 5
# Inlezen data
data = np.loadtxt('temperatuur.txt')
tijd = data[:, 0]
temperatuur = data[:, 1]

# Bepalen vectoren
een_vector = np.ones_like(tijd)
sin_vector = np.sin(2*np.pi/24 * tijd)

# Uitvoeren kleinste kwadraten oplossing
A = np.array([een_vector, tijd, sin_vector])
A = A.transpose()
[A, B, C] = np.linalg.solve(A.transpose() @ A, A.transpose() @ temperatuur)

# Maken fit vergelijking
x_data = np.linspace(0, tijd[-1], num=1000)
y_data = A + B*x_data + C*np.sin(2*np.pi/24*x_data)

# Plotten data en fit
# plt.style.use('classic')
plt.scatter(tijd, temperatuur, color='tab:red', label='data')
plt.plot(x_data, y_data, color='blue', label='fit', alpha=0.8)
plt.xlabel('Tijd [uur]')
plt.ylabel('T [°C]')
plt.title(f"Temperatuur kamer waarbij A={round(A,2)}, B={round(B,2)} en C={round(C,2)}")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()



# Opdracht 6
# Inlezen data
data = np.loadtxt('geleidbaarheid.txt')
temperatuur = data[:, 0]
geleidbaarheid = data[:, 1]

# Uitvoeren kleinste kwadraten oplossing
A = np.array([temperatuur**-1, temperatuur**2])
A = A.transpose()
[c1, c2] = np.linalg.solve(A.transpose() @ A, A.transpose() @ (1/geleidbaarheid))

# Maken fit vergelijking
x_data = np.linspace(0.001, temperatuur[-1], num=1000)
y_data = 1/(c1/x_data + c2*x_data**2)

# Plotten data en fit
# plt.style.use('dark_background')
plt.scatter(temperatuur, geleidbaarheid, color='tab:red', label='data')
plt.plot(x_data, y_data, color='blue', label='fit', alpha=0.8)
plt.xlabel('T [K]')
plt.ylabel('σ [S/m]')
plt.title(f"Geleidbaarheid bij verschillende temperaturen met c1={round(c1, 2)} en c2={round(c2, 5)}")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()