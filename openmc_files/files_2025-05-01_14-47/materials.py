'''
This script constructs OpenMC materials based on the provided design specifications. It defines three materials: MOX fuel, Zircaloy cladding, and Water moderator/coolant. The script sets the compositions, densities, and temperatures for each material using the OpenMC Python API.
'''
import openmc

# Define materials
materials = openmc.Materials()

# MOX fuel
mox = openmc.Material(name='MOX')
mox.add_nuclide('Pu239', 0.05)
mox.add_nuclide('U238', 0.95)
mox.set_density('g/cm3', 10.5)
materials.append(mox)

# Zircaloy cladding
zircaloy = openmc.Material(name='Zircaloy')
zircaloy.add_element('Zr', 0.98)
zircaloy.add_element('Sn', 0.02)
zircaloy.set_density('g/cm3', 6.55)
materials.append(zircaloy)

# Water moderator/coolant
water = openmc.Material(name='Water')
water.add_nuclide('H1', 2.0)
water.add_nuclide('O16', 1.0)
water.set_density('g/cm3', 0.7)
water.add_s_alpha_beta('c_H_in_H2O')
materials.append(water)


# Export to XML
materials.export_to_xml('materials.xml')