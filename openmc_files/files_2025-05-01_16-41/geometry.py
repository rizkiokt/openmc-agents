'''
This Python script constructs the geometry for a simplified BWR reactor model in OpenMC. It defines fuel rods, a square lattice arrangement, control rods, and reflective boundary conditions. The geometry is built using surfaces, cells, and universes, and the materials defined in the materials.xml file are assigned to the appropriate regions.
'''
import openmc
import numpy as np



# Geometry parameters
pellet_diameter = 0.8
cladding_outer_diameter = 0.95
gap_thickness = 0.008
lattice_pitch = 1.4
lattice_size = 10
control_rod_diameter = 1.0
control_rod_length = 360.0

# Create surfaces
fuel_or = openmc.Circle(r=pellet_diameter/2)
clad_ir = openmc.Circle(r=pellet_diameter/2 + gap_thickness)
clad_or = openmc.Circle(r=cladding_outer_diameter/2)

# Create cells
fuel_cell = openmc.Cell(name='Fuel Pellet')
fuel_cell.region = -fuel_or
fuel_cell.fill = 'MOX'

gap_cell = openmc.Cell(name='Gap')
gap_cell.region = +fuel_or & -clad_ir
gap_cell.fill = 'Water'

clad_cell = openmc.Cell(name='Cladding')
clad_cell.region = +clad_ir & -clad_or
clad_cell.fill = 'Zircaloy'

# Create a universe for the fuel rod
fuel_rod_universe = openmc.Universe(name='Fuel Rod')
fuel_rod_universe.add_cells([fuel_cell, gap_cell, clad_cell])

# Create surfaces for the lattice
lattice_lower_left = [-lattice_size/2 * lattice_pitch, -lattice_size/2 * lattice_pitch]

# Create the lattice
lattice = openmc.RectLattice(name='Fuel Lattice')
lattice.lower_left = lattice_lower_left
lattice.pitch = [lattice_pitch, lattice_pitch]
lattice.width = [lattice_pitch] * lattice_size
lattice.height = [lattice_pitch] * lattice_size

# Fill the lattice with fuel rod universes
lattice.universes = [[fuel_rod_universe] * lattice_size] * lattice_size

# Create a cell for the lattice
lattice_cell = openmc.Cell(name='Fuel Lattice Cell')
lattice_cell.fill = lattice

# Control rod geometry
control_rod_surface = openmc.Circle(r=control_rod_diameter / 2)
control_rod_cell = openmc.Cell(name='Control Rod')
control_rod_cell.region = -control_rod_surface
control_rod_cell.fill = 'B4C'

water_region = +control_rod_surface
water_cell = openmc.Cell(name='Water Moderator')
water_cell.region = water_region
water_cell.fill = 'Water'

control_rod_universe = openmc.Universe(name='Control Rod Assembly')
control_rod_universe.add_cells([control_rod_cell, water_cell])

# Create main universe
root_universe = openmc.Universe(name='Root Universe')
root_universe.add_cell(lattice_cell)

# Create the geometry
geometry = openmc.Geometry(root_universe)

# Boundary Conditions
x_min = openmc.XPlane(x0=-lattice_size/2 * lattice_pitch, boundary_type='reflective')
x_max = openmc.XPlane(x0=lattice_size/2 * lattice_pitch, boundary_type='reflective')
y_min = openmc.YPlane(y0=-lattice_size/2 * lattice_pitch, boundary_type='reflective')
y_max = openmc.YPlane(y0=lattice_size/2 * lattice_pitch, boundary_type='reflective')

geometry.root_universe.add_surface(x_min)
geometry.root_universe.add_surface(x_max)
geometry.root_universe.add_surface(y_min)
geometry.root_universe.add_surface(y_max)

# Export the geometry
geometry.export_to_xml('geometry.xml')