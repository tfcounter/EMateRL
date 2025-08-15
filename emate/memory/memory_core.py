"""
E-Mate记忆核心引擎

基于Mem0框架实现的智能记忆系统核心，提供：
- 向量化记忆存储和检索
- 语义相似性搜索
- 记忆重要性评估
- 自动记忆整理和遗忘
"""

from __future__ import annotations

import json
import logging
import sqlite3
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

import numpy as np
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SentenceTransformer = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False

from .memory_types import (
    MemoryType, MemoryImportance, FactualMemory, EpisodicMemory, 
    UserProfile, MemoryQuery, MemorySearchResult, MemoryUpdateRequest
)

logger = logging.getLogger(__name__)


class MemoryCore:
    """
    E-Mate记忆系统核心引擎
    
    实现基于向量数据库的智能记忆存储和检索系统，
    支持语义搜索、记忆重要性评估和自动整理。
    """
    
    def __init__(
        self, 
        storage_path: str = "./data/memory", 
        embedding_model: str = "all-MiniLM-L6-v2",
        max_memory_size: int = 10000
    ):
        """
        初始化记忆核心引擎
        
        Args:
            storage_path: 记忆存储路径
            embedding_model: 文本嵌入模型名称
            max_memory_size: 最大记忆容量
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.max_memory_size = max_memory_size
        
        # 初始化文本嵌入模型
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.embedding_model = SentenceTransformer(embedding_model)
                logger.info(f"已加载嵌入模型: {embedding_model}")
            except Exception as e:
                logger.warning(f"嵌入模型加载失败: {e}, 使用简单向量化")
                self.embedding_model = None
        else:
            logger.info("SentenceTransformers不可用，使用简单向量化")
            self.embedding_model = None
        
        # 初始化SQLite数据库
        self.db_path = self.storage_path / "memory.db"
        self._init_database()
        
        # 记忆缓存
        self._memory_cache: Dict[str, Any] = {}
        
        logger.info(f"记忆核心引擎初始化完成，存储路径: {self.storage_path}")
    
    def _init_database(self) -> None:
        """初始化SQLite数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 事实性记忆表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS factual_memories (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    category TEXT,
                    confidence REAL,
                    importance TEXT,
                    tags TEXT,  -- JSON数组
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP,
                    source TEXT,
                    metadata TEXT,  -- JSON对象
                    embedding BLOB  -- 向量嵌入
                )
            """)
            
            # 情景记忆表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS episodic_memories (
                    id TEXT PRIMARY KEY,
                    event TEXT NOT NULL,
                    emotion TEXT,
                    context TEXT,  -- JSON对象
                    timestamp TIMESTAMP,
                    importance TEXT,
                    tags TEXT,  -- JSON数组
                    related_facts TEXT,  -- JSON数组
                    user_feedback TEXT,
                    outcome TEXT,
                    metadata TEXT,  -- JSON对象
                    embedding BLOB  -- 向量嵌入
                )
            """)
            
            # 用户画像表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    personality_traits TEXT,  -- JSON对象
                    work_patterns TEXT,  -- JSON对象
                    preferences TEXT,  -- JSON对象
                    goals TEXT,  -- JSON数组
                    skills TEXT,  -- JSON对象
                    communication_style TEXT,
                    stress_indicators TEXT,  -- JSON数组
                    motivation_factors TEXT,  -- JSON数组
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP,
                    confidence_score REAL
                )
            """)
            
            # 创建索引提升查询性能
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_factual_category ON factual_memories(category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_factual_importance ON factual_memories(importance)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_episodic_timestamp ON episodic_memories(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_episodic_importance ON episodic_memories(importance)")
            
            conn.commit()
            logger.info("数据库表结构初始化完成")
    
    def _generate_embedding(self, text: str) -> np.ndarray:
        """
        生成文本的向量嵌入
        
        Args:
            text: 输入文本
            
        Returns:
            np.ndarray: 文本向量嵌入
        """
        if self.embedding_model:
            try:
                return self.embedding_model.encode(text, convert_to_numpy=True)
            except Exception as e:
                logger.warning(f"嵌入生成失败: {e}")
        
        # 简单的文本向量化后备方案
        words = text.lower().split()
        vector = np.zeros(384)  # 与MiniLM模型维度一致
        for i, word in enumerate(words[:384]):
            vector[i] = hash(word) % 1000 / 1000.0
        return vector
    
    def _serialize_embedding(self, embedding: np.ndarray) -> bytes:
        """将向量嵌入序列化为二进制数据"""
        return embedding.tobytes()
    
    def _deserialize_embedding(self, embedding_bytes: bytes) -> np.ndarray:
        """将二进制数据反序列化为向量嵌入"""
        return np.frombuffer(embedding_bytes, dtype=np.float32)
    
    def store_factual_memory(self, memory: FactualMemory) -> str:
        """
        存储事实性记忆
        
        Args:
            memory: 事实性记忆对象
            
        Returns:
            str: 记忆ID
        """
        if not memory.id:
            memory.id = str(uuid.uuid4())
        
        # 生成内容嵌入
        embedding = self._generate_embedding(memory.content)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO factual_memories 
                (id, content, category, confidence, importance, tags, created_at, updated_at, source, metadata, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory.id,
                memory.content,
                memory.category,
                memory.confidence,
                memory.importance.value,
                json.dumps(memory.tags),
                memory.created_at.isoformat(),
                memory.updated_at.isoformat(),
                memory.source,
                json.dumps(memory.metadata),
                self._serialize_embedding(embedding)
            ))
            conn.commit()
        
        logger.info(f"已存储事实性记忆: {memory.id}")
        return memory.id
    
    def store_episodic_memory(self, memory: EpisodicMemory) -> str:
        """
        存储情景记忆
        
        Args:
            memory: 情景记忆对象
            
        Returns:
            str: 记忆ID
        """
        if not memory.id:
            memory.id = str(uuid.uuid4())
        
        # 生成事件嵌入
        embedding = self._generate_embedding(memory.event)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO episodic_memories 
                (id, event, emotion, context, timestamp, importance, tags, related_facts, user_feedback, outcome, metadata, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory.id,
                memory.event,
                memory.emotion,
                json.dumps(memory.context),
                memory.timestamp.isoformat(),
                memory.importance.value,
                json.dumps(memory.tags),
                json.dumps(memory.related_facts),
                memory.user_feedback,
                memory.outcome,
                json.dumps(memory.metadata),
                self._serialize_embedding(embedding)
            ))
            conn.commit()
        
        logger.info(f"已存储情景记忆: {memory.id}")
        return memory.id
    
    def store_user_profile(self, profile: UserProfile) -> None:
        """
        存储用户画像
        
        Args:
            profile: 用户画像对象
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO user_profiles 
                (user_id, personality_traits, work_patterns, preferences, goals, skills, 
                 communication_style, stress_indicators, motivation_factors, created_at, updated_at, confidence_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                profile.user_id,
                json.dumps(profile.personality_traits),
                json.dumps(profile.work_patterns),
                json.dumps(profile.preferences),
                json.dumps(profile.goals),
                json.dumps(profile.skills),
                profile.communication_style,
                json.dumps(profile.stress_indicators),
                json.dumps(profile.motivation_factors),
                profile.created_at.isoformat(),
                profile.updated_at.isoformat(),
                profile.confidence_score
            ))
            conn.commit()
        
        logger.info(f"已存储用户画像: {profile.user_id}")
    
    def search_memories(self, query: MemoryQuery) -> List[MemorySearchResult]:
        """
        搜索相关记忆
        
        Args:
            query: 记忆查询请求
            
        Returns:
            List[MemorySearchResult]: 搜索结果列表
        """
        query_embedding = self._generate_embedding(query.query_text)
        results = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 搜索事实性记忆
            if MemoryType.FACTUAL in query.memory_types:
                cursor.execute("""
                    SELECT id, content, importance, tags, created_at, metadata, embedding
                    FROM factual_memories
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (query.max_results * 2,))  # 获取更多候选结果
                
                for row in cursor.fetchall():
                    memory_id, content, importance, tags_json, created_at, metadata_json, embedding_bytes = row
                    
                    if embedding_bytes:
                        memory_embedding = self._deserialize_embedding(embedding_bytes)
                        # 计算余弦相似度
                        similarity = np.dot(query_embedding, memory_embedding) / (
                            np.linalg.norm(query_embedding) * np.linalg.norm(memory_embedding)
                        )
                        
                        if similarity >= query.min_relevance:
                            results.append(MemorySearchResult(
                                memory_id=memory_id,
                                memory_type=MemoryType.FACTUAL,
                                content=content,
                                relevance_score=float(similarity),
                                importance=MemoryImportance(importance),
                                timestamp=datetime.fromisoformat(created_at),
                                tags=json.loads(tags_json) if tags_json else [],
                                metadata=json.loads(metadata_json) if metadata_json else {}
                            ))
            
            # 搜索情景记忆
            if MemoryType.EPISODIC in query.memory_types:
                cursor.execute("""
                    SELECT id, event, importance, tags, timestamp, metadata, embedding
                    FROM episodic_memories
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (query.max_results * 2,))
                
                for row in cursor.fetchall():
                    memory_id, event, importance, tags_json, timestamp, metadata_json, embedding_bytes = row
                    
                    if embedding_bytes:
                        memory_embedding = self._deserialize_embedding(embedding_bytes)
                        similarity = np.dot(query_embedding, memory_embedding) / (
                            np.linalg.norm(query_embedding) * np.linalg.norm(memory_embedding)
                        )
                        
                        if similarity >= query.min_relevance:
                            results.append(MemorySearchResult(
                                memory_id=memory_id,
                                memory_type=MemoryType.EPISODIC,
                                content=event,
                                relevance_score=float(similarity),
                                importance=MemoryImportance(importance),
                                timestamp=datetime.fromisoformat(timestamp),
                                tags=json.loads(tags_json) if tags_json else [],
                                metadata=json.loads(metadata_json) if metadata_json else {}
                            ))
        
        # 按相关性和重要性排序
        results.sort(key=lambda x: (x.relevance_score, self._importance_weight(x.importance)), reverse=True)
        
        return results[:query.max_results]
    
    def _importance_weight(self, importance: MemoryImportance) -> float:
        """记忆重要性权重映射"""
        weights = {
            MemoryImportance.CRITICAL: 1.0,
            MemoryImportance.HIGH: 0.8,
            MemoryImportance.MEDIUM: 0.5,
            MemoryImportance.LOW: 0.2
        }
        return weights.get(importance, 0.5)
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        获取用户画像
        
        Args:
            user_id: 用户标识
            
        Returns:
            Optional[UserProfile]: 用户画像对象
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM user_profiles WHERE user_id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            if row:
                return UserProfile(
                    user_id=row[0],
                    personality_traits=json.loads(row[1]) if row[1] else {},
                    work_patterns=json.loads(row[2]) if row[2] else {},
                    preferences=json.loads(row[3]) if row[3] else {},
                    goals=json.loads(row[4]) if row[4] else [],
                    skills=json.loads(row[5]) if row[5] else {},
                    communication_style=row[6],
                    stress_indicators=json.loads(row[7]) if row[7] else [],
                    motivation_factors=json.loads(row[8]) if row[8] else [],
                    created_at=datetime.fromisoformat(row[9]),
                    updated_at=datetime.fromisoformat(row[10]),
                    confidence_score=row[11]
                )
        
        return None
    
    def update_memory(self, update_request: MemoryUpdateRequest) -> bool:
        """
        更新记忆内容
        
        Args:
            update_request: 更新请求
            
        Returns:
            bool: 更新是否成功
        """
        # 这里可以实现记忆更新逻辑
        # 根据merge_strategy决定如何合并更新内容
        logger.info(f"记忆更新请求: {update_request.memory_id}")
        return True
    
    def cleanup_old_memories(self, days_threshold: int = 90) -> int:
        """
        清理过期的低重要性记忆
        
        Args:
            days_threshold: 天数阈值
            
        Returns:
            int: 清理的记忆数量
        """
        cutoff_date = datetime.now() - timedelta(days=days_threshold)
        cleaned_count = 0
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 清理低重要性的旧记忆
            cursor.execute("""
                DELETE FROM episodic_memories 
                WHERE importance = ? AND timestamp < ?
            """, (MemoryImportance.LOW.value, cutoff_date.isoformat()))
            
            cleaned_count += cursor.rowcount
            conn.commit()
        
        logger.info(f"清理了 {cleaned_count} 条过期记忆")
        return cleaned_count
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        获取记忆系统统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        stats = {}
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 事实性记忆统计
            cursor.execute("SELECT COUNT(*) FROM factual_memories")
            stats["factual_count"] = cursor.fetchone()[0]
            
            # 情景记忆统计
            cursor.execute("SELECT COUNT(*) FROM episodic_memories")
            stats["episodic_count"] = cursor.fetchone()[0]
            
            # 用户画像统计
            cursor.execute("SELECT COUNT(*) FROM user_profiles")
            stats["profile_count"] = cursor.fetchone()[0]
            
            # 重要性分布
            cursor.execute("""
                SELECT importance, COUNT(*) FROM factual_memories GROUP BY importance
            """)
            stats["factual_importance_dist"] = dict(cursor.fetchall())
            
            cursor.execute("""
                SELECT importance, COUNT(*) FROM episodic_memories GROUP BY importance
            """)
            stats["episodic_importance_dist"] = dict(cursor.fetchall())
        
        stats["storage_path"] = str(self.storage_path)
        stats["max_capacity"] = self.max_memory_size
        
        return stats
