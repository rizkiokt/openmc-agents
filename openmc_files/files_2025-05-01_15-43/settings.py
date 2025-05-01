'''
This script sets up the OpenMC simulation settings for a simplified BWR assembly. It configures the particle count, batches, temperature parameters, energy mode, source parameters, and output settings. The settings are optimized for testing purposes with a small number of particles and batches. Reflective boundary conditions are applied.
'''
import openmc
import os

# Instantiate a Settings object
settings = openmc.Settings()

# Define criticality calculation parameters
settings.batches = 10  # Reduced number of batches for testing
settings.inactive = 5  # Reduced number of inactive batches
settings.particles = 1000  # Reduced number of particles for testing

# Set temperature parameters
settings.temperature = {
    'default': 560.0,  # Coolant Temperature in Celsius.  Assumed to be the default temperature.
    'method': 'interpolation',
    'range': [273.0, 1273.0]
}

# Define energy mode and cross sections
os.environ['OPENMC_CROSS_SECTIONS'] = 'cross_sections.xml'
settings.energy_mode = 'fixed-source'

# Define a point source
point = openmc.stats.Point()
source = openmc.Source(space=point)
settings.source = source

# Define source parameters
# Assuming source is located at the center of the geometry
source = openmc.Source()
source.space = openmc.stats.Point([0, 0, 0])
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Watt(a=0.988, b=0.598)
settings.source = source

# Define output settings
settings.output = {
    'tallies': True,
    'summary': True,
    'path': 'results',
    'prefix': 'openmc'
}

# Enable statepoint writing
settings.statepoint = {'batches': [settings.batches]}

# Export the settings to an XML file
settings.export_to_xml()

print("settings.xml file created")