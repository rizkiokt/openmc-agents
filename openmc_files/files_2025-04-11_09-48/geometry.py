'''
This script constructs an OpenMC geometry for a simplified BWR reactor, including fuel assemblies, control rods, and a water reflector. It utilizes the materials defined in the materials.xml file (created in the previous step). The geometry consists of a lattice of fuel pins within an assembly, multiple assemblies arranged in a lattice, control rods that can be inserted or withdrawn, and a water reflector surrounding the core. Reflective boundary conditions are applied.
'''
import openmc
import numpy as npdef create_geometry():
    # Load materials
    materials = openmc.Materials.from_xml('materials.xml')
    mox = materials['MOX']
    zircaloy = materials['Zircaloy']
    water = materials['Water']
    boron_carbide = materials['Boron Carbide']

    # Geometry parameters
    pellet_radius = 0.8 / 2.0
    gap_radius = 0.8 / 2.0 + 0.008
    clad_radius = 0.95 / 2.0
    fuel_assembly_pitch = 20.0
    lattice_pitch = 1.4
    lattice_size = 10
    reflector_thickness = 20.0
    control_rod_radius = 1.0 / 2.0
    control_rod_length = 360.0

    # Surfaces
    fuel_surf = openmc.Circle(r=pellet_radius)
    gap_surf = openmc.Circle(r=gap_radius)
    clad_surf = openmc.Circle(r=clad_radius)
    control_rod_surf = openmc.Circle(r=control_rod_radius)

    # Cells
    fuel_cell = openmc.Cell(fill=mox, region=-fuel_surf)
    gap_cell = openmc.Cell(fill=water, region=+fuel_surf & -gap_surf)
    clad_cell = openmc.Cell(fill=zircaloy, region=+gap_surf & -clad_surf)

    # Create a cell for the control rod.  The region will be defined later
    control_rod_cell = openmc.Cell(fill=boron_carbide)

    # Create a Universe for the fuel rod
    fuel_rod_universe = openmc.Universe(cells=[fuel_cell, gap_cell, clad_cell])

    # Create a lattice
    assembly_lattice = openmc.RectLattice()
    assembly_lattice.pitch = [lattice_pitch, lattice_pitch]
    assembly_lattice.lower_left = [-lattice_pitch * lattice_size / 2.0, -lattice_pitch * lattice_size / 2.0]
    assembly_lattice.shape = [lattice_size, lattice_size]

    # Fill the lattice with the fuel rod universe
    assembly_lattice.universes = [[fuel_rod_universe] * lattice_size for _ in range(lattice_size)]

    # Create a cell for the lattice
    assembly_cell = openmc.Cell(fill=assembly_lattice)

    # Create a Universe for the assembly
    assembly_universe = openmc.Universe(cells=[assembly_cell])

    # Create a 3x3 array of assemblies
    num_assemblies = 3
    core_ll = [-fuel_assembly_pitch * num_assemblies / 2.0, -fuel_assembly_pitch * num_assemblies / 2.0]
    assembly_positions = []
    for i in range(num_assemblies):
        for j in range(num_assemblies):
            assembly_positions.append((core_ll[0] + i * fuel_assembly_pitch, core_ll[1] + j * fuel_assembly_pitch, 0.0))

    # Create root cells for each assembly
    root_cells = []
    for x, y, z in assembly_positions:
        c = openmc.Cell(fill=assembly_universe)
        c.translation = (x, y, z)
        root_cells.append(c)

    # Create the control rod surfaces (top and bottom planes)
    top_cr_surf = openmc.ZPlane(z0=control_rod_length/2.0)
    bottom_cr_surf = openmc.ZPlane(z0=-control_rod_length/2.0)

    # Create region for control rod.
    control_rod_region = -control_rod_surf & +bottom_cr_surf & -top_cr_surf
    control_rod_cell.region = control_rod_region

    # Position the control rod in the center of the geometry
    control_rod_cell.translation = (0, 0, 0)
    root_cells.append(control_rod_cell)


    # Create bounding surfaces for the reactor core
    x_min = openmc.XPlane(x0=core_ll[0] - reflector_thickness, boundary_type='reflective')
    x_max = openmc.XPlane(x0=core_ll[0] + fuel_assembly_pitch * num_assemblies + reflector_thickness, boundary_type='reflective')
    y_min = openmc.YPlane(y0=core_ll[1] - reflector_thickness, boundary_type='reflective')
    y_max = openmc.YPlane(y0=core_ll[1] + fuel_assembly_pitch * num_assemblies + reflector_thickness, boundary_type='reflective')
    z_min = openmc.ZPlane(z0=-control_rod_length/2.0 - reflector_thickness, boundary_type='reflective')
    z_max = openmc.ZPlane(z0=control_rod_length/2.0 + reflector_thickness, boundary_type='reflective')

    # Create a cell for the water reflector
    outer_region = +x_min & -x_max & +y_min & -y_max & +z_min & -z_max
    core_region = ~outer_region # everything inside the outer box is the core

    reflector_cell = openmc.Cell(fill=water, region=outer_region)
    root_cells.append(reflector_cell)

    # Create the root universe
    root_universe = openmc.Universe(cells=root_cells)

    # Create the geometry
    geometry = openmc.Geometry(root_universe)

    return geometry

if __name__ == '__main__':
    geometry = create_geometry()
    geometry.export_to_xml('geometry.xml')