import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8')
from scipy import stats as stats
from scipy.optimize import curve_fit


def data_analyse(data):
    gemiddelde = np.mean(data, axis=0)
    stdv = np.std(data, ddof=1)
    alpha = 0.05
    vrijheidsgraden = len(data) - 1
    t = stats.t.ppf(1 - alpha/2, vrijheidsgraden)
    betrouwbaarheid = (t*stdv)/np.sqrt(len(data))
    return print('Gemiddelde onbekende concentratie = '
                 f'{round(gemiddelde, 3)} ± {round(betrouwbaarheid, 3)}')


def con_data(maxima, n):
    hoek = []
    range1 = np.linspace(0, maxima, num=int(maxima/2+1))
    for i in range1:
        for j in range(n):
            hoek.append(i)
    hoek = np.array(hoek)
    return hoek



def ijklijn(self, a, b):
    return a*xdata + b


def bepalen_con(franjes):
    Concentratie = (franjes - popt[1])/popt[0]
    return Concentratie


def func(concentratie):
    Franjes = popt[0]*concentratie + popt[1]
    return Franjes


# Meting 2
xdata = con_data(10, 3)
ydata = np.array([60, 54, 48,           # 0g/100ml
                  54, 44, 48,           # 2g/100ml
                  40, 38, 48,           # 4g/100ml
                  39, 45, 35,           # 6g/100ml
                  33, 36, 34,           # 8g/100ml
                  35, 32, 37])          # 10g/100ml

popt, pcov = curve_fit(ijklijn, xdata, ydata, p0=(-2, 50))
stdv_con = np.sqrt(np.diag(pcov))

con_dense = np.linspace(0, 12, num=1000)
y = func(con_dense)

fig1 = plt.figure()
plt.scatter(xdata, ydata, label='Data')
plt.plot(con_dense, y, color='red', label=f'Lineaire fit: N = {round(popt[0], 2)}*con + {round(popt[1], 2)}')
plt.xlabel('Concentratie suikerwater [g/100mL]', weight='bold')
plt.ylabel('Aantal verschoven franjes [-]', weight='bold')
plt.title("Aantal verschoven franjes bij verschillende concentratie suikerwater - iteratie 2", weight='bold')
plt.legend()
plt.tight_layout()

onbekende_meting_1 = np.array([41, 40, 40, 34, 32])     # 5g/100mL
onbekende_meting_2 = np.array([34, 37, 34, 33])         # 7g/100mL

con1 = bepalen_con(onbekende_meting_1)
con2 = bepalen_con(onbekende_meting_2)


# Meting 3
xdata = con_data(12, 5)
ydata = np.array([54, 55, 49, 51, 44,       # 0g/100ml
                  68, 71, 74, 76, 81,       # 2g/100ml
                  67, 68, 70, 69, 74,       # 4g/100ml
                  80, 73, 82, 78, 85,       # 6g/100ml
                  60, 69, 63, 71, 64,       # 8g/100ml
                  49, 54, 55, 56, 52,       # 10g/100ml
                  52, 48, 46, 56, 49])      # 12g/100ml

popt, pcov = curve_fit(ijklijn, xdata, ydata, p0=(-2, 50))
stdv_con = np.sqrt(np.diag(pcov))

con_dense = np.linspace(0, 12, num=1000)
y = func(con_dense)

onbekende_meting_1 = np.array([58, 49, 63, 49, 56])         # 5g/100mL
onbekende_meting_2 = np.array([49, 52, 48, 53, 51])         # 7g/100mL

con3 = bepalen_con(onbekende_meting_1)
con4 = bepalen_con(onbekende_meting_2)

fig2 = plt.figure()
plt.scatter(xdata, ydata, label='Data')
plt.plot(con_dense, y, color='red', label=f'Lineaire fit: N = {round(popt[0], 2)}*con + {round(popt[1], 2)}')
plt.xlabel('Concentratie suikerwater [g/100mL]', weight='bold')
plt.ylabel('Aantal verschoven franjes [-]', weight='bold')
plt.title("Aantal verschoven franjes bij verschillende concentratie suikerwater - iteratie 3", weight='bold')
plt.legend()
plt.tight_layout()


if __name__ == '__main__':
    fig1.show()
    data_analyse(con1)
    data_analyse(con2)

    print("")

    fig2.show()
    data_analyse(con3)
    data_analyse(con4)
