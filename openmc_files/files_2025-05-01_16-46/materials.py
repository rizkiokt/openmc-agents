'''
This script creates OpenMC material objects based on the provided design specifications for a BWR reactor. It defines MOX fuel, Zircaloy cladding, Water moderator/coolant/reflector, and B4C control rod materials with their respective compositions, densities, and temperatures.
'''
import openmc

# Define useful constants
kelvin_to_eV = 8.617333262e-5  # eV/K

def create_materials():

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

    # Water Moderator/Coolant/Reflector
    water = openmc.Material(name='Water')
    water.add_nuclide('H1', 2.0)
    water.add_nuclide('O16', 1.0)
    water.set_density('g/cm3', 0.73)
    water.add_s_alpha_beta('HH2O', 'thermal') # add thermal scattering data
    materials.append(water)
    
    # B4C Control Rod
    b4c = openmc.Material(name='B4C')
    b4c.add_element('B', 4.0)
    b4c.add_element('C', 1.0)
    b4c.set_density('g/cm3', 2.52) # Typical density of B4C
    materials.append(b4c)

    return materials

if __name__ == '__main__':
    materials = create_materials()
    materials.export_to_xml('materials.xml')
