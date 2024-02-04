import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Opdracht 1
# =============================================================================

WACHTTIJDEN = np.loadtxt('Wachttijden.txt')

plt.hist(WACHTTIJDEN, edgecolor='black', bins=np.arange(min(WACHTTIJDEN), max(WACHTTIJDEN)+0.01, step=5))
plt.xlabel('Wachtijden [min]')
plt.ylabel('Aantal')
plt.title("Wachttijden histogram")
plt.show()

plt.hist(WACHTTIJDEN, bins=np.arange(min(WACHTTIJDEN), max(WACHTTIJDEN)+0.01, step=0.2))
plt.xlabel('Wachtijden [min]')
plt.ylabel('Aantal')
plt.title("Wachttijden histogram")
plt.show()

plt.hist(WACHTTIJDEN, edgecolor='black', bins=np.arange(min(WACHTTIJDEN), max(WACHTTIJDEN)+0.01, step=2))
plt.xlabel('Wachtijden [min]')
plt.ylabel('Aantal')
plt.title("Wachttijden histogram")
plt.show()

plt.hist(WACHTTIJDEN, color='tomato', edgecolor='darkgreen', bins=np.arange(min(WACHTTIJDEN), max(WACHTTIJDEN)+0.01, step=2))
plt.xlabel('Wachtijden [min]')
plt.ylabel('Aantal')
plt.title("Wachttijden histogram")
plt.show()

plt.hist(WACHTTIJDEN, color='tomato', density=True, edgecolor='darkgreen', bins=np.arange(min(WACHTTIJDEN), max(WACHTTIJDEN)+0.01, step=2))
plt.xlabel('Wachtijden [min]')
plt.ylabel('Kansdichtheid (Kans/wachtijd)')
plt.title("Wachttijden histogram")
plt.show()

# =============================================================================
# Opdracht 2
# =============================================================================

MU = 12.10
SIGMA = 0.17
P = 10000000
RAN_NUMBERS = MU + SIGMA * np.random.randn(P)

STEEKPROEF = MU + SIGMA * np.random.randn(50,9)
GEM_STEEKPROEF = STEEKPROEF.mean(axis = 1)

plt.hist(RAN_NUMBERS, color='red', edgecolor='black', bins=np.arange(min(RAN_NUMBERS), max(RAN_NUMBERS)+0.01, step=0.02))
plt.xlabel('Verbruik [mL]')
plt.ylabel('Popualtie Aantal')
plt.title("Populatieverdeling")
plt.show()

plt.hist(GEM_STEEKPROEF, color='aqua', edgecolor='black', bins=np.arange(min(RAN_NUMBERS), max(RAN_NUMBERS)+0.01, step=0.02))
plt.xlabel('Verbruik [mL]')
plt.ylabel('Steekproef gemiddelde')
plt.title("Steekproef gemiddelde verdeling")
plt.show()

# Maken van een dualplot
fig, ax1 = plt.subplots()
ax1.set_xlabel('Verbruik [mL]')
ax1.set_ylabel('Populatie Aantal', color='red')
ax1.hist(RAN_NUMBERS, color='red', edgecolor='black', alpha=0.7, bins=np.arange(min(RAN_NUMBERS), max(RAN_NUMBERS)+0.01, step=0.02))
ax1.tick_params(axis='y', labelcolor='tab:red')
ax2 = ax1.twinx()  
ax2.set_ylabel('Steekproef gemiddelde', color='cyan')
ax2.hist(GEM_STEEKPROEF, color='cyan', edgecolor='black', alpha=1, bins=np.arange(min(GEM_STEEKPROEF), max(GEM_STEEKPROEF)+0.01, step=0.02))
ax2.tick_params(axis='y', labelcolor='cyan')
plt.title("Populatieverdeling met steekproef gemiddelde")
fig.tight_layout()  
plt.grid()
plt.show()

STANDAARDEVIATIE = np.std(RAN_NUMBERS)
STEEKPROEFSTANDAARDDEVIATIE = np.std(GEM_STEEKPROEF, ddof=1)

# print(STANDAARDEVIATIE) 
# print(STEEKPROEFSTANDAARDDEVIATIE)
# print(STANDAARDEVIATIE / STEEKPROEFSTANDAARDDEVIATIE)

# =============================================================================
# Opdracht 3
# =============================================================================

MU = 180
SIGMA = 6
P = 1000000
LENGTE_MANNEN = MU + SIGMA * np.random.randn(P)

STEEKPROEF = MU + SIGMA * np.random.randn(9,9)
STEEKPROEFSTANDAARDDEVIATIE = np.std(STEEKPROEF, axis=1, ddof=1)

# print('Kleinste steekproef stdv =', min(STEEKPROEFSTANDAARDDEVIATIE))
# print('Grootste steekproef stdv =', max(STEEKPROEFSTANDAARDDEVIATIE))

plt.hist(LENGTE_MANNEN, color='aqua', edgecolor='black', alpha=1, bins=np.arange(min(LENGTE_MANNEN), max(LENGTE_MANNEN)+0.01, step=0.5))
plt.xlabel('lengte [cm]')
plt.ylabel('Aantal')
plt.title("Populatie: alle Nederlandse mannen (lengte)")
plt.xlim([160, 200])
plt.show()

plt.hist(STEEKPROEFSTANDAARDDEVIATIE, color='orange', edgecolor='black', alpha=1, bins=np.arange(min(STEEKPROEFSTANDAARDDEVIATIE), max(STEEKPROEFSTANDAARDDEVIATIE)+0.01, step=0.025))
plt.xlabel('Standaardeviatie')
plt.title("Steekproef stdv: alle Nederlandse mannen (lengte) met N = 9")
plt.show()

STEEKPROEF = MU + SIGMA * np.random.randn(5,9)
STEEKPROEFSTANDAARDDEVIATIE = np.std(STEEKPROEF, axis=1, ddof=1)

plt.hist(STEEKPROEFSTANDAARDDEVIATIE, color='orange', edgecolor='black', alpha=1, bins=np.arange(min(STEEKPROEFSTANDAARDDEVIATIE), max(STEEKPROEFSTANDAARDDEVIATIE)+0.01, step=0.025))
plt.xlabel('Standaardeviatie')
plt.title("Steekproef stdv: alle Nederlandse mannen (lengte) met N = 5")
plt.show()

STEEKPROEF = MU + SIGMA * np.random.randn(50,9)
STEEKPROEFSTANDAARDDEVIATIE = np.std(STEEKPROEF, axis=1, ddof=1)

plt.hist(STEEKPROEFSTANDAARDDEVIATIE, color='orange', edgecolor='black', alpha=1, bins=np.arange(min(STEEKPROEFSTANDAARDDEVIATIE), max(STEEKPROEFSTANDAARDDEVIATIE)+0.01, step=0.025))
plt.xlabel('Standaardeviatie')
plt.title("Steekproef stdv: alle Nederlandse mannen (lengte) met N = 50")
plt.show()

P = 25
LENGTE_MANNEN = MU + SIGMA * np.random.randn(P, 2)

STEEKPROEF = MU + SIGMA * np.random.randn(25,9)
STEEKPROEFSTANDAARDDEVIATIE = np.std(STEEKPROEF, axis=1, ddof=1)
POPULATIESTANDAARDDEVIATIE = np.std(LENGTE_MANNEN, ddof=1)
POPULATIESTANDAARDDEVIATIE_2 = np.std(LENGTE_MANNEN, axis=1, ddof=1)

# Maken van een dualplot
fig, ax1 = plt.subplots()
ax1.set_xlabel('Verbruik [mL]')
ax1.set_ylabel('Popualtie standaarddeviatie', color='aqua')
ax1.hist(POPULATIESTANDAARDDEVIATIE_2, color='aqua', edgecolor='aqua', alpha=1, bins=np.arange(min(POPULATIESTANDAARDDEVIATIE_2), max(POPULATIESTANDAARDDEVIATIE_2)+0.01, step=0.02))
ax1.tick_params(axis='y', labelcolor='aqua')
ax2 = ax1.twinx()  
ax2.set_ylabel('Steekproef standaarddeviatie', color='orange')
ax2.hist(STEEKPROEFSTANDAARDDEVIATIE, color='orange', edgecolor='orange', alpha=1, bins=np.arange(min(STEEKPROEFSTANDAARDDEVIATIE), max(STEEKPROEFSTANDAARDDEVIATIE)+0.01, step=0.02))
ax2.tick_params(axis='y', labelcolor='orange')
plt.title("Standaarddeviaties populatie en steekproef")
fig.tight_layout()  
plt.grid()
plt.show()

# print('stdv steekproef:', np.mean(STEEKPROEFSTANDAARDDEVIATIE))
# print('stdv populatie:', POPULATIESTANDAARDDEVIATIE)
# print('ratio:', np.mean(STEEKPROEFSTANDAARDDEVIATIE) / np.mean(POPULATIESTANDAARDDEVIATIE))