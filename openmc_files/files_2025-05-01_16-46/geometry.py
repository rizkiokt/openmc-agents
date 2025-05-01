'''
This script generates the OpenMC geometry for a simplified BWR reactor based on the provided specifications. It defines surfaces, cells, and universes to represent the fuel rods, assembly lattice, control rods, and reflector regions, incorporating the materials defined in the materials.xml file.  Reflective boundary conditions are applied.
'''
import openmc
import numpy as np

# Constants
ASSEMBLY_PITCH = 20.0
REFLECTOR_THICKNESS = 20.0

def create_geometry():

    # Load materials
    materials = openmc.Materials.from_xml('materials.xml')
    mox = materials['MOX']
    zircaloy = materials['Zircaloy']
    water = materials['Water']
    b4c = materials['B4C']

    # --- Fuel Rod --- 
    # Surfaces
    fuel_or = openmc.Circle(r=0.8/2) # pellet_diameter/2
    gap_or = openmc.Circle(r=0.8/2 + 0.008) # pellet_diameter/2 + gap_thickness
    clad_or = openmc.Circle(r=0.95/2) # cladding_outer_diameter/2

    # Cells
    fuel_cell = openmc.Cell(fill=mox, region=-fuel_or)
    gap_cell = openmc.Cell(fill=water, region=+fuel_or & -gap_or)
    clad_cell = openmc.Cell(fill=zircaloy, region=+gap_or & -clad_or)

    # Universe
    fuel_rod_universe = openmc.Universe(cells=[fuel_cell, gap_cell, clad_cell])

    # --- Assembly Lattice --- 
    lattice = openmc.RectLattice()
    lattice.pitch = [1.4, 1.4] # Lattice pitch
    lattice.lower_left = [-1.4*5, -1.4*5] # size = 10, so 5 in each direction from center
    lattice.universes = [[fuel_rod_universe]*10 for _ in range(10)] # 10x10 array of fuel rod universes

    assembly_cell = openmc.Cell(fill=lattice)
    assembly_universe = openmc.Universe(cells=[assembly_cell])

    # --- Control Rod --- 
    control_rod_or = openmc.Circle(r=1.0/2) # control_rod_diameter / 2
    control_rod_cell = openmc.Cell(fill=b4c, region=-control_rod_or)
    control_rod_universe = openmc.Universe(cells=[control_rod_cell])

    # Replace a fuel rod with a control rod (simplified insertion)
    lattice.universes[5][5] = control_rod_universe # Place the control rod at the center of the lattice

    # --- Reactor Core --- 
    core_ll = openmc.RectangularPrism(width=ASSEMBLY_PITCH*10, height=ASSEMBLY_PITCH*10, boundary_type='reflective') # 10x10 assembly core
    core_cell = openmc.Cell(fill=assembly_universe, region=-core_ll)
    root_universe = openmc.Universe(cells=[core_cell])

    # --- Reflector --- 
    # Surfaces
    lower_left = openmc.XPlane(x0=-ASSEMBLY_PITCH*5 - REFLECTOR_THICKNESS, boundary_type='reflective')
    upper_right = openmc.XPlane(x0=ASSEMBLY_PITCH*5 + REFLECTOR_THICKNESS, boundary_type='reflective')
    lower_bottom = openmc.YPlane(y0=-ASSEMBLY_PITCH*5 - REFLECTOR_THICKNESS, boundary_type='reflective')
    upper_top = openmc.YPlane(y0=ASSEMBLY_PITCH*5 + REFLECTOR_THICKNESS, boundary_type='reflective')

    # Reflector Region
    reflector_region = +lower_left & -upper_right & +lower_bottom & -upper_top & +core_ll

    # Reflector Cell
    reflector_cell = openmc.Cell(fill=water, region=reflector_region)

    # Root Cell & Universe
    root_cell = openmc.Cell(fill=root_universe, region=-core_ll)
    root_universe = openmc.Universe(cells=[root_cell, reflector_cell])

    # --- Geometry --- 
    geometry = openmc.Geometry(root_universe)

    return geometry

if __name__ == '__main__':
    geometry = create_geometry()
    geometry.export_to_xml('geometry.xml')