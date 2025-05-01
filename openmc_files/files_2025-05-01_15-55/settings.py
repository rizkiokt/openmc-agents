'''
This script creates the OpenMC settings XML file for a BWR reactor simulation. It sets parameters such as particle count, inactive/active batches, temperature, source, and output settings. It also configures reflective boundary conditions and specifies the energy mode and cross sections.
'''
import openmc

# Instantiate Settings object
settings = openmc.Settings()

# Define simulation parameters
settings.particles = 1000  # Number of particles to simulate per batch
settings.inactive = 10    # Number of inactive batches
settings.batches = 50       # Number of active batches

# Set temperature parameters
settings.temperature = {
    'default': 560.0,  # Temperature in Kelvin
    'method': 'interpolation',
    'multipole': True
}

# Set energy mode and cross sections
settings.energy_mode = 'continuous-energy'

# Define a point source
point = openmc.stats.Point((0, 0, 0))
source = openmc.Source(space=point)
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Watt(1.0) # Fission energy spectrum
settings.source = source

# Set output settings
settings.output = {
    'tallies': True,
    'summary': True,
    'path': 'results',
}

# Reflective Boundary Conditions - using the extent from the geometry
boundary = 1.4 * 10 / 2 # lattice_pitch * lattice_size / 2
surface1 = openmc.XPlane(x0=-boundary, boundary_type='reflective')
surface2 = openmc.XPlane(x0=boundary, boundary_type='reflective')
surface3 = openmc.YPlane(y0=-boundary, boundary_type='reflective')
surface4 = openmc.YPlane(y0=boundary, boundary_type='reflective')
surface5 = openmc.ZPlane(z0=-boundary, boundary_type='reflective')
surface6 = openmc.ZPlane(z0=boundary, boundary_type='reflective')

# Assign reflective boundaries to the root universe
# This is already handled by the geometry module, so this section is removed to avoid conflict.

# Export the settings to an XML file
settings.export_to_xml('settings.xml')