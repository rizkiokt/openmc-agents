'''
This script creates an OpenMC settings file for a simplified BWR assembly simulation. It configures the simulation parameters, including particle count, batches, temperature settings, energy mode, source parameters, and output settings. The settings are optimized for testing purposes with a small number of particles and batches.
'''
import openmc
import os

# Settings

# Instantiate a Settings object
settings = openmc.Settings()

# Define particle settings (small for testing)
settings.batches = 10
settings.inactive = 0
settings.particles = 100

# Set temperature settings
settings.temperature = {'default': 560.0, 'method': 'interpolation'}

# Define energy mode and cross sections
settings.energy_mode = 'fixed source'

# Specify cross_sections.xml file location through environment variable
xsection_path = os.environ.get('OPENMC_CROSS_SECTIONS')
if xsection_path:
    settings.cross_sections = xsection_path
else:
    raise ValueError('OPENMC_CROSS_SECTIONS environment variable not set.')

# Specify chain_file.xml file location through environment variable
chain_file_path = os.environ.get('OPENMC_DEPLETE_CHAIN')
if chain_file_path:
    settings.chain_file = chain_file_path
else:
    print('OPENMC_DEPLETE_CHAIN environment variable not set. Depletion is not activated.')

# Define a point source
point = openmc.stats.Point((0, 0, 0))
source = openmc.Source(space=point)
source.energy = openmc.stats.Watt(a=0.988, b=0.00278)
source.strength = 1.0
settings.source = [source]

# Define output settings
settings.output = {
    'tallies': False, # Disable tallies for faster execution during testing
    'summary': True, # Retain summary file
    'path': 'results',
    'prefix': 'openmc'
}

# Set the seed
settings.seed = 1

# Export to XML
settings.export_to_xml('settings.xml')