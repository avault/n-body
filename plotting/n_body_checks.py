import numpy as np
import os
import sys

# Plotting imports
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.use('PDF')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.transforms as transforms
import matplotlib.patheffects as path_effects

# Make the x and y ticks bigger
matplotlib.rcParams['xtick.labelsize'] = 20
matplotlib.rcParams['xtick.major.size'] = 10
matplotlib.rcParams['xtick.major.width'] = 2
matplotlib.rcParams['ytick.labelsize'] = 20
matplotlib.rcParams['ytick.major.size'] = 10
matplotlib.rcParams['ytick.major.width'] = 2

########################################################################

def plot_force_of_gravity(force_function, m1=1., m2=2., pos1 = np.array([0., 0.]), \
                          pos2 = np.array([1., 1.]), G = 6.67e-11):
  '''Plot the direction of the force of gravity on one mass due to another mass, using a function given by the user.'''
  
  # Get the force
  force = force_function(m1, m2, pos1, pos2, G)
  
  # Get the magnitude and direction of the force
  force_mag = np.linalg.norm(force)
  force_dir = force/force_mag
  
  # Make a plot
  fig = plt.figure(figsize=(10,8))
  ax = plt.gca()

  # Draw the masses
  ax.scatter(pos1[0], pos1[1], s=256, color='k')
  ax.scatter(pos2[0], pos2[1], s=256, color='k')

  # Draw the arrow
  ax.arrow(pos1[0], pos1[1], force_dir[0], force_dir[1], width=0.01, overhang=0.5, color='k')

  # Annotate masses
  ax.annotate(r'$m_1$', pos1, (10, -10), textcoords='offset points', fontsize=22, arrowprops={'arrowstyle': '-',})
  ax.annotate(r'$m_2$', pos2, (10, -10), textcoords='offset points', fontsize=22, arrowprops={'arrowstyle': '-',})

  # Annotate vector
  ax.annotate(r'$\vec F_{\rm{gravity}}$', (pos1 + force_dir)/2., (20, -20), textcoords='offset points', fontsize=22,)

  ax.set_xlabel('Horizontal Position (m)', fontsize=22)
  ax.set_ylabel('Vertical Position (m)', fontsize=22)

  current_dir = os.path.dirname(os.path.abspath(__file__))
  save_file = '{}/force_plot.png'.format(current_dir)

  plt.savefig(save_file, dpi=150)

########################################################################

def plot_total_force(total_force_function, i='default', particles='default', parameters='default'):

  if i == 'default':
    i = 0

  if parameters == 'default':
    parameters = {
      'n_particles' : np.random.randint(3, 10),
      'n_dimensions' : 2,
      'G' : 6.67e-11,
    }

  if particles == 'default':
    particles = {
      'masses' : np.random.uniform(0., 5.e4, parameters['n_particles']),
      'positions' : np.random.uniform(0., 3., (parameters['n_particles'], parameters['n_dimensions'])),
      'velocities' : np.random.uniform(-3., 3., (parameters['n_particles'], parameters['n_dimensions'])),
    }

  total_force = total_force_function(i, particles, parameters)

  # Make a plot
  fig = plt.figure(figsize=(10,8))
  ax = plt.gca()

  # Draw the masses
  ax.scatter(particles['positions'][:,0], particles['positions'][:,1], s=256, color='k')

  # Draw the arrow
  ax.arrow(particles['positions'][i,0], particles['positions'][i,1], total_force[0], total_force[1], width=0.01, overhang=0.5, color='k')

  # Annotate masses
  ax.annotate(r'$m_i$', particles['positions'][i], (10, -10), textcoords='offset points', fontsize=22, arrowprops={'arrowstyle': '-',})

  ax.set_xlabel('Horizontal Position (m)', fontsize=22)
  ax.set_ylabel('Vertical Position (m)', fontsize=22)

  current_dir = os.path.dirname(os.path.abspath(__file__))
  save_file = '{}/total_force_plot.png'.format(current_dir)

  plt.savefig(save_file, dpi=150)

  print 'Congratulations! Your code runs, and your plot is saved in {}'.format(current_dir)

########################################################################

def plot_all_total_forces(all_total_forces_function, particles='default', parameters='default'):

  if parameters == 'default':
    parameters = {
      'n_particles' : np.random.randint(3, 10),
      'n_dimensions' : 2,
      'G' : 6.67e-11,
    }

  if particles == 'default':
    particles = {
      'masses' : np.random.uniform(0., 5.e4, parameters['n_particles']),
      'positions' : np.random.uniform(0., 3., (parameters['n_particles'], parameters['n_dimensions'])),
      'velocities' : np.random.uniform(-3., 3., (parameters['n_particles'], parameters['n_dimensions'])),
    }

  total_forces = all_total_forces_function(particles, parameters)

  # Make a plot
  fig = plt.figure(figsize=(10,8))
  ax = plt.gca()

  # Draw the masses
  ax.scatter(particles['positions'][:,0], particles['positions'][:,1], s=256, color='k')

  # Draw the arrow
  for i in range(len(particles['masses'])):
    ax.arrow(particles['positions'][i,0], particles['positions'][i,1], total_forces[i,0], total_forces[i,1], width=0.01, overhang=0.5, color='k')

    # Annotate masses
    ax.annotate(r'$m_{}$'.format(i), particles['positions'][i], (10, -10), textcoords='offset points', fontsize=22, arrowprops={'arrowstyle': '-',})

  ax.set_xlabel('Horizontal Position (m)', fontsize=22)
  ax.set_ylabel('Vertical Position (m)', fontsize=22)

  current_dir = os.path.dirname(os.path.abspath(__file__))
  save_file = '{}/all_total_forces_plot.png'.format(current_dir)

  plt.savefig(save_file, dpi=150)

  print 'Congratulations! Your code runs, and your plot is saved in {}'.format(current_dir)
