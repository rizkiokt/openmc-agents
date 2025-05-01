'''
This Python script constructs an OpenMC geometry for a simplified Boiling Water Reactor (BWR) assembly. It defines the fuel rod, cladding, and coolant regions based on the provided specifications, arranges them in a square lattice, and creates the necessary cells and universes for the simulation. The geometry includes reflective boundary conditions and incorporates the materials defined in the materials.xml file.
'''
import openmc
import numpy as np



# Define geometry

# Define surfaces
pellet_radius = 0.8 / 2.0
gap_radius = 0.8 / 2.0 + 0.008
clad_radius = 0.95 / 2.0
assembly_pitch = 15.0
reflector_thickness = 20.0

# Fuel Pellet Surface
fuel_surf = openmc.Circle(r=pellet_radius)
fuel_or = openmc.ZCylinder(r=pellet_radius)

# Gap Surface
gap_surf = openmc.Circle(r=gap_radius)
gap_or = openmc.ZCylinder(r=gap_radius)

# Clad Surface
clad_surf = openmc.Circle(r=clad_radius)
clad_or = openmc.ZCylinder(r=clad_radius)

# Assembly Surface
assembly_surf = openmc.Square(side=assembly_pitch)
assembly_ur = openmc.XPlane(x0=-assembly_pitch/2.0, boundary_type='reflective')
assembly_ul = openmc.XPlane(x0=assembly_pitch/2.0, boundary_type='reflective')
assembly_vr = openmc.YPlane(y0=-assembly_pitch/2.0, boundary_type='reflective')
assembly_vt = openmc.YPlane(y0=assembly_pitch/2.0, boundary_type='reflective')

# Reflector Surfaces
lower_reflector = openmc.ZPlane(z0=-reflector_thickness, boundary_type='reflective')
upper_reflector = openmc.ZPlane(z0=360.0 + reflector_thickness, boundary_type='reflective')

# Define cells
# Fuel Cell
fuel_cell = openmc.Cell(name='Fuel')
fuel_cell.fill = 'MOX'
fuel_cell.region = -fuel_or

# Gap Cell
gap_cell = openmc.Cell(name='Gap')
gap_cell.fill = 'Water'
gap_cell.region = +fuel_or & -gap_or

# Clad Cell
clad_cell = openmc.Cell(name='Cladding')
clad_cell.fill = 'Zircaloy'
clad_cell.region = +gap_or & -clad_or

# Moderator Cell
moderator_cell = openmc.Cell(name='Moderator')
moderator_cell.fill = 'Water'
moderator_cell.region = +clad_or

# Create a fuel rod universe
fuel_rod_universe = openmc.Universe()
fuel_cell.universe = fuel_rod_universe
gap_cell.universe = fuel_rod_universe
clad_cell.universe = fuel_rod_universe
moderator_cell.universe = fuel_rod_universe

# Create the lattice
lattice = openmc.RectLattice(name='Fuel Lattice')
lattice.pitch = [1.4, 1.4]
lattice.lower_left = [-1.4 * 10 / 2.0, -1.4 * 10 / 2.0]
lattice.universes = [[fuel_rod_universe] * 10] * 10

# Create assembly cell
assembly_cell = openmc.Cell(name='Assembly')
assembly_cell.fill = lattice
assembly_cell.region = +assembly_ur & -assembly_ul & +assembly_vr & -assembly_vt & +lower_reflector & -upper_reflector

# Create root universe
root_universe = openmc.Universe()
assembly_cell.universe = root_universe


# Create geometry
geometry = openmc.Geometry(root_universe)

# Export to XML
geometry.export_to_xml('geometry.xml')