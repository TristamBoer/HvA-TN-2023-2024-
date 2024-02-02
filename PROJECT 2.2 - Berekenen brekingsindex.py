import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats as stats
plt.style.use('seaborn-v0_8')

# Bepalen constanten for fit vergelijking
n = 1.9    # Variëren om brekingsindex van onbekend materiaal te bepalen
d = 0.6e-3
lambda1 = 532e-9
i_degrees = np.linspace(0, 20, num=5)
i_radians = np.radians(i_degrees)
r = np.arcsin(np.sin(i_radians)/n)

# Maken van de fit vergelijking
N = 2*d/lambda1 * (n/np.cos(r) + np.tan(i_radians)*np.sin(i_radians) - np.tan(r)*np.sin(i_radians)
                   - (n-1) - 1/np.cos(i_radians))
# Gemeten data
data = {
    "Gemeten N 1_1": [0, 6, 17, 38, 60],
    "Gemeten N 1_2": [0, 5, 16, 35, 57],
    "Gemeten N 1_3": [0, 5, 16, 36, 58],

    "Gemeten N 2_1": [0, 5, 16, 37, 62],
    "Gemeten N 2_2": [0, 5, 15, 36, 63],
    "Gemeten N 2_3": [0, 5, 15, 36, 62],

    "Gemeten N 3_1": [0, 5, 15, 37, 64],
    "Gemeten N 3_2": [0, 5, 15, 38, 65],
    "Gemeten N 3_3": [0, 5, 15, 38, 65],

    "Gemeten N 4_1": [0, 5, 15, 36, 68],
    "Gemeten N 4_2": [0, 5, 16, 39, 72],
    "Gemeten N 4_3": [0, 5, 15, 38, 70],

    "Gemeten N 5_1": [0, 5, 17, 36, 65],
    "Gemeten N 5_2": [0, 5, 18, 37, 65],
    "Gemeten N 5_3": [0, 5, 17, 39, 68],

    "Gemeten N 6_1": [0, 5, 18, 37, 65],
    "Gemeten N 6_2": [0, 5, 17, 40, 68],
    "Gemeten N 6_3": [0, 5, 17, 43, 71],

    "Gemeten N 7_1": [0, 4, 18, 38, 71],
    "Gemeten N 7_2": [0, 5, 17, 38, 72],
    "Gemeten N 7_3": [0, 4, 17, 39, 70],

    "Gemeten N 8_1": [0, 4, 14, 36, 65],
    "Gemeten N 8_2": [0, 4, 15, 38, 66],
    "Gemeten N 8_3": [0, 4, 15, 37, 66],

    "Gemeten N 9_1": [0, 4, 13, 36, 64],
    "Gemeten N 9_2": [0, 5, 14, 37, 67],
    "Gemeten N 9_3": [0, 4, 14, 39, 68],

    "Gemeten N 10_1": [0, 5, 15, 36, 61],
    "Gemeten N 10_2": [0, 5, 16, 37, 63],
    "Gemeten N 10_3": [0, 5, 15, 37, 64]
}
df1 = pd.DataFrame(data)

# Betrouwbaarheid berekenen van de metingen
GEM_N = np.array(round(df1.mean(axis=1), 0))
# GEM_N = np.array(df1.mean(axis=1))
STDV_N = np.array(df1.std(axis=1, ddof=1))
Significantie = 0.05
Vrijheidsgraden = len(df1) - 1
t = stats.t.ppf(1 - Significantie/2, Vrijheidsgraden)
Betrouwbaarheid = (t*STDV_N) / np.sqrt(len(df1))

print(df1, end='\n\n')
print('Gemiddelde van N afgerond op geheel getal:', GEM_N)
print('Standaarddeviatie van N:', STDV_N)
print('Betrouwbaaheid van N:', Betrouwbaarheid)

# Plotten van fit en gemeten data
plt.plot(i_degrees, N, label='Fit vergelijking', color='red')
plt.errorbar(i_degrees, GEM_N, label='Gemeten data', xerr=0.5, yerr=Betrouwbaarheid, fmt='o',
             ecolor='black', capsize=3, capthick=1.2, elinewidth=1.2)
plt.xlabel('Invalshoek i [Graden]', weight='bold')
plt.ylabel('Hoeveelheid maxima N [-]', weight='bold')
plt.title("Hoeveelheid maxima bij verschillende hoeken van inval", weight='bold')
plt.tight_layout()
plt.legend()
plt.show()