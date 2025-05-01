'''
This script constructs the geometry for a BWR reactor based on the provided specifications. It defines the fuel rod, assembly lattice, and overall reactor geometry using OpenMC's surface, cell, and universe objects.  The geometry is then exported to an XML file for use in OpenMC simulations.
'''
import openmc
import numpy as np

# Define geometry

# Fuel Rod
fuel_or = openmc.Circle(r=0.8/2) # pellet_diameter/2
clad_ir = openmc.Circle(r=0.8/2 + 0.008) # pellet_diameter/2 + gap_thickness
clad_or = openmc.Circle(r=0.9/2) # cladding_outer_diameter/2

fuel_surf = openmc.ZCylinder(x0=0.0, y0=0.0, r=0.8/2) # pellet_diameter/2
gap_surf = openmc.ZCylinder(x0=0.0, y0=0.0, r=0.8/2 + 0.008) # pellet_diameter/2 + gap_thickness
clad_surf = openmc.ZCylinder(x0=0.0, y0=0.0, r=0.9/2) # cladding_outer_diameter/2
top = openmc.ZPlane(z0=180.0) # length/2
bottom = openmc.ZPlane(z0=-180.0) # -length/2

top_half = openmc.HalfSpace(top)
bottom_half = openmc.HalfSpace(bottom)

fuel_cell = openmc.Cell(name='Fuel')
fuel_cell.fill = mox
fuel_cell.region = -fuel_surf & +bottom_half & -top_half

gap_cell = openmc.Cell(name='Gap')
gap_cell.region = +fuel_surf & -gap_surf & +bottom_half & -top_half

clad_cell = openmc.Cell(name='Cladding')
clad_cell.fill = zircaloy
clad_cell.region = +gap_surf & -clad_surf & +bottom_half & -top_half


fuel_rod_universe = openmc.Universe()
fuel_rod_universe.add_cells([fuel_cell, gap_cell, clad_cell])

# Assembly Lattice
lattice = openmc.RectLattice(name='Fuel Assembly Lattice')
lattice.pitch = [1.5, 1.5]
lattice.lower_left = [-7.5, -7.5] # -pitch * size / 2
lattice.width = [1.5]*10
lattice.height = [1.5]*10



# Fill lattice with fuel rods
for i in range(10):
    for j in range(10):
        lattice.universes[i][j] = fuel_rod_universe


assembly_cell = openmc.Cell(name='Fuel Assembly')
assembly_cell.fill = lattice

assembly_universe = openmc.Universe()
assembly_universe.add_cell(assembly_cell)

# Reactor Core

# Surfaces for the core
core_radius = 10 * 1.5 / 2 # size * pitch / 2
core_top = openmc.ZPlane(z0=180.0) # length/2
core_bottom = openmc.ZPlane(z0=-180.0) # -length/2
core_or = openmc.ZCylinder(r=core_radius)

core_top_half = openmc.HalfSpace(core_top)
core_bottom_half = openmc.HalfSpace(core_bottom)

# Cells for the core
core_cell = openmc.Cell(name='Core')
core_cell.fill = assembly_universe
core_cell.region = -core_or & +core_bottom_half & -core_top_half

# Reflector
reflector_inner_surf = openmc.ZCylinder(r=core_radius)
reflector_outer_surf = openmc.ZCylinder(r=core_radius + 20.0)

reflector_cell = openmc.Cell(name='Reflector')
reflector_cell.fill = water
reflector_cell.region = +reflector_inner_surf & -reflector_outer_surf & +core_bottom_half & -core_top_half

# Reactor
root_universe = openmc.Universe()
root_universe.add_cells([core_cell, reflector_cell])


# Create geometry and assign the root universe
geometry = openmc.Geometry()
geometry.root_universe = root_universe

# Apply reflective boundary conditions
geometry.bounding_box = [(-100,-100,-180), (100,100,180)]

# Export to XML
geometry.export_to_xml('geometry.xml')