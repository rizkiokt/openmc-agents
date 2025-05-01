from typing import Dict, Any, List
import openmc
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from utils.llm import LLM
from workflows.state import State
from utils.objects import Code
from langchain_core.output_parsers import PydanticOutputParser
from utils.code_helpers import store_code
import os

def settings_builder(state: State):
    llm = LLM().llm
    parser = PydanticOutputParser(pydantic_object=Code)
    
    design_spec = state["design_spec"]
    materials_code = state["materials_code"]
    geometry_code = state["geometry_code"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert in OpenMC simulation settings. Your task is to create a Python file that 
        implements the simulation settings based on the design specification and existing materials/geometry code.
        
        The settings builder should:
        1. Configure appropriate particle count and batches, but make it small for testing
        2. Set temperature parameters
        3. Configure energy mode and cross sections
        4. Set up source parameters
        5. Configure output settings
        6. Follow OpenMC best practices for simulation settings
        7. No need to define cross sections and chain files are already defined in the environment variables
        
        Return the complete Python code that can be directly executed to create the OpenMC settings.
        
        {format_instructions}
        """),
        ("user", """Design Specification: {design_spec}
        Materials Code: {materials_code}
        Geometry Code: {geometry_code}
        Create the OpenMC settings builder Python code.
        """)
    ])
    
    chain = prompt | llm | parser

    try:
        settings_code = chain.invoke({
            "design_spec": design_spec,
            "materials_code": materials_code,
            "geometry_code": geometry_code,
            "format_instructions": parser.get_format_instructions()
        })
    except Exception as e:
        print(f"[ERROR] Failed to generate settings code: {e}")
        raise
    
    # store the settings code in the directory
    store_code(settings_code, os.path.join(state["directory"], "settings.py"))
    
    return {"settings_code": settings_code}