from langchain_core.prompts import ChatPromptTemplate
from utils.objects import DesignSpecification
from utils.llm import LLM
from workflows.state import State
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.output_parsers import PydanticOutputParser
import os
import json
from datetime import datetime

def design_agent(state: State):
    llm = LLM().llm
    search_tool = DuckDuckGoSearchRun()
    llm_with_tools = llm.bind_tools([search_tool])
    parser = PydanticOutputParser(pydantic_object=DesignSpecification)
    
    messages = state["messages"]
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert nuclear reactor designer. Your task is to interpret the user's design 
        requirements and create a detailed design specification for OpenMC simulation.
         
            Use the search_tool to find relevant information.
            
            Use the search results and your knowledge to inform your design decisions. Focus on:
            1. Material specifications (fuel composition, coolant properties)
            2. Geometry specifications (pin pitch, assembly layout)
            3. Target performance parameters
            
            {format_instructions}
            """),
            ("user", """Design request: {messages}
            
            """)
        ])
    
    chain = prompt | llm_with_tools | parser

    try:
        design_spec = chain.invoke({
            "messages": messages,
            "format_instructions": parser.get_format_instructions()
        })
    except Exception as e:
        print(f"[ERROR] Failed to create design spec: {e}")
        raise

    # Create the directory if it doesn't exist
    directory = f"openmc_files/files_{datetime.now().strftime('%Y-%m-%d_%H-%M')}"
    os.makedirs(directory, exist_ok=True)

    # Save the design specification to a file
    with open(os.path.join(directory, "design_spec.json"), "w") as f:
        json.dump(design_spec.model_dump(), f)
    
    return {"design_spec": design_spec, "directory": directory}

if __name__ == "__main__":
    result = design_agent(State(messages="I want a PWR fuel assembly with MOX fuels"))
    print(result)
