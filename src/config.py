"""
配置管理模块

🧒 小学生讲解:
这个文件就像一个"设置中心"，把所有需要配置的东西集中管理。
比如API密钥、模型名称等，都从环境变量读取，不硬编码在代码里。

🎓 面试话术:
"我使用Pydantic Settings进行配置管理，支持环境变量和.env文件，
符合12-Factor App的配置外部化原则。"
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置类 - 所有配置项都在这里定义"""
    
    # ===== LLM配置 =====
    deepseek_api_key: str = Field(
        default="",
        description="DeepSeek API密钥"
    )
    deepseek_base_url: str = Field(
        default="https://api.deepseek.com",
        description="DeepSeek API基础URL"
    )
    openai_api_key: str = Field(
        default="",
        description="OpenAI API密钥(备选)"
    )
    default_model: str = Field(
        default="deepseek-chat",
        description="默认使用的LLM模型"
    )
    
    # ===== 高德地图配置 =====
    amap_api_key: str = Field(
        default="",
        description="高德地图Web服务API密钥"
    )
    
    # ===== 应用配置 =====
    log_level: str = Field(
        default="INFO",
        description="日志级别"
    )
    api_port: int = Field(
        default=8000,
        description="API服务端口"
    )
    
    class Config:
        # 从.env文件加载配置
        env_file = ".env"
        env_file_encoding = "utf-8"
        # 环境变量名不区分大小写
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    获取配置单例
    
    使用lru_cache确保整个应用只创建一次Settings实例，
    避免重复读取环境变量。
    """
    return Settings()


# 快捷访问
settings = get_settings()


# ===== 测试代码 =====
if __name__ == "__main__":
    from rich import print as rprint
    
    rprint("[bold green]当前配置:[/bold green]")
    rprint(f"  DeepSeek API Key: {'已配置' if settings.deepseek_api_key else '❌ 未配置'}")
    rprint(f"  高德地图 API Key: {'已配置' if settings.amap_api_key else '❌ 未配置'}")
    rprint(f"  默认模型: {settings.default_model}")
    rprint(f"  日志级别: {settings.log_level}")
    rprint(f"  API端口: {settings.api_port}")
