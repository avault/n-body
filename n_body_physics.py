'''
This module determines how the system updates each time step.
'''

import numpy as np
import pdb

########################################################################

def update_system(particles, parameters):
  '''Update the system per timestep.'''

  # Get the forces
  forces = calculate_net_force_on_all_particles(particles, parameters)

  # Update the positions
  update_positions(particles, parameters, forces)

  # Get the forces again, this time for calculating velocities.
  forces_new = calculate_net_force_on_all_particles(particles, parameters)

  # Update the velocities
  update_velocities(particles, parameters, forces, forces_new)

########################################################################
# Calculate the forces
########################################################################

def calculate_force(m1, m2, pos1, pos2, G):
  '''Calculate the force on particle 1 due to particle 2. Doesn't use the dictionary structure.
  '''

  displacement = pos2 - pos1

  distance = np.linalg.norm(displacement)

  force = G*m1*m2*displacement/distance**3.

  return force

########################################################################

def calculate_net_force_on_particle(i, particles, parameters):
  '''Calculate the forces on a particle.

  Args:
  i -- particle index
  particles -- The particle information
  parameters -- The simulation parameter information
  '''

  total_force = np.zeros(len(particles['positions'][0]))

  m_i = particles['masses'][i]
  pos_i = particles['positions'][i]

  for j in range(len(particles['masses'])):

    # Skip over when the particles are the same.
    if i == j:
      continue

    force = calculate_force(m_i, particles['masses'][j], pos_i, particles['positions'][j], parameters['G'])

    total_force += force

  return total_force

########################################################################

def calculate_net_force_on_all_particles(particles, parameters):
  '''Calculate the forces on each particle

  Args:
  particles -- The particle information
  parameters -- The simulation parameter information
  '''

  total_forces = []
  for i in range(len(particles['masses'])):

    total_force = calculate_net_force_on_particle(i, particles, parameters)

    total_forces.append(total_force)

  return np.array(total_forces)

########################################################################
# Updating the particles
########################################################################

def update_position(i, particles, parameters, forces):
  '''Update a particular particle.

  Args:
  i -- Targeted particle
  particles -- The particle information
  parameters -- The simulation parameter information
  forces -- Forces on the particle.
  '''

  pos = particles['positions'][i]
  vel = particles['velocities'][i]
  acc = forces[i]/particles['masses'][i]

  new_pos = pos + vel*parameters['dt'] + 0.5*acc*parameters['dt']**2.

  return new_pos

########################################################################

def update_positions(particles, parameters, forces):
  '''Update the positions and velocities of each particle.

  Args:
  particles -- The particle information
  parameters -- The simulation parameter information
  forces -- Forces on the particles
  '''


  vel_term = particles['velocities']*parameters['dt']

  acc = forces/np.array([particles['masses'],]*parameters['n_dimensions']).transpose()
  acc_term = 0.5*acc*parameters['dt']**2.

  pos_change = vel_term + acc_term

  particles['positions'] += pos_change

########################################################################

def update_velocities(particles, parameters, forces_old, forces_new):

  acceleration_old = forces_old/np.array([particles['masses'],]*parameters['n_dimensions']).transpose() 
  acceleration_new = forces_new/np.array([particles['masses'],]*parameters['n_dimensions']).transpose() 

  vel_change = 0.5*(acceleration_old + acceleration_new)*parameters['dt']

  particles['velocities'] += vel_change

