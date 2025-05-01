'''
This script creates OpenMC material definitions based on the provided specifications for a BWR reactor. It defines materials like MOX fuel, Zircaloy cladding, Water moderator, and B4C control rods, setting their compositions, densities, and temperatures.
'''
import openmc



materials = openmc.Materials()

# MOX Fuel
mox = openmc.Material(name='MOX')
mox.add_nuclide('U235', 0.02)
mox.add_nuclide('U238', 0.93)
mox.add_nuclide('Pu239', 0.05)
mox.set_density('g/cm3', 10.5)
materials.append(mox)

# Zircaloy Cladding
zircaloy = openmc.Material(name='Zircaloy')
zircaloy.add_element('Zr', 0.98)
zircaloy.add_element('Sn', 0.02)
zircaloy.set_density('g/cm3', 6.55)
materials.append(zircaloy)

# Water Moderator
water = openmc.Material(name='Water')
water.add_nuclide('H1', 2.0)
water.add_nuclide('O16', 1.0)
water.set_density('g/cm3', 0.7)
water.add_s_alpha_beta('c_H_in_H2O')
materials.append(water)

# B4C Control Rod
b4c = openmc.Material(name='B4C')
b4c.add_nuclide('B10', 0.2)
b4c.add_nuclide('B11', 0.8)
b4c.add_element('C', 1.0)
b4c.set_density('g/cm3', 2.52)
materials.append(b4c)


# Export to XML
materials.export_to_xml('materials.xml')