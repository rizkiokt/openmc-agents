'''
This script creates an OpenMC geometry for a simplified BWR assembly based on the provided specifications. It defines fuel rods with MOX fuel and Zircaloy cladding, arranges them in a square lattice, and surrounds the assembly with water moderator. Control rods are also included.
'''
import openmc

# Geometry

# Define surfaces
pellet_radius = openmc.ZCylinder(r=0.82/2) # Pellet diameter is 0.82 cm
gap_radius = openmc.ZCylinder(r=0.82/2 + 0.008) # gap thickness is 0.008 cm
clad_radius = openmc.ZCylinder(r=0.95/2) # Cladding outer diameter is 0.95 cm

# Assembly bounding box (square)
assembly_pitch = 1.26 # Lattice pitch is 1.26 cm
assembly_size = 10 # 10x10 lattice

min_x = openmc.XPlane(x0=-assembly_size/2 * assembly_pitch).translate((-assembly_pitch/2,0,0))
max_x = openmc.XPlane(x0=assembly_size/2 * assembly_pitch).translate((assembly_pitch/2,0,0))
min_y = openmc.YPlane(y0=-assembly_size/2 * assembly_pitch).translate((0,-assembly_pitch/2,0))
max_y = openmc.YPlane(y0=assembly_size/2 * assembly_pitch).translate((0,assembly_pitch/2,0))
min_x.boundary_type = 'reflective'
max_x.boundary_type = 'reflective'
min_y.boundary_type = 'reflective'
max_y.boundary_type = 'reflective'

# Control rod surfaces (assuming withdrawn position for simplicity)
control_rod_radius = openmc.ZCylinder(r=1.0/2) # Control rod diameter is 1.0 cm

# Define cells

# Fuel Pellet
pellet_cell = openmc.Cell(name='Fuel Pellet')
pellet_cell.fill = 'MOX'
pellet_cell.region = -pellet_radius

# Gap
gap_cell = openmc.Cell(name='Gap')
gap_cell.fill = 'Water'
gap_cell.region = +pellet_radius & -gap_radius

# Cladding
clad_cell = openmc.Cell(name='Cladding')
clad_cell.fill = 'Zircaloy4'
clad_cell.region = +gap_radius & -clad_radius

# Moderator (outside cladding)
moderator_cell = openmc.Cell(name='Moderator')
moderator_cell.fill = 'Water'
moderator_cell.region = +clad_radius

# Control Rod
control_rod_cell = openmc.Cell(name='Control Rod')
control_rod_cell.fill = 'B4C'
control_rod_cell.region = -control_rod_radius

# Create a 1-fuel rod universe
fuel_rod_universe = openmc.Universe(name='Fuel Rod Universe')
fuel_rod_universe.add_cells([pellet_cell, gap_cell, clad_cell, moderator_cell])

# Control Rod universe
control_rod_universe = openmc.Universe(name='Control Rod Universe')
control_rod_universe.add_cell(control_rod_cell)

# Create a lattice
lattice = openmc.RectLattice(name='Fuel Lattice')
lattice.pitch = [assembly_pitch, assembly_pitch]
lattice.lower_left = [-assembly_size/2 * assembly_pitch, -assembly_size/2 * assembly_pitch]
lattice.width = [assembly_pitch] * assembly_size
lattice.height = [assembly_pitch] * assembly_size

# Fill the lattice with fuel rods, and put a control rod in the center
lattice.universes = [[fuel_rod_universe] * assembly_size for _ in range(assembly_size)]
lattice.universes[assembly_size//2][assembly_size//2] = control_rod_universe


# Create a universe for the entire assembly
assembly_universe = openmc.Universe(name='Assembly Universe')
assembly_cell = openmc.Cell(name='Assembly Cell')
assembly_cell.fill = lattice
assembly_cell.region = +min_x & -max_x & +min_y & -max_y
assembly_universe.add_cell(assembly_cell)

# Create the root universe
root_universe = openmc.Universe(name='Root Universe')
root_universe.add_cell(openmc.Cell(name='Root Cell', fill=assembly_universe, region=+min_x & -max_x & +min_y & -max_y))

# Create the geometry and assign the root universe
geometry = openmc.Geometry(root_universe)

# Export the geometry to XML
geometry.export_to_xml('geometry.xml')