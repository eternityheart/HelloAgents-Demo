"""
Phase 8.2: 行程数据模型
定义多日行程的结构化数据类型
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class POI(BaseModel):
    """兴趣点 (景点/餐厅/酒店)"""
    name: str = Field(description="地点名称")
    address: Optional[str] = Field(default=None, description="地址")
    rating: Optional[float] = Field(default=None, description="评分 (0-5)")
    duration: Optional[str] = Field(default=None, description="建议游玩时长")
    location: Optional[str] = Field(default=None, description="经纬度坐标")
    type: Optional[str] = Field(default=None, description="类型(景点/餐厅/酒店)")
    reason: Optional[str] = Field(default=None, description="推荐理由")


class DayPlan(BaseModel):
    """单日行程计划"""
    day: int = Field(description="第几天")
    date: Optional[str] = Field(default=None, description="日期 (YYYY-MM-DD)")
    weather: str = Field(default="未知", description="天气预报")
    weather_tip: Optional[str] = Field(default=None, description="天气提示")
    morning: List[POI] = Field(default_factory=list, description="上午活动")
    afternoon: List[POI] = Field(default_factory=list, description="下午活动")
    dinner: Optional[POI] = Field(default=None, description="晚餐推荐")
    hotel: Optional[POI] = Field(default=None, description="住宿推荐")


class Itinerary(BaseModel):
    """完整行程方案"""
    city: str = Field(description="目的地城市")
    days: int = Field(description="行程天数")
    preferences: List[str] = Field(default_factory=list, description="用户偏好标签")
    summary: Optional[str] = Field(default=None, description="行程概述")
    itinerary: List[DayPlan] = Field(default_factory=list, description="每日安排")
    tips: Optional[List[str]] = Field(default=None, description="旅行贴士")


class ItineraryRequest(BaseModel):
    """行程请求参数"""
    destination: str = Field(description="目的地")
    days: int = Field(default=3, ge=1, le=7, description="天数")
    preferences: List[str] = Field(default_factory=list, description="偏好")
    start_date: Optional[str] = Field(default=None, description="出发日期")
