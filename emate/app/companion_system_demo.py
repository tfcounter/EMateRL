"""
环境智能AI伙伴完整系统演示

展示E-Mate从状态感知到动作输出的完整流程，
体现"从助手到伙伴"的核心转变。
"""

from __future__ import annotations

import json
from typing import Dict, Any

from emate.core.contracts import InputState, PerceptionInput, SystemContext, MemoryInput, MemoryEpisode
from emate.core.graph import PersonaDecisionGraph
from emate.micro.state_discretizer import discretize_state
from emate.micro.action_map import map_action_to_output


def create_companion_scenarios() -> Dict[str, InputState]:
    """
    创建体现E-Mate环境智能AI伙伴特性的综合场景
    
    每个场景都展示E-Mate如何理解用户的多维状态，
    并提供相应的伙伴式支持。
    """
    scenarios = {}
    
    # 场景1：深度工作状态 - 工作节律协调
    scenarios["深度工作保护"] = InputState(
        perception_input=PerceptionInput(
            user_text="我要开始处理凤凰项目的核心算法了，这很重要",
            speech_emotion="calm",
            text_sentiment="neutral",
            context_flags=["deep_work_mode", "important_task", "quiet_space"],
            time_of_day="morning"
        ),
        memory_input=MemoryInput(
            facts=["凤凰项目是Q1的关键目标", "用户偏好早晨进行深度思考"],
            episodes=[
                MemoryEpisode(event="凤凰项目架构设计完成", emotion="satisfied", ts="2024-01-09T11:00:00Z"),
                MemoryEpisode(event="用户表达对项目进展的期待", emotion="focused", ts="2024-01-10T08:30:00Z")
            ]
        ),
        system_context=SystemContext(personality="StandardAssistant")
    )
    
    # 场景2：疲劳状态 - 健康守护
    scenarios["健康守护干预"] = InputState(
        perception_input=PerceptionInput(
            user_text="感觉眼睛有点酸，脖子也僵了",
            speech_emotion="fatigue",
            text_sentiment="negative",
            context_flags=["sitting_over_2h", "eye_strain", "neck_tension"],
            time_of_day="afternoon"
        ),
        memory_input=MemoryInput(
            facts=["用户容易久坐忘记休息", "下午2-3点是用户疲劳高峰"],
            episodes=[
                MemoryEpisode(event="用户连续工作3小时", emotion="tired", ts="2024-01-10T14:30:00Z"),
                MemoryEpisode(event="上次提醒休息被用户接受", emotion="grateful", ts="2024-01-09T15:00:00Z")
            ]
        ),
        system_context=SystemContext(personality="WarmSister")
    )
    
    # 场景3：压力状态 - 情感连接
    scenarios["情感支持陪伴"] = InputState(
        perception_input=PerceptionInput(
            user_text="这个bug找了两小时了，快崩溃了",
            speech_emotion="stress",
            text_sentiment="negative",
            context_flags=["frustration_high", "task_stuck", "emotional_distress"],
            time_of_day="evening"
        ),
        memory_input=MemoryInput(
            facts=["用户是完美主义者", "技术问题会让用户特别焦虑"],
            episodes=[
                MemoryEpisode(event="用户因bug调试感到挫败", emotion="frustrated", ts="2024-01-10T18:00:00Z"),
                MemoryEpisode(event="E-Mate提供了情感支持", emotion="comforted", ts="2024-01-09T17:30:00Z")
            ]
        ),
        system_context=SystemContext(personality="CuteCat")
    )
    
    # 场景4：目标回顾 - 个性化智能
    scenarios["个性化洞察"] = InputState(
        perception_input=PerceptionInput(
            user_text="这周工作效率怎么样？有什么可以改进的？",
            speech_emotion="calm",
            text_sentiment="neutral",
            context_flags=["self_reflection", "progress_review", "improvement_seeking"],
            time_of_day="evening"
        ),
        memory_input=MemoryInput(
            facts=["用户喜欢数据化反馈", "每周五会进行工作复盘"],
            episodes=[
                MemoryEpisode(event="完成了5个重要任务", emotion="accomplished", ts="2024-01-10T17:00:00Z"),
                MemoryEpisode(event="参加了3次会议", emotion="engaged", ts="2024-01-10T16:00:00Z"),
                MemoryEpisode(event="深度工作时间达到6小时", emotion="productive", ts="2024-01-10T15:00:00Z")
            ]
        ),
        system_context=SystemContext(personality="AnimeWizard")
    )
    
    # 场景5：环境干扰 - 环境协调
    scenarios["环境协调优化"] = InputState(
        perception_input=PerceptionInput(
            user_text="办公室太吵了，完全没法专注",
            speech_emotion="angry",
            text_sentiment="negative",
            context_flags=["environment_uncomfortable", "interruption_high", "noise_distraction"],
            time_of_day="afternoon"
        ),
        memory_input=MemoryInput(
            facts=["用户对噪音敏感", "安静环境能显著提升效率"],
            episodes=[
                MemoryEpisode(event="噪音干扰导致工作中断", emotion="irritated", ts="2024-01-10T14:00:00Z"),
                MemoryEpisode(event="E-Mate成功屏蔽了干扰", emotion="relieved", ts="2024-01-09T14:30:00Z")
            ]
        ),
        system_context=SystemContext(personality="ColdBoss")
    )
    
    return scenarios


def demo_companion_system():
    """演示E-Mate环境智能AI伙伴的完整系统能力"""
    print("🌱 E-Mate 环境智能AI伙伴 - 完整系统演示")
    print("=" * 60)
    print("展示从状态感知到动作输出的完整伙伴式支持流程\n")
    
    scenarios = create_companion_scenarios()
    
    for scenario_name, input_state in scenarios.items():
        print(f"📋 场景: {scenario_name}")
        print(f"   人格: {input_state.system_context.personality}")
        print(f"   用户输入: {input_state.perception_input.user_text}")
        print(f"   情感状态: {input_state.perception_input.speech_emotion}")
        print(f"   环境标记: {input_state.perception_input.context_flags}")
        
        # 1. 环境感知 - 状态离散化
        state_id = discretize_state(input_state)
        print(f"\n🧠 环境感知状态: {state_id}")
        
        # 解析状态维度
        state_parts = state_id.split("|")
        for part in state_parts:
            dimension, value = part.split("_", 1)
            dimension_names = {
                "RHYTHM": "工作节律",
                "HEALTH": "健康状态", 
                "EMOTION": "情感连接",
                "GOAL": "个人目标",
                "ENV": "环境上下文"
            }
            print(f"     • {dimension_names.get(dimension, dimension)}: {value}")
        
        # 2. 决策推理 - 简化版本，直接基于状态推荐动作
        recommended_action = _recommend_action_for_scenario(scenario_name)
        print(f"\n🎯 推荐动作: {recommended_action}")
        
        # 3. 动作输出 - 映射为具体指令
        try:
            output_command = map_action_to_output(
                recommended_action, 
                related_task="凤凰项目" if "凤凰" in input_state.perception_input.user_text else None,
                personality=input_state.system_context.personality
            )
            
            print(f"\n💫 伙伴响应:")
            print(f"     屏幕动画: {output_command.execution_output.screen_animation}")
            print(f"     灯光效果: {output_command.execution_output.light_effect}")
            print(f"     语音回应: {output_command.tts_output.text_to_speak}")
            print(f"     执行动作: {output_command.action.type}")
            
        except Exception as e:
            print(f"     ⚠️ 动作映射错误: {e}")
        
        print("\n" + "="*60 + "\n")


def _recommend_action_for_scenario(scenario_name: str) -> str:
    """
    基于场景推荐合适的E-Mate伙伴动作
    
    这是一个简化的启发式规则，在实际系统中会由
    Q-Learning或启发式决策逻辑来决定。
    """
    action_mapping = {
        "深度工作保护": "A_DEEP_WORK_MODE",
        "健康守护干预": "A_MOVEMENT_REMINDER", 
        "情感支持陪伴": "A_EMOTIONAL_SUPPORT",
        "个性化洞察": "A_PERSONALIZED_INSIGHT",
        "环境协调优化": "A_DISTRACTION_SHIELD"
    }
    
    return action_mapping.get(scenario_name, "A_GENTLE_PRESENCE")


def analyze_companion_capabilities():
    """分析E-Mate环境智能AI伙伴的能力覆盖"""
    print("🔍 E-Mate 伙伴能力分析")
    print("=" * 40)
    
    capabilities = {
        "工作节律协调": ["A_DEEP_WORK_MODE", "A_FOCUS_FLOW", "A_ENERGY_BOOST"],
        "健康守护": ["A_MOVEMENT_REMINDER", "A_BREATHING_GUIDE", "A_ENVIRONMENT_ADJUST"],
        "情感连接": ["A_EMOTIONAL_SUPPORT", "A_CELEBRATION", "A_GENTLE_PRESENCE"],
        "个性化智能": ["A_GOAL_PROGRESS", "A_HABIT_NUDGE", "A_PERSONALIZED_INSIGHT"],
        "环境协调": ["A_SPACE_OPTIMIZATION", "A_DISTRACTION_SHIELD", "A_AMBIENT_COMPANION"]
    }
    
    total_actions = sum(len(actions) for actions in capabilities.values())
    print(f"总计 {total_actions} 种伙伴动作能力\n")
    
    for capability, actions in capabilities.items():
        print(f"🎯 {capability}: {len(actions)} 种动作")
        for action in actions:
            action_name = action.replace("A_", "").replace("_", " ").title()
            print(f"   • {action_name}")
        print()


if __name__ == "__main__":
    demo_companion_system()
    print("\n")
    analyze_companion_capabilities()
