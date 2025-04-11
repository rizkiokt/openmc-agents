from langchain_core.prompts import ChatPromptTemplate
from utils.llm import LLM
from workflows.state import State
from utils.objects import Code
from langchain_core.output_parsers import PydanticOutputParser
from utils.code_helpers import store_code
import openmc
import os

def material_builder(state: State):
    llm = LLM().llm
    parser = PydanticOutputParser(pydantic_object=Code)
    
    design_spec = state["design_spec"]
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert in nuclear materials modeling. Your task is to create a Python file that 
        implements the material specifications from the design specification using OpenMC.
        
        The material builder should:
        1. Create appropriate OpenMC material objects for all specified materials
        2. Set correct compositions and densities
        3. Configure temperature and other material properties
        4. Follow OpenMC best practices for material modeling
        
        Return the complete Python code that can be directly executed to create the OpenMC materials.
         
        {format_instructions}
        """),
        ("user", """Design Specification: {design_spec}
        Create the OpenMC materials builder Python code.
        """)
    ])
    
    chain = prompt | llm | parser

    try:
        materials_code = chain.invoke({
            "design_spec": design_spec,
            "format_instructions": parser.get_format_instructions()
        })
    except Exception as e:
        print(f"[ERROR] Failed to generate materials code: {e}")
        raise
    
    # store the materials code in the directory
    store_code(materials_code, os.path.join(state["directory"], "materials.py"))
    
    return {"materials_code": materials_code}

if __name__ == "__main__":
    # Test with a sample design specification
    test_spec = dict(
        reactor_type="BWR",
        materials=[
            {
                "name": "UO2",
                "composition": {"U235": 0.05, "U238": 0.95},
                "density": 10.4,
                "temperature": 900
            },
            {
                "name": "Zircaloy",
                "composition": {"Zr": 1.0},
                "density": 6.49
            },
            {
                "name": "Water",
                "composition": {"H1": 2.0, "O16": 1.0},
                "density": 0.7
            }
        ]
    )
    result = material_builder(State(design_spec=test_spec))
    print(result) 