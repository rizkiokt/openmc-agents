'''
This script constructs the OpenMC settings for a Boiling Water Reactor (BWR) simulation. It configures the simulation parameters, including particle count, batches, temperature settings, energy mode, source parameters, and output settings. It adheres to OpenMC best practices for simulation configuration.
'''
import openmc
import os

# Define simulation settings
settings = openmc.Settings()

# Set temperature parameters
settings.temperature['method'] = 'interpolation'
settings.temperature['default'] = 294.0  # default temperature in Kelvin

# Define energy mode and cross sections
os.environ['OPENMC_CROSS_SECTIONS'] = 'cross_sections.xml'
os.environ['OPENMC_DEPLETE_CHAIN'] = 'chain_simple.xml'

# Set up source parameters
source = openmc.Source()
source.space = openmc.stats.Box([-7.0, -7.0, 0.0], [7.0, 7.0, 1.0])
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Watt(1.0)
settings.source = source

# Configure particle count and batches (small for testing)
settings.batches = 10
settings.inactive = 5
settings.particles = 100

# Configure output settings
settings.output = {
    'tallies': True,
    'summary': True,
    'path': 'results',
}

# Set up tallies (example, can be customized further)
tallies = openmc.Tallies()

# Add a flux tally over the entire geometry
cell_filter = openmc.CellFilter(openmc.Universe.get_by_name('root').cells.values())

flux_tally = openmc.Tally(name='flux')
flux_tally.filters = [cell_filter]
flux_tally.scores = ['flux']

tallies.append(flux_tally)

# Export to XML
settings.export_to_xml('settings.xml')
tallies.export_to_xml('tallies.xml')