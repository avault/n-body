'''Testing for n_body_physics.py
'''

import copy
import numpy as np
import numpy.testing as npt
import pdb
import unittest

import n_body_physics

########################################################################
# Test Cases
########################################################################

n_particles = 4
n_dimensions = 2

# Choose the simulation parameters (Based on parameters of the solar system)
parameters = {'G': 6.67e-11,
                  'dt' : 1.e13,
                  'n_dimensions' : n_dimensions,
                  'n_particles' : n_particles,
                  }

# Make the particles
particles = {}
particles['masses'] = np.random.uniform(1.e33, 3.e33, n_particles)
particles['positions'] = np.random.uniform(0., 3.e13, (n_particles, n_dimensions))
particles['velocities'] = np.random.uniform(-3.e6, 3.e6, (n_particles, n_dimensions))

# The forces
forces = n_body_physics.calculate_net_force_on_all_particles(particles, parameters)

########################################################################

class TestCalculateForce(unittest.TestCase):
  '''Testing for n_body_physics.calculate_force()'''

  def setUp(self):

    self.m1 = 1.
    self.m2 = 2.
    self.pos1 = np.array([0., 0.])
    self.pos2 = np.array([-1., -1.])

    self.G = 6.67e-11 # G in SI

  def test_runs(self):

    n_body_physics.calculate_force(self.m1, self.m2, self.pos1, self.pos2, self.G)

  def test_returns_results_of_proper_length(self):

    expected = self.pos1.size

    actual = len(n_body_physics.calculate_force(self.m1, self.m2, self.pos1, self.pos2, self.G))

    self.assertEqual(expected, actual)

  def test_returns_right_mag_simple_case(self):
    expected = self.G*self.m1*self.m2/2.

    force = n_body_physics.calculate_force(self.m1, self.m2, self.pos1, self.pos2, self.G)
    actual = np.linalg.norm(force)

    npt.assert_array_less(0., actual)

    npt.assert_allclose(expected, actual)

  def test_returns_right_direction_simple_case(self):
    expected = self.pos2/np.sqrt(2.)

    force = n_body_physics.calculate_force(self.m1, self.m2, self.pos1, self.pos2, self.G)
    actual = force/np.linalg.norm(force)

    npt.assert_allclose(expected, actual)

########################################################################
    
class TestCalculateNetForce(unittest.TestCase):
  '''Testing for n_body_physics.calculate_net_force_on_particle()'''

  def setUp(self):

    self.n_particles = 4
    self.n_dimensions = 2

    # Choose the simulation parameters
    self.parameters = {'G': 6.67e-11,
                      }

    # Make the particles
    self.particles = {}
    self.particles['masses'] = np.random.uniform(1., 3., self.n_particles)
    self.particles['positions'] = np.random.uniform(0., 3., (self.n_particles, self.n_dimensions))
    self.particles['velocities'] = np.random.uniform(-3., 3., (self.n_particles, self.n_dimensions))

    # What particle to arbitrarily choose
    self.i = 0

    # What function to run
    self.fn = n_body_physics.calculate_net_force_on_particle

    # What arguments to use
    self.args = (self.i, self.particles, self.parameters)

  def test_runs(self):

    result = self.fn(*self.args)

  def test_correct_size(self):

    actual = len(self.fn(*self.args))

    expected = self.n_dimensions

    self.assertEqual(expected, actual)

  def test_right_result(self):

    # Setup the particles for this particular case
    self.particles['masses'] = np.array([1., 2., 3.])
    self.particles['positions'] = np.array([[0., 0.], [1., -1.], [1., 2.]])

    # Calculate the expected force
    expected1 = n_body_physics.calculate_force(self.particles['masses'][0], self.particles['masses'][1], self.particles['positions'][0], self.particles['positions'][1], self.parameters['G'])
    expected2 = n_body_physics.calculate_force(self.particles['masses'][0], self.particles['masses'][2], self.particles['positions'][0], self.particles['positions'][2], self.parameters['G'])
    expected = expected1 + expected2

    actual = self.fn(self.i, self.particles, self.parameters)

    npt.assert_allclose(expected, actual)

########################################################################

class TestCalculateNetForceAllParticles(unittest.TestCase):
  '''Testing for n_body_physics.calculate_net_force_on_all_particles()'''

  def setUp(self):

    self.n_particles = 4
    self.n_dimensions = 2

    # Choose the simulation parameters
    self.parameters = {'G': 6.67e-11,
                      }

    # Make the particles
    self.particles = {}
    self.particles['masses'] = np.random.uniform(1., 3., self.n_particles)
    self.particles['positions'] = np.random.uniform(0., 3., (self.n_particles, self.n_dimensions))
    self.particles['velocities'] = np.random.uniform(-3., 3., (self.n_particles, self.n_dimensions))

    # What function to run
    self.fn = n_body_physics.calculate_net_force_on_all_particles

    # What arguments to use
    self.args = (self.particles, self.parameters)

  def test_runs(self):

    result = self.fn(*self.args)

  def test_right_dimensions(self):

    expected = self.particles['positions'].shape

    result = self.fn(*self.args)
    actual = result.shape

    self.assertEqual(expected, actual)

  def test_one_consistent(self):

    i = 1

    expected = n_body_physics.calculate_net_force_on_particle(i, self.particles, self.parameters)

    result = self.fn(*self.args)
    actual = result[i]

    npt.assert_allclose(expected, actual)

########################################################################
    
class TestUpdatePosition(unittest.TestCase):
  '''Testing for n_body_physics.update_position()'''

  def setUp(self):

    # What function to run
    self.fn = n_body_physics.update_position

    self.n_particles = 4
    self.n_dimensions = 2

    # Choose the simulation parameters
    self.parameters = {'G': 6.67e-11,
                      'dt' : 0.01
                      }

    # Make the particles
    self.particles = {}
    self.particles['masses'] = np.random.uniform(1., 3., self.n_particles)
    self.particles['positions'] = np.random.uniform(0., 3., (self.n_particles, self.n_dimensions))
    self.particles['velocities'] = np.random.uniform(-3., 3., (self.n_particles, self.n_dimensions))

    # The forces
    self.forces = n_body_physics.calculate_net_force_on_all_particles(self.particles, self.parameters)

    # Which particle to choose
    self.i = 1

    # What arguments to use
    self.args = (self.i, self.particles, self.parameters, self.forces)

  def test_runs(self):

    result = self.fn(*self.args)

  def test_right_dimensions(self):
    
    expected = self.n_dimensions

    result = self.fn(*self.args)
    actual = self.particles['positions'][self.i].size

    self.assertEqual(expected, actual)

########################################################################
    
class TestUpdatePositions(unittest.TestCase):
  '''Testing for n_body_physics.update_positions()'''

  def setUp(self):

    # What function to run
    self.fn = n_body_physics.update_positions

    # What arguments to use
    self.args = (particles, parameters, forces)

  def test_runs(self):

    result = self.fn(*self.args)

  def test_right_dimensions_still(self):

    expected = (parameters['n_particles'], parameters['n_dimensions'])

    result = self.fn(*self.args)
    actual = particles['positions'].shape

    self.assertEqual(expected, actual)

  def test_changes_positions(self):

    before = copy.deepcopy(particles['positions'])

    result = self.fn(*self.args)
    after = particles['positions']

    assert not np.allclose(before, after)

  def test_consistency_with_single_case(self):

    i = np.random.randint(len(particles['masses']))

    expected = n_body_physics.update_position(i, particles, parameters, forces)

    result = self.fn(*self.args)
    actual = particles['positions'][i]

    npt.assert_allclose(expected, actual)

########################################################################

class TestUpdateVelocities(unittest.TestCase):
  '''Testing for n_body_physics.update_velocities()'''

  def setUp(self):

    # What function to run
    self.fn = n_body_physics.update_velocities

    # Get the new forces
    n_body_physics.update_positions(particles, parameters, forces)
    forces_new = n_body_physics.calculate_net_force_on_all_particles(particles, parameters)

    # What arguments to use
    self.args = (particles, parameters, forces, forces_new)

  def test_runs(self):

    result = self.fn(*self.args)

  def test_right_dimensions_still(self):

    expected = (parameters['n_particles'], parameters['n_dimensions'])

    result = self.fn(*self.args)
    actual = particles['velocities'].shape

    self.assertEqual(expected, actual)

########################################################################

class TestUpdateSystem(unittest.TestCase):
  '''Testing for n_body_physics.update_system()'''

  def setUp(self):

    # What function to run
    self.fn = n_body_physics.update_system

    # What arguments to use
    self.args = (particles, parameters)

  def test_runs(self):

    result = self.fn(*self.args)

  def test_changes_positions(self):

    before = copy.deepcopy(particles['positions'])

    result = self.fn(*self.args)
    after = particles['positions']

    assert not np.allclose(before, after)

  def test_changes_velocities(self):

    before = copy.deepcopy(particles['velocities'])

    #pdb.set_trace()

    result = self.fn(*self.args)
    after = particles['velocities']

    assert not np.allclose(before, after)

  def test_finite(self):

    result = self.fn(*self.args)

    assert np.isfinite(particles['positions'].sum())
    assert np.isfinite(particles['velocities'].sum())
