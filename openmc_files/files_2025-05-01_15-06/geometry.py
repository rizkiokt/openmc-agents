'''
This script constructs an OpenMC geometry for a simplified BWR reactor based on the provided specifications. It defines surfaces, cells, and universes to represent the fuel rods, assembly, core, reflector, and overall reactor geometry. The script incorporates the materials defined in the previous step and applies appropriate boundary conditions.
'''
import openmc
import numpy as np

# Enable Just-In-Time compilation for improved performance
openmc.config['cross_sections'] = '/home/jovyan/chain_xs/cross_sections.xml'
openmc.config['chain_file'] = '/home/jovyan/chain_xs/chain_endfb71_pwr.xml'

def create_geometry():
    # Load materials from XML
    materials = openmc.Materials.from_xml('materials.xml')
    uo2 = materials['UO2']
    mox = materials['MOX']
    zircaloy = materials['Zircaloy']
    water = materials['Water']
    boron = materials['Boron']

    # --- Fuel Rod --- 
    # Surfaces
    fuel_rod_radius = 0.9 / 2.0  # Cladding outer radius
    pellet_radius = 0.8 / 2.0
    gap_radius = (0.8/2.0) + 0.008

    fuel_pellet_surf = openmc.Circle(r=pellet_radius)
    gap_surf = openmc.Circle(r=gap_radius)
    clad_surf = openmc.Circle(r=fuel_rod_radius)
    
    # Cells
    fuel_pellet_cell_1 = openmc.Cell(name='UO2 Fuel Pellet')
    fuel_pellet_cell_1.fill = uo2
    fuel_pellet_cell_1.region = -fuel_pellet_surf

    fuel_pellet_cell_2 = openmc.Cell(name='MOX Fuel Pellet')
    fuel_pellet_cell_2.fill = mox
    fuel_pellet_cell_2.region = -fuel_pellet_surf

    gap_cell = openmc.Cell(name='Gap')
    gap_cell.fill = water  # Assuming gap is filled with water
    gap_cell.region = +fuel_pellet_surf & -gap_surf

    clad_cell = openmc.Cell(name='Cladding')
    clad_cell.fill = zircaloy
    clad_cell.region = +gap_surf & -clad_surf

    # Universe
    fuel_rod_universe_1 = openmc.Universe(name='UO2 Fuel Rod')
    fuel_rod_universe_1.add_cells([fuel_pellet_cell_1, gap_cell, clad_cell])

    fuel_rod_universe_2 = openmc.Universe(name='MOX Fuel Rod')
    fuel_rod_universe_2.add_cells([fuel_pellet_cell_2, gap_cell, clad_cell])

    # --- Assembly ---
    # Lattice
    lattice_pitch = 1.3
    assembly_size = 10
    assembly_pitch = 20.0
    
    assembly_lattice = openmc.RectLattice(name='Fuel Assembly Lattice')
    assembly_lattice.pitch = [lattice_pitch, lattice_pitch]
    assembly_lattice.lower_left = [-assembly_size/2.0 * lattice_pitch, -assembly_size/2.0 * lattice_pitch]
    assembly_lattice.width = [lattice_pitch] * assembly_size
    assembly_lattice.height = [lattice_pitch] * assembly_size

    # Fill the lattice with fuel rods, alternating UO2 and MOX
    universes = [[fuel_rod_universe_1 if (i + j) % 2 == 0 else fuel_rod_universe_2
                  for j in range(assembly_size)]
                 for i in range(assembly_size)]

    assembly_lattice.universes = universes

    # Assembly Cell
    assembly_cell = openmc.Cell(name='Fuel Assembly')
    assembly_cell.fill = assembly_lattice
    
    # Assembly Universe
    assembly_universe = openmc.Universe(name='Fuel Assembly Universe')
    assembly_universe.add_cell(assembly_cell)

    # --- Core ---
    # Core Region (single assembly for simplicity)
    core_ll = openmc.Plane(x0=-assembly_pitch/2.0, y0=-assembly_pitch/2.0, name='core_ll', boundary_type='reflective')
    core_lr = openmc.Plane(x0=assembly_pitch/2.0, y0=-assembly_pitch/2.0, name='core_lr', boundary_type='reflective')
    core_ul = openmc.Plane(x0=-assembly_pitch/2.0, y0=assembly_pitch/2.0, name='core_ul', boundary_type='reflective')
    core_ur = openmc.Plane(x0=assembly_pitch/2.0, y0=assembly_pitch/2.0, name='core_ur', boundary_type='reflective')
    
    core_region = +core_ll & -core_lr & +core_ul & -core_ur

    # Core Cell
    core_cell = openmc.Cell(name='Core')
    core_cell.fill = assembly_universe
    core_cell.region = core_region

    # Core Universe
    root_universe = openmc.Universe(name='Root Universe')
    root_universe.add_cell(core_cell)

    # --- Reflector ---    
    reflector_thickness = 20.0

    # Reflector Surfaces
    reflector_ll = openmc.Plane(x0=-(assembly_pitch/2.0 + reflector_thickness), y0=-(assembly_pitch/2.0 + reflector_thickness), name='reflector_ll', boundary_type='reflective')
    reflector_lr = openmc.Plane(x0=(assembly_pitch/2.0 + reflector_thickness), y0=-(assembly_pitch/2.0 + reflector_thickness), name='reflector_lr', boundary_type='reflective')
    reflector_ul = openmc.Plane(x0=-(assembly_pitch/2.0 + reflector_thickness), y0=(assembly_pitch/2.0 + reflector_thickness), name='reflector_ul', boundary_type='reflective')
    reflector_ur = openmc.Plane(x0=(assembly_pitch/2.0 + reflector_thickness), y0=(assembly_pitch/2.0 + reflector_thickness), name='reflector_ur', boundary_type='reflective')

    # Reflector Region
    reflector_region = +reflector_ll & -reflector_lr & +reflector_ul & -reflector_ur & ~core_region

    # Reflector Cell
    reflector_cell = openmc.Cell(name='Reflector')
    reflector_cell.fill = zircaloy
    reflector_cell.region = reflector_region
    
    # Add the reflector cell to the root universe
    root_universe.add_cell(reflector_cell)

    # --- Control Rod --- 
    # This feature is not fully implemented in this example
    # It would involve creating a control rod universe and inserting it into the core.

    # Create Geometry and Export
    geometry = openmc.Geometry(root_universe)
    geometry.export_to_xml('geometry.xml')

    return geometry

# Create geometry
geometry = create_geometry()
