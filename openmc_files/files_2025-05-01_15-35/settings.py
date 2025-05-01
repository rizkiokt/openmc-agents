'''
This code creates the OpenMC settings for a BWR simulation. It configures the simulation parameters, including particle count, batches, temperature settings, energy mode, source parameters, and output settings. The settings are tailored for a simplified BWR model based on the provided design specifications and follow OpenMC best practices for simulation setup.
'''
import openmc
import os

def create_settings():
    # Instantiate Settings object
    settings = openmc.Settings()

    # Define general settings
    settings.run_mode = 'k-eigenvalue'

    # Define cross sections and chain file (assuming they are set via environment variables)
    settings.cross_sections = os.environ.get('OPENMC_CROSS_SECTIONS')
    settings.chain_file = os.environ.get('OPENMC_CHAIN_FILE')

    # Define temperature settings
    settings.temperature = {
        'default': 560.0,  # Default temperature in Kelvin
        'method': 'interpolation',
        'range': (273.0, 1000.0) # Temperature range for interpolation
    }

    # Define energy mode
    settings.energy_mode = 'continuous-energy'

    # Define source settings
    source = openmc.Source(space=openmc.stats.Box([-7, -7, -1], [7, 7, 1]),
                           angle=openmc.stats.Isotropic(),
                           energy=openmc.stats.Watt(a=0.988, b=2.249e-9))
    settings.source = source

    # Define particle settings (small for testing)
    settings.batches = 10
    settings.inactive = 5
    settings.particles = 100

    # Define output settings
    settings.output = {
        'tallies': True,
        'summary': True,
        'path': 'results'
    }

    return settings

if __name__ == '__main__':
    settings = create_settings()
    settings.export_to_xml()