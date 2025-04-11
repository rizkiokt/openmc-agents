from langchain_core.prompts import ChatPromptTemplate
from utils.llm import LLM
from workflows.state import State
from utils.objects import Code
from langchain_core.output_parsers import PydanticOutputParser
from utils.code_helpers import store_code
import os

def geometry_builder(state: State):
    llm = LLM().llm
    parser = PydanticOutputParser(pydantic_object=Code)
    
    design_spec = state["design_spec"]
    materials_code = state["materials_code"]
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert in OpenMC geometry modeling. Your task is to create a Python file that 
        implements the geometry specification from the design specification.
        
        The geometry builder should:
        1. Create appropriate OpenMC geometry objects (surfaces, cells, universes)
        2. Implement the assembly layout specified in the design
        3. Include proper material assignments
        4. Follow OpenMC best practices for geometry modeling
        
        Return the complete Python code that can be directly executed to create the OpenMC geometry.
         
        
        {format_instructions}
        """),
        ("user", """Design Specification: {design_spec}
        Materials Code: {materials_code}
        Create the OpenMC geometry builder Python code.
        """)
    ])
    
    chain = prompt | llm | parser

    try:
        geometry_code = chain.invoke({
            "design_spec": design_spec,
            "materials_code": materials_code,
            "format_instructions": parser.get_format_instructions()
        })
    except Exception as e:
        print(f"[ERROR] Failed to generate geometry code: {e}")
        raise
    
    # store the geometry code in the directory
    store_code(geometry_code, os.path.join(state["directory"], "geometry.py"))
    
    return {"geometry_code": geometry_code}

if __name__ == "__main__":
    # Test with a sample design specification
    test_spec = dict(
        reactor_type="BWR",
        materials=[],
        assembly={
            "type": "BWR",
            "fuel_rods": []
        }
    )
    materials_code = Code(
        imports="",
        code="",
        prefix=""
    )
    result = geometry_builder(State(design_spec=test_spec, materials_code=materials_code))
    print(result)

