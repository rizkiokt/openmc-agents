'''
This script generates OpenMC material definitions based on the provided design specifications for a BWR reactor. It creates materials for MOX fuel, Zircaloy4 cladding, Water moderator/coolant, and B4C control rods, setting their compositions, densities, and temperatures as specified.  The script includes temperature specifications for the coolant and utilizes OpenMC's built-in capabilities for defining materials and their properties.
'''
import openmc



# Define materials

# MOX Fuel
mox = openmc.Material(name='MOX')
mox.add_nuclide('Pu239', 0.05)
mox.add_nuclide('U238', 0.95)
mox.set_density('g/cm3', 10.5)

# Zircaloy-4 Cladding
zircaloy4 = openmc.Material(name='Zircaloy4')
zircaloy4.add_element('Zr', 0.98)
zircaloy4.add_element('Sn', 0.015)
zircaloy4.add_element('Fe', 0.002)
zircaloy4.add_element('Cr', 0.001)
zircaloy4.add_element('O', 0.002)
zircaloy4.set_density('g/cm3', 6.56)

# Water (Moderator/Coolant)
water = openmc.Material(name='Water')
water.add_nuclide('H1', 2.0)
water.add_nuclide('O16', 1.0)
water.set_density('g/cm3', 0.73)

# B4C Control Rods
b4c = openmc.Material(name='B4C')
b4c.add_element('B', 4.0)
b4c.add_element('C', 1.0)
b4c.set_density('g/cm3', 2.52) # Typical density for B4C

# Coolant Temperature
coolant_temperature = 560.0 # Kelvin

# Assign temperature to water
water.temperature = coolant_temperature

# Create a Materials collection
materials = openmc.Materials([mox, zircaloy4, water, b4c])

# Export to XML
materials.export_to_xml('materials.xml')