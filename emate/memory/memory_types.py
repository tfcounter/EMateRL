"""
E-Mate记忆系统数据类型定义

定义E-Mate环境智能AI伙伴的记忆结构，包括：
- 事实性记忆：长期稳定的用户信息和偏好
- 情景记忆：具体的交互经历和事件
- 用户画像：综合的个性化理解
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    """
    记忆类型枚举
    
    定义E-Mate支持的不同记忆类型，每种类型有不同的
    存储策略、检索方式和重要性权重。
    """
    FACTUAL = "factual"         # 事实性记忆：用户基本信息、偏好、习惯
    EPISODIC = "episodic"       # 情景记忆：具体交互、事件、体验
    PROFILE = "profile"         # 用户画像：综合理解和洞察
    GOAL = "goal"              # 目标记忆：用户的长期和短期目标
    PREFERENCE = "preference"   # 偏好记忆：用户的喜好和倾向
    HABIT = "habit"            # 习惯记忆：用户的行为模式


class MemoryImportance(str, Enum):
    """
    记忆重要性级别
    
    用于记忆的优先级排序和长期保留决策。
    """
    CRITICAL = "critical"       # 关键记忆，永久保留
    HIGH = "high"              # 高重要性，长期保留
    MEDIUM = "medium"          # 中等重要性，定期整理
    LOW = "low"                # 低重要性，可能被遗忘


class FactualMemory(BaseModel):
    """
    事实性记忆数据模型
    
    存储关于用户的长期稳定信息，如偏好、技能、
    工作习惯等不经常变化的事实。
    """
    id: Optional[str] = None                    # 记忆唯一标识
    content: str                                # 记忆内容描述
    category: str                               # 记忆分类（如"工作习惯"、"技术偏好"）
    confidence: float = Field(ge=0.0, le=1.0)  # 记忆可信度
    importance: MemoryImportance = MemoryImportance.MEDIUM  # 重要性级别
    tags: List[str] = Field(default_factory=list)          # 标签列表
    created_at: datetime = Field(default_factory=datetime.now)  # 创建时间
    updated_at: datetime = Field(default_factory=datetime.now)  # 更新时间
    source: str = "user_interaction"            # 记忆来源
    metadata: Dict[str, Any] = Field(default_factory=dict)  # 额外元数据


class EpisodicMemory(BaseModel):
    """
    情景记忆数据模型
    
    存储具体的交互事件和体验，包含时间、地点、
    情感等上下文信息。
    """
    id: Optional[str] = None                    # 记忆唯一标识
    event: str                                  # 事件描述
    emotion: Optional[str] = None               # 当时的情感状态
    context: Dict[str, Any] = Field(default_factory=dict)  # 事件上下文
    timestamp: datetime = Field(default_factory=datetime.now)  # 事件时间
    importance: MemoryImportance = MemoryImportance.MEDIUM     # 重要性级别
    tags: List[str] = Field(default_factory=list)             # 标签列表
    related_facts: List[str] = Field(default_factory=list)    # 相关事实记忆ID
    user_feedback: Optional[str] = None         # 用户反馈
    outcome: Optional[str] = None               # 事件结果
    metadata: Dict[str, Any] = Field(default_factory=dict)    # 额外元数据


class UserProfile(BaseModel):
    """
    用户画像数据模型
    
    基于长期观察和交互形成的用户综合理解，
    包含个性特征、工作模式、偏好等高层次洞察。
    """
    user_id: str                                # 用户标识
    personality_traits: Dict[str, float] = Field(default_factory=dict)  # 性格特征
    work_patterns: Dict[str, Any] = Field(default_factory=dict)         # 工作模式
    preferences: Dict[str, Any] = Field(default_factory=dict)           # 偏好设置
    goals: List[str] = Field(default_factory=list)                     # 目标列表
    skills: Dict[str, float] = Field(default_factory=dict)             # 技能水平
    communication_style: str = "standard"       # 沟通风格偏好
    stress_indicators: List[str] = Field(default_factory=list)         # 压力信号
    motivation_factors: List[str] = Field(default_factory=list)        # 激励因素
    created_at: datetime = Field(default_factory=datetime.now)         # 创建时间
    updated_at: datetime = Field(default_factory=datetime.now)         # 更新时间
    confidence_score: float = Field(default=0.5, ge=0.0, le=1.0)      # 画像可信度


class MemoryQuery(BaseModel):
    """
    记忆查询请求数据模型
    
    用于从记忆系统中检索相关信息的查询结构。
    """
    query_text: str                             # 查询文本
    memory_types: List[MemoryType] = Field(default_factory=lambda: list(MemoryType))  # 查询的记忆类型
    max_results: int = Field(default=10, ge=1, le=100)  # 最大返回结果数
    min_relevance: float = Field(default=0.3, ge=0.0, le=1.0)  # 最小相关度阈值
    time_range: Optional[Dict[str, datetime]] = None    # 时间范围过滤
    tags_filter: List[str] = Field(default_factory=list)  # 标签过滤
    importance_filter: List[MemoryImportance] = Field(default_factory=list)  # 重要性过滤


class MemorySearchResult(BaseModel):
    """
    记忆搜索结果数据模型
    
    包含检索到的记忆项及其相关性评分。
    """
    memory_id: str                              # 记忆标识
    memory_type: MemoryType                     # 记忆类型
    content: str                                # 记忆内容
    relevance_score: float                      # 相关性评分
    importance: MemoryImportance                # 重要性级别
    timestamp: datetime                         # 记忆时间戳
    tags: List[str]                            # 标签列表
    metadata: Dict[str, Any] = Field(default_factory=dict)  # 元数据


class MemoryUpdateRequest(BaseModel):
    """
    记忆更新请求数据模型
    
    用于更新或增强现有记忆的请求结构。
    """
    memory_id: str                              # 要更新的记忆ID
    updates: Dict[str, Any]                     # 更新内容
    merge_strategy: str = "replace"             # 合并策略：replace, merge, append
    update_reason: Optional[str] = None         # 更新原因
