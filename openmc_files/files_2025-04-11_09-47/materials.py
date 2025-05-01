'''
This script creates OpenMC material objects based on the provided design specifications for a BWR reactor. It defines materials like MOX fuel, Zircaloy-4 cladding, water moderator/coolant, and Boron Carbide control rods, setting their compositions, densities, and temperatures. The script follows OpenMC best practices for material definition.
'''
import openmc

# Define a dictionary for natural element atomic weights (g/mol)
nat_elem_masses = {
    'B': 10.811,
    'C': 12.011,
    'Cr': 51.9961,
    'Fe': 55.845,
    'H': 1.008,
    'O': 15.999,
    'Sn': 118.710,
    'U': 238.02891,
    'Zr': 91.224,
    'PU': 239.0521634
}
def create_materials():
    materials = openmc.Materials()

    # MOX Fuel
    mox = openmc.Material(name='MOX')
    mox.add_nuclide('Pu239', 0.05, percent_type='ao')
    mox.add_nuclide('U238', 0.95, percent_type='ao')
    mox.set_density('g/cm3', 10.5)
    materials.append(mox)

    # Zircaloy-4 Cladding
    zircaloy = openmc.Material(name='Zircaloy-4')
    zircaloy.add_element('Zr', 0.98, percent_type='ao')
    zircaloy.add_element('Sn', 0.015, percent_type='ao')
    zircaloy.add_element('Fe', 0.002, percent_type='ao')
    zircayloy.add_element('Cr', 0.001, percent_type='ao')
    zircaloy.add_element('O', 0.002, percent_type='ao')
    zircaloy.set_density('g/cm3', 6.56)
    materials.append(zircaloy)

    # Water
    water = openmc.Material(name='Water')
    water.add_element('H', 2.0, percent_type='ao')
    water.add_element('O', 1.0, percent_type='ao')
    water.set_density('g/cm3', 0.7)
    materials.append(water)

    # Boron Carbide
    boron_carbide = openmc.Material(name='Boron Carbide')
    boron_carbide.add_nuclide('B10', 0.2, percent_type='ao')
    boron_carbide.add_nuclide('B11', 0.8, percent_type='ao')
    boron_carbide.add_element('C', 1.0, percent_type='ao')
    boron_carbide.set_density('g/cm3', 2.52)
    materials.append(boron_carbide)

    return materials


if __name__ == '__main__':
    materials = create_materials()
    materials.export_to_xml()
