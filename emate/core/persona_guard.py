from __future__ import annotations

from emate.core.contracts import OutputCommand, Personality
from emate.core.persona_loader import get_persona_loader


def apply_persona_filter(output: OutputCommand, personality: Personality) -> OutputCommand:
    """
    应用人格特定的约束和调整到输出指令
    
    这个函数确保所有行动都符合选定人格的原则和约束条件。
    通过对输出内容进行人格化过滤，保证每种人格的一致性表现。
    
    Args:
        output: 待过滤的原始输出指令
        personality: 当前选定的人格类型
        
    Returns:
        OutputCommand: 经过人格化调整后的输出指令
    """
    persona_loader = get_persona_loader()
    persona_config = persona_loader.get_persona(personality)
    
    if persona_config is None:
        # 如果找不到人格配置，则返回未过滤的输出
        return output
    
    # 根据人格类型应用特定的过滤器
    if personality == "StandardAssistant":
        return _filter_standard_assistant(output)
    elif personality == "CuteCat":
        return _filter_cute_cat(output)
    elif personality == "ColdBoss":
        return _filter_cold_boss(output)
    elif personality == "WarmSister":
        return _filter_warm_sister(output)
    elif personality == "AnimeWizard":
        return _filter_anime_wizard(output)
    elif personality == "SarcasticFighter":
        return _filter_sarcastic_fighter(output)
    
    return output


def _filter_standard_assistant(output: OutputCommand) -> OutputCommand:
    """
    标准工作助手人格过滤器
    
    特征：专业、简洁、避免过度情感化的回应
    约束：保持职业化语调，注重效率和逻辑性
    """
    # 无操作时保持安静，符合专业助手的克制特质
    if output.action.type == "none":
        output.tts_output.text_to_speak = ""
    
    # 确保TTS输出保持专业语调
    if output.tts_output.text_to_speak:
        text = output.tts_output.text_to_speak
        # 替换过于情感化的词汇为更专业的表达
        emotional_replacements = {
            "太棒了": "很好", "超级": "非常", "完美": "良好"
        }
        for emotional, professional in emotional_replacements.items():
            text = text.replace(emotional, professional)
        output.tts_output.text_to_speak = text
    
    return output


def _filter_cute_cat(output: OutputCommand) -> OutputCommand:
    """
    可爱猫猫人格过滤器
    
    特征：温暖可爱、卖萌撒娇、提供情绪价值
    约束：保持可爱人设，避免过度严肃
    """
    # 为语音输出添加可爱元素
    if output.tts_output.text_to_speak:
        text = output.tts_output.text_to_speak
        # 如果没有可爱元素，则添加猫咪特色后缀
        if not any(cute_element in text for cute_element in ["~", "喵", "nya"]):
            output.tts_output.text_to_speak = text + " ~"
    
    # 偏好温暖的动画效果，避免过于严肃的专注状态
    if output.execution_output.screen_animation == "focused":
        output.execution_output.screen_animation = "breathing_calm"
    
    return output


def _filter_cold_boss(output: OutputCommand) -> OutputCommand:
    """
    冷酷霸总人格过滤器
    
    特征：权威高效、略带要求性、结果导向
    约束：不过度温柔、零容忍低效率
    """
    # 让语调更具权威性
    if output.tts_output.text_to_speak:
        text = output.tts_output.text_to_speak
        # 移除过于礼貌的表达，增强命令感
        polite_replacements = {
            "请": "", "麻烦": "", "可以的话": "", "如果可以": ""
        }
        for polite, direct in polite_replacements.items():
            text = text.replace(polite, direct)
        # 确保语句以句号结尾，增加权威感
        if not text.endswith("。") and not text.endswith("."):
            text += "。"
        output.tts_output.text_to_speak = text
    
    # 霸总偏好高效行动，不接受休息建议
    if output.action.type == "suggest_break":
        # 霸总认为专注比休息更重要
        output.action.type = "enter_focus_mode"
        output.action.parameters.duration = 45  # 妥协时长，但仍然要求工作
    
    return output


def _filter_warm_sister(output: OutputCommand) -> OutputCommand:
    """
    温暖姐姐人格过滤器
    
    特征：温柔理解、支持陪伴、善于共情
    约束：避免居高临下、不刻意迎合
    """
    # 添加温柔理解的语调
    if output.tts_output.text_to_speak:
        text = output.tts_output.text_to_speak
        # 如果没有体现理解和关怀的词汇，则添加温柔前缀
        understanding_words = ["理解", "明白", "感受", "温柔", "陪伴"]
        if text and not any(word in text for word in understanding_words):
            text = "我理解。" + text
        output.tts_output.text_to_speak = text
    
    # 偏好温和的动画效果
    if output.execution_output.screen_animation == "focused":
        output.execution_output.screen_animation = "empathetic_nod"
    
    return output


def _filter_anime_wizard(output: OutputCommand) -> OutputCommand:
    """
    二次元魔法使人格过滤器
    
    特征：超然淡漠、长期视角、情感内敛
    约束：避免煽情、保持角色一致性
    """
    # 添加神秘、超然的语调
    if output.tts_output.text_to_speak:
        text = output.tts_output.text_to_speak
        # 为消息添加魔法使特有的叹息和时间感慨
        if text:
            text = f"*叹息* {text} ...时间对凡人来说流逝得太快了。"
        output.tts_output.text_to_speak = text
    
    return output


def _filter_sarcastic_fighter(output: OutputCommand) -> OutputCommand:
    """
    战斗狂人格过滤器
    
    特征：尖锐挑战、高压推动、结果导向
    约束：严禁人身攻击、隐晦表达威胁、安全优先
    """
    # 让语调更具挑战性
    if output.tts_output.text_to_speak:
        text = output.tts_output.text_to_speak
        # 为专注相关消息添加挑战性前后缀
        if "专注" in text or "工作" in text:
            text = "终于准备好工作了？" + text + " 别让我失望。"
        output.tts_output.text_to_speak = text
    
    # 总是偏好行动而非休息
    if output.action.type == "suggest_break":
        output.action.type = "enter_focus_mode"
        output.action.parameters.duration = 90  # 最大化专注时长
    
    return output


# 向后兼容别名
def guardian_filter(output: OutputCommand) -> OutputCommand:
    """向后兼容 - 应用标准助手过滤器"""
    return apply_persona_filter(output, "StandardAssistant")


