"""
环境感知状态离散化模块

将E-Mate作为环境智能AI伴侣的多维感知信息压缩为状态标识符。
重点关注用户的工作节律、健康状态、情感连接和长期目标进展。

核心理念：
E-Mate不是功能性AI助手，而是工作空间中的智能伙伴，
需要感知和理解用户的整体状态，提供主动式、个性化的陪伴支持。

状态维度：
- 工作节律感知（专注状态、疲劳程度、工作强度）
- 健康守护维度（久坐时长、环境舒适度、压力水平）
- 情感连接状态（情绪状态、互动历史、信任程度）
- 个性化理解（长期目标进展、习惯模式、个人偏好）
- 环境协调能力（时间感知、空间状态、干扰水平）
"""

from __future__ import annotations

from typing import Tuple
from emate.core.contracts import InputState


def _safe(val: str | None, fallback: str) -> str:
    """
    安全获取字符串值，提供默认回退
    
    Args:
        val: 可能为None的字符串值
        fallback: 当val为None时的默认值
        
    Returns:
        str: val本身或fallback值
    """
    return val if val else fallback


def discretize_state(input_state: InputState) -> str:
    """
    将E-Mate的环境感知信息离散化为伙伴状态ID
    
    作为环境智能AI伙伴，E-Mate需要理解用户的整体工作和生活状态，
    而不仅仅是处理功能性指令。状态设计体现"从助手到伙伴"的转变。
    
    Args:
        input_state: 包含多维感知和记忆信息的完整环境状态
        
    Returns:
        str: 环境感知状态ID，如"RHYTHM_focused_flow|HEALTH_sitting_2h|EMOTION_stress_high|GOAL_phoenix_behind|ENV_afternoon_quiet"
    """
    p = input_state.perception_input
    m = input_state.memory_input
    flags = set(p.context_flags)

    # 1. 工作节律感知 - E-Mate理解用户的工作状态和专注程度
    work_rhythm = _assess_work_rhythm(p, flags)
    
    # 2. 健康守护维度 - 作为健康管家，监测用户的身体状态
    health_status = _assess_health_status(p, flags)
    
    # 3. 情感连接状态 - 理解用户的情感需求和压力水平
    emotional_connection = _assess_emotional_state(p, m)
    
    # 4. 个性化理解 - 基于长期记忆理解用户目标和习惯
    personal_context = _assess_personal_context(p, m, flags)
    
    # 5. 环境协调能力 - 感知工作环境和时间上下文
    environmental_context = _assess_environmental_context(p, flags)

    # 组合环境感知状态
    parts: Tuple[str, ...] = (
        f"RHYTHM_{work_rhythm}",        # 工作节律
        f"HEALTH_{health_status}",      # 健康状态
        f"EMOTION_{emotional_connection}",  # 情感连接
        f"GOAL_{personal_context}",     # 个人目标
        f"ENV_{environmental_context}", # 环境上下文
    )
    return "|".join(parts)


def _assess_work_rhythm(p, flags: set) -> str:
    """
    评估用户的工作节律状态
    
    E-Mate作为工作伙伴需要理解用户的专注状态、工作强度和疲劳程度，
    以提供合适的环境协调和主动支持。
    """
    # 检测深度工作状态
    if "deep_work_mode" in flags:
        return "deep_focus"
    
    # 基于情感和上下文推断工作节律
    if p.speech_emotion == "stress" and "deadline_near" in flags:
        return "intense_work"  # 高强度工作状态
    elif p.speech_emotion == "fatigue":
        return "energy_low"   # 能量不足状态
    elif p.speech_emotion == "calm" and "task_switching" not in flags:
        return "steady_flow"  # 稳定流状态
    elif "task_switching" in flags or "interruption_high" in flags:
        return "fragmented"   # 碎片化工作
    else:
        return "normal"       # 正常工作状态


def _assess_health_status(p, flags: set) -> str:
    """
    评估用户的健康守护需求
    
    E-Mate作为健康管家，监测用户的身体状态和工作习惯，
    提供非侵入式的健康提醒和环境调节。
    """
    # 久坐时长检测
    if "sitting_over_2h" in flags:
        return "sitting_long"
    elif "sitting_over_1h" in flags:
        return "sitting_moderate"
    
    # 压力相关健康状态
    if p.speech_emotion in ["stress", "angry"] and "high_workload" in flags:
        return "stress_high"
    elif p.speech_emotion == "fatigue":
        return "energy_depleted"
    
    # 环境舒适度
    if "environment_uncomfortable" in flags:
        return "env_poor"
    
    return "healthy"  # 健康状态良好


def _assess_emotional_state(p, m) -> str:
    """
    评估用户的情感连接和心理状态
    
    E-Mate需要建立情感连接，理解用户的情绪需求，
    提供有温度的陪伴和支持。
    """
    # 当前情绪状态
    if p.speech_emotion == "stress" and p.text_sentiment == "negative":
        return "overwhelmed"  # 不堪重负
    elif p.speech_emotion == "sad":
        return "need_comfort"  # 需要安慰
    elif p.speech_emotion == "happy":
        return "positive_mood"  # 积极情绪
    elif p.speech_emotion == "fatigue":
        return "emotionally_drained"  # 情绪耗竭
    
    # 基于历史互动评估情感连接
    recent_interactions = len([ep for ep in m.episodes if "interaction" in ep.event.lower()])
    if recent_interactions > 5:
        return "connected"  # 良好连接
    elif recent_interactions == 0:
        return "distant"    # 疏远状态
    
    return "neutral"  # 中性情感状态


def _assess_personal_context(p, m, flags: set) -> str:
    """
    评估个性化理解和长期目标进展
    
    E-Mate通过长期记忆理解用户的目标、习惯和偏好，
    提供个性化的支持和建议。
    """
    # 检查重要项目进展
    important_projects = ["凤凰", "phoenix", "重要项目"]
    if any(project in p.user_text.lower() for project in important_projects):
        if "deadline_near" in flags:
            return "important_behind"  # 重要项目落后
        else:
            return "important_progress"  # 重要项目进展中
    
    # 基于记忆评估目标进展
    goal_related_episodes = [ep for ep in m.episodes if any(
        goal_word in ep.event.lower() for goal_word in ["目标", "计划", "项目"]
    )]
    
    if len(goal_related_episodes) > 3:
        return "goal_active"  # 目标活跃追求
    elif len(goal_related_episodes) == 0:
        return "goal_unclear"  # 目标不明确
    
    return "routine"  # 日常状态


def _assess_environmental_context(p, flags: set) -> str:
    """
    评估环境协调和空间状态
    
    E-Mate作为环境智能伙伴，需要感知工作环境的状态，
    协调整个工作空间的智能化支持。
    """
    tod = _safe(p.time_of_day, "unknown")
    
    # 时间和环境组合评估
    if tod == "morning" and "energy_high" in flags:
        return "morning_fresh"  # 清晨活力
    elif tod == "afternoon" and "post_lunch_dip" in flags:
        return "afternoon_low"  # 午后低潮
    elif tod == "evening" and "overtime" in flags:
        return "evening_overtime"  # 晚间加班
    
    # 环境干扰水平
    if "interruption_high" in flags:
        return f"{tod}_chaotic"  # 混乱环境
    elif "quiet_space" in flags:
        return f"{tod}_peaceful"  # 安静环境
    
    return f"{tod}_normal"  # 正常环境


