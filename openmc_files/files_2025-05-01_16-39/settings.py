'''
This script sets up the OpenMC simulation settings for a simplified BWR reactor model. It configures parameters such as particle count, batches, temperature settings, energy mode, source parameters, and output settings. It follows OpenMC best practices to ensure an efficient and accurate simulation, including specifying the correct paths to cross-section data and fission product yield data.
'''
import openmc
import os

# Instantiate Settings object
settings = openmc.Settings()

# Define criticality source
source = openmc.Source()
source.space = openmc.stats.Box([-6.9, -6.9, -180], [6.9, 6.9, 180])
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Maxwell(3.95e-8)
settings.source = source

# Set runs parameters
settings.batches = 20  # Reduced number of batches for testing
settings.inactive = 5
settings.particles = 1000 # Reduced number of particles for testing

# Define temperature settings
settings.temperature = {
    'default': 294.0,
    'method': 'interpolation',
    'range': [200.0, 1500.0]
}

# Energy mode and cross sections
settings.energy_mode = 'fixed source'

# Path to cross_sections.xml
settings.cross_sections = os.environ.get('OPENMC_CROSS_SECTIONS')
settings.chain_file = os.environ.get('OPENMC_CHAIN_FILE')

# Output settings
settings.output = {
    'tallies': True,
    'summary': True,
    'path': 'results',
}

# Set up statepoint and results files
settings.statepoint = {
    'batches': [5, 10, 15, 20]
}

# Export to XML
settings.export_to_xml('settings.xml')