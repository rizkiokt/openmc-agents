from langchain_core.prompts import ChatPromptTemplate
from utils.llm import LLM
from workflows.state import State
from utils.objects import Code, RunState
from langchain_core.output_parsers import PydanticOutputParser
from utils.code_helpers import store_code
import openmc
import os
from pathlib import Path
import subprocess
import time
import json

def run_openmc(state: State):
    # run the openmc simulation
    # Store original directory
    original_dir = os.getcwd()
    error_details = None
    
    try:
        # Change to the state directory
        os.chdir(state["directory"])
        
        # Run the OpenMC files in sequence
        try:
            subprocess.run(["python", "materials.py"], check=True, capture_output=True, text=True)
            subprocess.run(["python", "geometry.py"], check=True, capture_output=True, text=True)
            subprocess.run(["python", "settings.py"], check=True, capture_output=True, text=True)
            subprocess.run(["openmc", "run"], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            error_details = {
                "error": f"OpenMC simulation failed: {str(e)}",
                "returncode": e.returncode,
                "stdout": e.stdout,
                "stderr": e.stderr,
                "cmd": e.cmd
            }
            return {"status": "fail", "error_details": error_details}
        except Exception as e:
            error_details = {
                "error": f"Unexpected error during simulation: {str(e)}",
                "traceback": str(e.__traceback__)
            }
            return {"status": "fail", "error_details": error_details}
            
    except Exception as e:
        error_details = {
            "error": f"Directory change failed: {str(e)}",
            "traceback": str(e.__traceback__)
        }
        return {"status": "fail", "error_details": error_details}
    finally:
        # Always return to original directory
        os.chdir(original_dir)
    
    return {"status": "success"}

def runner_agent(state: State):
    """
    Agent that runs OpenMC simulation and analyzes results.
    
    Args:
        state: State object containing workflow state
        
    Returns:
        Updated state with run analysis results
    """
    llm = LLM().llm
    parser = PydanticOutputParser(pydantic_object=RunState)
    
    # Run the simulation
    result = run_openmc(state)
    
    # Prepare the prompt with simulation results and code
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert in OpenMC simulation analysis. Your task is to analyze the simulation 
        results and provide feedback on any issues.
        
        Based on the simulation results and code, provide:
        1. Overall run status (complete or fail)
        2. Which code files need fixing (materials.py, geometry.py, settings.py)
        3. Specific suggestions for fixing the identified issues
        
        Focus on:
        - Material definitions and compositions
        - Geometry construction and boundaries
        - Simulation settings and parameters
        - Error messages and their implications
        
        {format_instructions}
        """),
        ("user", """Simulation Result: {result}
        Materials Code: {materials_code}
        Geometry Code: {geometry_code}
        Settings Code: {settings_code}
        
        Please analyze and provide feedback.
        """)
    ])
    
    chain = prompt | llm | parser
    
    try:
        run_state = chain.invoke({
            "result": result,
            "materials_code": state["materials_code"].code,
            "geometry_code": state["geometry_code"].code,
            "settings_code": state["settings_code"].code,
            "format_instructions": parser.get_format_instructions()
        })
    except Exception as e:
        print(f"[ERROR] Failed to analyze simulation results: {e}")
        raise
    
    # Update state with analysis results
    state["run_state"] = run_state
    
    # write the run_state to a file in the state directory
    with open(os.path.join(state["directory"], "run_state.json"), "w") as f:
        json.dump(run_state.model_dump(), f)
    
    return state