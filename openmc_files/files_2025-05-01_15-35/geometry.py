'''
This code constructs the geometry for a Boiling Water Reactor (BWR) based on the provided specifications. It defines the necessary surfaces, cells, and universes to represent the fuel rods, cladding, moderator, and assembly lattice. Reflective boundary conditions are applied to the outer surfaces of the geometry. The code adheres to OpenMC best practices for geometry modeling, ensuring a clear and maintainable structure.
'''
import openmc
import numpy as np

def create_geometry():
    # Define materials (assuming materials.xml is already created by the material definition code)
    materials = openmc.Materials.from_xml()
    mox = materials['MOX']
    zircaloy = materials['Zircaloy-4']
    water = materials['Water']

    # Define surfaces
    fuel_or = openmc.Sphere(r=0.82/2) # fuel pellet radius
    clad_ir = openmc.Sphere(r=0.82/2 + 0.008)
    clad_or = openmc.Sphere(r=0.95/2)

    # Define cells
    fuel_cell = openmc.Cell(name='Fuel Pellet', fill=mox)
    fuel_cell.region = -fuel_or

    gap_cell = openmc.Cell(name='Gap', fill=water) # or void, depending on modeling choice
    gap_cell.region = +fuel_or & -clad_ir

    clad_cell = openmc.Cell(name='Cladding', fill=zircaloy)
    clad_cell.region = +clad_ir & -clad_or

    # Define fuel rod universe
    fuel_rod_universe = openmc.Universe(name='Fuel Rod')
    fuel_rod_universe.add_cells([fuel_cell, gap_cell, clad_cell])

    # Define moderator cell
    moderator_cell = openmc.Cell(name='Moderator', fill=water)

    # Define lattice
    lattice = openmc.Lattice(name='Fuel Assembly Lattice')
    lattice.pitch = [1.4, 1.4]
    lattice.lower_left = [-1.4 * 10/2, -1.4 * 10/2]
    lattice.width = [1.4] * 10
    lattice.universes = [[fuel_rod_universe] * 10 for _ in range(10)]  # Fill with fuel rods

    # Define assembly cell
    assembly_cell = openmc.Cell(name='Fuel Assembly')
    assembly_cell.fill = lattice

    # Define assembly universe
    assembly_universe = openmc.Universe(name='Fuel Assembly Universe')
    assembly_universe.add_cell(assembly_cell)

    # Define bounding surfaces for the geometry
    x_min = openmc.XPlane(x0=-1.4 * 10/2, boundary_type='reflective')
    x_max = openmc.XPlane(x0=1.4 * 10/2, boundary_type='reflective')
    y_min = openmc.YPlane(y0=-1.4 * 10/2, boundary_type='reflective')
    y_max = openmc.YPlane(y0=1.4 * 10/2, boundary_type='reflective')
    z_min = openmc.ZPlane(z0=-100.0, boundary_type='reflective') # Add arbitrary height
    z_max = openmc.ZPlane(z0=100.0, boundary_type='reflective') # Add arbitrary height

    # Define the geometry
    geometry = openmc.Geometry(assembly_universe)
    geometry.root_universe.region = +x_min & -x_max & +y_min & -y_max & +z_min & -z_max

    return geometry

if __name__ == '__main__':
    geometry = create_geometry()
    geometry.export_to_xml()
