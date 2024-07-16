# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:50:04 2023

@author: thijs
"""

import wis_2_2_utilities_nochrono as util
import wis_2_2_systems_nochrono as systems

#set timestep
timestep = 1e-3
sim_time = 0.1

matrix_A = []
matrix_B = []

cart_x = 0
cart_v = 0
angle1_x = 0
angle1_v = 0
angle2_x = 0
angle2_v = 1
u_start = 0.0001

x_state = []
x_vector = [cart_x,cart_v,angle1_x,angle1_v,angle2_x,angle2_v]

class controller(): 
    def feedBack(self, observe):
        x_state.append(observe)
        u= 0
        return u

def main():
  model=systems.cart_inverted_pendulum(second_pendulum=True,pendulum2_length=0.4, state0 = x_vector, u0 = u_start)
  control = controller()
  simulation = util.simulation(model=model,timestep=timestep)
  simulation.setCost()
  simulation.max_duration = sim_time #seconde
  simulation.GIF_toggle = False #set to false to avoid frame and GIF creation
  
  
  while simulation.vis.Run():
      if simulation.time<simulation.max_duration:
        simulation.step()
        u = control.feedBack(simulation.observe())
        simulation.observe() 
        # if len(x_vector)<1:
        #     simulation.observe(cart_position)=1
        #     simulation.observe()
        # else:
        #     simulation.observe()
        
        simulation.control(u)
        simulation.log()
        simulation.refreshTime()
        
      else:
        print('Ending visualisation...')
        simulation.vis.GetDevice().closeDevice()
        
  simulation.writeData()
       
if __name__ == "__main__":
  main()

if cart_x == 0:
    if cart_v == 0:
        if angle1_x == 0:
            if angle1_v == 0:
                if angle2_x == 0:
                    if angle2_v == 0:
                        if u_start != 0:
                              matrix_B = (x_state[-1]-x_vector)/u_start/sim_time
                              print('matrix B is', matrix_B)
                    else:
                        matrix_A = (x_state[-1]-x_vector)/angle2_v/sim_time
                        print('matrix A kolom 6 is',matrix_A)
                else:
                    matrix_A = (x_state[-1]-x_vector)/angle2_x/sim_time
                    print('matrix A kolom 5 is',matrix_A)
            else:
                matrix_A = (x_state[-1]-x_vector)/angle1_v/sim_time
                print('matrix A kolom 4 is',matrix_A)
        else:
            matrix_A = (x_state[-1]-x_vector)/angle1_x/sim_time
            print('matrix A kolom 3 is',matrix_A)
    else:
        matrix_A = (x_state[-1]-x_vector)/cart_v/sim_time
        print('matrix A kolom 2 is',matrix_A)
else:
    matrix_A = (x_state[-1]-x_vector)/cart_x/sim_time
    print('matrix A kolom 1 is',matrix_A)


