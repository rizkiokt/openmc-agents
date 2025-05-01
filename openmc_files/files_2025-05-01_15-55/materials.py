'''
This script creates OpenMC material objects based on the provided design specifications for a BWR reactor. It defines materials like UO2, PuO2, MOX, Zircaloy, and Water, setting their compositions, densities, and temperatures. It includes handling for different isotopes and compounds.
'''
import openmc

# Constants
AVOGADRO = 6.02214179e-24

# Define materials
materials = openmc.Materials()

# UO2 Material
uo2 = openmc.Material(name='UO2')
uo2.add_nuclide('U235', 0.04)
uo2.add_nuclide('U238', 0.96)
uo2.add_element('O', 2.0)
uo2.set_density('g/cm3', 10.5)
materials.append(uo2)

# PuO2 Material
puo2 = openmc.Material(name='PuO2')
puo2.add_nuclide('Pu239', 0.7)
puo2.add_nuclide('Pu240', 0.3)
puo2.add_element('O', 2.0)
puo2.set_density('g/cm3', 11.0)
materials.append(puo2)

# MOX Material
mox = openmc.Material(name='MOX')
mox.add_element('U', 0.9, enrichment=4.0)
mox.add_nuclide('Pu239', 0.1*0.7)
mox.add_nuclide('Pu240', 0.1*0.3)
mox.add_element('O', 2.0)
mox.set_density('g/cm3', 10.6)
materials.append(mox)

# Zircaloy Material
zircaloy = openmc.Material(name='Zircaloy')
zircaloy.add_element('Zr', 0.98)
zircaloy.add_element('Sn', 0.02)
zircaloy.set_density('g/cm3', 6.55)
materials.append(zircaloy)

# Water Material
water = openmc.Material(name='Water')
water.add_nuclide('H1', 2.0)
water.add_nuclide('O16', 1.0)
water.set_density('g/cm3', 1.0)
water.add_s_alpha_beta('c_H_in_H2O')
materials.append(water)

# B4C Material
b4c = openmc.Material(name='B4C')
b4c.add_element('B', 4.0)
b4c.add_element('C', 1.0)
b4c.set_density('g/cm3', 2.52)
materials.append(b4c)

# Export to XML
materials.export_to_xml('materials.xml')