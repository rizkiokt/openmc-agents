'''
This script generates an OpenMC geometry for a simplified BWR reactor based on the provided specifications. It constructs fuel rods, a lattice representing the fuel assembly, and control rods.  Reflective boundary conditions are applied to the outer surfaces of the geometry. The geometry includes fuel, cladding, coolant (water), and control rod materials.
'''
import openmc
import numpy as np



# Geometry parameters
fuel_pellet_radius = 0.82 / 2.0
cladding_inner_radius = fuel_pellet_radius + 0.008
cladding_outer_radius = 0.95 / 2.0
lattice_pitch = 1.4
lattice_size = 10
control_rod_diameter = 1.0
control_rod_radius = control_rod_diameter / 2.0
assembly_height = 360.0

# Materials (assuming materials.xml is already created)
materials = openmc.Materials.from_xml('materials.xml')
mox = materials['MOX']
zircaloy4 = materials['Zircaloy4']
water = materials['Water']
b4c = materials['B4C']

# Surfaces
fuel_surf = openmc.ZCylinder(r=fuel_pellet_radius)
clad_inner_surf = openmc.ZCylinder(r=cladding_inner_radius)
clad_outer_surf = openmc.ZCylinder(r=cladding_outer_radius)
assembly_top = openmc.ZPlane(z=assembly_height/2.0)
assembly_bottom = openmc.ZPlane(z=-assembly_height/2.0)

# Bounding box for the entire geometry (for reflective BCs)
min_x = -lattice_size / 2.0 * lattice_pitch
max_x = lattice_size / 2.0 * lattice_pitch
min_y = -lattice_size / 2.0 * lattice_pitch
max_y = lattice_size / 2.0 * lattice_pitch

x_min = openmc.XPlane(x0=min_x, boundary_type='reflective')
x_max = openmc.XPlane(x0=max_x, boundary_type='reflective')
y_min = openmc.YPlane(y0=min_y, boundary_type='reflective')
y_max = openmc.YPlane(y0=max_y, boundary_type='reflective')

# Cells
fuel_cell = openmc.Cell(name='Fuel Pellet')
fuel_cell.fill = mox
fuel_cell.region = -fuel_surf & +assembly_bottom & -assembly_top & +x_min & -x_max & +y_min & -y_max

gap_cell = openmc.Cell(name='Gap')
gap_cell.region = +fuel_surf & -clad_inner_surf & +assembly_bottom & -assembly_top & +x_min & -x_max & +y_min & -y_max

clad_cell = openmc.Cell(name='Cladding')
clad_cell.fill = zircaloy4
clad_cell.region = +clad_inner_surf & -clad_outer_surf & +assembly_bottom & -assembly_top & +x_min & -x_max & +y_min & -y_max

moderator_cell = openmc.Cell(name='Moderator')
moderator_cell.fill = water
moderator_cell.region = +clad_outer_surf & +assembly_bottom & -assembly_top & +x_min & -x_max & +y_min & -y_max

# Create fuel rod Universe
fuel_rod_universe = openmc.Universe(name='Fuel Rod')
fuel_rod_universe.add_cells([fuel_cell, gap_cell, clad_cell, moderator_cell])

# Control Rod Geometry
control_rod_surface = openmc.ZCylinder(r=control_rod_radius)
control_rod_cell = openmc.Cell(name='Control Rod')
control_rod_cell.fill = b4c
control_rod_cell.region = -control_rod_surface & +assembly_bottom & -assembly_top & +x_min & -x_max & +y_min & -y_max

control_rod_universe = openmc.Universe(name='Control Rod')
control_rod_universe.add_cell(control_rod_cell)

# Lattice
lattice = openmc.RectLattice(name='Fuel Lattice')
lattice.pitch = [lattice_pitch, lattice_pitch]
lattice.lower_left = [-lattice_size / 2.0 * lattice_pitch, -lattice_size / 2.0 * lattice_pitch]
lattice.universes = [[fuel_rod_universe] * lattice_size for _ in range(lattice_size)]

#Replace a central pin with control rod
lattice.universes[lattice_size//2][lattice_size//2] = control_rod_universe

# Create a Universe for the entire lattice
lattice_cell = openmc.Cell(name='Lattice Cell')
lattice_cell.fill = lattice
lattice_cell.region = +assembly_bottom & -assembly_top & +x_min & -x_max & +y_min & -y_max

root_universe = openmc.Universe(name='Root Universe')
root_universe.add_cell(lattice_cell)

# Create the Geometry object
geometry = openmc.Geometry(root_universe)

# Export the geometry to XML
geometry.export_to_xml('geometry.xml')