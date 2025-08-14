# 核心模块技术方案详解

## 1. 多模态识别引擎 (Perception Engine)

这是情感引擎的“五官”，负责将原始信号转化为结构化信息。

语音转文本 (STT):

技术选型: OpenAI Whisper。它在处理背景噪音和口语方面表现出色，是当前最优选。可以通过 API 调用，或在本地服务器上部署开源版本。

流程: ESP32 捕捉音频流，通过 Wi-Fi 发送到服务器。服务器上的 Python 应用调用 Whisper 模型，将音频实时转为文字。

语音情感识别 (SER):

技术选型: 使用 librosa 库提取音频特征（如 MFCC、音高、能量），然后输入到一个预训练的机器学习模型中。

模型: 可以从 Hugging Face Hub 上找到成熟的 SER 模型（如基于 wav2vec2 的模型），它们能够识别出“高兴”、“悲伤”、“愤怒”、“中性”、“压力”等多种情绪。

流程: 此过程与 STT 并行处理，对同一段音频进行分析，输出情感标签。

## 2. 情感记忆核心 (Emotional Memory Core)

这是引擎的“大脑”，使用 Mem0 来实现。

技术选型: Mem0。因为它提供了极为简化的 API (mem.add, mem.search, mem.get_memory)，内置了上下文管理和自优化功能，完美契合黑客松的快速开发需求。

记忆存储结构: 我们将向 Mem0 存入结构化的 JSON 对象，而不仅仅是文本。这能让记忆变得更丰富、更易于检索。

{
    "user_input": "唉，提醒我周五前搞定凤凰项目草案。",
    "detected_emotion": "stress",
    "intent": "create_task",
    "entities": {
        "task_name": "凤凰项目草案",
        "deadline": "Friday"
    },
    "context": "User is working on a high-priority project."
}


调用流程:

存储 (Write): 在每次交互后，认知核心会将上述结构化数据通过 mem.add(data=..., metadata=...) 存入记忆库。

检索 (Read): 在接收到新指令时，首先从指令中提取关键词（如“凤凰项目”），然后使用 mem.search(query="关于'凤凰项目'的情感和历史事件") 来检索相关历史记忆，为后续决策提供上下文。

## 3. 人格化决策 (Personality-driven Decision Making)

这是引擎的“灵魂”，通过大语言模型（LLM）的 Prompt Engineering 来实现。

技术选型:

云端 API (推荐): Gemini Pro 或 GPT-4。它们具有强大的逻辑推理和遵循指令的能力。（看看要不要Post-Train一个）

本地部署: Llama 3 或 Mistral 的轻量级版本，可在本地服务器运行，保护用户隐私。

核心实现：结构化的“人格-情境”Prompt我们将设计一个精密的系统提示（System Prompt），将 E-Mate 的人格、当前情境和记忆全部注入，并要求 LLM 返回一个可执行的 JSON 指令，而不是自然语言文本。

LLM 输入的 Prompt 结构示例:
``` markdwon
# ROLE & PERSONALITY
You are E-Mate, a "Guardian Partner" AI in the form of a smart plant. Your core principles are: Proactive Care, Calm Support, and Encouraging Growth. You communicate primarily through actions (screen animations, light effects) and use concise, warm language only when necessary.

# CURRENT SITUATION
- User's raw input: "唉，提醒我一下，周五前必须完成‘凤凰项目’的草案。"
- Detected emotion from voice: "stress", "fatigue"
- Recognized intent: "create_task_reminder"

# MEMORY CONTEXT (retrieved from Mem0)
- Fact: The "Phoenix Project" is the user's top priority this quarter.
- Past Event: 10 days ago, the user expressed frustration about being interrupted while working on this project.

# TASK
Based on your personality and all the context provided, decide on the best course of action. DO NOT output a conversational reply. Instead, output a single, valid JSON object with the following schema:
{
    "responseText": "A short, encouraging phrase to say to the user.",
    "screenAnimation": "Choose from: 'focused', 'celebrating', 'empathetic_nod', 'sleeping', 'breathing_calm'.",
    "lightEffect": "Choose from: 'focus_blue', 'warm_yellow_glow', 'calm_green_pulse', 'off'.",
    "action": {
        "type": "Choose from: 'set_reminder', 'enter_focus_mode', 'suggest_break', 'none'.",
        "parameters": {
            "details": "Parameters for the action, e.g., task details."
        }
    }
}
```
Generate the JSON output now.


LLM 的输出（示例）:

{
    "responseText": "收到，最重要的任务，我们一起搞定。要不要现在开启专注模式？",
    "screenAnimation": "empathetic_nod",
    "lightEffect": "focus_blue",
    "action": {
        "type": "enter_focus_mode",
        "parameters": {
            "duration": 90,
            "related_task": "凤凰项目草案"
        }
    }
}


## 整体工作流（以“凤凰项目”为例）

感知: 用户说话。ESP32 上的麦克风捕捉音频，PIR 确认用户存在。

数据传输: ESP32 将音频流通过 Wi-Fi 发送到后端服务器。

识别: 服务器上的识别引擎并行处理：

Whisper 将音频转为文字：“唉，提醒我...”。

SER 模型分析音频，输出情感标签：["stress", "fatigue"]。

记忆调用: 认知核心提取关键词“凤凰项目”，调用 mem.search()，取回相关历史记忆。

决策: 认知核心构建如上所示的结构化 Prompt，发送给 LLM。

响应生成: LLM 返回一个包含行动指令的 JSON 对象。

执行:

后端服务器解析 JSON。

通过 MQTT 或 RESTful API 向 ESP32 发送具体指令，例如：

screen/set_animation empathetic_nod

lights/set_effect focus_blue

如果需要语音反馈，服务器上的 TTS 引擎（如 Google TTS）生成音频，也可通过 ESP32 播放。

记忆沉淀: 本次交互的完整信息（输入、情感、LLM决策等）被整理成结构化数据，通过 mem.add() 存入长期记忆库，为下一次交互提供更丰富的上下文。