from __future__ import annotations

import json
from typing import Any, Dict, List

from emate.core.contracts import InputState, PerceptionInput, SystemContext
from emate.core.graph import PersonaDecisionGraph
from emate.core.persona_loader import get_persona_loader


def run_extreme_scenarios_demo() -> Dict[str, Any]:
    """Demo multiple extreme scenarios to showcase personality differences."""
    graph = PersonaDecisionGraph()
    persona_loader = get_persona_loader()
    available_personas = persona_loader.list_available_personas()
    
    scenarios = {
        "疲劳求助": {
            "description": "用户疲劳状态下寻求任务提醒帮助",
            "input": PerceptionInput(
                user_text="唉，提醒我一下，周五前必须完成'凤凰项目'的草案。",
                speech_emotion="fatigue",
                text_sentiment="negative",
                context_flags=["deadline_near", "interruption_high"],
                time_of_day="afternoon",
            )
        },
        "纯压力场景": {
            "description": "高压状态下的紧急任务请求",
            "input": PerceptionInput(
                user_text="快帮我！明天就要交报告了！",
                speech_emotion="stress",
                text_sentiment="negative",
                context_flags=["deadline_near", "urgent"],
                time_of_day="evening",
            )
        },
        "平静求助": {
            "description": "平静状态下的正常工作安排",
            "input": PerceptionInput(
                user_text="请帮我安排一下今天的工作重点",
                speech_emotion="calm",
                text_sentiment="neutral",
                context_flags=[],
                time_of_day="morning",
            )
        }
    }
    
    results = {}
    
    for scenario_name, scenario_data in scenarios.items():
        results[scenario_name] = {
            "description": scenario_data["description"],
            "personas": {}
        }
        
        for personality in available_personas:
            input_state = InputState(
                perception_input=scenario_data["input"],
                system_context=SystemContext(personality=personality, agent_mode="QLearning"),
            )
            
            output = graph.run_once(input_state)
            persona_config = persona_loader.get_persona(personality)
            
            results[scenario_name]["personas"][personality] = {
                "name": persona_config.name if persona_config else personality,
                "action": output.action.type,
                "duration": output.action.parameters.duration,
                "tts": output.tts_output.text_to_speak,
                "animation": output.execution_output.screen_animation,
            }
    
    return results


def demo_extreme_scenarios():
    """Pretty-print extreme scenario comparisons."""
    results = run_extreme_scenarios_demo()
    
    print("=== E-Mate 极端场景人格对比演示 ===\n")
    
    for scenario_name, scenario_data in results.items():
        print(f"📋 场景: {scenario_name}")
        print(f"   描述: {scenario_data['description']}")
        print()
        
        # Show action type distribution
        action_counts = {}
        for persona_data in scenario_data["personas"].values():
            action = persona_data["action"]
            action_counts[action] = action_counts.get(action, 0) + 1
        
        print("   决策分布:")
        for action, count in action_counts.items():
            print(f"   - {action}: {count}个人格选择")
        print()
        
        # Show detailed responses
        for personality, persona_data in scenario_data["personas"].items():
            duration_info = f" ({persona_data['duration']}分钟)" if persona_data['duration'] else ""
            print(f"   🎭 {persona_data['name']}: {persona_data['action']}{duration_info}")
            print(f"      \"{persona_data['tts'][:60]}{'...' if len(persona_data['tts']) > 60 else ''}\"")
        print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    demo_extreme_scenarios()
