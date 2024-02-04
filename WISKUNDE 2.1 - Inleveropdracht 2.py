import numpy as np
from scipy import stats as stats

# =============================================================================
# Opdracht 2
# =============================================================================

# Significantieniveau
ALPHA = 0.05

# Meetresultaten steekproef
STEEKPROEF = np.array([50.4, 50.7, 49.1, 49, 51.1])

MU = np.mean(STEEKPROEF)
S = np.std(STEEKPROEF, ddof=1)
X = 50
N = 5
VRIJHEIDSGRADEN = N - 1

# Berekenen toetsingsgrootheid en kritische waarde
T = (np.abs(X - MU) * np.sqrt(N)) / S
T_KR = stats.t.ppf(1-ALPHA/2, VRIJHEIDSGRADEN)

print('T =', {T}, 'T_KR =', {T_KR})
print('')

# =============================================================================
# Opdracht 3
# =============================================================================

# Significantieniveau
ALPHA = 0.05

# Meetresultaten steekproef
OUDE_VULMACHINE_mL = np.array([1500.9, 1500, 1503.8, 1509.4, 1492.5, 1503.8, 1506.6, 1504.7,
                               1500.9, 1515, 1496.3, 1489.7, 1491.6, 1500, 1492.5])

NIEUWE_VULMACHINE_mL = np.array([1501.9, 1495.3, 1500, 1505.6, 1507.5, 1496.3, 1499.1, 1497.2,
                                 1504.7, 1496.3, 1504.7, 1501.9, 1502.8, 1494.4, 1495.3])

OUDE_VARIANTIE = (np.std(OUDE_VULMACHINE_mL, ddof=1))**2
NIEUWE_VARIANTIE = (np.std(NIEUWE_VULMACHINE_mL, ddof=1))**2

N_OUD = 15
N_NIEUW = 15

print('OUDE_VARIANTIE =', {OUDE_VARIANTIE}, 'NIEUWE_VARIANTIE =', {NIEUWE_VARIANTIE})

# Oude variantie is groter dan de nieuwe variantie, dus:
VRIJHEIDSGRADEN_1 = N_OUD - 1 
VRIJHEIDSGRADEN_2 = N_NIEUW - 1

# Berekenen toetsingsgrootheid en kritische waarde
F = OUDE_VARIANTIE / NIEUWE_VARIANTIE
F_KR = stats.f.ppf(1-ALPHA/2, VRIJHEIDSGRADEN_1, VRIJHEIDSGRADEN_2)

print('F =', {F}, 'F_KR =', {F_KR})