'''
This script sets up the OpenMC simulation settings for a BWR reactor model. It configures the particle transport parameters, temperature settings, energy mode, source definition, and output options for the simulation.
'''
import openmc
import os

def create_settings():
    # settings.xml
    settings = openmc.Settings()
    settings.run_mode = 'k-eigenvalue'

    # Define temperature parameters
    settings.temperature['method'] = 'interpolation'
    settings.temperature['default'] = 273.15 + 25  # room temperature

    # Energy mode and cross sections
    settings.energy_mode = 'continuous-energy'
    # assumes cross_sections.xml and chain_xs.xml are in env
    settings.cross_sections = os.environ.get('OPENMC_CROSS_SECTIONS')
    settings.photon_transport = False # disable photon transport to speed up calculation

    # Source definition
    source = openmc.Source()
    source.space = openmc.stats.Point((0,0,0))
    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Watt(a=0.988, b=0.001074) # fission energy distribution
    settings.source = source

    # Set up transport parameters
    settings.batches = 20 # increased batches
    settings.inactive = 5  # increased inactive batches
    settings.particles = 100 # reduced particles
    settings.keff_trigger = {'type': 'std_dev', 'threshold': 0.001}

    # Output settings
    settings.output = {
        'tallies': False,  # disable tallies.xml
        'summary': True, # keep summary.h5
        'path': 'results',
        'prefix': 'openmc'}

    # Set seed for reproducibility
    settings.seed = 1

    return settings

if __name__ == '__main__':
    settings = create_settings()
    settings.export_to_xml('settings.xml')