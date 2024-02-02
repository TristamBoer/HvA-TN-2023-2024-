import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8')


def lineaire_functie(frames, a, b):
    golflengte = a*frames + b
    return golflengte

def berekenen_frame(golflengte, a, b):
    frame = (golflengte - b) / a
    return frame


# Bekende golflengtes
class LEDlamp:
    golflengte_blauw = 450e-9
    golflengte_groen = 530e-9
    golflengte_rood = 660e-9

class Kwiklamp:
    golflengte_geel = 578e-9
    golflengte_groen = 546e-9
    golflengte_paars = 434e-9


# Uitlezen van alle metingen
LED_meting1 = np.loadtxt("output 1.csv", delimiter=',')
Kwik_meting1 = np.loadtxt("output 3A.csv", delimiter=',')
onbekende_lamp = np.loadtxt("output O1.csv", delimiter=',')


# Vinden pieken van alle metingen
golflengtes_LED_meting1 = find_peaks(LED_meting1, height=500)[0]
golflengtes_Kwik_meting1 = find_peaks(Kwik_meting1, height=500)[0]
golflengtes_Kwik_meting1 = np.delete(golflengtes_Kwik_meting1, 2)
golflengtes_onbekende_lamp = find_peaks(onbekende_lamp, height=5000)[0]


# Berekenen constanten (a en b) fit vergelijking
frames = np.linspace(0, 250, num=1000)
x1 = np.array(golflengtes_Kwik_meting1)
y1 = np.array([Kwiklamp.golflengte_paars, Kwiklamp.golflengte_groen])
een_vec = np.ones_like(x1)
A = np.array([x1, een_vec])
A = A.transpose()
[a, b] = np.linalg.solve(A.transpose() @ A, A.transpose() @ y1)


# Maken van de ijklijn
ijklijn = lineaire_functie(frames, a, b)


# Bepalen van de foutmarge
o1 = berekenen_frame(530e-9, a, b)
o2 = golflengtes_LED_meting1[1]
o3 = np.abs(o2 - o1)

o4 = berekenen_frame(450e-9, a, b)
o5 = golflengtes_LED_meting1[0]
o6 = np.abs(o5 - o4)

o7 = np.array([o3, o6])
foutmarge = np.std(o7, ddof=1)


# Berekenen golflengte van de onbekende lamp
onbekende_golflengte = lineaire_functie(golflengtes_onbekende_lamp[0], a, b)


# Plotten van alle figuren
fig1 = plt.figure()
plt.plot(LED_meting1, color='blue')
plt.xlabel('Frames [-]')
plt.ylabel('Intensiteit [a.u]')
plt.title("Intensiteit LED lamp")
plt.tight_layout()

fig2 = plt.figure()
plt.plot(Kwik_meting1, color='blue')
plt.xlabel('Frames [-]')
plt.ylabel('Intensiteit [a.u]')
plt.title("Intensiteit Kwik lamp")
plt.tight_layout()

fig3 = plt.figure()
plt.plot(onbekende_lamp, color='blue')
plt.xlabel('Frames [-]')
plt.ylabel('Intensiteit [a.u]')
plt.title("Intensiteit onbekende lamp")
plt.tight_layout()

fig4 = plt.figure()
plt.plot(frames, ijklijn, color='red', label='Lineaire fit')
plt.scatter(x1, y1, color='blue', label='Data kwiklamp')
plt.xlabel('Frames [-]')
plt.ylabel('Golflengte [m]')
plt.title("Ijklijn golflengte bij verschillende frames")
plt.legend()
plt.tight_layout()



if __name__ == '__main__':
    fig1.show()
    fig2.show()
    fig3.show()
    fig4.show()

    print(f"Golflengte onbekende lamp = {onbekende_golflengte*1e9} ± {foutmarge} [nm]")
