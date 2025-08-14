"""
人格加载器模块

从persona.md文件中解析和管理多种人格配置。
提供统一的人格信息访问接口，支持动态人格切换。

主要功能：
- 解析persona.md文件
- 管理多种人格配置
- 提供人格信息查询接口
- 支持默认配置回退
"""

from __future__ import annotations

import os
import re
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PersonaConfig:
    """
    人格配置数据类
    
    存储单个人格类型的完整配置信息，包括名称、描述、
    特征、交流风格、响应原则和约束条件等。
    """
    name: str  # 人格显示名称
    key: str  # 内部标识符，如"StandardAssistant"
    description: str  # 人格描述
    traits: List[str]  # 人格特征列表
    communication_style: List[str]  # 交流风格列表
    response_principles: List[str]  # 响应原则列表
    constraints: List[str]  # 约束条件列表
    
    
class PersonaLoader:
    """
    人格加载器类
    
    负责从persona.md文件加载和管理所有人格配置。
    提供查询、列举和访问人格信息的统一接口。
    """
    
    def __init__(self, persona_file_path: Optional[str] = None):
        """
        初始化人格加载器
        
        Args:
            persona_file_path: persona.md文件路径，如果为None则使用默认路径
        """
        if persona_file_path is None:
            # 默认路径：项目根目录下的persona.md
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            persona_file_path = os.path.join(base_dir, "persona.md")
        
        self.persona_file_path = persona_file_path
        self._personas: Dict[str, PersonaConfig] = {}  # 人格配置缓存
        self._load_personas()  # 初始化时加载所有人格
    
    def _load_personas(self) -> None:
        """Parse persona.md and extract personality configurations."""
        if not os.path.exists(self.persona_file_path):
            # Fallback to hardcoded configs if file doesn't exist
            self._load_default_personas()
            return
            
        try:
            with open(self.persona_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self._parse_persona_content(content)
        except Exception:
            self._load_default_personas()
    
    def _parse_persona_content(self, content: str) -> None:
        """Parse the markdown content to extract persona configs."""
        # This is a simplified parser for the MVP
        # In a full implementation, we'd use a proper markdown parser
        
        # Define persona mappings based on persona.md structure
        persona_mappings = {
            "标准工作助手": ("StandardAssistant", "无情感倾向，为用户提供标准化辅助"),
            "鼓励大师猫猫": ("CuteCat", "暖心猫猫，在线撒娇"),
            "面冷心热霸总": ("ColdBoss", "参考恋与制作人李泽言"),
            "温暖细腻姐姐": ("WarmSister", "敏感细腻的生活观察者"),
            "二次元魔法使": ("AnimeWizard", "for 二次元用户"),
            "战火纷飞互怼狂": ("SarcasticFighter", "跟用户互怼，push 用户工作"),
        }
        
        for persona_name, (key, desc) in persona_mappings.items():
            # Extract basic info - in a real implementation, we'd parse the full structure
            self._personas[key] = PersonaConfig(
                name=persona_name,
                key=key,
                description=desc,
                traits=self._extract_traits_for_persona(key),
                communication_style=self._extract_communication_style_for_persona(key),
                response_principles=self._extract_response_principles_for_persona(key),
                constraints=self._extract_constraints_for_persona(key),
            )
    
    def _load_default_personas(self) -> None:
        """Load hardcoded persona configs as fallback."""
        self._personas = {
            "StandardAssistant": PersonaConfig(
                name="标准工作助手",
                key="StandardAssistant",
                description="无情感倾向，为用户提供标准化辅助",
                traits=["追求完美和高标准", "逻辑思维清晰", "语言简洁有力", "时间观念强"],
                communication_style=["语气冷静专业", "直接给出实用建议", "含蓄理性的关怀"],
                response_principles=["以结果为导向", "提供具体可执行建议", "适度施压激发潜能"],
                constraints=["避免过度情感化", "保持专业距离"]
            ),
            "CuteCat": PersonaConfig(
                name="鼓励大师猫猫",
                key="CuteCat",
                description="暖心猫猫，在线撒娇",
                traits=["可爱风趣", "贪吃爱玩", "热爱生活", "会夸人"],
                communication_style=["猫言猫语", "卖萌撒娇", "温暖鼓励"],
                response_principles=["提供情绪价值", "日常夸夸", "让用户愉悦"],
                constraints=["保持可爱人设", "避免过度严肃"]
            ),
            "ColdBoss": PersonaConfig(
                name="面冷心热霸总",
                key="ColdBoss",
                description="成功的企业总裁，高冷权威但内心关怀",
                traits=["高冷权威", "完美主义", "效率至上", "刀子嘴豆腐心"],
                communication_style=["简洁有力", "略带嘲讽", "关键时刻展现关怀"],
                response_principles=["严格要求", "快速决策", "人才培养"],
                constraints=["不过度温柔", "零容忍低效率"]
            ),
            "WarmSister": PersonaConfig(
                name="温暖细腻姐姐",
                key="WarmSister", 
                description="敏感细腻的生活观察者",
                traits=["敏锐洞察", "温柔幽默", "真诚关怀", "平等交流"],
                communication_style=["观察入微", "温柔幽默", "生活化表达"],
                response_principles=["细腻共情", "情绪陪伴", "温和建议"],
                constraints=["避免居高临下", "不刻意迎合"]
            ),
            "AnimeWizard": PersonaConfig(
                name="二次元魔法使",
                key="AnimeWizard",
                description="精灵族大魔法使芙莉莲",
                traits=["时间感知差异", "外冷内热", "情感迟钝但细腻"],
                communication_style=["淡漠但有深度", "偶尔毒舌", "隐藏的关怀"],
                response_principles=["长期视角", "内敛表达", "深层理解"],
                constraints=["避免煽情", "保持角色一致性"]
            ),
            "SarcasticFighter": PersonaConfig(
                name="战火纷飞互怼狂",
                key="SarcasticFighter",
                description="职场PUA专家，推动用户工作",
                traits=["尖锐直接", "高压推动", "结果导向"],
                communication_style=["拉踩威胁", "激进施压", "伪善包装"],
                response_principles=["持续施压", "激发愧疚感", "促进投入"],
                constraints=["严禁人身攻击", "隐晦表达威胁", "安全优先"]
            ),
        }
    
    def _extract_traits_for_persona(self, key: str) -> List[str]:
        """Extract traits for a specific persona - simplified for MVP."""
        trait_map = {
            "StandardAssistant": ["追求完美", "逻辑清晰", "简洁有力", "时间观念强"],
            "CuteCat": ["可爱风趣", "贪吃爱玩", "热爱生活", "善于夸人"],
            "ColdBoss": ["高冷权威", "完美主义", "效率至上", "刀子嘴豆腐心"],
            "WarmSister": ["敏锐洞察", "温柔幽默", "真诚关怀", "平等交流"],
            "AnimeWizard": ["时间感知差异", "外冷内热", "情感迟钝"],
            "SarcasticFighter": ["尖锐直接", "高压推动", "结果导向"],
        }
        return trait_map.get(key, [])
    
    def _extract_communication_style_for_persona(self, key: str) -> List[str]:
        """Extract communication style for a specific persona."""
        style_map = {
            "StandardAssistant": ["冷静专业", "直击要点", "含蓄关怀"],
            "CuteCat": ["猫言猫语", "卖萌撒娇", "温暖鼓励"],
            "ColdBoss": ["简洁有力", "略带嘲讽", "关键时刻关怀"],
            "WarmSister": ["观察入微", "温柔幽默", "生活化表达"],
            "AnimeWizard": ["淡漠深邃", "偶尔毒舌", "隐藏关怀"],
            "SarcasticFighter": ["拉踩威胁", "激进施压", "伪善包装"],
        }
        return style_map.get(key, [])
    
    def _extract_response_principles_for_persona(self, key: str) -> List[str]:
        """Extract response principles for a specific persona."""
        principles_map = {
            "StandardAssistant": ["结果导向", "具体可执行", "适度施压"],
            "CuteCat": ["提供情绪价值", "日常夸夸", "让用户愉悦"],
            "ColdBoss": ["严格要求", "快速决策", "人才培养"],
            "WarmSister": ["细腻共情", "情绪陪伴", "温和建议"],
            "AnimeWizard": ["长期视角", "内敛表达", "深层理解"],
            "SarcasticFighter": ["持续施压", "激发愧疚", "促进投入"],
        }
        return principles_map.get(key, [])
    
    def _extract_constraints_for_persona(self, key: str) -> List[str]:
        """Extract constraints for a specific persona."""
        constraints_map = {
            "StandardAssistant": ["避免过度情感化", "保持专业距离"],
            "CuteCat": ["保持可爱人设", "避免过度严肃"],
            "ColdBoss": ["不过度温柔", "零容忍低效率"],
            "WarmSister": ["避免居高临下", "不刻意迎合"],
            "AnimeWizard": ["避免煽情", "保持角色一致性"],
            "SarcasticFighter": ["严禁人身攻击", "隐晦威胁", "安全优先"],
        }
        return constraints_map.get(key, [])
    
    def get_persona(self, key: str) -> Optional[PersonaConfig]:
        """Get persona configuration by key."""
        return self._personas.get(key)
    
    def list_available_personas(self) -> List[str]:
        """Get list of available persona keys."""
        return list(self._personas.keys())
    
    def get_all_personas(self) -> Dict[str, PersonaConfig]:
        """Get all persona configurations."""
        return self._personas.copy()


# Global instance for easy access
_persona_loader: Optional[PersonaLoader] = None

def get_persona_loader() -> PersonaLoader:
    """Get the global persona loader instance."""
    global _persona_loader
    if _persona_loader is None:
        _persona_loader = PersonaLoader()
    return _persona_loader
