from langgraph.graph import StateGraph, END
from graph.state import VoiceState
from graph.nodes import speech_to_text_node, language_detection_node


builder = StateGraph(VoiceState)

builder.add_node(
    "stt",
    speech_to_text_node
)
builder.add_node(
    "language_detection",
    language_detection_node
)

builder.set_entry_point("stt")

builder.add_edge(
    "stt",
    "language_detection"
)

builder.add_edge(
    "language_detection",
    END
)

graph = builder.compile()