'''Main file for our python N-Body solver.

For the advanced students...
- No, you don't need an "n_body" in front of every module, e.g. n_body_physics. That's just for clarity in this case.

Crucial programming concepts:
Comments
Functions
Arguments
Modules
Dictionaries
Conditionals
Loops
Configuration Files
Saving Data
Displaying Data
Numpy Arrays

Important programming concepts:
Commandline execution
Doc strings
'''

import n_body_physics
import n_body_data_handling
import n_body_setup
import n_body_wrapup

########################################################################

def run():
  '''Main simulation loop.'''

  particles, parameters = n_body_setup.load_settings()

  while not parameters['finished']:

    n_body_physics.update_system(particles, parameters)

    n_body_data_handling.save_data(particles, parameters)
 
    n_body_wrapup.check_if_finished(particles, parameters)

########################################################################

# What happens when the simulation is called from the command line.

if __name__ == '__main__':

  run()
