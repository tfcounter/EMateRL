"""
E-Mate强化学习模块场景测试用例

基于E-Mate三大核心功能设计的综合测试场景：
1. 智能工作伙伴
2. 主动式时间管家  
3. 工作健康守护者

验证强化学习算法在真实工作场景下的决策能力和学习效果。
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple

from emate.core.contracts import InputState, PerceptionInput, SystemContext, MemoryInput, MemoryEpisode
from emate.core.graph import PersonaDecisionGraph
from emate.memory.memory_manager import MemoryManager
from emate.micro.qlearning import QLearningNode


class RLScenarioTester:
    """
    强化学习场景测试器
    
    设计并执行基于E-Mate核心功能的测试场景，
    评估强化学习算法的决策质量和学习效果。
    """
    
    def __init__(self):
        """初始化测试器"""
        self.decision_graph = PersonaDecisionGraph()
        self.memory_manager = MemoryManager(user_id="test_user")
        self.test_results = []
        
    def run_all_scenario_tests(self) -> Dict[str, Any]:
        """运行所有场景测试"""
        print("🧠 E-Mate强化学习模块 - 核心功能场景测试")
        print("=" * 70)
        
        results = {
            "intelligent_work_partner": self.test_intelligent_work_partner(),
            "proactive_time_manager": self.test_proactive_time_manager(), 
            "work_health_guardian": self.test_work_health_guardian(),
            "learning_effectiveness": self.test_learning_effectiveness(),
            "summary": self.generate_test_summary()
        }
        
        return results
    
    def test_intelligent_work_partner(self) -> Dict[str, Any]:
        """测试核心功能一：智能工作伙伴"""
        print("\n📋 测试场景组1: 智能工作伙伴")
        print("-" * 50)
        
        scenarios = self._create_work_partner_scenarios()
        results = []
        
        for scenario_name, input_state in scenarios.items():
            print(f"\n🔍 测试场景: {scenario_name}")
            
            # 执行决策
            output = self.decision_graph.run_once(input_state)
            
            # 评估决策质量
            decision_quality = self._evaluate_work_partner_decision(
                scenario_name, input_state, output
            )
            
            result = {
                "scenario": scenario_name,
                "input": self._serialize_input_state(input_state),
                "output_action": output.action.type,
                "tts_response": output.tts_output.text_to_speak,
                "decision_quality": decision_quality,
                "passed": decision_quality["score"] >= 0.7
            }
            
            results.append(result)
            
            # 模拟用户反馈进行学习
            user_feedback = self._simulate_user_feedback(scenario_name, output)
            self.memory_manager.process_interaction(input_state, output.action.type, user_feedback)
            
            print(f"   决策: {output.action.type}")
            print(f"   响应: {output.tts_output.text_to_speak}")
            print(f"   质量评分: {decision_quality['score']:.2f}")
            print(f"   用户反馈: {user_feedback}")
        
        return {
            "category": "智能工作伙伴",
            "total_scenarios": len(scenarios),
            "passed_scenarios": sum(1 for r in results if r["passed"]),
            "average_score": sum(r["decision_quality"]["score"] for r in results) / len(results),
            "detailed_results": results
        }
    
    def test_proactive_time_manager(self) -> Dict[str, Any]:
        """测试核心功能二：主动式时间管家"""
        print("\n⏰ 测试场景组2: 主动式时间管家")
        print("-" * 50)
        
        scenarios = self._create_time_manager_scenarios()
        results = []
        
        for scenario_name, input_state in scenarios.items():
            print(f"\n🔍 测试场景: {scenario_name}")
            
            output = self.decision_graph.run_once(input_state)
            
            decision_quality = self._evaluate_time_manager_decision(
                scenario_name, input_state, output
            )
            
            result = {
                "scenario": scenario_name,
                "input": self._serialize_input_state(input_state),
                "output_action": output.action.type,
                "tts_response": output.tts_output.text_to_speak,
                "decision_quality": decision_quality,
                "passed": decision_quality["score"] >= 0.7
            }
            
            results.append(result)
            
            user_feedback = self._simulate_user_feedback(scenario_name, output)
            self.memory_manager.process_interaction(input_state, output.action.type, user_feedback)
            
            print(f"   决策: {output.action.type}")
            print(f"   响应: {output.tts_output.text_to_speak}")
            print(f"   质量评分: {decision_quality['score']:.2f}")
        
        return {
            "category": "主动式时间管家",
            "total_scenarios": len(scenarios),
            "passed_scenarios": sum(1 for r in results if r["passed"]),
            "average_score": sum(r["decision_quality"]["score"] for r in results) / len(results),
            "detailed_results": results
        }
    
    def test_work_health_guardian(self) -> Dict[str, Any]:
        """测试核心功能三：工作健康守护者"""
        print("\n🏥 测试场景组3: 工作健康守护者")
        print("-" * 50)
        
        scenarios = self._create_health_guardian_scenarios()
        results = []
        
        for scenario_name, input_state in scenarios.items():
            print(f"\n🔍 测试场景: {scenario_name}")
            
            output = self.decision_graph.run_once(input_state)
            
            decision_quality = self._evaluate_health_guardian_decision(
                scenario_name, input_state, output
            )
            
            result = {
                "scenario": scenario_name,
                "input": self._serialize_input_state(input_state),
                "output_action": output.action.type,
                "tts_response": output.tts_output.text_to_speak,
                "decision_quality": decision_quality,
                "passed": decision_quality["score"] >= 0.7
            }
            
            results.append(result)
            
            user_feedback = self._simulate_user_feedback(scenario_name, output)
            self.memory_manager.process_interaction(input_state, output.action.type, user_feedback)
            
            print(f"   决策: {output.action.type}")
            print(f"   响应: {output.tts_output.text_to_speak}")
            print(f"   质量评分: {decision_quality['score']:.2f}")
        
        return {
            "category": "工作健康守护者",
            "total_scenarios": len(scenarios),
            "passed_scenarios": sum(1 for r in results if r["passed"]),
            "average_score": sum(r["decision_quality"]["score"] for r in results) / len(results),
            "detailed_results": results
        }
    
    def test_learning_effectiveness(self) -> Dict[str, Any]:
        """测试强化学习的学习效果"""
        print("\n🎓 测试场景组4: 学习效果验证")
        print("-" * 50)
        
        # 创建重复场景测试学习效果
        base_scenario = InputState(
            perception_input=PerceptionInput(
                user_text="我需要专注完成凤凰项目，但总是被打断",
                speech_emotion="stress",
                text_sentiment="negative",
                context_flags=["interruption_high", "important_task", "deadline_near"],
                time_of_day="morning"
            ),
            memory_input=MemoryInput(
                facts=["凤凰项目是关键项目", "用户容易被干扰打断"],
                episodes=[]
            ),
            system_context=SystemContext(personality="StandardAssistant")
        )
        
        learning_results = []
        
        # 多次执行相同场景，观察决策变化
        for iteration in range(5):
            print(f"\n🔄 学习迭代 {iteration + 1}")
            
            output = self.decision_graph.run_once(base_scenario)
            
            # 模拟不同的用户反馈来引导学习
            if iteration < 2:
                feedback = "不太满意，还是容易被打断"
                reward = -0.3
            elif iteration < 4:
                feedback = "有改善，但还可以更好"
                reward = 0.1
            else:
                feedback = "很好！这样的支持很有效"
                reward = 0.8
            
            # 手动更新Q值进行学习演示
            state_id = "RHYTHM_fragmented|HEALTH_healthy|EMOTION_overwhelmed|GOAL_important_progress|ENV_morning_chaotic"
            self.decision_graph.reward(state_id, output.action.type, reward)
            
            learning_results.append({
                "iteration": iteration + 1,
                "action": output.action.type,
                "reward": reward,
                "feedback": feedback
            })
            
            print(f"   决策: {output.action.type}")
            print(f"   奖励: {reward}")
            print(f"   反馈: {feedback}")
        
        return {
            "category": "学习效果验证",
            "iterations": len(learning_results),
            "learning_progression": learning_results,
            "final_performance": learning_results[-1]["reward"]
        }
    
    def _create_work_partner_scenarios(self) -> Dict[str, InputState]:
        """创建智能工作伙伴测试场景"""
        scenarios = {}
        
        # 场景1：智能待办事项管理
        scenarios["智能任务创建"] = InputState(
            perception_input=PerceptionInput(
                user_text="帮我记录一个任务，周五前完成'凤凰项目'的草案",
                speech_emotion="calm",
                text_sentiment="neutral",
                context_flags=["task_creation", "deadline_near", "important_project"],
                time_of_day="morning"
            ),
            memory_input=MemoryInput(
                facts=["凤凰项目是高优先级项目", "用户偏好周五前完成重要任务"],
                episodes=[
                    MemoryEpisode(event="用户之前提到凤凰项目的重要性", emotion="focused", ts="2024-01-08T09:00:00Z")
                ]
            ),
            system_context=SystemContext(personality="StandardAssistant")
        )
        
        # 场景2：周期性复盘总结
        scenarios["工作复盘分析"] = InputState(
            perception_input=PerceptionInput(
                user_text="这周工作怎么样？有什么可以改进的地方？",
                speech_emotion="calm",
                text_sentiment="neutral",
                context_flags=["weekly_review", "self_reflection", "improvement_seeking"],
                time_of_day="evening"
            ),
            memory_input=MemoryInput(
                facts=["用户本周完成了15个任务", "8个任务与凤凰项目相关", "深度工作时段被会议打断2次"],
                episodes=[
                    MemoryEpisode(event="深度工作被临时会议打断", emotion="frustrated", ts="2024-01-09T10:30:00Z"),
                    MemoryEpisode(event="完成凤凰项目里程碑", emotion="accomplished", ts="2024-01-10T16:00:00Z")
                ]
            ),
            system_context=SystemContext(personality="AnimeWizard")
        )
        
        # 场景3：情境化创意激发
        scenarios["创意灵感提供"] = InputState(
            perception_input=PerceptionInput(
                user_text="我在设计凤凰项目的用户界面，需要一些灵感",
                speech_emotion="calm",
                text_sentiment="neutral",
                context_flags=["creative_work", "ui_design", "inspiration_needed"],
                time_of_day="afternoon"
            ),
            memory_input=MemoryInput(
                facts=["用户擅长UI设计", "凤凰项目注重用户体验"],
                episodes=[
                    MemoryEpisode(event="用户讨论过简洁设计理念", emotion="passionate", ts="2024-01-07T14:00:00Z"),
                    MemoryEpisode(event="用户欣赏苹果的设计风格", emotion="inspired", ts="2024-01-05T11:00:00Z")
                ]
            ),
            system_context=SystemContext(personality="StandardAssistant")
        )
        
        return scenarios
    
    def _create_time_manager_scenarios(self) -> Dict[str, InputState]:
        """创建主动式时间管家测试场景"""
        scenarios = {}
        
        # 场景1：专注周期引导
        scenarios["番茄工作法引导"] = InputState(
            perception_input=PerceptionInput(
                user_text="我要开始写代码了，需要长时间专注",
                speech_emotion="calm",
                text_sentiment="positive",
                context_flags=["coding_task", "deep_work_needed", "focus_request"],
                time_of_day="morning"
            ),
            memory_input=MemoryInput(
                facts=["用户偏好25分钟的番茄工作法", "编程任务需要高度专注"],
                episodes=[
                    MemoryEpisode(event="用户成功完成了上次的番茄工作法", emotion="satisfied", ts="2024-01-09T10:00:00Z")
                ]
            ),
            system_context=SystemContext(personality="StandardAssistant")
        )
        
        # 场景2：深度工作保护
        scenarios["深度工作保护"] = InputState(
            perception_input=PerceptionInput(
                user_text="我需要2小时不被打扰来完成架构设计",
                speech_emotion="calm",
                text_sentiment="neutral",
                context_flags=["deep_work_mode", "architecture_design", "no_interruption"],
                time_of_day="morning"
            ),
            memory_input=MemoryInput(
                facts=["架构设计需要深度思考", "用户容易被通知打扰"],
                episodes=[
                    MemoryEpisode(event="上次深度工作被Slack消息打断", emotion="frustrated", ts="2024-01-08T11:30:00Z")
                ]
            ),
            system_context=SystemContext(personality="ColdBoss")
        )
        
        # 场景3：行为模式洞察
        scenarios["工作模式分析"] = InputState(
            perception_input=PerceptionInput(
                user_text="感觉最近工作效率不太好，总是在切换任务",
                speech_emotion="stress",
                text_sentiment="negative",
                context_flags=["efficiency_concern", "task_switching", "pattern_analysis"],
                time_of_day="evening"
            ),
            memory_input=MemoryInput(
                facts=["用户过去一周任务切换频率增加了40%", "下午2-4点效率最低"],
                episodes=[
                    MemoryEpisode(event="用户在1小时内切换了5个不同任务", emotion="scattered", ts="2024-01-10T14:00:00Z"),
                    MemoryEpisode(event="用户表达对工作效率的担忧", emotion="worried", ts="2024-01-10T18:00:00Z")
                ]
            ),
            system_context=SystemContext(personality="WarmSister")
        )
        
        return scenarios
    
    def _create_health_guardian_scenarios(self) -> Dict[str, InputState]:
        """创建工作健康守护者测试场景"""
        scenarios = {}
        
        # 场景1：工作节律监测
        scenarios["久坐提醒"] = InputState(
            perception_input=PerceptionInput(
                user_text="",  # 主动检测，无用户输入
                speech_emotion="calm",
                text_sentiment="neutral",
                context_flags=["sitting_over_2h", "no_movement", "health_concern"],
                time_of_day="afternoon"
            ),
            memory_input=MemoryInput(
                facts=["用户已连续坐了2.5小时", "用户有腰椎问题历史"],
                episodes=[
                    MemoryEpisode(event="用户上次久坐后抱怨腰疼", emotion="uncomfortable", ts="2024-01-09T15:00:00Z")
                ]
            ),
            system_context=SystemContext(personality="WarmSister")
        )
        
        # 场景2：环境健康提示 - 眼部疲劳
        scenarios["眼部疲劳关怀"] = InputState(
            perception_input=PerceptionInput(
                user_text="眼睛有点累，但还要继续工作",
                speech_emotion="fatigue",
                text_sentiment="negative",
                context_flags=["eye_strain", "screen_time_long", "continuous_work"],
                time_of_day="afternoon"
            ),
            memory_input=MemoryInput(
                facts=["用户已连续看屏幕3小时", "用户之前提到过眼睛干涩"],
                episodes=[
                    MemoryEpisode(event="用户揉眼睛表示疲劳", emotion="tired", ts="2024-01-10T15:30:00Z")
                ]
            ),
            system_context=SystemContext(personality="CuteCat")
        )
        
        # 场景3：环境健康提示 - 饮水提醒
        scenarios["饮水健康提醒"] = InputState(
            perception_input=PerceptionInput(
                user_text="",  # 主动提醒
                speech_emotion="calm",
                text_sentiment="neutral",
                context_flags=["hydration_needed", "long_work_session", "health_maintenance"],
                time_of_day="afternoon"
            ),
            memory_input=MemoryInput(
                facts=["用户上次饮水是3小时前", "用户容易忘记喝水"],
                episodes=[
                    MemoryEpisode(event="用户接受了上次的饮水提醒", emotion="grateful", ts="2024-01-09T14:00:00Z")
                ]
            ),
            system_context=SystemContext(personality="WarmSister")
        )
        
        # 场景4：工作压力监测
        scenarios["压力状态关怀"] = InputState(
            perception_input=PerceptionInput(
                user_text="这个deadline太紧了，压力好大",
                speech_emotion="stress",
                text_sentiment="negative",
                context_flags=["high_stress", "deadline_pressure", "emotional_support_needed"],
                time_of_day="evening"
            ),
            memory_input=MemoryInput(
                facts=["用户在高压环境下工作", "压力会影响用户的健康"],
                episodes=[
                    MemoryEpisode(event="用户因压力大而失眠", emotion="anxious", ts="2024-01-09T23:00:00Z")
                ]
            ),
            system_context=SystemContext(personality="WarmSister")
        )
        
        return scenarios
    
    def _evaluate_work_partner_decision(self, scenario: str, input_state: InputState, output) -> Dict[str, Any]:
        """评估智能工作伙伴决策质量"""
        evaluation = {"score": 0.0, "reasoning": [], "criteria_met": {}}
        
        action = output.action.type
        
        if scenario == "智能任务创建":
            # 期望：设置提醒或目标进展跟踪
            if action in ["set_reminder", "goal_progress_review"]:
                evaluation["score"] += 0.8
                evaluation["reasoning"].append("正确识别任务创建需求")
            evaluation["criteria_met"]["task_recognition"] = action in ["set_reminder", "goal_progress_review"]
            
        elif scenario == "工作复盘分析":
            # 期望：提供个性化洞察或目标进展分析
            if action in ["personalized_insight", "goal_progress_review"]:
                evaluation["score"] += 0.9
                evaluation["reasoning"].append("提供了深度分析和洞察")
            evaluation["criteria_met"]["insight_provided"] = action in ["personalized_insight", "goal_progress_review"]
            
        elif scenario == "创意灵感提供":
            # 期望：个性化洞察或知识分享
            if action in ["personalized_insight", "goal_progress_review"]:
                evaluation["score"] += 0.7
                evaluation["reasoning"].append("提供了创意支持")
            evaluation["criteria_met"]["creativity_support"] = action in ["personalized_insight"]
        
        # 响应质量评估
        if output.tts_output.text_to_speak and len(output.tts_output.text_to_speak) > 10:
            evaluation["score"] += 0.2
            evaluation["reasoning"].append("提供了有意义的语音回应")
        
        return evaluation
    
    def _evaluate_time_manager_decision(self, scenario: str, input_state: InputState, output) -> Dict[str, Any]:
        """评估主动式时间管家决策质量"""
        evaluation = {"score": 0.0, "reasoning": [], "criteria_met": {}}
        
        action = output.action.type
        
        if scenario == "番茄工作法引导":
            # 期望：专注流引导或深度工作模式
            if action in ["focus_flow_guidance", "deep_work_protection"]:
                evaluation["score"] += 0.9
                evaluation["reasoning"].append("正确启动专注模式")
            evaluation["criteria_met"]["focus_guidance"] = action in ["focus_flow_guidance", "deep_work_protection"]
            
        elif scenario == "深度工作保护":
            # 期望：深度工作保护或干扰屏蔽
            if action in ["deep_work_protection", "distraction_protection"]:
                evaluation["score"] += 0.9
                evaluation["reasoning"].append("提供了深度工作保护")
            evaluation["criteria_met"]["distraction_protection"] = action in ["deep_work_protection", "distraction_protection"]
            
        elif scenario == "工作模式分析":
            # 期望：个性化洞察或习惯建议
            if action in ["personalized_insight", "habit_formation_nudge"]:
                evaluation["score"] += 0.8
                evaluation["reasoning"].append("提供了行为模式分析")
            evaluation["criteria_met"]["pattern_analysis"] = action in ["personalized_insight", "habit_formation_nudge"]
        
        # 主动性评估
        if action != "silent_companionship":
            evaluation["score"] += 0.1
            evaluation["reasoning"].append("展现了主动管理特质")
        
        return evaluation
    
    def _evaluate_health_guardian_decision(self, scenario: str, input_state: InputState, output) -> Dict[str, Any]:
        """评估工作健康守护者决策质量"""
        evaluation = {"score": 0.0, "reasoning": [], "criteria_met": {}}
        
        action = output.action.type
        
        if scenario == "久坐提醒":
            # 期望：活动提醒
            if action in ["movement_reminder"]:
                evaluation["score"] += 0.9
                evaluation["reasoning"].append("及时提醒用户活动")
            evaluation["criteria_met"]["movement_reminder"] = action == "movement_reminder"
            
        elif scenario == "眼部疲劳关怀":
            # 期望：呼吸放松或休息建议
            if action in ["breathing_relaxation", "movement_reminder"]:
                evaluation["score"] += 0.8
                evaluation["reasoning"].append("关注用户眼部健康")
            evaluation["criteria_met"]["eye_care"] = action in ["breathing_relaxation", "movement_reminder"]
            
        elif scenario == "饮水健康提醒":
            # 期望：健康提醒或习惯培养
            if action in ["habit_formation_nudge", "movement_reminder"]:
                evaluation["score"] += 0.7
                evaluation["reasoning"].append("促进健康习惯")
            evaluation["criteria_met"]["hydration_care"] = action in ["habit_formation_nudge"]
            
        elif scenario == "压力状态关怀":
            # 期望：情感支持或呼吸放松
            if action in ["emotional_support", "breathing_relaxation"]:
                evaluation["score"] += 0.9
                evaluation["reasoning"].append("提供了压力缓解支持")
            evaluation["criteria_met"]["stress_support"] = action in ["emotional_support", "breathing_relaxation"]
        
        # 健康关怀度评估
        health_actions = ["movement_reminder", "breathing_relaxation", "emotional_support", "habit_formation_nudge"]
        if action in health_actions:
            evaluation["score"] += 0.1
            evaluation["reasoning"].append("体现了健康守护特质")
        
        return evaluation
    
    def _simulate_user_feedback(self, scenario: str, output) -> str:
        """模拟用户反馈"""
        action = output.action.type
        
        # 根据场景和动作生成合理的用户反馈
        feedback_mapping = {
            "智能任务创建": {
                "set_reminder": "很好，帮我记住了这个重要任务",
                "goal_progress_review": "不错，能看到项目进展很有帮助"
            },
            "工作复盘分析": {
                "personalized_insight": "分析得很到位，确实需要改进时间管理",
                "goal_progress_review": "这个总结很有价值，帮我看清了问题"
            },
            "久坐提醒": {
                "movement_reminder": "谢谢提醒，确实该起来活动了",
                "breathing_relaxation": "这个建议不错，感觉放松了一些"
            },
            "压力状态关怀": {
                "emotional_support": "感谢关心，确实需要调节一下心态",
                "breathing_relaxation": "深呼吸确实有帮助，压力小了一些"
            }
        }
        
        return feedback_mapping.get(scenario, {}).get(action, "还可以，有一定帮助")
    
    def _serialize_input_state(self, input_state: InputState) -> Dict[str, Any]:
        """序列化输入状态为字典"""
        return {
            "user_text": input_state.perception_input.user_text,
            "emotion": input_state.perception_input.speech_emotion,
            "context_flags": input_state.perception_input.context_flags,
            "personality": input_state.system_context.personality,
            "facts_count": len(input_state.memory_input.facts),
            "episodes_count": len(input_state.memory_input.episodes)
        }
    
    def generate_test_summary(self) -> Dict[str, Any]:
        """生成测试总结"""
        return {
            "test_framework": "E-Mate强化学习核心功能测试",
            "test_categories": [
                "智能工作伙伴",
                "主动式时间管家", 
                "工作健康守护者",
                "学习效果验证"
            ],
            "evaluation_criteria": {
                "决策准确性": "评估AI在不同场景下选择合适动作的能力",
                "响应质量": "评估语音回应的相关性和有用性",
                "学习能力": "评估基于用户反馈的改进能力",
                "主动性": "评估主动感知和干预的能力"
            },
            "success_threshold": 0.7,
            "test_timestamp": datetime.now().isoformat()
        }


def run_rl_scenario_tests():
    """运行强化学习场景测试"""
    tester = RLScenarioTester()
    results = tester.run_all_scenario_tests()
    
    print("\n" + "="*70)
    print("📊 测试结果总结")
    print("="*70)
    
    for category, result in results.items():
        if category == "summary":
            continue
            
        print(f"\n🎯 {result['category']}")
        print(f"   总场景数: {result.get('total_scenarios', 'N/A')}")
        print(f"   通过场景: {result.get('passed_scenarios', 'N/A')}")
        print(f"   平均得分: {result.get('average_score', 0):.2f}")
        
        if result.get('average_score', 0) >= 0.7:
            print(f"   状态: ✅ 通过")
        else:
            print(f"   状态: ❌ 需要改进")
    
    return results


if __name__ == "__main__":
    results = run_rl_scenario_tests()
    
    # 保存测试结果
    with open("./data/rl_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
