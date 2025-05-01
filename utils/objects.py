from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict

class RunState(BaseModel):
    """State object for tracking the progress and results of a reactor design run."""
    status: Literal["complete", "fail"] = Field(description="Status of the run")
    code_to_fix: List[str] = Field(description="List of files that need fixing (materials.py, geometry.py, and/or settings.py)")
    suggestions: List[str] = Field(description="Specific suggestions for fixing the code")
    error: Optional[str] = Field(description="Error message if any", default=None)


class Code(BaseModel):
    """Schema for code solutions to questions about LCEL."""

    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")


class MaterialSpec(BaseModel):
    """Specification for a material in the reactor design."""
    name: str = Field(..., description="Name of the material, e.g. 'UO2'")
    composition: Dict[str, float] = Field(
        ...,
        description="Material composition as atomic fractions. Example: {'U235': 0.05, 'U238': 0.95}",
        example={"U235": 0.05, "U238": 0.95}
    )
    density: float = Field(..., description="Material density in g/cm^3")
    temperature: Optional[float] = Field(None, description="Material temperature in Kelvin")

class FuelRodSpec(BaseModel):
    fuel_material: str
    cladding_material: str
    pellet_diameter: float  # cm
    cladding_outer_diameter: float  # cm
    gap_thickness: Optional[float] = 0.008  # cm, default for UO2-Zircaloy
    enrichment: Optional[float] = Field(None, description="U235 enrichment if applicable")

class TRISOSpec(BaseModel):
    fuel_kernel_material: str
    fuel_kernel_radius: float  # cm
    buffer_thickness: float
    ipyro_thickness: float
    siC_thickness: float
    opyro_thickness: float
    packing_fraction: float  # e.g., 0.3
    matrix_material: str

class LatticeSpec(BaseModel):
    """Specification for a fuel assembly lattice.
    
    The lattice defines the arrangement of fuel pins and other components in the assembly.
    For square lattices, the contents should be a 2D array where each element represents
    a material or component name (e.g., "fuel", "water_rod", "control_rod").
    For hexagonal lattices, the contents should be a 2D array with appropriate hexagonal
    symmetry.
    """
    type: Literal["square", "hexagonal"]
    pitch: float = Field(..., description="Distance between pin centers in cm")
    size: Optional[int] = Field(None, description="Number of pins per side (e.g., 17 for 17x17)")

class AssemblySpec(BaseModel):
    type: Literal["PWR", "BWR", "HTGR-Prismatic", "HTGR-Pebble"]
    fuel_rods: Optional[List[FuelRodSpec]] = None
    triso_particles: Optional[TRISOSpec] = None
    lattice: Optional[LatticeSpec] = None
    assembly_pitch: Optional[float] = None  # cm
    moderator_material: str
    reflector_material: Optional[str] = None

class CoolantSpec(BaseModel):
    type: Literal["water", "helium", "CO2", "sodium"]
    temperature: float  # K
    pressure: Optional[float] = None  # Pa
    boron_ppm: Optional[float] = None  # for PWR

class ControlRodSpec(BaseModel):
    material: str
    position: Optional[str] = Field(None, description="e.g., inserted, withdrawn, partially")
    diameter: Optional[float] = Field(None, description="Control rod diameter in cm")
    length: Optional[float] = Field(None, description="Control rod length in cm")

class DesignSpecification(BaseModel):
    reactor_type: Literal["PWR", "BWR", "HTGR-Prismatic", "HTGR-Pebble", "Other"]
    materials: List[MaterialSpec]
    assembly: AssemblySpec
    coolant: CoolantSpec
    control_rods: Optional[List[ControlRodSpec]] = None
    reflector_thickness: Optional[float] = None  # cm
    boundary_conditions: Literal["vacuum", "reflective", "periodic"]
