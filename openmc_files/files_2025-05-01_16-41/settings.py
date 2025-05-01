'''
This script sets up the OpenMC simulation settings for a BWR reactor model. It configures the simulation parameters such as particle number, batches, temperature, energy mode, source, and output settings, following OpenMC best practices.
'''
import openmc
import os

# Instantiate a Settings object
settings = openmc.Settings()

# Define simulation parameters
settings.batches = 10  # Reduced number of batches for testing
settings.inactive = 5  # Number of inactive batches
settings.particles = 1000  # Reduced number of particles for testing

# Set temperature
settings.temperature = {'default': 560.0}

# Create an energy filter
energy_filter = openmc.EnergyFilter(np.logspace(-3, 7, 101))

# Activate the 'entropy' maximization source sampling mode
settings.entropy_on = False

# Define a point source
point = openmc.stats.Point((0, 0, 0))
source = openmc.Source(space=point)
settings.source = source

# OpenMC best practices - set cross_sections and chain_file environment variables
os.environ['OPENMC_CROSS_SECTIONS'] = 'cross_sections.xml'
os.environ['OPENMC_DEPLETE_CHAIN'] = 'chain_endfb71.xml'

# Define the output files
settings.output = {
    'tallies': True,
    'summary': True,
    'path': 'results',
    'cross_sections': True
}

# Export to XML
settings.export_to_xml('settings.xml')