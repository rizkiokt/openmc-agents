'''
This script creates OpenMC material objects based on the provided design specifications for a BWR reactor. It defines materials for MOX fuel, Zircaloy-4 cladding, water moderator/coolant, and B4C control rods. Densities and compositions are set according to the specifications. Temperature is not explicitly set for the materials as the specification did not provide exact values. However, the Coolant temperature is provided, which could be used to set the temperature of the water material.
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

# Water Moderator/Coolant
water = openmc.Material(name='Water')
water.add_nuclide('H1', 2.0)
water.add_nuclide('O16', 1.0)
water.set_density('g/cm3', 0.73)

# B4C Control Rod Material
b4c = openmc.Material(name='B4C')
b4c.add_element('B', 4.0)
b4c.add_element('C', 1.0)
b4c.set_density('g/cm3', 2.52) # Typical density for B4C

# Create a Materials object and export to XML
materials = openmc.Materials([mox, zircaloy4, water, b4c])
materials.export_to_xml()

print("materials.xml file created")