'''
This script constructs OpenMC material objects based on the provided design specifications. It defines materials for MOX fuel, Zircaloy cladding, water moderator/coolant, and Boron Carbide control rods. The script sets material compositions, densities, and temperatures as specified.
'''
import openmc

# Constants
avogadro = 6.02214076e23def create_materials():
    materials = openmc.Materials()

    # MOX Fuel
    mox = openmc.Material(name='MOX')
    mox.add_nuclide('Pu239', 0.05)
    mox.add_nuclide('U238', 0.95)
    mox.set_density('g/cm3', 10.5)
    materials.append(mox)

    # Zircaloy Cladding
    zircaloy = openmc.Material(name='Zircaloy')
    zircaloy.add_element('Zr', 0.98)
    zircaloy.add_element('Sn', 0.02)
    zircaloy.set_density('g/cm3', 6.55)
    materials.append(zircaloy)

    # Water Moderator/Coolant
    water = openmc.Material(name='Water')
    water.add_nuclide('H1', 2.0)
    water.add_nuclide('O16', 1.0)
    water.set_density('g/cm3', 1.0)
    water.add_s_alpha_beta('c_H_in_H2O') # add thermal scattering data
    materials.append(water)

    # Boron Carbide Control Rods
    boron_carbide = openmc.Material(name='Boron Carbide')
    boron_carbide.add_nuclide('B10', 0.2)
    boron_carbide.add_nuclide('B11', 0.8)
    boron_carbide.add_element('C', 1.0)
    boron_carbide.set_density('g/cm3', 2.52)
    materials.append(boron_carbide)

    return materials

if __name__ == '__main__':
    materials = create_materials()
    materials.export_to_xml('materials.xml')