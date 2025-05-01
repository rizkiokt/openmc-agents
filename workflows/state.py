from typing import TypedDict, List
from utils.objects import DesignSpecification, Code
from utils.objects import RunState

class State(TypedDict):
    messages: List
    directory: str
    design_spec: DesignSpecification
    search_results: list[dict]
    materials_code: Code
    geometry_code: Code
    tallies_code: Code
    settings_code: Code
    keff: float
    ppf: float
    results: dict
    run_state: RunState

