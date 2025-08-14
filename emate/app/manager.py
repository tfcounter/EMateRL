from __future__ import annotations

import json
from typing import Any

from emate.core.contracts import InputState, PerceptionInput, SystemContext
from emate.core.graph import PersonaDecisionGraph


def run_demo() -> dict[str, Any]:
    graph = PersonaDecisionGraph()
    input_state = InputState(
        perception_input=PerceptionInput(
            user_text="唉，提醒我一下，周五前必须完成‘凤凰项目’的草案。",
            speech_emotion="stress",
            text_sentiment="negative",
            context_flags=["deadline_near", "interruption_high"],
            time_of_day="afternoon",
        ),
        system_context=SystemContext(personality="StandardAssistant", agent_mode="QLearning"),
    )

    output = graph.run_once(input_state)
    return json.loads(output.model_dump_json())


if __name__ == "__main__":
    import pprint

    pprint.pp(run_demo())


