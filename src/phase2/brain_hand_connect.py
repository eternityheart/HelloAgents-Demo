"""
Day 2.3 实验: 手脑连接验证 🧠⚡🤚

🧒 小学生讲解:
之前我们有了"大脑"(LLM)和"手"(高德API)。
今天我们要把它们连起来！
你说中文，大脑听懂后，自动指挥手去查数据，然后再告诉你结果。
这就是"Agent"的雏形！

🎓 面试话术:
"在基础设施搭建阶段，我实现了'手脑协同'验证。
通过 Prompt Engineering 描述工具能力（Weather/POI），
利用 LLM 的推理能力输出结构化指令（JSON），
动态调度高德地图的真实 Web API，实现了从自然语言到 API 调用的端到端链路。"
"""

import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# 设置代理（DeepSeek API 需要）
# 注意：高德 API 调用时我们会显式禁用代理
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"

# 加载环境变量
load_dotenv()


# ========================================
# Step 1: 基础设施配置
# ========================================
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
AMAP_API_KEY = os.getenv("AMAP_API_KEY")
BASE_URL = "https://api.deepseek.com"

if not DEEPSEEK_API_KEY or not AMAP_API_KEY:
    print("❌ 错误: 请检查 .env 文件，确保 DEEPSEEK_API_KEY 和 AMAP_API_KEY 都已配置")
    exit(1)

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL)

# 高德工具代码映射
CITY_CODES = {"北京": "110000", "上海": "310000", "广州": "440100", "深圳": "440300"}
POI_TYPES = {"景点": "110000", "餐厅": "050000", "酒店": "100000"}


# ========================================
# Step 2: 定义工具 (The "Hands")
# ========================================
def get_weather(city: str) -> dict:
    """真实调用高德天气 API"""
    city_code = CITY_CODES.get(city)
    if not city_code:
        return {"error": f"暂不支持城市: {city} (仅支持: 北京/上海/广州/深圳)"}
    
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    try:
        resp = requests.get(
            url, 
            params={"key": AMAP_API_KEY, "city": city_code, "extensions": "base"},
            proxies={"http": None, "https": None}
        )
        data = resp.json()
        if data["status"] == "1" and data["lives"]:
            live = data["lives"][0]
            return f"{city}天气: {live['weather']}, 温度: {live['temperature']}℃, 风力: {live['windpower']}级"
        return f"查询失败: {data}"
    except Exception as e:
        return f"API调用出错: {str(e)}"

def search_poi(city: str, keyword: str, poi_type: str = "景点") -> list:
    """真实调用高德 POI 搜索 API"""
    url = "https://restapi.amap.com/v3/place/text"
    type_code = POI_TYPES.get(poi_type, "110000") # 默认景点
    
    try:
        resp = requests.get(
            url,
            params={
                "key": AMAP_API_KEY,
                "city": city,
                "keywords": keyword,
                "types": type_code,
                "citylimit": "true",
                "offset": 3  # 只取前3个
            },
            proxies={"http": None, "https": None}
        )
        data = resp.json()
        if data["status"] == "1":
            results = []
            for poi in data.get("pois", []):
                results.append(f"{poi['name']} ({poi['address']})")
            return results if results else ["未找到相关地点"]
        return f"查询失败: {data}"
    except Exception as e:
        return f"API调用出错: {str(e)}"


# ========================================
# Step 3: 定义大脑 (The "Brain")
# ========================================
SYSTEM_PROMPT = """
你是 HelloAgents 的调度中枢。
你有两个强力工具：
1. get_weather(city): 查询天气。参数 city 必须是 北京/上海/广州/深圳 之一。
2. search_poi(city, keyword, poi_type): 搜索地点。poi_type 只能是 景点/餐厅/酒店。

用户输入被你接收后，请分析意图，返回 JSON 格式：
{
    "tool": "get_weather" 或 "search_poi",
    "args": { ...参数... },
    "thought": "你的思考过程"
}

如果无需调用工具，返回:
{
    "tool": "none",
    "response": "直接回复的内容"
}
"""

def brain_process(user_query: str):
    print(f"👤 用户: {user_query}")
    
    # 1. 思考 (Think)
    print("🧠 大脑正在思考...", end="", flush=True)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ],
        response_format={"type": "json_object"}
    )
    content = response.choices[0].message.content
    print("完成!")
    
    try:
        decision = json.loads(content)
        print(f"🤔 意图识别: {decision['thought']}")
        print(f"🛠️ 决定调用: {decision['tool']} 参数: {decision.get('args')}")
        
        # 2. 行动 (Act)
        result = "无结果"
        if decision["tool"] == "get_weather":
            args = decision["args"]
            result = get_weather(args["city"])
            
        elif decision["tool"] == "search_poi":
            args = decision["args"]
            result = search_poi(args["city"], args.get("keyword", ""), args.get("poi_type", "景点"))
            
        elif decision["tool"] == "none":
            print(f"🤖 回复: {decision.get('response')}")
            return

        print(f"✅ 真实API结果: {result}")
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ 大脑短路了: {e}")
        print(f"原始内容: {content}")


# ========================================
# Step 4: 运行测试
# ========================================
if __name__ == "__main__":
    print("=" * 60)
    print("🧠⚡🤚 手脑连接测试")
    print("注意: 确保你 .env 里配置了正确的 API KEY")
    print("=" * 60)
    
    # 测试 Case 1: 天气
    brain_process("帮我查查北京现在的天气")
    print()
    
    # 测试 Case 2: POI
    brain_process("上海有哪些好吃的必胜客？")
    print()
    
    # 测试 Case 3: 闲聊
    brain_process("你好，你叫什么名字？")
