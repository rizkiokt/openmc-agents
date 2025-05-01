'''
This script constructs the geometry for a simplified BWR reactor using OpenMC. It defines fuel rods, cladding, and moderator regions, and then assembles them into a lattice representing the reactor core. The geometry includes control rods and a reflector region. Reflective boundary conditions are applied to the outer surfaces.
'''
import openmc
import numpy as np

# Constants from design specification
ASSEMBLY_PITCH = 15.0
REFLECTOR_THICKNESS = 20.0def create_geometry():
    # Load materials
    materials = openmc.Materials.from_xml('materials.xml')
    mox = materials['MOX']
    zircaloy = materials['Zircaloy-4']
    water = materials['Water']
    boron_carbide = materials['Boron Carbide']

    # --- Fuel Rod --- 
    # Surfaces
    fuel_rod_radius = 1.0 / 2.0
    clad_inner_radius = fuel_rod_radius + 0.008
    clad_outer_radius = 1.2 / 2.0

    fuel_surf = openmc.Circle(r=fuel_rod_radius)
    gap_inner_surf = openmc.Circle(r=clad_inner_radius)
    clad_outer_surf = openmc.Circle(r=clad_outer_radius)

    # Cells
    fuel_cell = openmc.Cell(name='Fuel').set_fill(mox).set_region(-fuel_surf)
    gap_cell = openmc.Cell(name='Gap').set_fill(water).set_region(+fuel_surf & -gap_inner_surf)
    clad_cell = openmc.Cell(name='Cladding').set_fill(zircaloy).set_region(+gap_inner_surf & -clad_outer_surf)
    moderator_cell = openmc.Cell(name='Moderator').set_fill(water).set_region(+clad_outer_surf)

    # Universe
    fuel_rod_universe = openmc.Universe(cells=[fuel_cell, gap_cell, clad_cell, moderator_cell])

    # --- Assembly Lattice --- 
    lattice_pitch = 1.5
    lattice_size = 10
    assembly_universe = openmc.Universe(name='Assembly Universe')
    
    # Create a 2D array of fuel rod universes
    lattice = openmc.RectLattice(name='Fuel Lattice')
    lattice.pitch = [lattice_pitch, lattice_pitch]
    lattice.lower_left = [-lattice_pitch * lattice_size / 2, -lattice_pitch * lattice_size / 2]
    lattice.shape = [lattice_size, lattice_size]
    lattice.universes = [[fuel_rod_universe] * lattice_size for _ in range(lattice_size)]

    # Create a cell for the lattice
    lattice_cell = openmc.Cell(name='Lattice Cell').set_fill(lattice)
    assembly_universe.add_cell(lattice_cell)

    # --- Control Rod --- 
    control_rod_radius = 2.0 / 2.0
    control_rod_surf = openmc.Circle(r=control_rod_radius)
    control_rod_cell = openmc.Cell(name='Control Rod').set_fill(boron_carbide).set_region(-control_rod_surf)
    control_rod_universe = openmc.Universe(cells=[control_rod_cell])

    # Replace a fuel rod with a control rod (example: center of the lattice)
    lattice.universes[lattice_size // 2][lattice_size // 2] = control_rod_universe

    # --- Reactor Core --- 
    core_universe = openmc.Universe(name='Core Universe')
    assembly_cell = openmc.Cell(name='Assembly Cell').set_fill(assembly_universe)
    core_universe.add_cell(assembly_cell)

    # --- Reactor --- 
    reactor_universe = openmc.Universe(name='Reactor Universe')
    
    # Surfaces
    x_min = openmc.XPlane(x0=-ASSEMBLY_PITCH / 2 - REFLECTOR_THICKNESS).set_boundary_type('reflective')
    x_max = openmc.XPlane(x0=ASSEMBLY_PITCH / 2 + REFLECTOR_THICKNESS).set_boundary_type('reflective')
    y_min = openmc.YPlane(y0=-ASSEMBLY_PITCH / 2 - REFLECTOR_THICKNESS).set_boundary_type('reflective')
    y_max = openmc.YPlane(y0=ASSEMBLY_PITCH / 2 + REFLECTOR_THICKNESS).set_boundary_type('reflective')
    z_min = openmc.ZPlane(z0=-180.0).set_boundary_type('reflective') # Half of control rod length
    z_max = openmc.ZPlane(z0=180.0).set_boundary_type('reflective') # Half of control rod length
    
    # Region
    reactor_region = +x_min & -x_max & +y_min & -y_max & +z_min & -z_max

    # Cells
    core_cell = openmc.Cell(name='Core Cell').set_fill(core_universe).set_region(reactor_region)
    reactor_universe.add_cell(core_cell)

    # --- Geometry --- 
    geometry = openmc.Geometry(reactor_universe)
    return geometry

if __name__ == '__main__':
    geometry = create_geometry()
    geometry.export_to_xml()
