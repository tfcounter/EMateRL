from __future__ import annotations

import json
from typing import Any

from emate.core.contracts import InputState, PerceptionInput, SystemContext, Personality
from emate.core.graph import PersonaDecisionGraph
from emate.core.persona_loader import get_persona_loader


def run_multi_persona_demo() -> dict[str, Any]:
    """Demo showing different personalities responding to the same scenario."""
    graph = PersonaDecisionGraph()
    
    # Base scenario: stressed user with deadline pressure
    base_input = PerceptionInput(
        user_text="唉，提醒我一下，周五前必须完成'凤凰项目'的草案。",
        speech_emotion="stress",
        text_sentiment="negative",
        context_flags=["deadline_near", "interruption_high"],
        time_of_day="afternoon",
    )
    
    # Test all available personalities
    persona_loader = get_persona_loader()
    available_personas = persona_loader.list_available_personas()
    
    results = {}
    
    for personality in available_personas:
        input_state = InputState(
            perception_input=base_input,
            system_context=SystemContext(personality=personality, agent_mode="QLearning"),
        )
        
        output = graph.run_once(input_state)
        persona_config = persona_loader.get_persona(personality)
        
        results[personality] = {
            "persona_name": persona_config.name if persona_config else personality,
            "description": persona_config.description if persona_config else "",
            "output": json.loads(output.model_dump_json())
        }
    
    return results


def demo_personality_comparison():
    """Pretty-print comparison of all personalities."""
    results = run_multi_persona_demo()
    
    print("=== E-Mate 多人格决策演示 ===")
    print("场景: 用户压力状态下的'凤凰项目'任务提醒请求\n")
    
    for personality, data in results.items():
        print(f"🎭 {data['persona_name']} ({personality})")
        print(f"   描述: {data['description']}")
        print(f"   TTS输出: \"{data['output']['tts_output']['text_to_speak']}\"")
        print(f"   动作类型: {data['output']['action']['type']}")
        if data['output']['action']['parameters']['duration']:
            print(f"   专注时长: {data['output']['action']['parameters']['duration']}分钟")
        print(f"   屏幕动画: {data['output']['execution_output']['screen_animation']}")
        print(f"   灯光效果: {data['output']['execution_output']['light_effect']}")
        print()


if __name__ == "__main__":
    demo_personality_comparison()
