"""
环境感知演示模块

展示E-Mate作为环境智能AI伙伴的状态感知能力。
重点演示"从助手到伙伴"的转变，体现主动式、个性化的陪伴支持。
"""

from __future__ import annotations

import json
from typing import Any, Dict

from emate.core.contracts import InputState, PerceptionInput, SystemContext, MemoryInput, MemoryEpisode
from emate.core.graph import PersonaDecisionGraph
from emate.micro.state_discretizer import discretize_state


def create_environmental_scenarios() -> Dict[str, InputState]:
    """
    创建体现E-Mate环境感知能力的多种场景
    
    这些场景展示E-Mate如何理解用户的工作节律、健康状态、
    情感需求和个性化上下文。
    """
    scenarios = {}
    
    # 场景1：深度工作中的用户需要保护
    scenarios["深度专注保护"] = InputState(
        perception_input=PerceptionInput(
            user_text="我要开始处理凤凰项目的核心算法了",
            speech_emotion="calm",
            text_sentiment="neutral",
            context_flags=["deep_work_mode", "important_task", "quiet_space"],
            time_of_day="morning"
        ),
        memory_input=MemoryInput(
            facts=["凤凰项目是本季度最重要的工作", "用户偏好早晨进行深度思考"],
            episodes=[
                MemoryEpisode(event="凤凰项目算法设计会议", emotion="focused", ts="2024-01-10T09:00:00Z"),
                MemoryEpisode(event="用户表达对项目进展的担忧", emotion="stress", ts="2024-01-09T14:30:00Z")
            ]
        ),
        system_context=SystemContext(personality="StandardAssistant")
    )
    
    # 场景2：久坐疲劳需要健康干预
    scenarios["健康守护提醒"] = InputState(
        perception_input=PerceptionInput(
            user_text="感觉有点累了，但还有好多事要做",
            speech_emotion="fatigue",
            text_sentiment="negative",
            context_flags=["sitting_over_2h", "high_workload", "deadline_near"],
            time_of_day="afternoon"
        ),
        memory_input=MemoryInput(
            facts=["用户习惯午后能量下降", "用户重视工作效率"],
            episodes=[
                MemoryEpisode(event="用户连续工作3小时未休息", emotion="fatigue", ts="2024-01-10T15:00:00Z"),
                MemoryEpisode(event="用户接受了上次的休息建议", emotion="grateful", ts="2024-01-09T15:30:00Z")
            ]
        ),
        system_context=SystemContext(personality="WarmSister")
    )
    
    # 场景3：压力状态需要情感支持
    scenarios["情感支持陪伴"] = InputState(
        perception_input=PerceptionInput(
            user_text="这个bug怎么都找不到，快要疯了",
            speech_emotion="stress",
            text_sentiment="negative",
            context_flags=["task_switching", "interruption_high", "frustration_high"],
            time_of_day="evening"
        ),
        memory_input=MemoryInput(
            facts=["用户是完美主义者", "技术问题会让用户特别焦虑"],
            episodes=[
                MemoryEpisode(event="用户因技术难题感到挫败", emotion="frustrated", ts="2024-01-10T18:00:00Z"),
                MemoryEpisode(event="E-Mate提供了调试建议", emotion="helpful", ts="2024-01-10T18:15:00Z")
            ]
        ),
        system_context=SystemContext(personality="CuteCat")
    )
    
    # 场景4：目标进展需要个性化洞察
    scenarios["个性化洞察"] = InputState(
        perception_input=PerceptionInput(
            user_text="凤凰项目的进展怎么样了？",
            speech_emotion="calm",
            text_sentiment="neutral",
            context_flags=["goal_review", "progress_check"],
            time_of_day="morning"
        ),
        memory_input=MemoryInput(
            facts=["凤凰项目是Q1的关键目标", "用户喜欢数据化的进展反馈"],
            episodes=[
                MemoryEpisode(event="完成了凤凰项目的需求分析", emotion="accomplished", ts="2024-01-08T16:00:00Z"),
                MemoryEpisode(event="凤凰项目架构设计评审通过", emotion="satisfied", ts="2024-01-09T11:00:00Z"),
                MemoryEpisode(event="开始凤凰项目核心开发", emotion="focused", ts="2024-01-10T09:00:00Z")
            ]
        ),
        system_context=SystemContext(personality="AnimeWizard")
    )
    
    # 场景5：工作环境需要协调优化
    scenarios["环境协调优化"] = InputState(
        perception_input=PerceptionInput(
            user_text="办公室今天好吵，很难集中注意力",
            speech_emotion="angry",
            text_sentiment="negative", 
            context_flags=["environment_uncomfortable", "interruption_high", "noise_distraction"],
            time_of_day="afternoon"
        ),
        memory_input=MemoryInput(
            facts=["用户对噪音比较敏感", "安静环境能显著提升用户效率"],
            episodes=[
                MemoryEpisode(event="用户抱怨办公环境嘈杂", emotion="irritated", ts="2024-01-10T14:00:00Z"),
                MemoryEpisode(event="E-Mate建议使用降噪耳机", emotion="helpful", ts="2024-01-09T14:30:00Z")
            ]
        ),
        system_context=SystemContext(personality="ColdBoss")
    )
    
    return scenarios


def demo_environmental_awareness():
    """演示E-Mate的环境感知和状态理解能力"""
    print("=== E-Mate 环境智能AI伙伴 - 状态感知演示 ===\n")
    print("展示E-Mate如何理解用户的多维状态，提供主动式、个性化的陪伴支持\n")
    
    scenarios = create_environmental_scenarios()
    
    for scenario_name, input_state in scenarios.items():
        print(f"🌱 场景: {scenario_name}")
        print(f"   人格: {input_state.system_context.personality}")
        print(f"   用户状态: {input_state.perception_input.user_text}")
        print(f"   情感: {input_state.perception_input.speech_emotion}")
        print(f"   环境标记: {input_state.perception_input.context_flags}")
        
        # 生成环境感知状态ID
        state_id = discretize_state(input_state)
        print(f"   🧠 环境感知状态: {state_id}")
        
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
        
        print("\n" + "="*60 + "\n")


def analyze_state_space_coverage():
    """分析新状态空间的覆盖范围和多样性"""
    scenarios = create_environmental_scenarios()
    state_ids = []
    
    print("=== 环境感知状态空间分析 ===\n")
    
    for scenario_name, input_state in scenarios.items():
        state_id = discretize_state(input_state)
        state_ids.append(state_id)
        
    print(f"生成了 {len(set(state_ids))} 个不同的状态ID")
    print(f"状态重复率: {(len(state_ids) - len(set(state_ids))) / len(state_ids) * 100:.1f}%")
    
    # 分析各维度的分布
    dimensions = {"RHYTHM": [], "HEALTH": [], "EMOTION": [], "GOAL": [], "ENV": []}
    
    for state_id in state_ids:
        parts = state_id.split("|")
        for part in parts:
            dim, value = part.split("_", 1)
            if dim in dimensions:
                dimensions[dim].append(value)
    
    print("\n各维度状态分布:")
    for dim, values in dimensions.items():
        unique_values = set(values)
        print(f"  {dim}: {len(unique_values)} 种状态 - {list(unique_values)}")
    
    return state_ids


if __name__ == "__main__":
    demo_environmental_awareness()
    print("\n")
    analyze_state_space_coverage()
