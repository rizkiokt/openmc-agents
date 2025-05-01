'''
This Python script constructs the geometry for a Boiling Water Reactor (BWR) assembly using OpenMC. It defines the fuel rod, cladding, gap, and lattice structures based on the provided specifications.  The geometry is built using OpenMC's surface, cell, and universe objects, and the assembly layout is implemented with a lattice. Reflective boundary conditions are applied to the outer surfaces of the geometry.
'''
import openmc
import numpy as np

# Geometry Parameters
pellet_diameter = 0.8
cladding_outer_diameter = 0.95
gap_thickness = 0.008
fuel_rod_pitch = 1.6
lattice_size = 10
control_rod_diameter = 1.0
control_rod_length = 360.0

# Surfaces
fuel_or = openmc.Sphere(r=pellet_diameter/2)
clad_ir = openmc.Sphere(r=pellet_diameter/2 + gap_thickness)
clad_or = openmc.Sphere(r=cladding_outer_diameter/2)

# Rectangular prism for assembly
assembly_width = fuel_rod_pitch * lattice_size
min_x = openmc.XPlane(-assembly_width/2).translate((-1e-6, 0, 0))
max_x = openmc.XPlane(assembly_width/2).translate((1e-6, 0, 0))
min_y = openmc.YPlane(-assembly_width/2).translate((0, -1e-6, 0))
max_y = openmc.YPlane(assembly_width/2).translate((0, 1e-6, 0))
min_z = openmc.ZPlane(-control_rod_length/2)
max_z = openmc.ZPlane(control_rod_length/2)
min_x.boundary_type = 'reflective'
max_x.boundary_type = 'reflective'
min_y.boundary_type = 'reflective'
max_y.boundary_type = 'reflective'
min_z.boundary_type = 'vacuum'
max_z.boundary_type = 'vacuum'


# Cells
fuel_cell = openmc.Cell(name='fuel')
fuel_cell.fill = openmc.Material.from_xml('materials.xml', 'MOX')
fuel_cell.region = -fuel_or

gap_cell = openmc.Cell(name='gap')
gap_cell.region = +fuel_or & -clad_ir
gap_cell.fill = openmc.Material.from_xml('materials.xml', 'Water')

clad_cell = openmc.Cell(name='clad')
clad_cell.fill = openmc.Material.from_xml('materials.xml', 'Zircaloy')
clad_cell.region = +clad_ir & -clad_or


# Instantiate Universe
fuel_rod_universe = openmc.Universe()
fuel_rod_universe.add_cells([fuel_cell, gap_cell, clad_cell])

# Moderator cell
moderator_cell = openmc.Cell(name='moderator')
moderator_cell.fill = openmc.Material.from_xml('materials.xml', 'Water')

# Create a 1x1 universe containing only moderator
moderator_universe = openmc.Universe()
moderator_universe.add_cell(moderator_cell)

# Control rod cell and universe
control_rod_surf = openmc.Sphere(r=control_rod_diameter/2)
control_rod_cell = openmc.Cell(name='control_rod')
control_rod_cell.fill = openmc.Material.from_xml('materials.xml', 'B4C')
control_rod_cell.region = -control_rod_surf
control_rod_universe = openmc.Universe()
control_rod_universe.add_cell(control_rod_cell)

# Create the lattice
lattice = openmc.RectLattice(name='fuel_lattice')
lattice.pitch = [fuel_rod_pitch, fuel_rod_pitch]
lattice.lower_left = [-fuel_rod_pitch * lattice_size / 2, -fuel_rod_pitch * lattice_size / 2]
lattice.universes = np.empty((lattice_size, lattice_size), dtype=openmc.Universe)

# Fill the lattice with fuel rods, replace one with control rod
for i in range(lattice_size): 
    for j in range(lattice_size):
        lattice.universes[i,j] = fuel_rod_universe

# Replace center rod with control rod
lattice.universes[lattice_size//2, lattice_size//2] = control_rod_universe

# Create assembly cell and universe
assembly_cell = openmc.Cell(name='assembly')
assembly_cell.fill = lattice
assembly_cell.region = +min_x & -max_x & +min_y & -max_y & +min_z & -max_z
assembly_universe = openmc.Universe()
assembly_universe.add_cell(assembly_cell)

# Create geometry and assign root universe
geometry = openmc.Geometry()
geometry.root_universe = assembly_universe

# Export geometry
geometry.export_to_xml()