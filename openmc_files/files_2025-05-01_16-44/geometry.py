'''
This Python code constructs an OpenMC geometry for a simplified BWR fuel assembly based on the provided specifications. It defines the necessary surfaces, cells, and universes to represent the fuel rods, moderator, and assembly lattice. Reflective boundary conditions are applied. Control rods are not explicitly modeled in this simplified example.
'''
import openmc
import numpy as np

def create_geometry():
    # Materials (assuming materials are already defined as in the material description)
    mats = create_materials()
    mox = mats['MOX']
    zircaloy = mats['Zircaloy']
    water = mats['Water']

    # Geometry
    # Surfaces
    pellet_outer_radius = openmc.ZCylinder(r=0.8)
    gap_outer_radius = openmc.ZCylinder(r=0.808)
    clad_outer_radius = openmc.ZCylinder(r=0.9)
    assembly_top = openmc.ZPlane(z=180.0)
    assembly_bottom = openmc.ZPlane(z=-180.0)

    # Cells
    # Fuel Pellet
    fuel_pellet = openmc.Cell(name='Fuel Pellet')
    fuel_pellet.fill = mox
    fuel_pellet.region = -pellet_outer_radius

    # Fuel Gap
    fuel_gap = openmc.Cell(name='Fuel Gap')
    fuel_gap.fill = water  # Assuming gap is filled with water or gas with water properties
    fuel_gap.region = +pellet_outer_radius & -gap_outer_radius

    # Cladding
    clad = openmc.Cell(name='Cladding')
    clad.fill = zircaloy
    clad.region = +gap_outer_radius & -clad_outer_radius

    # Moderator
    moderator = openmc.Cell(name='Moderator')
    moderator.fill = water
    moderator.region = +clad_outer_radius

    # Fuel Rod Universe
    fuel_rod_universe = openmc.Universe(name='Fuel Rod')
    fuel_rod_universe.add_cells([fuel_pellet, fuel_gap, clad, moderator])

    # Assembly Lattice
    lattice = openmc.RectLattice(name='Fuel Assembly Lattice')
    lattice.lower_left = [-1.5 * 5, -1.5 * 5]
    lattice.pitch = [1.5, 1.5]
    lattice.width = [1.5] * 10
    lattice.height = [1.5] * 10
    lattice.universes = [[fuel_rod_universe] * 10 for _ in range(10)]

    # Assembly Cell
    assembly_cell = openmc.Cell(name='Fuel Assembly')
    assembly_cell.fill = lattice
    assembly_cell.region = +assembly_bottom & -assembly_top

    # Root Universe
    root_universe = openmc.Universe(name='Root Universe')
    root_universe.add_cell(assembly_cell)

    # Geometry Object
    geometry = openmc.Geometry(root_universe)

    # Boundary Conditions (Reflective)
    geometry.root_universe.bounding_box = ((-7.5, -7.5, -180.0), (7.5, 7.5, 180.0))
    for surface in geometry.get_all_surfaces().values():
        if isinstance(surface, openmc.ZPlane): #Apply only to top and bottom
            surface.boundary_type = 'reflective'
        else:
            surface.boundary_type = 'reflective'

    return geometry


def create_materials():
    # Instantiate materials
    mats = openmc.Materials()

    # MOX Fuel
    mox = openmc.Material(name='MOX')
    mox.add_nuclide('Pu239', 0.05)
    mox.add_nuclide('U238', 0.95)
    mox.set_density('g/cm3', 10.5)
    mats.append(mox)

    # Zircaloy Cladding
    zircaloy = openmc.Material(name='Zircaloy')
    zircaloy.add_nuclide('Zr', 0.98)
    zircaloy.add_nuclide('Sn', 0.02)
    zircaloy.set_density('g/cm3', 6.55)
    mats.append(zircaloy)

    # Water Moderator/Coolant
    water = openmc.Material(name='Water')
    water.add_nuclide('H1', 2.0)
    water.add_nuclide('O16', 1.0)
    water.set_density('g/cm3', 0.7)
    water.add_s_alpha_beta('HH2O', '740K')
    mats.append(water)

    # B4C Control Rod
    b4c = openmc.Material(name='B4C')
    b4c.add_nuclide('B10', 0.2)
    b4c.add_nuclide('B11', 0.8)
    b4c.add_nuclide('C', 1.0)
    b4c.set_density('g/cm3', 2.52)
    mats.append(b4c)

    return mats


if __name__ == '__main__':
    # Create geometry
    geometry = create_geometry()

    # Export to XML
    geometry.export_to_xml()

    # Create materials XML (assuming materials are defined elsewhere)
    materials = create_materials()
    materials.export_to_xml()
