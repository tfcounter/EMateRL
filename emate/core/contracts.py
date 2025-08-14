"""
数据契约定义模块

这个模块定义了整个E-Mate系统中使用的所有数据结构和类型定义。
通过Pydantic模型确保数据的类型安全和验证。

主要包含：
- 输入输出的数据结构定义
- 人格、情感、动作等枚举类型
- 系统各模块间的数据传递契约
"""

from __future__ import annotations

from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field


# 语音情感类型：从语音识别中提取的情感状态
SpeechEmotion = Literal["stress", "calm", "happy", "sad", "angry", "fatigue"]

# 文本情感类型：从文本分析中得出的情感倾向
TextSentiment = Literal["positive", "neutral", "negative"]

# 时间段类型：用于上下文感知的时间信息
TimeOfDay = Literal["morning", "afternoon", "evening", "night"]

# 人格类型：支持的所有人格种类
Personality = Literal[
    "StandardAssistant",  # 标准工作助手：专业高效
    "CuteCat",           # 鼓励大师猫猫：可爱暖心
    "ColdBoss",          # 面冷心热霸总：权威严格
    "WarmSister",        # 温暖细腻姐姐：善解人意
    "AnimeWizard",       # 二次元魔法使：超然淡定
    "SarcasticFighter"   # 战火纷飞互怼狂：尖锐推动
]

# 智能体模式：决策策略的类型
AgentMode = Literal["QLearning", "GSPO", "Hybrid"]

# 屏幕动画类型：E-Mate环境智能AI伙伴的丰富表达能力
ScreenAnimation = Literal[
    # 传统动画（向后兼容）
    "focused",            # 专注状态
    "celebrating",        # 庆祝状态  
    "empathetic_nod",     # 理解点头
    "sleeping",           # 休眠状态
    "breathing_calm",     # 平静呼吸
    
    # 工作节律协调动画
    "deep_focus_shield",  # 深度专注护盾
    "flow_waves",         # 心流波纹
    "energy_spark",       # 能量火花
    
    # 健康守护动画
    "gentle_stretch",     # 温和伸展
    "breathing_guide",    # 呼吸引导
    "environment_adjust", # 环境调节
    
    # 情感连接动画
    "empathetic_presence", # 理解陪伴
    "celebration_sparkle", # 庆祝闪烁
    "gentle_pulse",       # 温和脉动
    
    # 个性化智能动画
    "progress_chart",     # 进展图表
    "habit_formation",    # 习惯形成
    "wisdom_sharing",     # 智慧分享
    
    # 环境协调动画
    "space_harmony",      # 空间和谐
    "shield_protection",  # 护盾保护
    "ambient_waves",      # 环境波纹
    
    # 伙伴陪伴动画
    "gentle_breathing",   # 温和呼吸
]

# 灯光效果类型：E-Mate环境智能伙伴的情感表达光谱
LightEffect = Literal[
    # 传统灯效（向后兼容）
    "focus_blue",           # 专注蓝光
    "warm_yellow_glow",     # 温暖黄光
    "calm_green_pulse",     # 平静绿光脉冲
    "off",                  # 关闭
    
    # 工作节律协调灯效
    "focus_deep_blue",      # 深度专注蓝
    "flow_gradient",        # 心流渐变
    "energizing_orange",    # 活力橙光
    
    # 健康守护灯效
    "health_green_pulse",   # 健康绿脉冲
    "calm_breathing",       # 平静呼吸光
    "comfort_warm",         # 舒适暖光
    
    # 情感连接灯效
    "warm_embrace",         # 温暖拥抱
    "joy_rainbow",          # 喜悦彩虹
    "soft_presence",        # 柔和存在
    
    # 个性化智能灯效
    "progress_blue",        # 进展蓝光
    "habit_purple",         # 习惯紫光
    "insight_gold",         # 洞察金光
    
    # 环境协调灯效
    "optimization_white",   # 优化白光
    "protection_cyan",      # 保护青光
    "ambient_mood",         # 环境氛围
    
    # 伙伴陪伴灯效
    "soft_ambient",         # 柔和环境光
]

# 动作类型：E-Mate环境智能AI伙伴的完整能力谱系
ActionType = Literal[
    # 传统功能（向后兼容）
    "set_reminder",           # 设置提醒
    "enter_focus_mode",       # 进入专注模式
    "suggest_break",          # 建议休息
    "none",                   # 无操作
    
    # 工作节律协调
    "deep_work_protection",   # 深度工作保护
    "focus_flow_guidance",    # 专注流引导
    "energy_boost_suggestion", # 能量提升建议
    
    # 健康守护
    "movement_reminder",      # 活动提醒
    "breathing_relaxation",   # 呼吸放松
    "environment_optimization", # 环境优化
    
    # 情感连接
    "emotional_support",      # 情感支持
    "achievement_celebration", # 成就庆祝
    "quiet_companionship",    # 安静陪伴
    
    # 个性化智能
    "goal_progress_review",   # 目标进展回顾
    "habit_formation_nudge",  # 习惯养成推动
    "personalized_insight",   # 个性化洞察
    
    # 环境协调
    "workspace_optimization", # 工作空间优化
    "distraction_protection", # 干扰保护
    "ambient_atmosphere",     # 环境氛围调节
    
    # 伙伴陪伴
    "silent_companionship",   # 静默陪伴
]


class PerceptionInput(BaseModel):
    """
    感知输入数据模型
    
    包含从多模态识别引擎获得的所有感知信息，
    是决策系统的主要输入来源。
    """
    user_text: str = ""  # 用户输入的文本（语音转文本结果）
    speech_emotion: Optional[SpeechEmotion] = None  # 语音情感识别结果
    text_sentiment: Optional[TextSentiment] = None  # 文本情感分析结果
    context_flags: List[str] = Field(default_factory=list)  # 上下文标记列表
    time_of_day: Optional[TimeOfDay] = None  # 当前时间段


class MemoryEpisode(BaseModel):
    """
    记忆片段数据模型
    
    表示一个具体的历史事件，包含事件描述、
    关联情感和时间戳信息。
    """
    event: str  # 事件描述
    emotion: Optional[str] = None  # 关联的情感标签
    ts: Optional[str] = None  # 时间戳（ISO8601格式）


class MemoryInput(BaseModel):
    """
    记忆输入数据模型
    
    包含从Mem0记忆系统检索到的相关历史信息，
    为决策提供上下文和背景知识。
    """
    facts: List[str] = Field(default_factory=list)  # 事实性记忆列表
    episodes: List[MemoryEpisode] = Field(default_factory=list)  # 情景记忆列表


class SystemContext(BaseModel):
    """
    系统上下文数据模型
    
    包含当前系统的配置信息，如人格设置、
    长期目标和智能体模式等。
    """
    personality: Personality = "StandardAssistant"  # 当前人格类型
    long_term_goals: List[str] = Field(default_factory=list)  # 长期目标列表
    agent_mode: AgentMode = "QLearning"  # 智能体决策模式


class InputState(BaseModel):
    """
    完整输入状态数据模型
    
    整合了感知输入、记忆信息和系统上下文，
    是决策图处理的完整输入数据结构。
    """
    perception_input: PerceptionInput  # 感知输入（必需）
    memory_input: MemoryInput = Field(default_factory=MemoryInput)  # 记忆输入（可选）
    system_context: SystemContext = Field(default_factory=SystemContext)  # 系统上下文（可选）


class ActionParameters(BaseModel):
    """
    动作参数数据模型
    
    包含执行特定动作时需要的参数信息，
    如专注时长、相关任务、截止时间等。
    """
    duration: Optional[int] = None  # 持续时间（分钟）
    related_task: Optional[str] = None  # 相关任务名称
    deadline: Optional[str] = None  # 截止时间（ISO8601格式）


class Action(BaseModel):
    """
    动作数据模型
    
    表示系统要执行的具体行动，包含动作类型
    和相应的参数信息。
    """
    type: ActionType  # 动作类型
    parameters: ActionParameters = Field(default_factory=ActionParameters)  # 动作参数


class ExecutionOutput(BaseModel):
    """
    执行输出数据模型
    
    包含需要发送给硬件执行器的指令，
    如屏幕动画和灯光效果。
    """
    screen_animation: Optional[ScreenAnimation] = None  # 屏幕动画类型
    light_effect: Optional[LightEffect] = None  # 灯光效果类型


class TTSOutput(BaseModel):
    """
    语音合成输出数据模型
    
    包含需要通过TTS引擎合成并播放的
    语音内容。
    """
    text_to_speak: Optional[str] = None  # 待合成的文本内容


class MemoryToStore(BaseModel):
    """
    待存储记忆数据模型
    
    包含需要写入Mem0记忆系统的信息，
    用于后续的学习和回顾。
    """
    input: Dict[str, Any]  # 输入数据的字典表示
    decision_reasoning: str  # 决策推理过程
    final_action: str  # 最终执行的动作


class MemoryOutput(BaseModel):
    """
    记忆输出数据模型
    
    包含需要写回记忆系统的数据，
    用于经验积累和学习改进。
    """
    memory_to_store: Optional[MemoryToStore] = None  # 待存储的记忆数据


class OutputCommand(BaseModel):
    """
    完整输出指令数据模型
    
    整合了所有下游模块需要的指令信息，
    是决策图输出的完整数据结构。
    """
    execution_output: ExecutionOutput = Field(default_factory=ExecutionOutput)  # 执行器指令
    tts_output: TTSOutput = Field(default_factory=TTSOutput)  # TTS指令
    action: Action = Field(default_factory=lambda: Action(type="none"))  # 具体动作
    memory_output: MemoryOutput = Field(default_factory=MemoryOutput)  # 记忆写回指令


def build_default_output() -> OutputCommand:
    """
    构建默认的输出指令
    
    Returns:
        OutputCommand: 包含默认值的输出指令对象
    """
    return OutputCommand()


