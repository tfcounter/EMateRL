from __future__ import annotations

from typing import Optional

from emate.core.contracts import (
    InputState,
    OutputCommand,
    build_default_output,
)
from emate.core.persona_guard import apply_persona_filter
from emate.micro.state_discretizer import discretize_state
from emate.micro.qlearning import QLearningNode
from emate.micro.action_map import (
    ACTIONS,
    map_action_to_output,
)
from emate.memory.memory_manager import MemoryManager


class PersonaDecisionGraph:
    """
    人格化决策图 - 轻量级的类Agno图编排器
    
    这是一个轻量级的编排器，避免对Agno API的早期硬依赖，
    同时符合dev_plan的节点边界设计，便于后续迁移。
    
    主要功能：
    - 将输入状态离散化
    - 通过Q学习或启发式规则选择动作
    - 应用人格化过滤
    - 生成最终的输出指令
    """

    def __init__(self) -> None:
        """初始化人格化决策图，创建Q学习节点"""
        self.ql = QLearningNode(actions=ACTIONS)

    def run_once(self, input_state: InputState) -> OutputCommand:
        """
        执行一次完整的决策流程
        
        Args:
            input_state: 包含感知输入、记忆上下文和系统配置的输入状态
            
        Returns:
            OutputCommand: 经过人格化处理的最终输出指令
        """
        # 第一步：感知输入转换为离散状态
        state_id = discretize_state(input_state)

        # 第二步：启发式决策（符合PRD人格特征的快速决策）
        action_id = self._heuristic_action(input_state)
        if action_id is None:
            # 如果启发式规则未匹配，则使用Q学习策略选择动作
            action_id = self.ql.select_action(state_id)

        # 第三步：将抽象动作ID映射为具体输出指令
        personality = input_state.system_context.personality
        output = map_action_to_output(action_id, related_task=self._guess_task(input_state), personality=personality)

        # 第四步：应用人格化约束过滤器
        output = apply_persona_filter(output, personality)

        # 第五步：返回最终输出（记忆回写由调用者处理）
        return output

    def reward(self, prev_state_id: str, action_id: str, reward: float, next_state_id: Optional[str] = None) -> None:
        """
        提供奖励反馈以更新Q学习模型
        
        Args:
            prev_state_id: 前一个状态ID
            action_id: 执行的动作ID
            reward: 奖励值（正值表示好的结果，负值表示不好的结果）
            next_state_id: 下一个状态ID（可选）
        """
        self.ql.update(prev_state_id, action_id, reward, next_state_id)

    @staticmethod
    def _guess_task(input_state: InputState) -> Optional[str]:
        """
        从用户输入中推测任务名称
        
        Args:
            input_state: 输入状态
            
        Returns:
            Optional[str]: 推测的任务名称，如果无法推测则返回None
        """
        text = (input_state.perception_input.user_text or "").lower()
        # 简单的启发式规则提取任务关键词
        if "凤凰" in text or "phoenix" in text:
            return "凤凰项目草案"
        elif "报告" in text:
            return "工作报告"
        elif "项目" in text:
            return "项目任务"
        return None

    def _heuristic_action(self, input_state: InputState) -> Optional[str]:
        """
        基于人格特征的启发式动作选择
        
        根据当前人格类型路由到对应的启发式决策逻辑，
        每种人格都有其独特的决策偏好和行为模式。
        
        Args:
            input_state: 输入状态
            
        Returns:
            Optional[str]: 选定的动作ID，如果无匹配规则则返回None
        """
        personality = input_state.system_context.personality
        
        # 路由到人格特定的启发式逻辑
        if personality == "StandardAssistant":
            return self._heuristic_standard_assistant(input_state)
        elif personality == "CuteCat":
            return self._heuristic_cute_cat(input_state)
        elif personality == "ColdBoss":
            return self._heuristic_cold_boss(input_state)
        elif personality == "WarmSister":
            return self._heuristic_warm_sister(input_state)
        elif personality == "AnimeWizard":
            return self._heuristic_anime_wizard(input_state)
        elif personality == "SarcasticFighter":
            return self._heuristic_sarcastic_fighter(input_state)
        
        return None
    
    @staticmethod
    def _heuristic_standard_assistant(input_state: InputState) -> Optional[str]:
        """
        标准工作助手的启发式决策逻辑
        
        特点：高效、逻辑化的决策
        原则：专业逻辑，环境感知+智能协调
        """
        from emate.micro.action_map import (
            A_DEEP_WORK_MODE, A_FOCUS_FLOW, A_SET_REMINDER, 
            A_MOVEMENT_REMINDER, A_GOAL_PROGRESS, A_DISTRACTION_SHIELD
        )
        
        p = input_state.perception_input
        flags = set(p.context_flags)
        
        # 深度工作保护
        if "deep_work_mode" in flags or ("important_task" in flags and "quiet_space" in flags):
            return A_DEEP_WORK_MODE
            
        # 环境干扰处理
        if "interruption_high" in flags or "noise_distraction" in flags:
            return A_DISTRACTION_SHIELD
            
        # 健康状态关注
        if "sitting_over_2h" in flags or p.speech_emotion == "fatigue":
            return A_MOVEMENT_REMINDER
            
        # 目标进展回顾
        if "progress_review" in flags or "goal_review" in flags:
            return A_GOAL_PROGRESS
            
        # 专注流引导
        if p.speech_emotion == "calm" and "task_switching" not in flags:
            return A_FOCUS_FLOW
            
        # 传统提醒功能
        if "deadline_near" in flags:
            return A_SET_REMINDER
        
        return None
    
    @staticmethod
    def _heuristic_cute_cat(input_state: InputState) -> Optional[str]:
        """
        可爱猫猫的启发式决策逻辑
        
        特点：关怀体贴、支持温暖、偏好温和方式
        原则：优先情感连接和健康守护
        """
        from emate.micro.action_map import (
            A_EMOTIONAL_SUPPORT, A_BREATHING_GUIDE, A_CELEBRATION,
            A_GENTLE_PRESENCE, A_MOVEMENT_REMINDER, A_SET_REMINDER
        )
        
        p = input_state.perception_input
        flags = set(p.context_flags)
        
        # 猫猫优先提供情感支持
        if p.speech_emotion in {"stress", "sad"} or "emotional_distress" in flags:
            return A_EMOTIONAL_SUPPORT  # "别难过啦~ 小猫咪永远支持你！"
            
        # 庆祝用户成就
        if p.speech_emotion == "happy" or "achievement_unlocked" in flags:
            return A_CELEBRATION  # "哇！太棒了！让我们一起庆祝吧！"
        
        # 关心用户健康，疲劳时温和提醒
        if p.speech_emotion == "fatigue" or "sitting_over_2h" in flags:
            if "eye_strain" in flags:
                return A_BREATHING_GUIDE  # 眼睛累了，深呼吸放松
            else:
                return A_MOVEMENT_REMINDER  # "该起来走走啦！"
        
        # 安静陪伴
        if p.speech_emotion == "calm":
            return A_GENTLE_PRESENCE
            
        return A_SET_REMINDER
    
    @staticmethod
    def _heuristic_cold_boss(input_state: InputState) -> Optional[str]:
        """
        冷酷霸总的启发式决策逻辑
        
        特点：结果导向、不容忍弱点
        原则：环境优化，最大化生产力
        """
        from emate.micro.action_map import (
            A_DEEP_WORK_MODE, A_DISTRACTION_SHIELD, A_SPACE_OPTIMIZATION,
            A_ENERGY_BOOST, A_GOAL_PROGRESS
        )
        
        p = input_state.perception_input
        flags = set(p.context_flags)
        
        # 霸总首要任务：消除干扰，优化环境
        if "interruption_high" in flags or "noise_distraction" in flags:
            return A_DISTRACTION_SHIELD  # "干扰屏蔽激活。专注环境受保护。"
            
        # 工作空间优化
        if "environment_uncomfortable" in flags:
            return A_SPACE_OPTIMIZATION  # "空间优化。效率最大化。"
            
        # 深度工作保护
        if "important_task" in flags or "deadline_near" in flags:
            return A_DEEP_WORK_MODE  # "深度工作模式。所有干扰将被屏蔽。"
            
        # 能量管理（霸总也需要效率）
        if p.speech_emotion == "fatigue":
            return A_ENERGY_BOOST  # "能量不足会影响效率。补充。"
            
        # 目标进展追踪
        if "progress_review" in flags:
            return A_GOAL_PROGRESS  # "进展报告。数据说明一切。"
        
        return A_DEEP_WORK_MODE  # 默认深度工作模式
    
    @staticmethod
    def _heuristic_warm_sister(input_state: InputState) -> Optional[str]:
        """
        温暖姐姐的启发式决策逻辑
        
        特点：善于共情、平衡方式
        原则：健康守护与情感支持并重
        """
        from emate.micro.action_map import (
            A_MOVEMENT_REMINDER, A_BREATHING_GUIDE, A_EMOTIONAL_SUPPORT,
            A_ENVIRONMENT_ADJUST, A_HABIT_NUDGE, A_SET_REMINDER
        )
        
        p = input_state.perception_input
        flags = set(p.context_flags)
        
        # 姐姐优先关注健康和情感需求
        if "sitting_over_2h" in flags or p.speech_emotion == "fatigue":
            return A_MOVEMENT_REMINDER  # "坐了这么久，起来走走吧，我担心你的身体。"
            
        # 压力和情感支持
        if p.speech_emotion in {"stress", "sad"} or "emotional_distress" in flags:
            return A_EMOTIONAL_SUPPORT  # "我感受到了你的情绪，别担心，有我陪着你呢。"
            
        # 呼吸放松指导
        if "eye_strain" in flags or p.speech_emotion == "stress":
            return A_BREATHING_GUIDE  # "来，跟我一起慢慢呼吸"
            
        # 环境舒适度调节
        if "environment_uncomfortable" in flags:
            return A_ENVIRONMENT_ADJUST  # "我注意到环境有些不舒适"
            
        # 习惯养成支持
        if "improvement_seeking" in flags:
            return A_HABIT_NUDGE  # "养成好习惯需要时间，我会耐心提醒你的。"
            
        return A_SET_REMINDER  # "我会帮你记住的"
    
    @staticmethod
    def _heuristic_anime_wizard(input_state: InputState) -> Optional[str]:
        """
        二次元魔法使的启发式决策逻辑
        
        特点：超然淡漠、长期视角
        原则：个性化洞察和智慧分享
        """
        from emate.micro.action_map import (
            A_PERSONALIZED_INSIGHT, A_GOAL_PROGRESS, A_HABIT_NUDGE,
            A_AMBIENT_COMPANION, A_SET_REMINDER
        )
        
        p = input_state.perception_input
        flags = set(p.context_flags)
        
        # 魔法使擅长提供深层洞察
        if "progress_review" in flags or "self_reflection" in flags:
            return A_GOAL_PROGRESS  # "*查看进展卷轴* 让我解读你的成长轨迹。"
            
        # 个性化智慧分享
        if "improvement_seeking" in flags or p.speech_emotion == "calm":
            return A_PERSONALIZED_INSIGHT  # "*分享古老智慧* 从你的行为中，我看到了深层的模式。"
            
        # 习惯修行指导
        if "habit_formation" in flags:
            return A_HABIT_NUDGE  # "*传授智慧* 习惯是通往强大的基石...持续修行。"
            
        # 环境氛围调节（魔法师的神秘氛围）
        if "environment_uncomfortable" in flags:
            return A_AMBIENT_COMPANION  # "*调和环境气息* 合适的氛围能激发内在潜力。"
        
        # 重要任务的记录
        if "凤凰" in p.user_text or "phoenix" in p.user_text.lower():
            return A_SET_REMINDER  # "*叹息* 又一个凡人的任务要记住...好吧。"
        
        return A_PERSONALIZED_INSIGHT  # 默认提供洞察
    
    @staticmethod
    def _heuristic_sarcastic_fighter(input_state: InputState) -> Optional[str]:
        """
        战斗狂的启发式决策逻辑
        
        特点：高压推动、毫无同情
        原则：激发潜能，庆祝成就，推动突破
        """
        from emate.micro.action_map import (
            A_DEEP_WORK_MODE, A_ENERGY_BOOST, A_CELEBRATION,
            A_GOAL_PROGRESS, A_DISTRACTION_SHIELD
        )
        
        p = input_state.perception_input
        flags = set(p.context_flags)
        
        # 庆祝成就（毒舌式的认可）
        if p.speech_emotion == "happy" or "achievement_unlocked" in flags:
            return A_CELEBRATION  # "哟，终于有点样子了！继续加油，别骄傲。"
            
        # 能量激发（战斗狂的方式）
        if p.speech_emotion == "fatigue":
            return A_ENERGY_BOOST  # "累了？这才多久？算了，去充个电再回来。"
            
        # 干扰清除（战斗模式）
        if "interruption_high" in flags or "noise_distraction" in flags:
            return A_DISTRACTION_SHIELD  # "这些干扰真烦人！我来搞定它们。"
            
        # 目标进展追踪（严格监督）
        if "progress_review" in flags:
            return A_GOAL_PROGRESS  # "看看你到底做了多少...希望有点进展。"
            
        # 深度工作推动
        if "important_task" in flags or p.speech_emotion in {"stress", "angry"}:
            return A_DEEP_WORK_MODE  # "终于要认真工作了？好吧，我帮你挡住那些无聊的干扰。"
        
        return A_DEEP_WORK_MODE  # 默认深度工作推动


