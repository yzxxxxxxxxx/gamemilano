"""
Pydantic数据模型
定义API请求和响应的数据结构
"""
from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


# ========== 赛事相关模型 ==========

class EventBase(BaseModel):
    """赛事基础模型"""
    sport: Optional[str] = None
    discipline: Optional[str] = None
    title: str
    event_time: Optional[datetime] = None
    location: Optional[str] = None
    is_team_china: bool = False
    type: Optional[str] = "preliminary"


class EventCreate(EventBase):
    """创建赛事的请求模型"""
    pass


class EventResponse(EventBase):
    """赛事响应模型"""
    id: str
    reminded: bool = False  # 用户是否设置了提醒

    class Config:
        from_attributes = True


# ========== 奖牌相关模型 ==========

class MedalBase(BaseModel):
    """奖牌基础模型"""
    country: str
    iso: str
    gold: int = 0
    silver: int = 0
    bronze: int = 0


class MedalResponse(MedalBase):
    """奖牌榜响应模型"""
    id: str
    rank: int  # 排名（按金牌数计算）

    class Config:
        from_attributes = True


class ChinaMedalResponse(BaseModel):
    """中国队奖牌摘要响应"""
    rank: int
    gold: int
    silver: int
    bronze: int
    total: int
    updated_at: datetime


class HistoricalEditionResponse(BaseModel):
    """历史届次响应模型"""
    year: int
    location: str
    countries_count: Optional[int] = 0
    events_count: Optional[int] = 0


class HistoricalMedalResponse(BaseModel):
    """历史奖牌榜单项响应"""
    rank: int
    country: str
    iso: str
    gold: int
    silver: int
    bronze: int
    total: int


class HistoricalEventResponse(BaseModel):
    """历史赛事数据响应"""
    id: str
    sport_name: str
    event_name: str
    gold_country: Optional[str] = None
    gold_iso: Optional[str] = None
    silver_country: Optional[str] = None
    silver_iso: Optional[str] = None
    bronze_country: Optional[str] = None
    bronze_iso: Optional[str] = None


# ========== AI相关模型 ==========

class AIAthleteRequest(BaseModel):
    """AI运动员查询请求"""
    athlete_name: str


class AIEventRequest(BaseModel):
    """AI赛事预测请求"""
    event_title: str


class AIResponse(BaseModel):
    """AI响应模型"""
    success: bool
    message: str


# ========== 提醒相关模型 ==========

class ReminderCreate(BaseModel):
    """创建提醒请求"""
    event_id: str
    user_id: str = "default_user"  # 简化处理，使用默认用户


class ReminderResponse(BaseModel):
    """提醒响应"""
    id: str
    event_id: str
    user_id: str
