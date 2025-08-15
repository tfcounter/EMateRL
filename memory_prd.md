
# 1) 记忆总览：短期 vs 长期

**短期（工作记忆 / Session memory）**

* 用途：维持最近若干轮对话、当前任务计划、工具调用结果与中间变量。
* 形态：滚动窗口 +（可选）对历史的“会话摘要”。
* 生命周期：随会话存在；可通过存储驱动持久化（否则脚本结束即丢失）。([Agno][1])

**长期（持久记忆 / User memory）**

* 用途：跨会话的人物档案（偏好、身份、事实）、重要结论与常驻知识线索。
* 形态：结构化事实 + 向量化的语义片段（便于召回）；必要时附 topic 标签与来源。
* 生命周期：持久化，带“可信度/重要度/新鲜度”元数据，支持更新与忘却。
* 在 Agno 中，对应 **User Memories** 与 **Session Summaries** 两类原生能力。([Agno][2])

# 2) 数据模型与检索策略（推荐）

**记录结构（建议）**

* `id, user_id, type{fact, pref, identity, task}, text, topics[], source, created_at, last_seen, importance∈[0,1], confidence∈[0,1], vector`
* 其中 `topics` 与 `vector` 便于快速过滤 + 语义召回；`importance/last_seen` 便于衰减。

**检索打分（用于组装上下文包）**
`score = 0.45*semantic + 0.25*recency + 0.2*importance + 0.1*exact_tag`

* 先按 topic/tag 粗过滤，再做语义 Top-K（K≈8），最后与近几轮对话去重合并。
* 召回物料组成“上下文包”：最近 N 轮 + 会话摘要（1条）+ 语义记忆（Top-K）+ 关键工具输出（Top-M）。

**巩固与遗忘（每轮或定期触发）**

* 抽取新事实（NER/正则+LLM 提取器），合并重复（embedding 近邻 + 文本相似度阈值）。
* `importance` 低且久未命中（如 30 天）则自动衰减/回收；被用户纠正的设高权重并锁定。

# 3) 基于 Agno 的最小可用实现

**核心开关与类型（Agno 原生）**

* 短期存储：`storage=...`（SQLite/Postgres/Mongo 等），用于持久化会话与状态。([Agno][1])
* 用户记忆：`memory=Memory(...)` + `enable_agentic_memory=True`（由 Agent 决定何时写入记忆）；或 `enable_user_memories=True`（每轮自动运行记忆管理器）。
* 会话摘要：`enable_session_summaries=True`（历史很长时自动生成摘要并持久化）。([Agno][2])
* 将已有记忆注入提示词：`add_memory_references=True`。([Agno][3])

**示例（SQLite 入门版）**

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory

DB_FILE = "tmp/agent.db"
memory = Memory(db=SqliteMemoryDb(table_name="user_memories", db_file=DB_FILE))
storage = SqliteStorage(table_name="agent_sessions", db_file=DB_FILE)

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    storage=storage,                        # 短期会话可持久化
    memory=memory,                          # 长期用户记忆
    enable_agentic_memory=True,             # Agent 可“写入/修改/删除”记忆
    enable_session_summaries=True,          # 自动会话摘要
    add_history_to_messages=True,           # 将最近历史拼入消息
    num_history_runs=3,
    read_chat_history=True,                 # 提供工具按需读取更久的历史
    add_memory_references=True              # 已有记忆注入系统提示
)
# 运行时带上 user_id / session_id 以多用户多会话隔离
resp = agent.print_response("我叫小李，我喜欢骑行。", user_id="u1", session_id="s1", stream=True)
```

上面使用的三类记忆与选项均出自 Agno 官方“Memory / Session Storage / User Memories / Session Summaries”文档与代码示例。([Agno][2])

**生产版（Postgres & pgvector，可混合语义检索）**

* 用 Postgres 承载 `storage=PostgresStorage(...)`；
* 用户长期语义片段放 pgvector / Qdrant / Pinecone 等，Agno 原生支持多种向量库与混合检索（hybrid）。([Agno][1])

# 4) 进阶：把“知识库”与“记忆”分工

* **记忆（Memory）**：以“和用户相关的可复用事实”为主，量小但高价值（姓名、偏好、约束、历史决策）。
* **知识库（Knowledge / Vector DB）**：面向文档与外部资料，量大，按 RAG 召回。Agno 内置多家向量库与混合检索，便于与记忆共同组成上下文。([Agno][4])

# 5) 与 Mem0 集成（选配，做“跨应用的用户画像”）

若希望把用户画像托管在独立服务里，可将 Mem0 的结果注入 Agent `context`，或直接用其工具写读记忆（Agno 示例已给出）。
优点：跨 Agent/服务共享；自带语义检索与多模态支持。([Agno][5], [Mem0][6])

# 6) 默认参数与工程建议

* **窗口**：`num_history_runs=3~5`；摘要长度 \~ 200–400 中文字。([Agno][2])
* **Top-K**：语义记忆 K=6–10；知识库 K=8–12；两者去重后 ≤ 模型上下文预算的 30–50%。
* **多租户**：所有读写均显式传入 `user_id` / `session_id`。([Agno][2])
* **治理**：提供“查看/删除我的记忆”的工具；对 PII 做红线屏蔽；被用户纠正的事实提升 `importance` 并锁定。
* **可观测性**：把“本轮提供给模型的上下文包”落盘，便于复盘与评估。
* **服务化**：在 FastAPI/Playground/多副本环境下务必配置 `storage`，否则内建内存不会跨请求保存。([Agno][1])

