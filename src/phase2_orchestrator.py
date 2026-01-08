"""
Phase 2: Orchestrator - 大脑构建（意图提取与任务分解）

🧒 小学生讲解:
你是旅行社老板，来了一个客户说：
"我想去北京玩3天，喜欢历史文化"

坏员工（直接干活型）：马上开始编行程，可能漏掉很多细节
好员工（先规划型）：先分解任务
  → 目的地：北京
  → 天数：3天  
  → 偏好：历史、文化
  → 待办：查景点、查天气、规划路线

这个"好员工"就是 Orchestrator（编排者/大脑）

学习目标:
1. 理解Orchestrator在多Agent系统中的角色
2. 学会用Prompt让LLM输出结构化JSON
3. 掌握Pydantic数据校验

🎓 面试话术:
"Orchestrator负责将模糊的用户需求分解为结构化的子任务。
我使用Pydantic进行强类型校验，确保LLM输出符合后续流程的Schema要求。
这是'意图提取'（Intent Extraction）的标准实现。"
"""

from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
import json
import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()


# ===== Step 1: 定义数据结构 =====

class TravelPreference(str, Enum):
    """旅行偏好枚举"""
    HISTORY = "历史"
    CULTURE = "文化"
    NATURE = "自然"
    FOOD = "美食"
    SHOPPING = "购物"
    RELAXATION = "休闲"
    ADVENTURE = "冒险"
    FAMILY = "亲子"


class ActionType(str, Enum):
    """子任务类型枚举"""
    SEARCH_ATTRACTIONS = "查景点"
    CHECK_WEATHER = "查天气"
    SEARCH_HOTELS = "查酒店"
    SEARCH_RESTAURANTS = "查餐厅"
    PLAN_ROUTE = "规划路线"
    ESTIMATE_BUDGET = "估算预算"


class TravelIntent(BaseModel):
    """
    旅行意图的结构化表示
    
    🧒 小学生讲解:
    这就像一个"订单表格"，规定了必填项和选填项
    """
    destination: str = Field(
        description="目的地城市名称",
        examples=["北京", "上海", "成都"]
    )
    
    days: int = Field(
        ge=1, le=30,  # 大于等于1，小于等于30
        description="旅行天数"
    )
    
    preferences: List[str] = Field(
        default=[],
        description="旅行偏好标签"
    )
    
    budget_level: Optional[str] = Field(
        default="中等",
        description="预算级别：低、中等、高"
    )
    
    travelers: Optional[int] = Field(
        default=1, ge=1,
        description="出行人数"
    )
    
    special_requirements: Optional[str] = Field(
        default=None,
        description="特殊需求，如'带老人'、'有小孩'"
    )
    
    needed_actions: List[str] = Field(
        description="需要执行的子任务列表"
    )


# ===== Step 2: Orchestrator Agent =====

class OrchestratorAgent:
    """
    编排者Agent - 负责理解用户意图并分解任务
    
    🧒 工作流程:
    用户需求（模糊） → Orchestrator分析 → 结构化JSON（清晰）
    """
    
    # 系统提示词
    SYSTEM_PROMPT = """你是一个旅行规划系统的"大脑"（Orchestrator）。

你的任务是：分析用户的旅行需求，提取关键信息，输出结构化的JSON。

## 输出格式要求：
必须输出以下JSON结构，不要有任何额外文字：
{
  "destination": "城市名",
  "days": 天数(整数),
  "preferences": ["偏好1", "偏好2"],
  "budget_level": "低/中等/高",
  "travelers": 人数(整数),
  "special_requirements": "特殊需求或null",
  "needed_actions": ["查景点", "查天气", ...]
}

## 可用的偏好标签：
历史、文化、自然、美食、购物、休闲、冒险、亲子

## 可用的子任务：
查景点、查天气、查酒店、查餐厅、规划路线、估算预算

## 重要规则：
1. destination 必须是具体的中国城市名
2. days 必须是1-30之间的整数
3. needed_actions 根据用户需求智能决定，至少包含"查景点"
4. 如果用户没说预算，默认"中等"
5. 如果用户没说人数，默认1人

## 示例输入：
"我想去北京玩3天，喜欢历史文化，预算有限"

## 示例输出：
{
  "destination": "北京",
  "days": 3,
  "preferences": ["历史", "文化"],
  "budget_level": "低",
  "travelers": 1,
  "special_requirements": null,
  "needed_actions": ["查景点", "查天气", "规划路线"]
}"""

    def __init__(self):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("请配置 DEEPSEEK_API_KEY 环境变量")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        )
        self.model = os.getenv("DEFAULT_MODEL", "deepseek-chat")
    
    def extract_intent(self, user_request: str) -> TravelIntent:
        """
        从用户请求中提取旅行意图
        
        Args:
            user_request: 用户的自然语言请求
            
        Returns:
            TravelIntent: 结构化的旅行意图对象
            
        Raises:
            ValidationError: 如果LLM输出不符合Schema
        """
        print(f"\n🧠 Orchestrator 分析中...")
        print(f"   用户输入: {user_request}")
        
        # 调用LLM提取意图
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_request}
            ],
            # 强制JSON输出（如果模型支持）
            response_format={"type": "json_object"}
        )
        
        json_str = response.choices[0].message.content
        print(f"   LLM原始输出: {json_str[:200]}...")
        
        # 使用Pydantic验证和解析
        try:
            intent = TravelIntent.model_validate_json(json_str)
            print(f"   ✅ 意图提取成功!")
            return intent
        except ValidationError as e:
            print(f"   ❌ 数据校验失败: {e}")
            raise
    
    def visualize_intent(self, intent: TravelIntent) -> str:
        """可视化显示提取的意图"""
        result = []
        result.append("┌" + "─" * 40 + "┐")
        result.append("│ 📋 旅行意图分析结果                    │")
        result.append("├" + "─" * 40 + "┤")
        result.append(f"│ 🏙️  目的地: {intent.destination:<27}│")
        result.append(f"│ 📅 天数: {intent.days}天{' ' * 28}│"[:43] + "│")
        result.append(f"│ 👥 人数: {intent.travelers}人{' ' * 28}│"[:43] + "│")
        result.append(f"│ 💰 预算: {intent.budget_level:<28}│")
        result.append(f"│ 🏷️  偏好: {', '.join(intent.preferences):<27}│"[:43] + "│")
        if intent.special_requirements:
            result.append(f"│ ⚠️  特殊: {intent.special_requirements:<27}│"[:43] + "│")
        result.append("├" + "─" * 40 + "┤")
        result.append("│ 📝 待执行任务:                          │")
        for action in intent.needed_actions:
            result.append(f"│   • {action:<35}│")
        result.append("└" + "─" * 40 + "┘")
        return "\n".join(result)


# ===== 测试代码 =====

def main():
    """交互式测试"""
    print("=" * 60)
    print("🧠 Phase 2: Orchestrator Agent (大脑)")
    print("=" * 60)
    print("我会分析你的旅行需求，提取结构化信息")
    print("试着输入:")
    print("  - 我想去北京玩3天，喜欢历史")
    print("  - 上海2日游，带小孩，预算高")
    print("  - 成都5天美食之旅")
    print("输入 'quit' 退出\n")
    
    orchestrator = OrchestratorAgent()
    
    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 再见!")
            break
        if not user_input:
            continue
        
        try:
            intent = orchestrator.extract_intent(user_input)
            print(orchestrator.visualize_intent(intent))
            
            # 也输出原始JSON方便调试
            print("\n📦 JSON格式:")
            print(intent.model_dump_json(indent=2, ensure_ascii=False))
        except ValidationError as e:
            print(f"\n❌ 解析失败,请重新描述你的需求: {e}")


def test_orchestrator():
    """
    验收测试
    
    ✅ 验收标准:
    1. 所有测试用例能成功提取意图
    2. destination是有效城市名
    3. days是合理数字
    4. needed_actions不为空
    """
    print("\n📋 开始 Orchestrator 验收测试...\n")
    
    try:
        orchestrator = OrchestratorAgent()
    except ValueError as e:
        print(f"⚠️ 跳过测试: {e}")
        return
    
    test_cases = [
        "我想去北京玩3天，喜欢历史文化",
        "上海2日游，要吃好吃的",
        "成都5天，带小孩，要轻松点，预算充足",
        "西安历史之旅，4天"
    ]
    
    passed = 0
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"测试 {i}/{len(test_cases)}: {case}")
        print("-" * 50)
        
        try:
            intent = orchestrator.extract_intent(case)
            print(orchestrator.visualize_intent(intent))
            
            # 验证关键字段
            assert intent.destination, "destination不能为空"
            assert 1 <= intent.days <= 30, "days必须在1-30之间"
            assert len(intent.needed_actions) > 0, "needed_actions不能为空"
            
            print(f"\n✅ 测试通过")
            passed += 1
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 测试结果: {passed}/{len(test_cases)} 通过")
    print("=" * 50)


if __name__ == "__main__":
    import sys
    
    if "--test" in sys.argv:
        test_orchestrator()
    else:
        main()
