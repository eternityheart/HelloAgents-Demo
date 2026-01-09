"""
Day 1 API Test - Non-interactive demo
"""
import os
import sys

# Add proxy support
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def test_api():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: DEEPSEEK_API_KEY not found")
        return
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    
    print("=" * 50)
    print("Testing DeepSeek API Connection...")
    print("=" * 50)
    print()
    print("Question: What are some fun places to visit in Beijing?")
    print()
    print("Agent Response:")
    print("-" * 40)
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful travel assistant. Reply in Chinese."},
            {"role": "user", "content": "What are some fun places to visit in Beijing? Keep it brief, 3 recommendations."}
        ],
        max_tokens=500
    )
    
    print(response.choices[0].message.content)
    print("-" * 40)
    print()
    print("API Test Successful!")

if __name__ == "__main__":
    test_api()
