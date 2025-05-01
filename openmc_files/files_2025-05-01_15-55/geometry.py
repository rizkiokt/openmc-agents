'''
This script constructs the geometry for a BWR reactor using OpenMC, based on the provided specifications. It defines surfaces, cells, and universes to represent the fuel rods, cladding, moderator, and assembly lattice. Reflective boundary conditions are applied.
'''
import openmc
import numpy as np

# Geometry parameters
pellet_diameter_mox = 0.8
cladding_outer_diameter_mox = 0.9
gap_thickness_mox = 0.008

pellet_diameter_uo2 = 0.8
cladding_outer_diameter_uo2 = 0.9
gap_thickness_uo2 = 0.008

lattice_pitch = 1.4
lattice_size = 10

control_rod_diameter = 1.0
control_rod_length = 360.0

# Materials (assumed to be defined in a separate materials.xml file)
materials = openmc.Materials.from_xml('materials.xml')

# Find materials in the materials list
water = materials['Water']
mox = materials['MOX']
uo2 = materials['UO2']
zircaloy = materials['Zircaloy']
b4c = materials['B4C']

# Surfaces
# Fuel Rod (MOX)
pellet_outer_radius_mox = openmc.Sphere(r=pellet_diameter_mox / 2)
gap_outer_radius_mox = openmc.Sphere(r=pellet_diameter_mox / 2 + gap_thickness_mox)
cladding_outer_radius_mox = openmc.Sphere(r=cladding_outer_diameter_mox / 2)

# Fuel Rod (UO2)
pellet_outer_radius_uo2 = openmc.Sphere(r=pellet_diameter_uo2 / 2)
gap_outer_radius_uo2 = openmc.Sphere(r=pellet_diameter_uo2 / 2 + gap_thickness_uo2)
cladding_outer_radius_uo2 = openmc.Sphere(r=cladding_outer_diameter_uo2 / 2)

# Assembly Lattice
assembly_lower_left = openmc.Rectangle(x0=-lattice_pitch * lattice_size / 2, y0=-lattice_pitch * lattice_size / 2, x1=lattice_pitch * lattice_size / 2, y1=lattice_pitch * lattice_size / 2)

# Control Rod
control_rod_radius = openmc.Sphere(r=control_rod_diameter / 2)
control_rod_top = openmc.ZPlane(z0=control_rod_length/2)
control_rod_bottom = openmc.ZPlane(z0=-control_rod_length/2)

# Cells
# Fuel Rod (MOX)
pellet_cell_mox = openmc.Cell(name='MOX Pellet', fill=mox, region=-pellet_outer_radius_mox)
gap_cell_mox = openmc.Cell(name='Gap (MOX)', fill=water, region=+pellet_outer_radius_mox & -gap_outer_radius_mox)
cladding_cell_mox = openmc.Cell(name='Cladding (MOX)', fill=zircaloy, region=+gap_outer_radius_mox & -cladding_outer_radius_mox)

# Fuel Rod (UO2)
pellet_cell_uo2 = openmc.Cell(name='UO2 Pellet', fill=uo2, region=-pellet_outer_radius_uo2)
gap_cell_uo2 = openmc.Cell(name='Gap (UO2)', fill=water, region=+pellet_outer_radius_uo2 & -gap_outer_radius_uo2)
cladding_cell_uo2 = openmc.Cell(name='Cladding (UO2)', fill=zircaloy, region=+gap_outer_radius_uo2 & -cladding_outer_radius_uo2)

# Moderator
moderator_cell = openmc.Cell(name='Moderator', fill=water, region=+cladding_outer_radius_mox & +cladding_outer_radius_uo2)

# Control Rod
control_rod_cell = openmc.Cell(name='Control Rod', fill=b4c, region=-control_rod_radius & +control_rod_bottom & -control_rod_top)

# Universes
# Fuel Rod (MOX)
fuel_rod_universe_mox = openmc.Universe(cells=[pellet_cell_mox, gap_cell_mox, cladding_cell_mox])

# Fuel Rod (UO2)
fuel_rod_universe_uo2 = openmc.Universe(cells=[pellet_cell_uo2, gap_cell_uo2, cladding_cell_uo2])

# Control Rod Universe
control_rod_universe = openmc.Universe(cells=[control_rod_cell])

# Assembly
assembly_universe = openmc.Universe(name='Assembly')

# Create a 2D array of universes for the lattice
universes = np.empty((lattice_size, lattice_size), dtype=openmc.Universe)

# Fill the lattice with fuel rods (MOX and UO2, alternating pattern)
for i in range(lattice_size): 
    for j in range(lattice_size):
        if (i + j) % 2 == 0:
            universes[i, j] = fuel_rod_universe_mox
        else:
            universes[i, j] = fuel_rod_universe_uo2

# Place the control rod in the center
universes[lattice_size//2, lattice_size//2] = control_rod_universe

# Create the lattice
lattice = openmc.RectLattice(name='Fuel Lattice')
lattice.lower_left = [-lattice_pitch * lattice_size / 2, -lattice_pitch * lattice_size / 2]
lattice.pitch = [lattice_pitch, lattice_pitch]
lattice.universes = universes.tolist()

# Create a cell for the lattice
lattice_cell = openmc.Cell(name='Lattice Cell', fill=lattice, region=-assembly_lower_left)

# Place the lattice in the assembly universe
assembly_universe.add_cell(lattice_cell)

# Root Universe
root_universe = openmc.Universe(name='Root')
root_universe.add_cell(openmc.Cell(name='Assembly Cell', fill=assembly_universe))

# Geometry
geometry = openmc.Geometry(root_universe)

# Boundary Conditions
geometry.export_to_xml('geometry.xml')

# OpenMC Settings
settings = openmc.Settings()
settings.particles = 1000
settings.inactive = 10
settings.batches = 50

# Create a box source
boundary = lattice_pitch * lattice_size / 2
source = openmc.Source()
source.space = openmc.stats.Box([-boundary, -boundary, -1], [boundary, boundary, 1])
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Watt(1.0)
settings.source = source

# Reflective Boundary Conditions
surface1 = openmc.XPlane(x0=-boundary, boundary_type='reflective')
surface2 = openmc.XPlane(x0=boundary, boundary_type='reflective')
surface3 = openmc.YPlane(y0=-boundary, boundary_type='reflective')
surface4 = openmc.YPlane(y0=boundary, boundary_type='reflective')
surface5 = openmc.ZPlane(z0=-100, boundary_type='reflective')
surface6 = openmc.ZPlane(z0=100, boundary_type='reflective')

settings.export_to_xml('settings.xml')