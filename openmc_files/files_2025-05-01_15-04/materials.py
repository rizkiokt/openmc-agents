'''
This script constructs OpenMC materials based on the provided specifications for a Boiling Water Reactor (BWR). It defines materials like MOX fuel, Zircaloy cladding, water moderator/coolant, and B4C control rods, setting their compositions, densities, and temperatures as specified.  The script leverages the OpenMC Python API to create and configure these materials.
'''
import openmc

# Define a dictionary for natural element atomic weight fractions
nat_w = {'B10': 0.199, 'B11': 0.801, 'Zr': 1.0, 'Sn': 1.0, 'H1': 1.0, 'O16': 1.0, 'U235': 1.0, 'U238': 1.0, 'Pu239': 1.0, 'C': 1.0}

# Define a function to create an OpenMC material from a composition dictionary
def create_material(name, composition, density, temperature=None):
    mat = openmc.Material(name=name)
    mat.set_density('g/cm3', density)
    for nuclide, atom_frac in composition.items():
        mat.add_nuclide(nuclide, atom_frac, 'ao')
    if temperature:
        mat.temperature = temperature
    return mat

# Instantiate Materials
materials = openmc.Materials()

# MOX Fuel
mox = create_material(
    name='MOX',
    composition={'U235': 0.02, 'U238': 0.93, 'Pu239': 0.05},
    density=10.5
)
materials.append(mox)

# Zircaloy Cladding
zircaloy = create_material(
    name='Zircaloy',
    composition={'Zr': 0.98, 'Sn': 0.02},
    density=6.55
)
materials.append(zircaloy)

# Water (Moderator/Coolant)
water = create_material(
    name='Water',
    composition={'H1': 2.0, 'O16': 1.0},
    density=0.7
)
materials.append(water)

# B4C (Control Rods)
b4c = create_material(
    name='B4C',
    composition={'B10': 0.2, 'B11': 0.8, 'C': 1.0},
    density=2.52
)
materials.append(b4c)

# Export to XML
materials.export_to_xml()
