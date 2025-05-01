'''
This code defines the materials used in a Boiling Water Reactor (BWR) based on the provided design specifications. It creates OpenMC material objects for MOX fuel, Zircaloy-4 cladding, and Water moderator/coolant, setting their compositions, densities, and temperatures as specified. The code adheres to OpenMC best practices for material modeling.
'''
import openmc

# Define functions for creating OpenMC materials

def create_materials():
    # Instantiate Materials
    materials = openmc.Materials()

    # MOX Fuel
    mox = openmc.Material(name='MOX')
    mox.add_nuclide('U235', 0.02)
    mox.add_nuclide('U238', 0.93)
    mox.add_nuclide('Pu239', 0.05)
    mox.set_density('g/cm3', 10.5)
    materials.append(mox)

    # Zircaloy-4 Cladding
    zircaloy = openmc.Material(name='Zircaloy-4')
    zircaloy.add_element('Zr', 0.98)
    zircaloy.add_element('Sn', 0.015)
    zircaloy.add_element('Fe', 0.002)
    zircaloy.add_element('Cr', 0.001)
    zircaloy.add_element('O', 0.002)
    zircaloy.set_density('g/cm3', 6.56)
    materials.append(zircaloy)

    # Water (Moderator/Coolant)
    water = openmc.Material(name='Water')
    water.add_nuclide('H1', 2.0)
    water.add_nuclide('O16', 1.0)
    water.set_density('g/cm3', 0.7)
    water.temperature = 560.0 # Kelvin
    materials.append(water)

    return materials

if __name__ == '__main__':
    materials = create_materials()
    materials.export_to_xml()
