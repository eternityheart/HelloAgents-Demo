"""
Day 1.3 实验: HelloAgents 架构演示

🧒 小学生讲解:
这个代码展示了我们选择的 Orchestrator-Workers 模式：
1. Orchestrator (大脑) - 理解用户意图，决定调用哪个专家
2. Workers (手脚) - 专家各自执行任务，汇报结果

🎓 面试话术:
"我们采用 Orchestrator-Workers 模式，中央调度器负责意图理解和任务编排，
Workers 专注单一职责。这种设计既有中心控制的可靠性，又有专家分工的灵活性。"
"""

import os
import json

os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# ========================================
# Step 1: 定义 Workers (专家)
# ========================================

class ScoutWorker:
    """景点专员 - 负责查询景点信息"""
    
    name = "Scout"
    description = "景点专员，负责查询旅游景点"
    
    def execute(self, city: str) -> str:
        print(f"  🔍 [Scout] 正在查询 {city} 的景点...")
        # 模拟数据（后续会换成真实API）
        spots = {
            "北京": ["故宫", "长城", "颐和园", "天坛"],
            "上海": ["外滩", "东方明珠", "豫园", "迪士尼"],
            "广州": ["广州塔", "陈家祠", "白云山", "沙面"]
        }
        result = spots.get(city, [f"{city}暂无数据"])
        print(f"  ✅ [Scout] 找到 {len(result)} 个景点")
        return f"{city}推荐景点: {', '.join(result)}"


class MeteorologistWorker:
    """天气专员 - 负责查询天气信息"""
    
    name = "Meteorologist"
    description = "天气专员，负责查询天气预报"
    
    def execute(self, city: str) -> str:
        print(f"  🌤️ [Meteorologist] 正在查询 {city} 的天气...")
        weather = {
            "北京": "晴天，-2°C ~ 8°C，适合户外活动",
            "上海": "多云，5°C ~ 12°C，记得带伞",
            "广州": "小雨，15°C ~ 22°C，穿轻薄外套"
        }
        result = weather.get(city, f"{city}天气数据暂无")
        print(f"  ✅ [Meteorologist] 天气查询完成")
        return result


# ========================================
# Step 2: 定义 Orchestrator (大脑)
# ========================================

class Orchestrator:
    """
    中央调度器 - 理解意图，分配任务
    
    这就是 HelloAgents 的核心：
    1. 接收用户请求
    2. 分析意图
    3. 调用合适的 Worker
    4. 汇总结果
    """
    
    def __init__(self):
        self.workers = {
            "scout": ScoutWorker(),
            "meteorologist": MeteorologistWorker()
        }
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
    
    def analyze_intent(self, user_query: str) -> dict:
        """用 LLM 分析用户意图"""
        
        print(f"\n🧠 [Orchestrator] 分析用户意图...")
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": """你是一个意图分析器。根据用户输入，判断需要哪些专家。
返回 JSON 格式，包含:
- city: 城市名
- needs_spots: 是否需要景点 (true/false)
- needs_weather: 是否需要天气 (true/false)

只返回 JSON，不要其他内容。"""
                },
                {"role": "user", "content": user_query}
            ],
            response_format={"type": "json_object"}
        )
        
        intent = json.loads(response.choices[0].message.content)
        print(f"  📋 意图解析: {intent}")
        return intent
    
    def plan(self, user_query: str) -> str:
        """执行规划"""
        
        print("=" * 50)
        print(f"👤 用户请求: {user_query}")
        print("=" * 50)
        
        # Step 1: 分析意图
        intent = self.analyze_intent(user_query)
        city = intent.get("city", "未知")
        
        # Step 2: 分配任务给 Workers
        results = []
        
        if intent.get("needs_spots"):
            print(f"\n📌 [Orchestrator] 派遣 Scout 查询景点...")
            result = self.workers["scout"].execute(city)
            results.append(result)
        
        if intent.get("needs_weather"):
            print(f"\n📌 [Orchestrator] 派遣 Meteorologist 查询天气...")
            result = self.workers["meteorologist"].execute(city)
            results.append(result)
        
        # Step 3: 汇总结果
        print(f"\n📊 [Orchestrator] 汇总 {len(results)} 个结果...")
        
        final_response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个旅行助手，根据收集到的信息给用户一个简洁的回答。"
                },
                {
                    "role": "user",
                    "content": f"用户问: {user_query}\n\n收集到的信息:\n" + "\n".join(results)
                }
            ]
        )
        
        answer = final_response.choices[0].message.content
        
        print("=" * 50)
        print(f"🤖 最终回答:\n{answer}")
        print("=" * 50)
        
        return answer


# ========================================
# Step 3: 测试
# ========================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 HelloAgents Orchestrator-Workers 演示")
    print("=" * 60)
    
    orchestrator = Orchestrator()
    
    # 测试 1: 只问景点
    print("\n" + "=" * 60)
    print("测试 1: 只问景点")
    print("=" * 60)
    orchestrator.plan("北京有什么好玩的地方？")
    
    # 测试 2: 只问天气
    print("\n" + "=" * 60)
    print("测试 2: 只问天气")
    print("=" * 60)
    orchestrator.plan("上海今天天气怎么样？")
    
    # 测试 3: 综合查询
    print("\n" + "=" * 60)
    print("测试 3: 综合查询（景点+天气）")
    print("=" * 60)
    orchestrator.plan("我想去广州玩，帮我看看有什么景点，天气怎么样？")
    
    print("\n" + "=" * 60)
    print("🎉 演示完成!")
    print("=" * 60)
