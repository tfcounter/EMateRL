"""
E-Mate Agent Memory Module

基于Mem0框架的智能记忆系统，为E-Mate环境智能AI伙伴提供：
- 长期记忆存储和检索
- 事实性记忆和情景记忆管理  
- 个性化用户理解
- 上下文感知的记忆召回
"""

from .memory_core import MemoryCore
from .memory_types import MemoryType, FactualMemory, EpisodicMemory, UserProfile
from .memory_manager import MemoryManager

__all__ = [
    "MemoryCore",
    "MemoryType", 
    "FactualMemory",
    "EpisodicMemory", 
    "UserProfile",
    "MemoryManager"
]
