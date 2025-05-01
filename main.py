
from workflows.openmc_design import openmc_design_builder

def main():
    # Create the design workflow graph
    graph = openmc_design_builder()
    
    # Example design request
    design_request = """
    Design a BWR assembly with MOX fuel.
    Target parameters:
    - k-eff between 1.0 and 1.1
    - Peak pin power factor < 1.5
    """
    
    # Run the design workflow
    print("Starting design workflow...")
    result = graph.invoke({"messages": design_request})
    
    print("\nDesign workflow completed!")
    print(f"Generated files are stored in: {result['directory']}")


if __name__ == "__main__":
    main()
