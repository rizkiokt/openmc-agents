🧪 Project: Agentic Reactor Design Workflow with OpenMC
📝 Project Description
This project implements an agentic workflow system to prototype nuclear reactor designs using OpenMC. It targets automatic generation, simulation, and optimization of core designs such as BWR assemblies with MOX fuel, aiming to meet performance targets like k-effective and peak pin power factor (PPF).

It uses:

LangChain to orchestrate prompt chains and tools.
LangGraph to structure the workflow as a reactive computation graph.
Google Gemini LLM to perform design interpretation, code generation, and error diagnosis.
Python to interface with OpenMC and manage file I/O.

📦 Stack
langchain
langgraph
google-generativeai (Gemini LLM SDK)
openmc
numpy, h5py (for data extraction)

⚙️ Functionality Overview
1. Design Agent – interprets user design prompts (e.g., "BWR MOX") and outputs a design plan.
2. Material Builder – generates OpenMC materials.xml from fuel/coolant specs.
3. Geometry Builder – generates geometry.xml with lattice structures.
4. Settings Builder – creates settings.xml for transport simulation.
5. Runner Agent – executes OpenMC and monitors output.
6. Analyzer Agent – reads statepoint.h5 to check k-eff, PPF, etc.
7. Fixer & Optimizer Agent – modifies input files if targets are not met.


Update README.md as needed as well as requirements.txt