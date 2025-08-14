from __future__ import annotations

import json
from typing import Any

from emate.core.contracts import InputState, PerceptionInput, SystemContext, Personality
from emate.core.graph import PersonaDecisionGraph
from emate.core.persona_loader import get_persona_loader


def run_stress_fatigue_demo() -> dict[str, Any]:
    """Demo showing different personalities responding to stress + fatigue + create_reminder scenario."""
    graph = PersonaDecisionGraph()
    
    # Specific scenario: User with stress AND fatigue asking for reminder
    base_input = PerceptionInput(
        user_text="唉，提醒我一下，周五前必须完成'凤凰项目'的草案。",
        speech_emotion="fatigue",  # Key: fatigue instead of just stress
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
            "output": json.loads(output.model_dump_json()),
            "decision_reasoning": _explain_decision(personality, input_state, output.action.type)
        }
    
    return results


def _explain_decision(personality: str, input_state: InputState, action_type: str) -> str:
    """解释为什么这个人格做出了这个决策"""
    # 将英文动作类型转换为中文描述
    action_chinese = {
        "enter_focus_mode": "开启专注模式",
        "suggest_break": "建议休息",
        "set_reminder": "设置提醒",
        "none": "无操作"
    }
    
    action_cn = action_chinese.get(action_type, action_type)
    
    explanations = {
        "StandardAssistant": f"检测到疲劳+截止日期临近，{action_cn}以保持专业效率",
        "CuteCat": f"发现主人疲劳了，优先关心健康，{action_cn}让主人休息~",
        "ColdBoss": f"疲劳不是借口，截止日期就是截止日期，{action_cn}强制执行",
        "WarmSister": f"感受到你的疲惫，{action_cn}平衡关怀与任务需求",
        "AnimeWizard": f"凡人的疲劳...时间流逝如常，{action_cn}以长远视角处理",
        "SarcasticFighter": f"又累了？正好用{action_cn}推你一把，没有退路！",
    }
    
    return explanations.get(personality, f"选择了{action_cn}")


def demo_stress_fatigue_comparison():
    """Pretty-print comparison focusing on stress+fatigue scenario."""
    results = run_stress_fatigue_demo()
    
    print("=== E-Mate 人格化决策演示：压力+疲劳+提醒场景 ===")
    print("场景详情:")
    print("- User's raw input: \"唉，提醒我一下，周五前必须完成'凤凰项目'的草案。\"")
    print("- Detected emotion from voice: \"fatigue\"")
    print("- Text sentiment: \"negative\"")
    print("- Recognized intent: \"create_task_reminder\"")
    print("- Context flags: [\"deadline_near\", \"interruption_high\"]\n")
    
    for personality, data in results.items():
        print(f"🎭 {data['persona_name']} ({personality})")
        print(f"   决策推理: {data['decision_reasoning']}")
        print(f"   选择行动: {data['output']['action']['type']}")
        
        if data['output']['action']['parameters'].get('duration'):
            print(f"   专注时长: {data['output']['action']['parameters']['duration']}分钟")
        
        print(f"   TTS回应: \"{data['output']['tts_output']['text_to_speak']}\"")
        print(f"   屏幕动画: {data['output']['execution_output']['screen_animation']}")
        print(f"   灯光效果: {data['output']['execution_output']['light_effect']}")
        print()


if __name__ == "__main__":
    demo_stress_fatigue_comparison()
