### 技术设计文档：E-Mate 人格化决策模块（基于 Agno 的 RL Agents 体系）

#### 0. 对齐 PRD：人格、感知与记忆的一致性原则

- 人格基线：支持多种人格类型的动态切换，包括：
  - 标准工作助手：专业高效，逻辑清晰
  - 鼓励大师猫猫：可爱暖心，情绪价值
  - 面冷心热霸总：权威严格，内心关怀
  - 温暖细腻姐姐：敏锐洞察，温柔陪伴
  - 二次元魔法使：淡漠深邃，长期视角
  - 战火纷飞互怼狂：尖锐推动，结果导向
- 感知输入：多模态意图与情感识别（STT、SER、文本情感、行为模式），来自“多模态识别引擎”。
- 记忆规范：采用 Mem0 进行事实性与情景记忆的结构化存取；所有决策需检索关联记忆，形成“感知-记忆-人格”闭环。

---

#### 1. 体系结构（Agno 图）与角色分工

以 Agno 的图状架构组织人格化决策流，形成一个“可观察、可插拔、可演进”的决策中枢：

- Coordinator（Graph Orchestrator）
  - 负责路由、追踪与可视化，输出唯一的 `output_command`。
- PerceptionAdapterNode
  - 适配上游识别结果为统一的 `input_state`。
- MemoryQueryNode（Mem0）
  - 基于关键词与情境检索事实/情景记忆，产出可用的 `memory_context`。
- PersonaGuardNode
  - 基于当前选定人格的约束规则，对候选行动进行过滤与调整。
- PolicyRouterNode
  - 在 Micro（Q-learning）与 Macro（GSPO-LLM）策略间路由，或进行加权融合。
- MicroPolicySubgraph（Q-learning）
  - StateDiscretizerNode → QLearningNode → ActionMapperNode。
- MacroPolicySubgraph（GSPO-like 反思）
  - PromptEngineNode → PolicyGenerationNode → SelfEvaluationNode → SPOUpdateNode → PlanExecutionNode。
- ActionComposerNode
  - 合并多策略结果，进行冲突解决与兜底策略。
- ExecutorInterfaceNode
  - 下发屏幕动画、灯效、TTS、专注模式、提醒等指令。
- MemoryWritebackNode
  - 将本次决策的结构化摘要沉淀回 Mem0（含情感标签与执行结果）。
- RewardCollectorNode
  - 汇聚显式/隐式奖惩信号并持久化，为 RL 学习闭环提供反馈。

---

#### 2. I/O 契约（统一数据合同）

为所有 Node 统一输入输出格式，降低耦合并提升可测试性。

```json
{
  "perception_input": {
    "user_text": "string",
    "speech_emotion": "stress|calm|happy|sad|angry|fatigue",
    "text_sentiment": "positive|neutral|negative",
    "context_flags": ["interruption_high", "deadline_near", "long_session"],
    "time_of_day": "morning|afternoon|evening|night"
  },
  "memory_input": {
    "facts": ["Phoenix is top priority"],
    "episodes": [
      {
        "event": "work on Phoenix interrupted",
        "emotion": "frustration",
        "ts": "ISO8601"
      }
    ]
  },
  "system_context": {
    "personality": "StandardAssistant",
    "long_term_goals": ["improve coding skill"],
    "agent_mode": "QLearning|GSPO|Hybrid"
  }
}
```

输出 `output_command`：

```json
{
  "execution_output": {
    "screen_animation": "focused|celebrating|empathetic_nod|sleeping|breathing_calm",
    "light_effect": "focus_blue|warm_yellow_glow|calm_green_pulse|off"
  },
  "tts_output": {
    "text_to_speak": "string"
  },
  "action": {
    "type": "set_reminder|enter_focus_mode|suggest_break|none",
    "parameters": {
      "duration": 90,
      "related_task": "Phoenix draft",
      "deadline": "ISO8601"
    }
  },
  "memory_output": {
    "memory_to_store": {
      "input": {"...": "..."},
      "decision_reasoning": "string",
      "final_action": "string"
    }
  }
}
```

---

#### 3. 环境建模：状态-动作-奖励（Micro-Agent）

- 状态（离散化前特征）
  - 来自感知：`speech_emotion`、`text_sentiment`、`time_of_day`、`context_flags`、`user_text slots (intent, entities)`。
  - 来自记忆：与当前任务关联的事实/情景标签（如“高优先级”、“历史被打断”）。
- 状态离散化（StateDiscretizerNode）
  - 规则组合映射到有限状态集，如：`S_Afternoon_Stress_DeadlineNear_WithInterruptHistory`。
- 动作（ActionMapperNode 映射动作原子）
  - `enter_focus_mode(duration=25|45|90)`、`set_reminder(ts)`、`suggest_break(type=breathing|walk)`、`none`。
- 奖励设计（RewardCollectorNode 聚合）
  - 显式：用户 thumbs up/down、确认/否定（+1/-1 或强度权重）。
  - 隐式：
    - SER 情绪改善（如 stress↓、calm↑）映射为正奖励。
    - 任务完成/进度推进（来自任务系统或日程）正奖励。
    - 打断频次下降、专注时长上升为正奖励。
  - 奖励整合：
    - R = w1·explicit + w2·emotion_delta + w3·task_signal + w4·focus_metrics（权重可个性化与自动调优）。

---

#### 4. 算法配置（Micro vs. Macro）

- Micro（Q-Learning）
  - 学习率 α=0.3（自适应下调），折扣 γ=0.85，ε-greedy 初始 ε=0.3，按交互数指数衰减至 0.05。
  - Q-Table 按 `(state_id, action_id)` 持久化（本地 JSON/npz），冷启动可用启发式预填（persona 先验）。
  - 支持在线 `POST /reward {state, action, reward}` 更新；并定期 `snapshot`。
  - 可选升级路线：若状态维度增大，引入 DQN（MLP）或离散化改进（tile coding）。
- Macro（GSPO-like + LLM）
  - 用 LLM 进行“生成-评估-优化”循环；`SPOUpdateNode` 将偏好对记录到日志，并驱动“人格宪法/准则”版本化（`persona_vN.md|yaml`）。
  - 与 Mem0 紧耦合：检索事实/情景，作为 Prompt 的“证据块”。
  - 约束满足：`PersonaGuardNode` 在执行前应用当前人格的特定约束规则。

---

#### 5. 记忆增强与数据模式（Mem0）

- 写入（MemoryWritebackNode）：
```json
{
  "user_input": "...",
  "detected_emotion": "stress",
  "intent": "create_task_reminder",
  "entities": {"task": "Phoenix draft", "deadline": "Friday"},
  "chosen_policy": "QLearning|GSPO|Hybrid",
  "final_action": {"type": "enter_focus_mode", "duration": 90},
  "decision_reasoning": "short rationale",
  "outcome_signals": {"explicit": 1, "emotion_delta": 0.4}
}
```
- 检索（MemoryQueryNode）：结合 keyword、entity、时间窗与情感标签，返回“事实 + 情景”上下文，用于稳态与跨会话一致性。

---

#### 6. 多代理协作（Agno 多 Agent 团队）

- 角色建议：
  - Intent Agent（解析/slotting）
  - Memory Agent（检索/摘要）
  - Persona Agent（约束/过滤）
  - Policy Agent（Micro/Macro 策略）
  - Execution Agent（指令下发与回执）
  - Feedback Agent（奖励提取与指标聚合）
- 机制：任务分工 + 冲突解决（ActionComposerNode），可替换、可并行。

---

#### 7. 外部工具与执行接口

- 行为执行：屏幕动画、灯效、TTS、系统免打扰/专注模式、提醒/日程。
- 建议工具接入（根据 Agno 工具体系扩展）：
  - OS/Calendar/Notification tools、MQTT/REST 设备控制器。
  - 可选通用工具：Web 搜索、金融等（非本 MVP 关键）。

---

#### 8. 评估指标与实验方法

- 关键指标（与 PRD 对齐）：
  - 人格一致性率（符合当前选定人格约束的比例）≥ 99%。
  - 情绪改善幅度（SER delta ≥ 0.2 按会话计）。
  - 专注时长提升（会话 7 天滚动均值）。
  - 任务达成率（deadline 前完成）。
  - 用户正反馈率（显式正反馈 / 总交互）。
- 实验设计：
  - A/B：Micro vs. Macro vs. Hybrid。
  - 合成回放：使用日志回放生成稳定可重现的训练曲线。
  - 失效注入：极端负面情绪/连续打断/密集日程等压力场景。

---

#### 9. 迭代与里程碑（4 周）

- 第 1 周（MVP 环路打通）
  - 完成 I/O 契约与 Agno Graph 骨架；接入 Mem0 读写；实现 `StateDiscretizerNode`、`QLearningNode`、`ActionMapperNode`；完成执行器的最小指令集（动画/灯效/专注模式）。
- 第 2 周（奖励与评估）
  - RewardCollectorNode 汇总显式/隐式信号；Q-table 持久化与可视化；加入 PersonaGuardNode；指标仪表板（情感 delta、专注时长、任务率）。
- 第 3 周（Macro 与反思）
  - 宏观策略子图（PromptEngine/PolicyGeneration/SelfEvaluation/SPOUpdate/PlanExecution）；人格宪法版本化与热切换；Hybrid 路由与冲突解决。
- 第 4 周（稳健性与演示）
  - 压测、边界场景、回放套件；现场演示剧本（“凤凰项目”场景）；文档与脚本完善。

---

#### 10. 目录结构建议（代码落地）

```
emate/
  core/
    graph.py                 # Agno graph assembly
    contracts.py             # dataclasses/schemas for IO
    persona_guard.py         # PersonaGuardNode
    reward.py                # RewardCollectorNode
  micro/
    state_discretizer.py     # StateDiscretizerNode
    qlearning.py             # QLearningNode (persist Q-table)
    action_map.py            # ActionMapperNode
  macro/
    prompts.py               # PromptEngineNode
    policy_gen.py            # PolicyGenerationNode (LLM)
    self_eval.py             # SelfEvaluationNode (LLM judge)
    spo_update.py            # SPOUpdateNode (preference logging + persona switch)
    plan_exec.py             # PlanExecutionNode
  memory/
    mem0_client.py           # Mem0 read/write adapter
  exec/
    actuators.py             # screen/lights/tts/focus mode
    router.py                # ExecutorInterfaceNode
  app/
    manager.py               # AgentManager entry
    config.yaml              # persona/version/weights
    persona_v1.yaml          # StandardAssistant constitution v1
    persona_v2.yaml          # evolved rules v2
  tests/
    replay/
      phoenix_session.json   # synthetic logs for playback
```

---

#### 11. 安全、隐私与合规

- 本地优先：SER/STT 可本地推理（Whisper/SER），仅在必要时调用云 LLM。
- 数据最小化：仅写入与策略与复盘相关的最小字段；敏感字段脱敏。
- 可解释性：保留“决策理由”与“人格约束触发点”便于审计。

---

#### 12. 关键实现要点（开发提示）

- Persona 宪法以声明式 YAML 编写，`PersonaGuardNode` 通过规则匹配做硬过滤与替代建议。
- Q-learning 的状态爆炸风险通过：精简离散特征、历史窗口限制、必要时引入函数逼近（DQN）。
- 奖励稀疏问题通过多通道奖励整合与密集中间奖励（如专注 25min 成功）缓解。
- Macro 子图的“优化”先以偏好日志 + 宪法演进模拟，待 MVP 稳定后可接 PPO/BRPO 等策略微调管线。

---

#### 13. 示例 Prompt（对齐 whole_dev.md 的 JSON 指令规范）

```markdown
# ROLE & PERSONALITY
You are E-Mate with [PERSONALITY] persona. Adapt your response style according to the selected personality traits and constraints.

# CURRENT SITUATION
- user_text: "唉，提醒我一下，周五前必须完成‘凤凰项目’的草案。"
- speech_emotion: "stress", text_sentiment: "negative"

# MEMORY CONTEXT
- Fact: Phoenix is top priority this quarter.
- Episode: interruptions caused frustration before.

# TASK
Return a single JSON with keys: responseText, screenAnimation, lightEffect, action{type, parameters}.
```

---

#### 14. 演示剧本（与 PRD 场景对齐）

- 用户口述带有叹息与“必须完成”的高压请求 → SER/意图识别 → Mem0 检索“高优先级+被打断史” → PersonaGuard 过滤 → PolicyRouter 选 Micro（或 Hybrid） → 动作合成（专注模式 90 分钟 + 蓝色灯效 + 同理短语）→ 执行 → 写回记忆 → 奖励采集（显式 + 情绪改善）。

---

本方案在不牺牲工程可行性的前提下，实现了支持多种人格类型的动态决策系统，利用 Agno 的图式与多代理组合能力，结合 Mem0 记忆、反思细化与多通道奖励，形成可进化的多人格决策中枢。

