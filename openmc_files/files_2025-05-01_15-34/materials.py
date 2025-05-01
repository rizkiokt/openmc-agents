'''
This script constructs OpenMC material objects based on the provided design specifications for a Boiling Water Reactor (BWR). It defines materials like MOX fuel, Zircaloy cladding, water moderator/coolant, and Boron Carbide control rods. The script sets the composition, density, and temperature (where applicable) for each material.
'''
import openmc



# Define materials

# MOX Fuel
mox = openmc.Material(name='MOX')
mox.add_nuclide('U235', 0.02)
mox.add_nuclide('U238', 0.93)
mox.add_nuclide('Pu239', 0.05)
mox.set_density('g/cm3', 10.5)

# Zircaloy Cladding
zircaloy = openmc.Material(name='Zircaloy')
zircaloy.add_element('Zr', 0.98)
zircaloy.add_element('Sn', 0.02)
zircaloy.set_density('g/cm3', 6.55)

# Water Moderator/Coolant
water = openmc.Material(name='Water')
water.add_nuclide('H1', 2.0)
water.add_nuclide('O16', 1.0)
water.set_density('g/cm3', 0.7)
water.add_sapt(openmc.data.get_thermal_name('H1', 'HH2O'))

# Boron Carbide Control Rod
boron_carbide = openmc.Material(name='Boron Carbide')
boron_carbide.add_nuclide('B10', 0.2)
boron_carbide.add_nuclide('B11', 0.8)
boron_carbide.add_element('C', 1.0)
boron_carbide.set_density('g/cm3', 2.52)

# Create a Materials collection
materials = openmc.Materials([mox, zircaloy, water, boron_carbide])

# Export to XML
materials.export_to_xml('materials.xml')