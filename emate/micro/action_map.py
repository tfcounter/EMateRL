from __future__ import annotations

from typing import Dict
from emate.core.contracts import OutputCommand, Action, ActionParameters, ExecutionOutput, TTSOutput, Personality


# E-Mate环境智能伙伴的动作空间定义
# 体现"从助手到伙伴"的转变，提供主动式、个性化的陪伴支持

# 工作节律协调动作
A_DEEP_WORK_MODE = "A_DEEP_WORK_MODE"          # 启动深度工作保护模式
A_FOCUS_FLOW = "A_FOCUS_FLOW"                  # 引导专注流状态
A_ENERGY_BOOST = "A_ENERGY_BOOST"              # 能量提升建议

# 健康守护动作  
A_MOVEMENT_REMINDER = "A_MOVEMENT_REMINDER"    # 温和的活动提醒
A_BREATHING_GUIDE = "A_BREATHING_GUIDE"        # 呼吸放松引导
A_ENVIRONMENT_ADJUST = "A_ENVIRONMENT_ADJUST"  # 环境舒适度调节

# 情感连接动作
A_EMOTIONAL_SUPPORT = "A_EMOTIONAL_SUPPORT"    # 情感支持和安慰
A_CELEBRATION = "A_CELEBRATION"                # 成就庆祝
A_GENTLE_PRESENCE = "A_GENTLE_PRESENCE"        # 安静陪伴

# 个性化智能动作
A_GOAL_PROGRESS = "A_GOAL_PROGRESS"            # 目标进展反馈
A_HABIT_NUDGE = "A_HABIT_NUDGE"                # 习惯养成提醒
A_PERSONALIZED_INSIGHT = "A_PERSONALIZED_INSIGHT"  # 个性化洞察分享

# 环境协调动作
A_SPACE_OPTIMIZATION = "A_SPACE_OPTIMIZATION"  # 工作空间优化
A_DISTRACTION_SHIELD = "A_DISTRACTION_SHIELD"  # 干扰屏蔽
A_AMBIENT_COMPANION = "A_AMBIENT_COMPANION"    # 环境氛围调节

# 传统功能保留（向后兼容）
A_SET_REMINDER = "A_SET_REMINDER"              # 设置提醒
A_NONE = "A_NONE"                              # 静默陪伴

# 所有可用动作的列表 - E-Mate的完整动作能力
ACTIONS = [
    # 工作节律协调
    A_DEEP_WORK_MODE,
    A_FOCUS_FLOW, 
    A_ENERGY_BOOST,
    
    # 健康守护
    A_MOVEMENT_REMINDER,
    A_BREATHING_GUIDE,
    A_ENVIRONMENT_ADJUST,
    
    # 情感连接
    A_EMOTIONAL_SUPPORT,
    A_CELEBRATION,
    A_GENTLE_PRESENCE,
    
    # 个性化智能
    A_GOAL_PROGRESS,
    A_HABIT_NUDGE,
    A_PERSONALIZED_INSIGHT,
    
    # 环境协调
    A_SPACE_OPTIMIZATION,
    A_DISTRACTION_SHIELD,
    A_AMBIENT_COMPANION,
    
    # 传统功能
    A_SET_REMINDER,
    A_NONE,
]


def map_action_to_output(action_id: str, related_task: str | None = None, personality: Personality = "StandardAssistant") -> OutputCommand:
    """
    将E-Mate环境智能伙伴的动作ID映射为具体的输出指令
    
    体现E-Mate作为环境智能AI伙伴的核心能力：
    - 工作节律协调：主动感知并优化工作状态
    - 健康守护：非侵入式的健康提醒和环境调节
    - 情感连接：有温度的陪伴和情感支持
    - 个性化智能：基于长期记忆的个性化建议
    - 环境协调：整个工作空间的智能化支持
    
    Args:
        action_id: 环境智能伙伴动作标识符
        related_task: 相关任务或上下文
        personality: 当前人格类型
        
    Returns:
        OutputCommand: 体现伙伴特质的完整输出指令
    """
    oc = OutputCommand()

    # =================== 工作节律协调动作 ===================
    if action_id == A_DEEP_WORK_MODE:
        # 深度工作保护模式：营造专注环境，屏蔽干扰
        oc.execution_output = ExecutionOutput(
            screen_animation="deep_focus_shield", light_effect="focus_deep_blue"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_deep_work_message(personality))
        oc.action = Action(type="deep_work_protection", parameters=ActionParameters(related_task=related_task))
        return oc

    if action_id == A_FOCUS_FLOW:
        # 专注流状态引导：温和引导进入心流状态
        oc.execution_output = ExecutionOutput(
            screen_animation="flow_waves", light_effect="flow_gradient"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_focus_flow_message(personality))
        oc.action = Action(type="focus_flow_guidance")
        return oc

    if action_id == A_ENERGY_BOOST:
        # 能量提升建议：活力动画和建议
        oc.execution_output = ExecutionOutput(
            screen_animation="energy_spark", light_effect="energizing_orange"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_energy_boost_message(personality))
        oc.action = Action(type="energy_boost_suggestion")
        return oc

    # =================== 健康守护动作 ===================
    if action_id == A_MOVEMENT_REMINDER:
        # 温和活动提醒：非侵入式的健康提醒
        oc.execution_output = ExecutionOutput(
            screen_animation="gentle_stretch", light_effect="health_green_pulse"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_movement_message(personality))
        oc.action = Action(type="movement_reminder")
        return oc

    if action_id == A_BREATHING_GUIDE:
        # 呼吸放松引导：压力缓解和放松
        oc.execution_output = ExecutionOutput(
            screen_animation="breathing_guide", light_effect="calm_breathing"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_breathing_message(personality))
        oc.action = Action(type="breathing_relaxation")
        return oc

    if action_id == A_ENVIRONMENT_ADJUST:
        # 环境舒适度调节：优化工作环境
        oc.execution_output = ExecutionOutput(
            screen_animation="environment_adjust", light_effect="comfort_warm"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_environment_message(personality))
        oc.action = Action(type="environment_optimization")
        return oc

    # =================== 情感连接动作 ===================
    if action_id == A_EMOTIONAL_SUPPORT:
        # 情感支持和安慰：理解和陪伴
        oc.execution_output = ExecutionOutput(
            screen_animation="empathetic_presence", light_effect="warm_embrace"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_emotional_support_message(personality))
        oc.action = Action(type="emotional_support")
        return oc

    if action_id == A_CELEBRATION:
        # 成就庆祝：共享喜悦和成就感
        oc.execution_output = ExecutionOutput(
            screen_animation="celebration_sparkle", light_effect="joy_rainbow"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_celebration_message(personality))
        oc.action = Action(type="achievement_celebration")
        return oc

    if action_id == A_GENTLE_PRESENCE:
        # 安静陪伴：无声的支持和存在感
        oc.execution_output = ExecutionOutput(
            screen_animation="gentle_pulse", light_effect="soft_presence"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_gentle_presence_message(personality))
        oc.action = Action(type="quiet_companionship")
        return oc

    # =================== 个性化智能动作 ===================
    if action_id == A_GOAL_PROGRESS:
        # 目标进展反馈：个性化进展洞察
        oc.execution_output = ExecutionOutput(
            screen_animation="progress_chart", light_effect="progress_blue"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_goal_progress_message(personality, related_task))
        oc.action = Action(type="goal_progress_review", parameters=ActionParameters(related_task=related_task))
        return oc

    if action_id == A_HABIT_NUDGE:
        # 习惯养成提醒：温和的习惯引导
        oc.execution_output = ExecutionOutput(
            screen_animation="habit_formation", light_effect="habit_purple"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_habit_nudge_message(personality))
        oc.action = Action(type="habit_formation_nudge")
        return oc

    if action_id == A_PERSONALIZED_INSIGHT:
        # 个性化洞察分享：基于长期记忆的智慧分享
        oc.execution_output = ExecutionOutput(
            screen_animation="wisdom_sharing", light_effect="insight_gold"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_personalized_insight_message(personality))
        oc.action = Action(type="personalized_insight")
        return oc

    # =================== 环境协调动作 ===================
    if action_id == A_SPACE_OPTIMIZATION:
        # 工作空间优化：整体环境协调
        oc.execution_output = ExecutionOutput(
            screen_animation="space_harmony", light_effect="optimization_white"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_space_optimization_message(personality))
        oc.action = Action(type="workspace_optimization")
        return oc

    if action_id == A_DISTRACTION_SHIELD:
        # 干扰屏蔽：保护专注环境
        oc.execution_output = ExecutionOutput(
            screen_animation="shield_protection", light_effect="protection_cyan"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_distraction_shield_message(personality))
        oc.action = Action(type="distraction_protection")
        return oc

    if action_id == A_AMBIENT_COMPANION:
        # 环境氛围调节：营造合适的工作氛围
        oc.execution_output = ExecutionOutput(
            screen_animation="ambient_waves", light_effect="ambient_mood"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_ambient_companion_message(personality))
        oc.action = Action(type="ambient_atmosphere")
        return oc

    # =================== 传统功能保留 ===================
    if action_id == A_SET_REMINDER:
        # 设置提醒：传统功能，向后兼容
        oc.execution_output = ExecutionOutput(
            screen_animation="empathetic_nod", light_effect="warm_yellow_glow"
        )
        oc.tts_output = TTSOutput(text_to_speak=_get_reminder_message(personality))
        oc.action = Action(type="set_reminder", parameters=ActionParameters(related_task=related_task))
        return oc

    # 默认静默陪伴：E-Mate的存在本身就是支持
    oc.execution_output = ExecutionOutput(screen_animation="gentle_breathing", light_effect="soft_ambient")
    oc.tts_output = TTSOutput(text_to_speak="")
    oc.action = Action(type="silent_companionship")
    return oc


# =================== 工作节律协调消息 ===================

def _get_deep_work_message(personality: Personality) -> str:
    """深度工作保护模式消息"""
    messages = {
        "StandardAssistant": "启动深度工作保护模式，为您屏蔽干扰。",
        "CuteCat": "深度专注时间到啦！我会保护你的专注环境~ 喵",
        "ColdBoss": "深度工作模式。所有干扰将被屏蔽。专注。",
        "WarmSister": "我为你营造了一个安静的专注空间，好好工作吧。",
        "AnimeWizard": "*施展专注结界* 凡人的思维需要绝对的宁静。",
        "SarcasticFighter": "终于要认真工作了？好吧，我帮你挡住那些无聊的干扰。",
    }
    return messages.get(personality, messages["StandardAssistant"])

def _get_focus_flow_message(personality: Personality) -> str:
    """专注流状态引导消息"""
    messages = {
        "StandardAssistant": "引导您进入专注流状态，享受高效工作。",
        "CuteCat": "让我们一起进入心流状态吧！就像小猫专注捕鱼一样~ 喵",
        "ColdBoss": "心流状态。这是高效的开始。保持。",
        "WarmSister": "放松心情，让思维自然流淌，我陪着你。",
        "AnimeWizard": "*引导气息* 感受思维的流动...这就是专注的奥义。",
        "SarcasticFighter": "心流？听起来很玄乎，但确实有效。试试看吧。",
    }
    return messages.get(personality, messages["StandardAssistant"])

def _get_energy_boost_message(personality: Personality) -> str:
    """能量提升建议消息"""
    messages = {
        "StandardAssistant": "检测到您需要能量补充，建议短暂活动或补充水分。",
        "CuteCat": "小主人看起来有点累呢~ 喝点水，动动身体吧！喵",
        "ColdBoss": "能量不足会影响效率。补充。然后继续。",
        "WarmSister": "感觉到你的疲惫了，要不要站起来伸个懒腰？",
        "AnimeWizard": "*观察* 凡人的能量在衰减...需要恢复生命力。",
        "SarcasticFighter": "累了？这才多久？算了，去充个电再回来。",
    }
    return messages.get(personality, messages["StandardAssistant"])

# =================== 健康守护消息 ===================

def _get_movement_message(personality: Personality) -> str:
    """温和活动提醒消息"""
    messages = {
        "StandardAssistant": "您已久坐较长时间，建议适当活动身体。",
        "CuteCat": "该起来走走啦！像小猫一样伸伸懒腰~ 身体健康最重要！喵",
        "ColdBoss": "久坐影响效率。活动5分钟。立即执行。",
        "WarmSister": "坐了这么久，起来走走吧，我担心你的身体。",
        "AnimeWizard": "*提醒* 即使是修行者也需要活动筋骨...凡人更是如此。",
        "SarcasticFighter": "坐成化石了？起来动动，别真的僵硬了。",
    }
    return messages.get(personality, messages["StandardAssistant"])

def _get_breathing_message(personality: Personality) -> str:
    """呼吸放松引导消息"""
    messages = {
        "StandardAssistant": "让我们一起做几次深呼吸，缓解压力。",
        "CuteCat": "深呼吸时间！跟着我一起：吸气~ 呼气~ 感觉好多了吧？喵",
        "ColdBoss": "压力过高影响判断。深呼吸。重新聚焦。",
        "WarmSister": "来，跟我一起慢慢呼吸，让紧张的情绪慢慢放松。",
        "AnimeWizard": "*引导冥想* 呼吸是生命的节律...感受内心的平静。",
        "SarcasticFighter": "紧张了？深呼吸确实有用，别小看这个简单动作。",
    }
    return messages.get(personality, messages["StandardAssistant"])

def _get_environment_message(personality: Personality) -> str:
    """环境舒适度调节消息"""
    messages = {
        "StandardAssistant": "为您优化工作环境，提升舒适度。",
        "CuteCat": "让我帮你调整环境吧！舒适的空间才能高效工作~ 喵",
        "ColdBoss": "环境优化。舒适度直接影响产出。调整完毕。",
        "WarmSister": "我注意到环境有些不舒适，让我为你调节一下。",
        "AnimeWizard": "*调和元素* 环境的和谐是内心平静的基础。",
        "SarcasticFighter": "环境这么糟糕还想高效？让我来搞定。",
    }
    return messages.get(personality, messages["StandardAssistant"])

# =================== 情感连接消息 ===================

def _get_emotional_support_message(personality: Personality) -> str:
    """情感支持和安慰消息"""
    messages = {
        "StandardAssistant": "我理解您现在的感受，我会陪伴在您身边。",
        "CuteCat": "别难过啦~ 小猫咪永远支持你！有什么困难我们一起面对！喵",
        "ColdBoss": "情绪波动很正常。重新整理思路。我在这里。",
        "WarmSister": "我感受到了你的情绪，别担心，有我陪着你呢。",
        "AnimeWizard": "*温和注视* 即使是最强的战士也有脆弱的时候...我理解。",
        "SarcasticFighter": "哎，看你这样子...算了，我陪着你，别想太多。",
    }
    return messages.get(personality, messages["StandardAssistant"])

def _get_celebration_message(personality: Personality) -> str:
    """成就庆祝消息"""
    messages = {
        "StandardAssistant": "恭喜您取得了进展！值得庆祝。",
        "CuteCat": "哇！太棒了！让我们一起庆祝吧！你真的很厉害~ 喵喵喵！",
        "ColdBoss": "不错。继续保持这个水准。",
        "WarmSister": "我为你感到骄傲！这个成就来之不易。",
        "AnimeWizard": "*点头赞许* 凡人也能达到如此高度...令人刮目相看。",
        "SarcasticFighter": "哟，终于有点样子了！继续加油，别骄傲。",
    }
    return messages.get(personality, messages["StandardAssistant"])

def _get_gentle_presence_message(personality: Personality) -> str:
    """安静陪伴消息"""
    messages = {
        "StandardAssistant": "",  # 安静陪伴通常无声
        "CuteCat": "",  # 小猫的安静陪伴
        "ColdBoss": "",  # 老板的无声支持
        "WarmSister": "",  # 姐姐的温暖存在
        "AnimeWizard": "",  # 法师的静默守护
        "SarcasticFighter": "",  # 战士的默默支持
    }
    return messages.get(personality, "")

# =================== 个性化智能消息 ===================

def _get_goal_progress_message(personality: Personality, related_task: str | None = None) -> str:
    """目标进展反馈消息"""
    task_context = f"关于{related_task}，" if related_task else ""
    messages = {
        "StandardAssistant": f"{task_context}让我为您分析一下进展情况。",
        "CuteCat": f"{task_context}让我看看你的进展如何~ 我来帮你总结！喵",
        "ColdBoss": f"{task_context}进展报告。数据说明一切。",
        "WarmSister": f"{task_context}我来帮你梳理一下目标进展，别着急。",
        "AnimeWizard": f"{task_context}*查看进展卷轴* 让我解读你的成长轨迹。",
        "SarcasticFighter": f"{task_context}看看你到底做了多少...希望有点进展。",
    }
    return messages.get(personality, messages["StandardAssistant"])

def _get_habit_nudge_message(personality: Personality) -> str:
    """习惯养成提醒消息"""
    messages = {
        "StandardAssistant": "温和提醒您保持良好的工作习惯。",
        "CuteCat": "好习惯要坚持哦~ 小猫咪相信你能做到！喵",
        "ColdBoss": "习惯决定效率。坚持。不要找借口。",
        "WarmSister": "养成好习惯需要时间，我会耐心提醒你的。",
        "AnimeWizard": "*传授智慧* 习惯是通往强大的基石...持续修行。",
        "SarcasticFighter": "又该提醒你了...什么时候能自觉点？",
    }
    return messages.get(personality, messages["StandardAssistant"])

def _get_personalized_insight_message(personality: Personality) -> str:
    """个性化洞察分享消息"""
    messages = {
        "StandardAssistant": "基于您的工作模式，我有一些个性化建议。",
        "CuteCat": "我观察到一些有趣的模式！让我分享一些小洞察~ 喵",
        "ColdBoss": "数据分析完成。个性化建议如下。",
        "WarmSister": "通过长期观察，我发现了一些能帮到你的规律。",
        "AnimeWizard": "*分享古老智慧* 从你的行为中，我看到了深层的模式。",
        "SarcasticFighter": "我发现了你的一些...有趣的工作习惯，听听建议吧。",
    }
    return messages.get(personality, messages["StandardAssistant"])

# =================== 环境协调消息 ===================

def _get_space_optimization_message(personality: Personality) -> str:
    """工作空间优化消息"""
    messages = {
        "StandardAssistant": "正在为您优化整个工作空间的协调性。",
        "CuteCat": "让我把工作空间变得更舒适！就像整理小窝一样~ 喵",
        "ColdBoss": "空间优化。效率最大化。环境就绪。",
        "WarmSister": "我来帮你打造一个更舒适的工作环境。",
        "AnimeWizard": "*调和空间能量* 和谐的空间带来内心的平静。",
        "SarcasticFighter": "这工作环境...算了，让我来优化一下。",
    }
    return messages.get(personality, messages["StandardAssistant"])

def _get_distraction_shield_message(personality: Personality) -> str:
    """干扰屏蔽消息"""
    messages = {
        "StandardAssistant": "为您启动干扰屏蔽，保护专注环境。",
        "CuteCat": "小猫守护模式开启！不会让任何干扰打扰到你~ 喵",
        "ColdBoss": "干扰屏蔽激活。专注环境受保护。",
        "WarmSister": "我会帮你挡住那些烦人的干扰，安心工作吧。",
        "AnimeWizard": "*施展护盾结界* 专注的心灵需要绝对的保护。",
        "SarcasticFighter": "这些干扰真烦人！我来搞定它们。",
    }
    return messages.get(personality, messages["StandardAssistant"])

def _get_ambient_companion_message(personality: Personality) -> str:
    """环境氛围调节消息"""
    messages = {
        "StandardAssistant": "调节环境氛围，营造适合的工作状态。",
        "CuteCat": "让我调节一下氛围~ 舒适的环境让工作更愉快！喵",
        "ColdBoss": "氛围调节。适合当前工作状态。",
        "WarmSister": "我来为你营造一个温馨的工作氛围。",
        "AnimeWizard": "*调和环境气息* 合适的氛围能激发内在潜力。",
        "SarcasticFighter": "氛围这种东西...算了，确实有点用。",
    }
    return messages.get(personality, messages["StandardAssistant"])

# =================== 传统功能保留 ===================

def _get_reminder_message(personality: Personality) -> str:
    """设置提醒消息（传统功能）"""
    messages = {
        "StandardAssistant": "已为您设置任务提醒。",
        "CuteCat": "收到啦！我会提醒你的~ 别担心，我在这里！",
        "ColdBoss": "提醒已设置。别指望我手把手教你。",
        "WarmSister": "我理解你有很多事情要记住。我会温柔地提醒你的。",
        "AnimeWizard": "*叹息* 又一个凡人的任务要记住...好吧。",
        "SarcasticFighter": "真的？这种基础任务也要提醒？行吧。",
    }
    return messages.get(personality, messages["StandardAssistant"])


