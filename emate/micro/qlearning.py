"""
Q学习节点模块

实现基于表格的Q学习算法，使用epsilon-greedy策略进行动作选择。
通过本地JSON文件进行持久化存储，保持MVP的简单性和可移植性。

主要功能：
- Q表的维护和更新
- epsilon-greedy动作选择
- 学习参数的自适应调整
- Q表的本地持久化存储
"""

from __future__ import annotations

import json
import os
import random
from typing import Dict, List

from emate.core.contracts import InputState


class QLearningNode:
    """
    Q学习节点类
    
    实现标准的表格Q学习算法，支持epsilon-greedy策略。
    所有学习参数可配置，Q表通过本地JSON文件持久化。
    
    特点：
    - 支持动态epsilon衰减
    - 自动Q表初始化
    - 本地文件持久化
    - 简单易用的API接口
    """

    def __init__(
        self,
        actions: List[str],
        alpha: float = 0.3,
        gamma: float = 0.85,
        epsilon: float = 0.3,
        min_epsilon: float = 0.05,
        epsilon_decay: float = 0.995,
        storage_path: str | None = None,
    ) -> None:
        """
        初始化Q学习节点
        
        Args:
            actions: 可用动作列表
            alpha: 学习率，控制新信息的接受程度 (0-1)
            gamma: 折扣因子，控制未来奖励的重要性 (0-1)
            epsilon: 探索率，控制随机探索的概率 (0-1)
            min_epsilon: 最小探索率，防止epsilon衰减过小
            epsilon_decay: epsilon衰减率，每次更新后epsilon的衰减比例
            storage_path: Q表存储路径，如果为None则使用默认路径
        """
        self.actions = actions  # 动作空间
        self.alpha = alpha  # 学习率
        self.gamma = gamma  # 折扣因子
        self.epsilon = epsilon  # 当前探索率
        self.min_epsilon = min_epsilon  # 最小探索率
        self.epsilon_decay = epsilon_decay  # 探索率衰减
        self.q_table: Dict[str, Dict[str, float]] = {}  # Q值表
        self.storage_path = storage_path or self._default_storage_path()  # 存储路径
        self._load()  # 从文件加载已有的Q表

    def _default_storage_path(self) -> str:
        """
        获取默认的Q表存储路径
        
        Returns:
            str: Q表JSON文件的默认存储路径
        """
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
        os.makedirs(base_dir, exist_ok=True)  # 确保目录存在
        return os.path.join(base_dir, "qtable.json")

    def _load(self) -> None:
        """
        从本地文件加载Q表数据
        
        如果文件不存在或加载失败，则初始化空的Q表。
        """
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.q_table = json.load(f)
            except Exception:
                # 文件损坏或格式错误时重新初始化
                self.q_table = {}

    def _save(self) -> None:
        """
        将当前Q表保存到本地文件
        
        使用JSON格式保存，包含中文字符支持和格式化缩进。
        保存失败时静默处理，不影响程序运行。
        """
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.q_table, f, ensure_ascii=False, indent=2)
        except Exception:
            # 保存失败时静默处理，避免影响主流程
            pass

    def _ensure_state(self, state_id: str) -> None:
        """
        确保指定状态在Q表中存在
        
        如果状态不存在，则为该状态初始化所有动作的Q值为0。
        
        Args:
            state_id: 状态标识符
        """
        if state_id not in self.q_table:
            # 为新状态初始化所有动作的Q值
            self.q_table[state_id] = {a: 0.0 for a in self.actions}

    def select_action(self, state_id: str) -> str:
        """
        使用epsilon-greedy策略选择动作
        
        以epsilon的概率进行随机探索，否则选择Q值最高的动作。
        
        Args:
            state_id: 当前状态标识符
            
        Returns:
            str: 选择的动作标识符
        """
        self._ensure_state(state_id)
        
        # epsilon-greedy策略：以epsilon概率随机探索
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        
        # 贪心选择：选择Q值最高的动作
        action_values = self.q_table[state_id]
        return max(action_values, key=action_values.get)

    def update(self, state_id: str, action_id: str, reward: float, next_state_id: str | None = None) -> None:
        """
        使用Q学习公式更新Q值
        
        根据收到的奖励和下一状态更新Q表，然后保存到文件并衰减epsilon。
        
        Args:
            state_id: 当前状态标识符
            action_id: 执行的动作标识符
            reward: 收到的即时奖励
            next_state_id: 下一状态标识符（可选）
        """
        self._ensure_state(state_id)
        
        # 获取当前Q值
        current = self.q_table[state_id].get(action_id, 0.0)
        
        # 计算目标Q值
        target = reward
        if next_state_id is not None:
            # 如果有下一状态，使用TD学习公式
            self._ensure_state(next_state_id)
            next_max = max(self.q_table[next_state_id].values())
            target = reward + self.gamma * next_max

        # 使用学习率更新Q值
        new_value = current + self.alpha * (target - current)
        self.q_table[state_id][action_id] = new_value
        
        # 保存更新后的Q表
        self._save()
        
        # 衰减探索率
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)


