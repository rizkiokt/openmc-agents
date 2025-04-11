import asyncio
import json
from pathlib import Path
import pytest
import pytest_asyncio
from agents.design_agent import DesignAgent, DesignSpecification

@pytest_asyncio.fixture
async def design_agent():
    """Create a design agent instance for testing."""
    return DesignAgent()

@pytest.fixture
def output_dir():
    """Get the output directory path."""
    return Path("openmc_files")

@pytest.mark.asyncio
async def test_bwr_mox_design(design_agent, output_dir):
    """Test BWR MOX fuel assembly design."""
    design_request = """
    Design a BWR assembly with MOX fuel.
    Target parameters:
    - k-eff between 1.0 and 1.1
    - Peak pin power factor < 1.5
    - Core height around 3.6m
    - Assembly pitch around 15cm
    """
    
    # Generate design
    spec = await design_agent.generate_design(design_request)
    
    # Check basic properties
    assert spec.reactor_type == "BWR"
    assert spec.fuel_type == "MOX"
    
    # Check core dimensions
    assert "height" in spec.core_dimensions
    assert "assembly_pitch" in spec.core_dimensions
    assert 350 <= spec.core_dimensions["height"] <= 370  # cm
    assert 14 <= spec.core_dimensions["assembly_pitch"] <= 16  # cm
    
    # Check target parameters
    assert "k_eff" in spec.target_parameters
    assert "ppf" in spec.target_parameters
    assert 1.0 <= spec.target_parameters["k_eff"]["min"] <= 1.1
    assert spec.target_parameters["ppf"]["max"] <= 1.5
    
    # Check material specifications
    assert "fuel" in spec.material_specifications
    assert "coolant" in spec.material_specifications
    assert "cladding" in spec.material_specifications
    
    # Check geometry specifications
    assert "pin_pitch" in spec.geometry_specifications
    assert "fuel_radius" in spec.geometry_specifications
    assert "clad_thickness" in spec.geometry_specifications
    
    # Check output files
    assert (output_dir / "design_specification.json").exists()
    assert (output_dir / "design_specification.txt").exists()

@pytest.mark.asyncio
async def test_pwr_uo2_design(design_agent, output_dir):
    """Test PWR UO2 fuel assembly design."""
    design_request = """
    Design a PWR assembly with UO2 fuel.
    Target parameters:
    - k-eff between 1.0 and 1.1
    - Peak pin power factor < 1.4
    - Core height around 3.66m
    - Assembly pitch around 21.5cm
    """
    
    # Generate design
    spec = await design_agent.generate_design(design_request)
    
    # Check basic properties
    assert spec.reactor_type == "PWR"
    assert spec.fuel_type == "UO2"
    
    # Check core dimensions
    assert "height" in spec.core_dimensions
    assert "assembly_pitch" in spec.core_dimensions
    assert 360 <= spec.core_dimensions["height"] <= 370  # cm
    assert 20 <= spec.core_dimensions["assembly_pitch"] <= 23  # cm
    
    # Check target parameters
    assert "k_eff" in spec.target_parameters
    assert "ppf" in spec.target_parameters
    assert 1.0 <= spec.target_parameters["k_eff"]["min"] <= 1.1
    assert spec.target_parameters["ppf"]["max"] <= 1.4
    
    # Check material specifications
    assert "fuel" in spec.material_specifications
    assert "coolant" in spec.material_specifications
    assert "cladding" in spec.material_specifications
    
    # Check geometry specifications
    assert "pin_pitch" in spec.geometry_specifications
    assert "fuel_radius" in spec.geometry_specifications
    assert "clad_thickness" in spec.geometry_specifications

@pytest.mark.asyncio
async def test_invalid_design(design_agent):
    """Test handling of invalid design requests."""
    design_request = "Design a fusion reactor"  # Not supported
    
    with pytest.raises(Exception):
        await design_agent.generate_design(design_request)

def test_output_files(output_dir):
    """Test the format and content of output files."""
    # Check JSON file
    with open(output_dir / "design_specification.json", 'r') as f:
        json_data = json.load(f)
        assert "reactor_type" in json_data
        assert "fuel_type" in json_data
        assert "core_dimensions" in json_data
        assert "target_parameters" in json_data
        assert "material_specifications" in json_data
        assert "geometry_specifications" in json_data
    
    # Check text file
    with open(output_dir / "design_specification.txt", 'r') as f:
        text_content = f.read()
        assert "Reactor Design Specification" in text_content
        assert "Core Dimensions" in text_content
        assert "Target Parameters" in text_content
        assert "Material Specifications" in text_content
        assert "Geometry Specifications" in text_content

if __name__ == "__main__":
    # Run tests
    pytest.main(["-v", "tests/test_design_agent.py"]) 