import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats as stats

# Berekenen van de achtergrond activiteit
MINUTEN = 5
SECONDEN = 60
A_achtergrond = 18 / (MINUTEN * SECONDEN)

# Maken van eerste tabel
data1 = {
    "Massa percentages Kalium [%]": [30, 40, 50, 60, 70],
    "Vervalreeksen N [-]": [48, 54, 54, 60, 63]
}
df1 = pd.DataFrame(data1)
df1["tijd t [s]"] = MINUTEN * SECONDEN
df1["Gemiddelde activiteit A [Bq]"] = (df1["Vervalreeksen N [-]"] / df1["tijd t [s]"]) - A_achtergrond
STDV1 = np.std(df1["Gemiddelde activiteit A [Bq]"], ddof=1)

print(df1, end='\n\n')

# Toepassen van een lineaire regressie van de eerste tabel
EEN_VECTOR = np.ones_like(df1["Massa percentages Kalium [%]"])
A1 = np.array([df1["Massa percentages Kalium [%]"], EEN_VECTOR])
A1 = A1.transpose()
o1 = np.linalg.solve(A1.transpose() @ A1, A1.transpose() @ df1["Gemiddelde activiteit A [Bq]"])
[a1, b1] = o1
x1 = np.linspace(0, 100, num=1000)
y1 = a1 * x1 + b1

# Plotten van de eerste tabel en de bijbehorende regressie
plt.scatter(df1["Massa percentages Kalium [%]"], df1["Gemiddelde activiteit A [Bq]"], label='Data')
plt.plot(x1, y1, color='red', label='Fit')
plt.errorbar(df1["Massa percentages Kalium [%]"], df1["Gemiddelde activiteit A [Bq]"], xerr=1, yerr=STDV1, fmt='o',
             ecolor='black', capsize=5, capthick=2, elinewidth=2)
plt.xlabel('Massa percentages Kalium [%]')
plt.ylabel('Gemiddelde activiteit A [Bq]')
plt.title("Bètaverval bij verschillende massa% kalium40")
plt.legend()
plt.grid()
plt.show()

# Maken van de tweede tabel
data2 = {
    "tijd t [s]": [1 * SECONDEN, 2 * SECONDEN, 3 * SECONDEN, 4 * SECONDEN, 5 * SECONDEN],
    "Vervalreeksen N [-]": [11, 21, 34, 44, 54]
}
df2 = pd.DataFrame(data2)
df2["Gemiddelde activiteit A [Bq]"] = (df2["Vervalreeksen N [-]"] / df2["tijd t [s]"]) - A_achtergrond
STDV2 = np.std(df2["Gemiddelde activiteit A [Bq]"], ddof=1)

print(df2, end='\n\n')

# Toepassen van een lineaire regressie van de tweede tabel
EEN_VECTOR = np.ones_like(df2["tijd t [s]"])
A2 = np.array([df2["tijd t [s]"], EEN_VECTOR])
A2 = A2.transpose()
o2 = np.linalg.solve(A1.transpose() @ A2, A1.transpose() @ df2["Gemiddelde activiteit A [Bq]"])
[a2, b2] = o2
x2 = np.linspace(0, 300, num=1000)
y2 = a2 * x2 + b2

# Plotten van de tweede tabel en de bijbehorende regressie
plt.scatter(df2["tijd t [s]"], df2["Gemiddelde activiteit A [Bq]"], label='Data')
plt.plot(x2, y2, color='red', label='Fit')
plt.errorbar(df2["tijd t [s]"], df2["Gemiddelde activiteit A [Bq]"], yerr=STDV2, fmt='o',
             ecolor='black', capsize=5, capthick=2, elinewidth=2)
plt.xlabel('Tijd [s]')
plt.ylabel('Gemiddelde activiteit A [Bq]')
plt.title("Bètaverval 70% KCL bij verschillende tijdsintervallen")
plt.legend()
plt.grid()
plt.show()

# Berekenen massa% kalium van een onbekende stof
VERVALREEKSEN = np.array([52, 58, 63, 52, 58])
y = (VERVALREEKSEN / (MINUTEN * SECONDEN)) - A_achtergrond
x = ((y - b1) / a1) * 0.522
GEM_KALIUM = np.mean(x)
s = np.std(x, ddof=1)
ALPHA = 0.05
VRIJHEIDSGRADEN = len(x) - 1
t = stats.t.ppf(1 - ALPHA/2, VRIJHEIDSGRADEN)
BETROUWBAARHEID = (t * s) / np.sqrt(len(x))

print('Gemiddelde massa% Kalium =', GEM_KALIUM, '%')
print('Standaarddeviatie massa% KCl =', s, "%")
print('Betrouwbaarheid massa% =', BETROUWBAARHEID, '%')
print('Betrouwbaarheidsinterval massa% =', GEM_KALIUM, '+-', BETROUWBAARHEID, '%')