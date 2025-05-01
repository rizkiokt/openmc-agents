'''
This script generates the OpenMC settings XML file for a simplified BWR reactor simulation. It configures the simulation parameters such as particle count, number of inactive and active batches, temperature settings, energy mode, and source parameters. It also sets up the output settings to produce statepoint and summary files for post-processing and analysis. The script adheres to OpenMC best practices to ensure accurate and efficient simulation.
'''
import openmc

# Enable Just-In-Time compilation for improved performance
openmc.config['cross_sections'] = '/home/jovyan/chain_xs/cross_sections.xml'
openmc.config['chain_file'] = '/home/jovyan/chain_xs/chain_endfb71_pwr.xml'

def create_settings():
    # Instantiate a Settings object
    settings = openmc.Settings()

    # Define runtime parameters
    settings.batches = 200
    settings.inactive = 50
    settings.particles = 10000

    # Set temperature parameters
    settings.temperature = {'default': 560.0, 'method': 'interpolation'}

    # Define energy mode and cross sections
    settings.energy_mode = 'fixed source'

    # Create a DT source
    source = openmc.Source(space=openmc.stats.Box([-1, -1, -1], [1, 1, 1]))
    settings.source = source

    # Define output settings
    settings.output = {
        'summary': True,
        'statepoint': True,
    }

    # Set the source
    source = openmc.Source()
    source.space = openmc.stats.Box([-1, -1, -1], [1, 1, 1])
    settings.source = source

    # Export to XML
    settings.export_to_xml('settings.xml')

# Create settings
create_settings()
