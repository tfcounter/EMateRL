"""
E-Mate环境智能AI伙伴完整系统测试

端到端测试完整的决策流程：
感知输入 → 状态离散化 → 决策推理 → 动作输出 → 人格化响应
"""

from __future__ import annotations

import json
from typing import Dict, Any

from emate.core.contracts import InputState, PerceptionInput, SystemContext, MemoryInput, MemoryEpisode
from emate.core.graph import PersonaDecisionGraph


def create_comprehensive_test_scenarios() -> Dict[str, InputState]:
    """
    创建全面的测试场景，覆盖E-Mate的各种伙伴能力
    """
    scenarios = {}
    
    # 场景1：早晨深度工作 - 测试工作节律协调
    scenarios["早晨深度工作"] = InputState(
        perception_input=PerceptionInput(
            user_text="今天要完成凤凰项目的核心算法设计，很重要",
            speech_emotion="calm",
            text_sentiment="neutral",
            context_flags=["deep_work_mode", "important_task", "quiet_space", "energy_high"],
            time_of_day="morning"
        ),
        memory_input=MemoryInput(
            facts=["凤凰项目是Q1最重要目标", "用户早晨效率最高", "算法设计需要长时间专注"],
            episodes=[
                MemoryEpisode(event="凤凰项目需求分析完成", emotion="satisfied", ts="2024-01-08T17:00:00Z"),
                MemoryEpisode(event="用户表达对项目重要性的认知", emotion="focused", ts="2024-01-10T08:00:00Z")
            ]
        ),
        system_context=SystemContext(personality="StandardAssistant")
    )
    
    # 场景2：午后疲劳 - 测试健康守护
    scenarios["午后疲劳干预"] = InputState(
        perception_input=PerceptionInput(
            user_text="眼睛好累，脖子僵硬，但还有任务要做",
            speech_emotion="fatigue",
            text_sentiment="negative",
            context_flags=["sitting_over_2h", "eye_strain", "high_workload", "post_lunch_dip"],
            time_of_day="afternoon"
        ),
        memory_input=MemoryInput(
            facts=["用户容易午后疲劳", "久坐是用户的主要健康风险", "用户重视工作进度"],
            episodes=[
                MemoryEpisode(event="连续工作3小时未休息", emotion="tired", ts="2024-01-10T14:30:00Z"),
                MemoryEpisode(event="上次休息建议被接受并感谢", emotion="grateful", ts="2024-01-09T15:00:00Z")
            ]
        ),
        system_context=SystemContext(personality="WarmSister")
    )
    
    # 场景3：技术困难压力 - 测试情感连接
    scenarios["技术困难压力"] = InputState(
        perception_input=PerceptionInput(
            user_text="这个算法bug找了3小时了，完全没有头绪，快要崩溃了",
            speech_emotion="stress",
            text_sentiment="negative", 
            context_flags=["frustration_high", "task_stuck", "deadline_near", "emotional_distress"],
            time_of_day="evening"
        ),
        memory_input=MemoryInput(
            facts=["用户是完美主义者", "技术问题会让用户特别焦虑", "用户需要情感支持"],
            episodes=[
                MemoryEpisode(event="因技术难题感到挫败", emotion="frustrated", ts="2024-01-10T18:00:00Z"),
                MemoryEpisode(event="E-Mate之前提供过有效的情感支持", emotion="comforted", ts="2024-01-09T19:00:00Z")
            ]
        ),
        system_context=SystemContext(personality="CuteCat")
    )
    
    # 场景4：周末复盘 - 测试个性化智能
    scenarios["周末工作复盘"] = InputState(
        perception_input=PerceptionInput(
            user_text="这一周工作怎么样？凤凰项目进展如何？有什么需要改进的？",
            speech_emotion="calm",
            text_sentiment="neutral",
            context_flags=["self_reflection", "progress_review", "improvement_seeking", "goal_review"],
            time_of_day="evening"
        ),
        memory_input=MemoryInput(
            facts=["凤凰项目是核心目标", "用户喜欢数据化反馈", "用户有持续改进的习惯"],
            episodes=[
                MemoryEpisode(event="完成凤凰项目需求分析", emotion="accomplished", ts="2024-01-08T16:00:00Z"),
                MemoryEpisode(event="凤凰项目架构设计进展", emotion="productive", ts="2024-01-09T14:00:00Z"),
                MemoryEpisode(event="开始核心算法开发", emotion="focused", ts="2024-01-10T09:00:00Z"),
                MemoryEpisode(event="解决了关键技术难题", emotion="satisfied", ts="2024-01-10T17:00:00Z")
            ]
        ),
        system_context=SystemContext(personality="AnimeWizard")
    )
    
    # 场景5：嘈杂环境干扰 - 测试环境协调
    scenarios["嘈杂环境干扰"] = InputState(
        perception_input=PerceptionInput(
            user_text="办公室今天特别吵，会议声、电话声，完全没法专注工作",
            speech_emotion="angry",
            text_sentiment="negative",
            context_flags=["environment_uncomfortable", "interruption_high", "noise_distraction", "task_switching"],
            time_of_day="afternoon"
        ),
        memory_input=MemoryInput(
            facts=["用户对噪音非常敏感", "安静环境能显著提升用户效率", "用户需要专注完成重要任务"],
            episodes=[
                MemoryEpisode(event="噪音干扰导致工作效率下降", emotion="irritated", ts="2024-01-10T14:00:00Z"),
                MemoryEpisode(event="E-Mate成功帮助屏蔽了干扰", emotion="relieved", ts="2024-01-09T15:30:00Z")
            ]
        ),
        system_context=SystemContext(personality="ColdBoss")
    )
    
    # 场景6：成就庆祝 - 测试积极情感连接
    scenarios["项目里程碑达成"] = InputState(
        perception_input=PerceptionInput(
            user_text="太好了！凤凰项目的核心算法终于调通了，性能比预期还好！",
            speech_emotion="happy",
            text_sentiment="positive",
            context_flags=["achievement_unlocked", "milestone_reached", "performance_exceeded"],
            time_of_day="evening"
        ),
        memory_input=MemoryInput(
            facts=["凤凰项目是用户最重要的工作", "算法性能是关键指标", "用户为此投入了大量精力"],
            episodes=[
                MemoryEpisode(event="凤凰项目启动", emotion="determined", ts="2024-01-05T09:00:00Z"),
                MemoryEpisode(event="算法设计遇到困难", emotion="frustrated", ts="2024-01-08T16:00:00Z"),
                MemoryEpisode(event="持续优化算法性能", emotion="persistent", ts="2024-01-10T14:00:00Z")
            ]
        ),
        system_context=SystemContext(personality="SarcasticFighter")
    )
    
    return scenarios


def run_complete_system_test():
    """运行完整的E-Mate系统测试"""
    print("🌱 E-Mate 环境智能AI伙伴 - 完整系统测试")
    print("=" * 70)
    print("测试完整决策流程：感知 → 状态理解 → 智能决策 → 伙伴响应\n")
    
    # 创建决策图实例
    decision_graph = PersonaDecisionGraph()
    
    # 运行所有测试场景
    scenarios = create_comprehensive_test_scenarios()
    
    for i, (scenario_name, input_state) in enumerate(scenarios.items(), 1):
        print(f"📋 测试场景 {i}: {scenario_name}")
        print(f"   👤 人格: {input_state.system_context.personality}")
        print(f"   🗣️  用户输入: {input_state.perception_input.user_text}")
        print(f"   😊 情感状态: {input_state.perception_input.speech_emotion}")
        print(f"   🏷️  环境标记: {input_state.perception_input.context_flags}")
        print(f"   ⏰ 时间: {input_state.perception_input.time_of_day}")
        
        # 显示记忆上下文
        print(f"   💭 记忆事实: {len(input_state.memory_input.facts)} 条")
        print(f"   📚 历史经历: {len(input_state.memory_input.episodes)} 条")
        
        try:
            # 运行完整的决策流程
            print(f"\n🧠 执行决策流程...")
            output_command = decision_graph.run_once(input_state)
            
            print(f"✨ E-Mate伙伴响应:")
            print(f"     🎬 屏幕动画: {output_command.execution_output.screen_animation}")
            print(f"     💡 灯光效果: {output_command.execution_output.light_effect}")
            print(f"     🎵 语音回应: {output_command.tts_output.text_to_speak}")
            print(f"     ⚡ 执行动作: {output_command.action.type}")
            
            if output_command.action.parameters:
                if output_command.action.parameters.duration:
                    print(f"     ⏱️  持续时间: {output_command.action.parameters.duration} 分钟")
                if output_command.action.parameters.related_task:
                    print(f"     📋 相关任务: {output_command.action.parameters.related_task}")
            
        except Exception as e:
            print(f"     ❌ 系统错误: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*70 + "\n")


def analyze_system_performance():
    """分析系统性能和覆盖范围"""
    print("📊 E-Mate系统性能分析")
    print("=" * 40)
    
    scenarios = create_comprehensive_test_scenarios()
    
    # 统计各维度覆盖
    emotions_covered = set()
    times_covered = set()
    personalities_covered = set()
    context_flags_covered = set()
    
    for scenario_name, input_state in scenarios.items():
        emotions_covered.add(input_state.perception_input.speech_emotion)
        times_covered.add(input_state.perception_input.time_of_day)
        personalities_covered.add(input_state.system_context.personality)
        context_flags_covered.update(input_state.perception_input.context_flags)
    
    print(f"🎭 测试场景总数: {len(scenarios)}")
    print(f"😊 情感状态覆盖: {len(emotions_covered)} 种 - {list(emotions_covered)}")
    print(f"⏰ 时间段覆盖: {len(times_covered)} 种 - {list(times_covered)}")
    print(f"👤 人格类型覆盖: {len(personalities_covered)} 种 - {list(personalities_covered)}")
    print(f"🏷️  上下文标记覆盖: {len(context_flags_covered)} 种")
    
    print(f"\n🎯 测试覆盖的伙伴能力:")
    capability_mapping = {
        "早晨深度工作": "工作节律协调",
        "午后疲劳干预": "健康守护",
        "技术困难压力": "情感连接",
        "周末工作复盘": "个性化智能",
        "嘈杂环境干扰": "环境协调",
        "项目里程碑达成": "情感连接(积极)"
    }
    
    for scenario, capability in capability_mapping.items():
        print(f"     • {scenario} → {capability}")


if __name__ == "__main__":
    run_complete_system_test()
    print("\n")
    analyze_system_performance()
