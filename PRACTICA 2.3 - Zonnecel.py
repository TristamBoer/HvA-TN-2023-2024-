from scipy.optimize import minimize_scalar

'''
LED lamp zonder filter
'''

def wiskundige_functie(x):
    # Definieer hier de wiskundige functie waarvan je het maximum wilt vinden
    function = -0.2352 * x ** 2 + 2.4179 * x - 0.3044
    return function


def vind_maximum_wiskundige_functie():
    # Optimaliseer de negatieve van de wiskundige functie om het maximum te vinden
    result = minimize_scalar(lambda x: -wiskundige_functie(x), bounds=(-10, 10), method='bounded')

    if result.success:
        return result.x, -result.fun  # Return het x-punt en de maximale waarde van de functie
    else:
        raise ValueError("Optimalisatie mislukt: " + result.message)


# Vind het maximum van de wiskundige functie binnen het opgegeven bereik
x_max, y_max = vind_maximum_wiskundige_functie()
print("mpp LED [W]:", y_max, "op U [V] =", x_max)

'''
LED lamp met blauw licht
'''

def wiskundige_functie(x):
    function = -0.0804*x**2 + 0.1539*x - 0.0008
    return function

x_max, y_max = vind_maximum_wiskundige_functie()
print("mpp blauw [W]:", y_max, "op U [V] =", x_max)

'''
LED lamp met rood licht
'''

def wiskundige_functie(x):
    function = -0.0953*x**2 + 0.5832*x - 0.0084
    return function

x_max, y_max = vind_maximum_wiskundige_functie()
print("mpp rood [W]:", y_max, "op U [V] =", x_max)

'''
LED lamp met groen licht
'''

def wiskundige_functie(x):
    function = -0.0948*x**2 + 0.5488*x - 0.0064
    return function

x_max, y_max = vind_maximum_wiskundige_functie()
print("mpp groen [W]:", y_max, "op U [V] =", x_max)