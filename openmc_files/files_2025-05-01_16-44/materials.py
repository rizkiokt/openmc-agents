'''
This Python code creates OpenMC material objects based on the provided design specifications for a Boiling Water Reactor (BWR). It defines materials like MOX fuel, Zircaloy cladding, water moderator/coolant, and B4C control rods with their respective compositions, densities, and temperatures.
'''
import openmc



def create_materials():
    # Instantiate materials
    mats = openmc.Materials()

    # MOX Fuel
    mox = openmc.Material(name='MOX')
    mox.add_nuclide('Pu239', 0.05)
    mox.add_nuclide('U238', 0.95)
    mox.set_density('g/cm3', 10.5)
    mats.append(mox)

    # Zircaloy Cladding
    zircaloy = openmc.Material(name='Zircaloy')
    zircaloy.add_nuclide('Zr', 0.98)
    zircaloy.add_nuclide('Sn', 0.02)
    zircaloy.set_density('g/cm3', 6.55)
    mats.append(zircaloy)

    # Water Moderator/Coolant
    water = openmc.Material(name='Water')
    water.add_nuclide('H1', 2.0)
    water.add_nuclide('O16', 1.0)
    water.set_density('g/cm3', 0.7)
    water.add_s_alpha_beta('HH2O', '740K')
    mats.append(water)

    # B4C Control Rod
    b4c = openmc.Material(name='B4C')
    b4c.add_nuclide('B10', 0.2)
    b4c.add_nuclide('B11', 0.8)
    b4c.add_nuclide('C', 1.0)
    b4c.set_density('g/cm3', 2.52)
    mats.append(b4c)

    return mats

if __name__ == '__main__':
    materials = create_materials()
    materials.export_to_xml()
