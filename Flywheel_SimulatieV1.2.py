# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 15:56:37 2024

@author: denni
"""

import numpy as np 
import matplotlib.pyplot as plt 
from numpy import sin

#Definieer constantes
m_p = 17e-2 #[kg]
m_c = 15e-2 #[kg]
g = 9.81 #[m/s**2]
l = 15e-2 #[m]
k = 0.0 #[dempingscoëfficiënt]

N = 100 #Hoeveelheid tijdstappen per seconde
Tstart = 0
Teind = 100
Nstap = (Teind*N) + 1
t = np.linspace(Tstart, Teind, Nstap) 
dt = Teind/(Nstap - 1) 

#Groepeer de constantes
c1 = (m_p*g*l)/2 + (m_c*g*l)
c2 = l + m_c*(l)**2
c3 = (-c2/(dt)**2) + (k/dt)
c4 = ((2*c2)/(dt)**2) - (k/dt)
c5 = (-c2/(dt)**2)

x = np.zeros_like(t) #Array voor de hoekverandering
z = np.zeros_like(t) #Array voor de hoekverandering zonder PID-controller
u = np.zeros_like(t) #Array voor de output v/d PID-controller
e = np.zeros_like(t) #Array voor de absolute fout van de simulatie

bandwidth = 80 #Maximale hoek die de slinger kan maken
target_value = 0 
x0 = 30 #Starthoek van de slinger
v0 = 0 #Startsnelheid van de slinger

#PID_parameters
Kp = -0.01
Ki = -0.0008
Kd = -0.03

prev_error = target_value - x0
integral = 0

#Simulatie met PID-controller
x[0] = x0
x[1] = x0 + dt*v0
for i in range(1, Nstap - 1):
    error = target_value - x[i] #PID-controller
    integral += error * dt
    derivative = (error - prev_error) / dt
    prev_error = error
    PID_output = Kp*error + Ki*integral + Kd*derivative
    
    e[i] = error 
    u[i] = PID_output
    u[i] = np.clip(u[i], -2, 2) #Limiteer de output t/m het bereik van de motor
    
    x[i] = np.clip(x[i], -bandwidth , bandwidth) #Limiteer de hoeken tot een bepaalt bereik
    x[i+1] = u[i]/c3 - c4/c3 * x[i] - c5/c3 * x[i-1] - c1/c3 * sin(x[i]) #Bereken de volgende hoek d.m.v. de bewegingsvergelijking
    

#Simulatie zonder PID-controller
z[0] = x0 
z[1] = z[0] + dt*v0
for i in range(1, Nstap - 1):
    z[i] = np.clip(z[i], -bandwidth, bandwidth)
    z[i+1] = - c4/c3*z[i] - c5/c3*z[i-1] - c1/c3*sin(z[i])
    
#Plot de simulatie
plt.figure(figsize=(10,6))
plt.title('Simulatie inverted flywheel zonder demping')
plt.plot(t, z, 'dodgerblue', label='Simulatie zonder PID')
plt.plot(t, x, 'darkorange', label='Hoekverandering pendulum')
plt.xlabel('Tijd (s)')
plt.ylabel('hoek theta')
plt.legend()
plt.show()

#Plot de in/output van de PID-contoller
plt.figure(figsize=(10,6))
plt.title('Simulatie inverted flywheel zonder demping')
plt.plot(t, e, 'green', label='Input PID controller')
plt.plot(t, u, 'red', label='Output PID controller')
plt.xlabel('Tijd (s)')
plt.legend()
plt.show()


