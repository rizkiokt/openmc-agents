# Agentic Reactor Design Workflow with OpenMC

This project implements an agentic workflow system for prototyping nuclear reactor designs using OpenMC. The system uses LangChain and LangGraph to orchestrate a series of specialized agents that handle different aspects of the reactor design process.

## Project Structure

```
.
├── agents/                    # Agent implementations
│   ├── design_agent.py       # Interprets design requirements
│   ├── material_builder.py   # Generates materials.xml
│   ├── geometry_builder.py   # Generates geometry.xml
│   ├── settings_builder.py   # Generates settings.xml
│   ├── runner_agent.py       # Executes OpenMC
│   ├── analyzer_agent.py     # Analyzes simulation results
│   └── optimizer_agent.py    # Optimizes design parameters
├── reactor_design_workflow.py # Main workflow orchestrator
├── requirements.txt          # Project dependencies
└── README.md                # This file
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Set up your Gemini API key:
   ```bash
   export GEMINI_API_KEY=your_api_key
   ```

2. Run the workflow:
   ```python
   from reactor_design_workflow import ReactorDesignWorkflow
   
   workflow = ReactorDesignWorkflow()
   
   design_spec = {
       "reactor_type": "BWR",
       "fuel_type": "MOX",
       "targets": {
           "k_eff": {"min": 1.0, "max": 1.1},
           "ppf": {"max": 1.5}
       }
   }
   
   results = await workflow.run(design_spec)
   ```

## Workflow Steps

1. **Design Agent**: Interprets user design prompts and creates detailed specifications
2. **Material Builder**: Generates OpenMC materials.xml from fuel/coolant specs
3. **Geometry Builder**: Creates geometry.xml with lattice structures
4. **Settings Builder**: Configures settings.xml for transport simulation
5. **Runner Agent**: Executes OpenMC and monitors output
6. **Analyzer Agent**: Reads statepoint.h5 to check k-eff, PPF, etc.
7. **Optimizer Agent**: Modifies input files if targets are not met

## Requirements

- Python 3.8+
- OpenMC
- Google Gemini API key
- Other dependencies listed in requirements.txt

## License

MIT License 