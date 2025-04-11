import openmc
import numpy as np
from typing import Dict, Any, List, Tuple

def create_fuel_pin(fuel_radius: float, 
                   clad_thickness: float, 
                   gap_thickness: float,
                   fuel_material: openmc.Material,
                   clad_material: openmc.Material,
                   gap_material: openmc.Material) -> Tuple[openmc.Cell, openmc.Cell, openmc.Cell]:
    """
    Create a fuel pin cell with fuel, gap, and cladding.
    
    Args:
        fuel_radius: Radius of fuel pellet in cm
        clad_thickness: Thickness of cladding in cm
        gap_thickness: Thickness of gap in cm
        fuel_material: OpenMC material for fuel
        clad_material: OpenMC material for cladding
        gap_material: OpenMC material for gap
        
    Returns:
        Tuple of (fuel_cell, gap_cell, clad_cell)
    """
    # Create surfaces
    fuel_surface = openmc.ZCylinder(r=fuel_radius)
    gap_surface = openmc.ZCylinder(r=fuel_radius + gap_thickness)
    clad_surface = openmc.ZCylinder(r=fuel_radius + gap_thickness + clad_thickness)
    
    # Create cells
    fuel_cell = openmc.Cell(fill=fuel_material)
    fuel_cell.region = -fuel_surface
    
    gap_cell = openmc.Cell(fill=gap_material)
    gap_cell.region = +fuel_surface & -gap_surface
    
    clad_cell = openmc.Cell(fill=clad_material)
    clad_cell.region = +gap_surface & -clad_surface
    
    return fuel_cell, gap_cell, clad_cell

def create_assembly(pin_pitch: float,
                   n_pins: int,
                   pin_cells: List[openmc.Cell],
                   coolant_material: openmc.Material) -> openmc.Universe:
    """
    Create a fuel assembly from pin cells.
    
    Args:
        pin_pitch: Distance between pin centers in cm
        n_pins: Number of pins per side
        pin_cells: List of pin cells to use
        coolant_material: OpenMC material for coolant
        
    Returns:
        Universe containing the assembly
    """
    assembly = openmc.Universe()
    
    # Create lattice
    lattice = openmc.RectLattice()
    lattice.lower_left = (-n_pins/2 * pin_pitch, -n_pins/2 * pin_pitch)
    lattice.pitch = (pin_pitch, pin_pitch)
    
    # Create array of cells
    cells = np.full((n_pins, n_pins), pin_cells[0])
    for i in range(n_pins):
        for j in range(n_pins):
            if (i + j) % 2 == 0:
                cells[i,j] = pin_cells[0]  # Fuel pin
            else:
                cells[i,j] = openmc.Cell(fill=coolant_material)  # Coolant
    
    lattice.universes = cells
    assembly.add_cell(openmc.Cell(fill=lattice))
    
    return assembly

def create_core(assembly_pitch: float,
                n_assemblies: int,
                assemblies: List[openmc.Universe],
                reflector_material: openmc.Material) -> openmc.Universe:
    """
    Create a reactor core from assemblies.
    
    Args:
        assembly_pitch: Distance between assembly centers in cm
        n_assemblies: Number of assemblies per side
        assemblies: List of assembly universes
        reflector_material: OpenMC material for reflector
        
    Returns:
        Universe containing the core
    """
    core = openmc.Universe()
    
    # Create core lattice
    lattice = openmc.RectLattice()
    lattice.lower_left = (-n_assemblies/2 * assembly_pitch, -n_assemblies/2 * assembly_pitch)
    lattice.pitch = (assembly_pitch, assembly_pitch)
    
    # Create array of assemblies
    assembly_array = np.full((n_assemblies, n_assemblies), assemblies[0])
    for i in range(n_assemblies):
        for j in range(n_assemblies):
            if i == 0 or i == n_assemblies-1 or j == 0 or j == n_assemblies-1:
                # Add reflector
                assembly_array[i,j] = openmc.Universe()
                assembly_array[i,j].add_cell(openmc.Cell(fill=reflector_material))
            else:
                # Add fuel assembly
                assembly_array[i,j] = assemblies[0]
    
    lattice.universes = assembly_array
    core.add_cell(openmc.Cell(fill=lattice))
    
    return core

def extract_tallies(statepoint_file: str) -> Dict[str, np.ndarray]:
    """
    Extract tally data from statepoint file.
    
    Args:
        statepoint_file: Path to statepoint.h5 file
        
    Returns:
        Dictionary mapping tally names to numpy arrays
    """
    with openmc.StatePoint(statepoint_file) as sp:
        tallies = {}
        for tally_id, tally in sp.tallies.items():
            tallies[tally.name] = tally.mean
        return tallies 