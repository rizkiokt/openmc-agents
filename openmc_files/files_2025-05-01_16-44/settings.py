'''
This Python code sets up the OpenMC simulation settings for a simplified BWR model, including particle transport parameters, temperature settings, source definition, and output configuration. The settings are tailored for a quick test run with a small number of particles and batches.
'''
import openmc
import os

# Define simulation parameters
n_particles = 1000  # Reduced for quick testing
n_batches = 10  # Reduced for quick testing

# Instantiate Settings object
settings = openmc.Settings()
settings.batches = n_batches
settings.inactive = 0
settings.particles = n_particles
settings.temperature = {
    'default': 560.0,  # Temperature in Kelvin
    'method': 'interpolation'
}

# Set cross-sections environment variable
settings.cross_sections = os.environ.get('OPENMC_CROSS_SECTIONS')
settings.photon_transport = False
settings.run_mode = 'fixed source'

# Define a point source
point = openmc.stats.Point((0, 0, 0))
source = openmc.Source(space=point)
settings.source = source

# Set output settings
settings.output = {
    'tallies': True,
    'summary': True,
    'path': 'results',
    'prefix': 'openmc'
}

# Enable statepoint writing
settings.statepoint = {'batches': [n_batches]}

# Export settings to XML
settings.export_to_xml()
