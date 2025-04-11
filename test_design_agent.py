import asyncio
from agents.design_agent import DesignAgent

async def test_design_agent():
    # Create design agent
    agent = DesignAgent()
    
    # Test case 1: BWR with MOX fuel
    design_request = """
    Design a BWR assembly with MOX fuel.
    Target parameters:
    - k-eff between 1.0 and 1.1
    - Peak pin power factor < 1.5
    - Core height around 3.6m
    - Assembly pitch around 15cm
    """
    
    print("Testing BWR MOX design...")
    spec = await agent.generate_design(design_request)
    print("\nGenerated specification:")
    print(f"Reactor Type: {spec.reactor_type}")
    print(f"Fuel Type: {spec.fuel_type}")
    print(f"Core Dimensions: {spec.core_dimensions}")
    print(f"Target Parameters: {spec.target_parameters}")
    
    # Test case 2: PWR with UO2 fuel
    design_request = """
    Design a PWR assembly with UO2 fuel.
    Target parameters:
    - k-eff between 1.0 and 1.1
    - Peak pin power factor < 1.4
    - Core height around 3.66m
    - Assembly pitch around 21.5cm
    """
    
    print("\nTesting PWR UO2 design...")
    spec = await agent.generate_design(design_request)
    print("\nGenerated specification:")
    print(f"Reactor Type: {spec.reactor_type}")
    print(f"Fuel Type: {spec.fuel_type}")
    print(f"Core Dimensions: {spec.core_dimensions}")
    print(f"Target Parameters: {spec.target_parameters}")

if __name__ == "__main__":
    asyncio.run(test_design_agent()) 