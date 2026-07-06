from langsmith import Client
from langchain_core.tracers.context import tracing_v2_enabled

client = Client()

def enable_tracing():
    return tracing_v2_enabled(project_name="ProdPilot AI")