"""
E-Mate记忆管理器

提供高级的记忆管理接口，整合记忆存储、检索、分析和维护功能。
为E-Mate环境智能AI伙伴提供统一的记忆服务。
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple

from emate.core.contracts import InputState, PerceptionInput, MemoryInput, MemoryEpisode
from .memory_core import MemoryCore
from .memory_types import (
    MemoryType, MemoryImportance, FactualMemory, EpisodicMemory, 
    UserProfile, MemoryQuery, MemorySearchResult
)

logger = logging.getLogger(__name__)


class MemoryManager:
    """
    E-Mate记忆管理器
    
    提供高级记忆管理功能，包括：
    - 智能记忆存储和分类
    - 上下文感知的记忆检索
    - 用户画像构建和更新
    - 记忆重要性评估
    - 自动记忆整理和维护
    """
    
    def __init__(self, storage_path: str = "./data/memory", user_id: str = "default_user"):
        """
        初始化记忆管理器
        
        Args:
            storage_path: 记忆存储路径
            user_id: 用户标识
        """
        self.user_id = user_id
        self.memory_core = MemoryCore(storage_path)
        
        # 初始化或加载用户画像
        self.user_profile = self.memory_core.get_user_profile(user_id)
        if not self.user_profile:
            self.user_profile = UserProfile(user_id=user_id)
            self.memory_core.store_user_profile(self.user_profile)
        
        logger.info(f"记忆管理器初始化完成，用户: {user_id}")
    
    def process_interaction(self, input_state: InputState, decision_result: str, user_feedback: Optional[str] = None) -> None:
        """
        处理用户交互，自动提取和存储记忆
        
        Args:
            input_state: 输入状态
            decision_result: 决策结果
            user_feedback: 用户反馈
        """
        p = input_state.perception_input
        
        # 存储情景记忆
        episodic_memory = EpisodicMemory(
            event=f"用户输入：{p.user_text}，系统响应：{decision_result}",
            emotion=p.speech_emotion,
            context={
                "time_of_day": p.time_of_day,
                "context_flags": p.context_flags,
                "text_sentiment": p.text_sentiment,
                "personality": input_state.system_context.personality
            },
            timestamp=datetime.now(),
            importance=self._assess_interaction_importance(input_state),
            tags=self._extract_tags_from_interaction(input_state),
            user_feedback=user_feedback,
            outcome=decision_result
        )
        
        self.memory_core.store_episodic_memory(episodic_memory)
        
        # 提取并存储事实性记忆
        facts = self._extract_facts_from_interaction(input_state)
        for fact in facts:
            self.memory_core.store_factual_memory(fact)
        
        # 更新用户画像
        self._update_user_profile_from_interaction(input_state)
        
        logger.info(f"已处理交互记忆，存储了 {len(facts)} 条事实记忆")
    
    def retrieve_relevant_memories(self, current_input: PerceptionInput, max_results: int = 5) -> MemoryInput:
        """
        检索与当前输入相关的记忆
        
        Args:
            current_input: 当前感知输入
            max_results: 最大结果数量
            
        Returns:
            MemoryInput: 相关记忆输入
        """
        # 构建查询
        query = MemoryQuery(
            query_text=current_input.user_text,
            memory_types=[MemoryType.FACTUAL, MemoryType.EPISODIC],
            max_results=max_results,
            min_relevance=0.3
        )
        
        # 搜索相关记忆
        search_results = self.memory_core.search_memories(query)
        
        # 转换为MemoryInput格式
        facts = []
        episodes = []
        
        for result in search_results:
            if result.memory_type == MemoryType.FACTUAL:
                facts.append(result.content)
            elif result.memory_type == MemoryType.EPISODIC:
                episodes.append(MemoryEpisode(
                    event=result.content,
                    emotion=result.metadata.get("emotion", "neutral"),
                    ts=result.timestamp.isoformat()
                ))
        
        return MemoryInput(facts=facts, episodes=episodes)
    
    def _assess_interaction_importance(self, input_state: InputState) -> MemoryImportance:
        """
        评估交互的重要性级别
        
        Args:
            input_state: 输入状态
            
        Returns:
            MemoryImportance: 重要性级别
        """
        p = input_state.perception_input
        flags = set(p.context_flags)
        
        # 关键词检测
        critical_keywords = ["凤凰项目", "phoenix", "重要", "紧急", "关键"]
        high_keywords = ["项目", "任务", "工作", "目标"]
        
        text_lower = p.user_text.lower()
        
        if any(keyword in text_lower for keyword in critical_keywords):
            return MemoryImportance.CRITICAL
        
        if any(keyword in text_lower for keyword in high_keywords):
            return MemoryImportance.HIGH
        
        # 基于上下文标记评估
        if "deadline_near" in flags or "important_task" in flags:
            return MemoryImportance.HIGH
        
        if "achievement_unlocked" in flags or "milestone_reached" in flags:
            return MemoryImportance.HIGH
        
        if "emotional_distress" in flags or p.speech_emotion in {"stress", "sad"}:
            return MemoryImportance.MEDIUM
        
        return MemoryImportance.MEDIUM
    
    def _extract_tags_from_interaction(self, input_state: InputState) -> List[str]:
        """
        从交互中提取标签
        
        Args:
            input_state: 输入状态
            
        Returns:
            List[str]: 标签列表
        """
        tags = []
        p = input_state.perception_input
        
        # 添加情感标签
        if p.speech_emotion:
            tags.append(f"emotion:{p.speech_emotion}")
        
        if p.text_sentiment:
            tags.append(f"sentiment:{p.text_sentiment}")
        
        # 添加时间标签
        if p.time_of_day:
            tags.append(f"time:{p.time_of_day}")
        
        # 添加上下文标签
        tags.extend(p.context_flags)
        
        # 添加人格标签
        tags.append(f"personality:{input_state.system_context.personality}")
        
        # 提取内容相关标签
        text_lower = p.user_text.lower()
        if "项目" in text_lower or "project" in text_lower:
            tags.append("work:project")
        if "任务" in text_lower or "task" in text_lower:
            tags.append("work:task")
        if "休息" in text_lower or "break" in text_lower:
            tags.append("health:break")
        
        return list(set(tags))  # 去重
    
    def _extract_facts_from_interaction(self, input_state: InputState) -> List[FactualMemory]:
        """
        从交互中提取事实性记忆
        
        Args:
            input_state: 输入状态
            
        Returns:
            List[FactualMemory]: 事实性记忆列表
        """
        facts = []
        p = input_state.perception_input
        text_lower = p.user_text.lower()
        
        # 提取项目相关事实
        if "凤凰项目" in p.user_text or "phoenix" in text_lower:
            facts.append(FactualMemory(
                content="用户正在进行凤凰项目的开发工作",
                category="work_projects",
                confidence=0.9,
                importance=MemoryImportance.HIGH,
                tags=["work", "project", "phoenix"],
                source="user_interaction"
            ))
        
        # 提取偏好相关事实
        if "喜欢" in p.user_text or "偏好" in p.user_text:
            facts.append(FactualMemory(
                content=f"用户偏好信息：{p.user_text}",
                category="user_preferences",
                confidence=0.7,
                importance=MemoryImportance.MEDIUM,
                tags=["preference"],
                source="user_interaction"
            ))
        
        # 提取工作习惯事实
        if p.time_of_day and any(word in text_lower for word in ["工作", "专注", "任务"]):
            facts.append(FactualMemory(
                content=f"用户在{p.time_of_day}时段进行工作相关活动",
                category="work_patterns",
                confidence=0.6,
                importance=MemoryImportance.MEDIUM,
                tags=["work_pattern", f"time:{p.time_of_day}"],
                source="user_interaction"
            ))
        
        return facts
    
    def _update_user_profile_from_interaction(self, input_state: InputState) -> None:
        """
        根据交互更新用户画像
        
        Args:
            input_state: 输入状态
        """
        p = input_state.perception_input
        
        # 更新工作模式
        if p.time_of_day:
            time_key = f"{p.time_of_day}_activity"
            if time_key not in self.user_profile.work_patterns:
                self.user_profile.work_patterns[time_key] = 0
            self.user_profile.work_patterns[time_key] += 1
        
        # 更新压力指标
        if p.speech_emotion == "stress" and "stress_triggers" not in self.user_profile.stress_indicators:
            context_desc = f"在{p.context_flags}情况下表现出压力"
            if context_desc not in self.user_profile.stress_indicators:
                self.user_profile.stress_indicators.append(context_desc)
        
        # 更新沟通偏好
        personality = input_state.system_context.personality
        if personality != "StandardAssistant":
            if "preferred_personalities" not in self.user_profile.preferences:
                self.user_profile.preferences["preferred_personalities"] = {}
            
            pref_key = personality
            if pref_key not in self.user_profile.preferences["preferred_personalities"]:
                self.user_profile.preferences["preferred_personalities"][pref_key] = 0
            self.user_profile.preferences["preferred_personalities"][pref_key] += 1
        
        # 更新时间戳
        self.user_profile.updated_at = datetime.now()
        
        # 保存更新的画像
        self.memory_core.store_user_profile(self.user_profile)
    
    def get_user_insights(self) -> Dict[str, Any]:
        """
        获取用户洞察分析
        
        Returns:
            Dict[str, Any]: 用户洞察信息
        """
        insights = {
            "profile_summary": {
                "user_id": self.user_profile.user_id,
                "confidence_score": self.user_profile.confidence_score,
                "last_updated": self.user_profile.updated_at.isoformat()
            },
            "work_patterns": self.user_profile.work_patterns,
            "preferences": self.user_profile.preferences,
            "stress_indicators": self.user_profile.stress_indicators,
            "goals": self.user_profile.goals
        }
        
        # 添加记忆统计
        memory_stats = self.memory_core.get_memory_stats()
        insights["memory_stats"] = memory_stats
        
        return insights
    
    def analyze_interaction_patterns(self, days: int = 7) -> Dict[str, Any]:
        """
        分析用户交互模式
        
        Args:
            days: 分析天数
            
        Returns:
            Dict[str, Any]: 交互模式分析结果
        """
        # 查询最近的交互记忆
        query = MemoryQuery(
            query_text="用户交互",
            memory_types=[MemoryType.EPISODIC],
            max_results=100,
            min_relevance=0.1
        )
        
        recent_memories = self.memory_core.search_memories(query)
        
        # 分析模式
        patterns = {
            "total_interactions": len(recent_memories),
            "emotion_distribution": {},
            "time_distribution": {},
            "common_topics": [],
            "stress_events": 0
        }
        
        for memory in recent_memories:
            # 情感分布
            emotion = memory.metadata.get("emotion", "unknown")
            patterns["emotion_distribution"][emotion] = patterns["emotion_distribution"].get(emotion, 0) + 1
            
            # 时间分布
            time_of_day = memory.metadata.get("time_of_day", "unknown")
            patterns["time_distribution"][time_of_day] = patterns["time_distribution"].get(time_of_day, 0) + 1
            
            # 压力事件计数
            if emotion in ["stress", "angry", "frustrated"]:
                patterns["stress_events"] += 1
        
        return patterns
    
    def cleanup_memories(self, days_threshold: int = 30) -> Dict[str, int]:
        """
        清理过期记忆
        
        Args:
            days_threshold: 天数阈值
            
        Returns:
            Dict[str, int]: 清理统计
        """
        cleaned_count = self.memory_core.cleanup_old_memories(days_threshold)
        
        return {
            "cleaned_memories": cleaned_count,
            "threshold_days": days_threshold,
            "cleanup_time": datetime.now().isoformat()
        }
