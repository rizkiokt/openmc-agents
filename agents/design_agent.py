from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class DesignSpecification(BaseModel):
    """Model for reactor design specifications"""
    reactor_type: str = Field(description="Type of reactor (e.g., BWR, PWR)")
    fuel_type: str = Field(description="Type of fuel (e.g., MOX, UO2)")
    core_dimensions: Dict[str, float] = Field(description="Core dimensions in cm")
    fuel_assembly_layout: Dict[str, Any] = Field(description="Fuel assembly layout specifications")
    target_parameters: Dict[str, Dict[str, float]] = Field(description="Target performance parameters")

class DesignAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro")
        self.parser = PydanticOutputParser(pydantic_object=DesignSpecification)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert nuclear reactor designer. Your task is to interpret the user's design 
            requirements and create a detailed design specification for OpenMC simulation.
            
            {format_instructions}
            """),
            ("human", "{input}")
        ])
    
    async def generate_design(self, design_request: str) -> DesignSpecification:
        """
        Generate a detailed design specification from a user request.
        
        Args:
            design_request: String describing the desired reactor design
            
        Returns:
            DesignSpecification object containing detailed design parameters
        """
        # TODO: Implement the design generation logic using the LLM
        # This should:
        # 1. Format the prompt with the design request
        # 2. Call the LLM
        # 3. Parse the response into a DesignSpecification
        pass 