'''
This script creates OpenMC material objects based on the provided design specifications. It defines materials like UO2, PuO2, MOX, Zircaloy, Water, and Boron with their respective compositions, densities, and temperatures. The script adheres to OpenMC best practices for material modeling.
'''
import openmc

# Enable Just-In-Time compilation for improved performance
openmc.config['cross_sections'] = '/home/jovyan/chain_xs/cross_sections.xml'
openmc.config['chain_file'] = '/home/jovyan/chain_xs/chain_endfb71_pwr.xml'

def create_materials():
    materials = openmc.Materials()

    # UO2 Material
    uo2 = openmc.Material(name='UO2')
    uo2.add_nuclide('U235', 0.04)
    uo2.add_nuclide('U238', 0.96)
    uo2.set_density('g/cm3', 10.0)
    materials.append(uo2)

    # PuO2 Material
    puo2 = openmc.Material(name='PuO2')
    puo2.add_nuclide('Pu239', 0.7)
    puo2.add_nuclide('Pu240', 0.3)
    puo2.set_density('g/cm3', 11.0)
    materials.append(puo2)

    # MOX Material
    mox = openmc.Material(name='MOX')
    mox.add_element('U', 0.9, enrichment=4.0)  # Assuming UO2 is natural uranium with 4% U235
    mox.add_element('Pu', 0.1,  mass_fraction=1.0) # Assuming PuO2 is pure Plutonium
    mox.add_element('O', 2.0)
    mox.set_density('g/cm3', 10.5)
    materials.append(mox)

    # Zircaloy Material
    zircaloy = openmc.Material(name='Zircaloy')
    zircaloy.add_element('Zr', 0.98)
    zircaloy.add_element('Sn', 0.02)
    zircaloy.set_density('g/cm3', 6.5)
    zircaloy.temperature = 600.0
    materials.append(zircaloy)

    # Water Material
    water = openmc.Material(name='Water')
    water.add_nuclide('H1', 2.0)
    water.add_nuclide('O16', 1.0)
    water.set_density('g/cm3', 0.7)
    water.temperature = 560.0
    materials.append(water)

    # Boron Material
    boron = openmc.Material(name='Boron')
    boron.add_nuclide('B10', 0.2)
    boron.add_nuclide('B11', 0.8)
    boron.set_density('g/cm3', 2.34)
    materials.append(boron)

    return materials

# Create materials
materials = create_materials()

# Export to XML
materials.export_to_xml('materials.xml')
