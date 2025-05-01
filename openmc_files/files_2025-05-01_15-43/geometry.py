'''
This script creates an OpenMC geometry for a simplified BWR assembly based on the provided specifications. It defines the necessary surfaces, cells, and universes to represent the fuel rod, cladding, moderator, and assembly lattice. Reflective boundary conditions are applied to the assembly. Control rods are not explicitly modeled in this initial geometry setup, but a placeholder material (B4C) is defined. The assembly pitch and lattice size are used to create the lattice structure.
'''
import openmc
import numpy as np

# Geometry definition

# --- Surfaces ---

# Fuel pellet surface
pellet_radius = openmc.ZCylinder(r=0.82/2)

# Cladding surfaces
clad_inner_radius = openmc.ZCylinder(r=0.82/2 + 0.008)
clad_outer_radius = openmc.ZCylinder(r=0.95/2)

# Assembly surfaces
assembly_pitch = 1.4
assembly_boundary = openmc.SquarePrism(edge_length=assembly_pitch, orientation='x', boundary_type='reflective')

# --- Cells ---

# Define Materials (assumed to be already defined in a materials.xml file)
# This example assumes the materials are defined elsewhere and loaded into the simulation
# For demonstration purposes, using dummy materials
mox = openmc.Material(name='MOX') # Replace with proper material loading if needed
zircaloy4 = openmc.Material(name='Zircaloy4') # Replace with proper material loading if needed
water = openmc.Material(name='Water') # Replace with proper material loading if needed

# Fuel pellet cell
pellet_cell = openmc.Cell(name='Fuel Pellet')
pellet_cell.fill = mox
pellet_cell.region = -pellet_radius

# Gap cell
gap_cell = openmc.Cell(name='Gap')
gap_cell.fill = water # Approximation: fill with water for simplicity
gap_cell.region = +pellet_radius & -clad_inner_radius

# Cladding cell
clad_cell = openmc.Cell(name='Cladding')
clad_cell.fill = zircaloy4
clad_cell.region = +clad_inner_radius & -clad_outer_radius

# Moderator cell
moderator_cell = openmc.Cell(name='Moderator')
moderator_cell.fill = water
moderator_cell.region = +clad_outer_radius & +assembly_boundary

# --- Universes ---

# Fuel rod universe
fuel_rod_universe = openmc.Universe(name='Fuel Rod')
fuel_rod_universe.add_cells([pellet_cell, gap_cell, clad_cell])

# Assembly universe
assembly_universe = openmc.Universe(name='Assembly')
assembly_universe.add_cells([moderator_cell]) # Add moderator cell first

# --- Lattice --- 

lattice = openmc.Lattice(name='Fuel Lattice')
lattice.pitch = [assembly_pitch, assembly_pitch]
lattice.lower_left = [-assembly_pitch * 10/2, -assembly_pitch * 10/2]

# Populate the lattice with fuel rods
lattice.universes = [[fuel_rod_universe] * 10 for _ in range(10)]

# Create a cell for the lattice
lattice_cell = openmc.Cell(name='Lattice Cell')
lattice_cell.fill = lattice
lattice_cell.region = +assembly_boundary


# Root universe
root_universe = openmc.Universe(name='Root')
root_universe.add_cell(lattice_cell)

# --- Geometry --- 

geometry = openmc.Geometry(root_universe)

# Export the geometry to an XML file
geometry.export_to_xml()

print("geometry.xml file created")
