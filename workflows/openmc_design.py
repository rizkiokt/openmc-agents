from langgraph.graph import StateGraph, START, END
from workflows.state import State
from agents.design_agent import design_agent
from agents.material_builder import material_builder
from agents.geometry_builder import geometry_builder
from agents.settings_builder import settings_builder
from agents.runner_agent import runner_agent

def openmc_design_builder():


    builder = StateGraph(State)

    builder.add_node("design_agent", design_agent)
    builder.add_node("material_builder", material_builder)
    builder.add_node("geometry_builder", geometry_builder)
    builder.add_node("settings_builder", settings_builder)
    builder.add_node("runner_agent", runner_agent)
    builder.add_edge(START, "design_agent")
    builder.add_edge("design_agent", "material_builder")
    builder.add_edge("material_builder", "geometry_builder")
    builder.add_edge("geometry_builder", "settings_builder")
    builder.add_edge("settings_builder", "runner_agent")
    builder.add_edge("runner_agent", END)

    graph = builder.compile()

    return graph

if __name__ == "__main__":
    graph = openmc_design_builder()

    from IPython.display import Image, display
    display(Image(graph.get_graph().draw_mermaid_png()))

    solution = graph.invoke({"messages": "I want a BWR fuel assembly with MOX fuels with k-eff between 1.0 and 1.1 and peaking factor <1.5"})
