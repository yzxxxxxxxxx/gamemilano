"""
赛事API路由
提供赛事列表、精选赛事等接口
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, date
from supabase import create_client, Client

from backend.config import SUPABASE_URL, SUPABASE_KEY
from backend.models import EventResponse, EventCreate

router = APIRouter(prefix="/api/events", tags=["events"])

def get_supabase() -> Client:
    """获取Supabase客户端"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


@router.get("", response_model=List[EventResponse])
async def get_events(
    event_date: Optional[date] = Query(None, description="筛选指定日期的赛事"),
    team_china_only: bool = Query(False, description="仅显示中国队参赛项目"),
    user_id: str = Query("default_user", description="用户ID，用于获取提醒状态")
):
    """
    获取赛事列表
    支持按日期和中国队筛选
    """
    supabase = get_supabase()
    
    try:
        # 构建查询
        query = supabase.table("events").select("*")
        
        # 按日期筛选
        if event_date:
            start_of_day = datetime.combine(event_date, datetime.min.time())
            end_of_day = datetime.combine(event_date, datetime.max.time())
            query = query.gte("event_time", start_of_day.isoformat())
            query = query.lte("event_time", end_of_day.isoformat())
        
        # 中国队筛选
        if team_china_only:
            query = query.eq("is_team_china", True)
        
        # 按时间排序
        query = query.order("event_time", desc=False)
        
        result = query.execute()
        events = result.data
        
        # 如果数据库为空，返回示例数据
        if not events:
            print("数据库为空，返回示例数据")
            events = [
                {
                    "id": "sample-1",
                    "sport": "自由式滑雪",
                    "discipline": "女子大跳台",
                    "title": "自由式滑雪：女子大跳台决赛",
                    "event_time": "2026-02-06T16:00:00Z",
                    "location": "科尔蒂纳公园",
                    "is_team_china": True,
                    "type": "final"
                },
                {
                    "id": "sample-2",
                    "sport": "花样滑冰",
                    "discipline": "双人滑",
                    "title": "花样滑冰：双人滑短节目",
                    "event_time": "2026-02-06T14:30:00Z",
                    "location": "米兰冰上竞技场",
                    "is_team_china": True,
                    "type": "preliminary"
                },
                {
                    "id": "sample-3",
                    "sport": "短道速滑",
                    "discipline": "短道速滑",
                    "title": "短道速滑：男子1500米决赛",
                    "event_time": "2026-02-07T10:00:00Z",
                    "location": "米兰冰上竞技场",
                    "is_team_china": True,
                    "type": "final"
                },
                {
                    "id": "sample-4",
                    "sport": "冰球",
                    "discipline": "男子冰球",
                    "title": "男子冰球：小组赛 - 加拿大 vs 芬兰",
                    "event_time": "2026-02-06T12:00:00Z",
                    "location": "米兰体育馆",
                    "is_team_china": False,
                    "type": "preliminary"
                },
                {
                    "id": "sample-5",
                    "sport": "速度滑冰",
                    "discipline": "速度滑冰",
                    "title": "速度滑冰：女子3000米决赛",
                    "event_time": "2026-02-08T11:00:00Z",
                    "location": "米兰奥林匹克椭圆形体育场",
                    "is_team_china": False,
                    "type": "final"
                }
            ]
        
        # 获取用户提醒状态
        reminders_result = supabase.table("user_reminders").select("event_id").eq("user_id", user_id).execute()
        reminded_event_ids = {r["event_id"] for r in reminders_result.data}
        
        # 组装响应
        response_events = []
        for event in events:
            response_events.append(EventResponse(
                id=event["id"],
                sport=event["sport"],
                discipline=event["discipline"],
                title=event["title"],
                event_time=event["event_time"],
                location=event["location"],
                is_team_china=event["is_team_china"],
                type=event["type"],
                reminded=event["id"] in reminded_event_ids
            ))
        
        return response_events
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取赛事失败: {str(e)}")


@router.get("/featured", response_model=List[EventResponse])
@router.get("/featured", response_model=List[EventResponse])
async def get_featured_events(
    limit: int = Query(5, description="返回数量限制"),
    date: Optional[date] = Query(None, description="筛选指定日期的赛事"),
    user_id: str = Query("default_user", description="用户ID")
):
    """
    获取精选赛事
    逻辑：
    1. 必须是未来的比赛 (event_time >= now) [如果指定了日期，则为该日期内的比赛]
    2. 严格筛选：中国队参加 (is_team_china=true) 或 决赛 (type='final' / title contain '决赛'/'金牌')
    """
    supabase = get_supabase()
    
    try:
        current_time = datetime.now().isoformat()
        
        # 构建查询
        query = supabase.table("events").select("*")
        
        # 时间筛选
        if date:
            start_of_day = datetime.combine(date, datetime.min.time())
            end_of_day = datetime.combine(date, datetime.max.time())
            query = query.gte("event_time", start_of_day.isoformat())
            query = query.lte("event_time", end_of_day.isoformat())
        else:
            # 默认为当前时间之后的未来赛事
            query = query.gte("event_time", current_time)
            
        result_limit = limit if limit > 0 else 100
        
        # 辅助函数：添加时间筛选
        def apply_time_filter(qry):
            if date:
                start = datetime.combine(date, datetime.min.time()).isoformat()
                end = datetime.combine(date, datetime.max.time()).isoformat()
                return qry.gte("event_time", start).lte("event_time", end)
            else:
                return qry.gte("event_time", current_time)

        # 1. 首先获取中国队参加的赛事
        query_china = supabase.table("events").select("*")
        query_china = apply_time_filter(query_china)
        query_china = query_china.eq("is_team_china", True).order("event_time").limit(result_limit)
        
        result_china = query_china.execute()
        china_events = result_china.data
        
        featured_events = list(china_events)
        existing_ids = {e["id"] for e in featured_events}
        
        # 2. 如果数量不够（或者指定了日期），补充决赛/金牌赛
        # 如果指定了日期，我们希望尽可能多地展示当天的重点比赛，而不仅仅是填满limit
        should_fetch_more = len(featured_events) < result_limit or date is not None
        
        if should_fetch_more:
            needed = result_limit - len(featured_events)
            if date: needed = 100 # 如果是日期筛选，多取一些
            
            # 尝试获取 title 包含 "决赛" 或 "金牌" 的赛事
            query_finals = supabase.table("events").select("*")
            query_finals = apply_time_filter(query_finals)
            
            # 使用简单的 ilike 逐个尝试 (Supabase SDK or_ 语法有时不稳定)
            # 这里我们只查 title 包含 决赛 的，简单点
            query_finals = query_finals.ilike("title", "%决赛%").order("event_time").limit(needed * 2)
            
            result_finals = query_finals.execute()
            
            for event in result_finals.data:
                if event["id"] not in existing_ids:
                    featured_events.append(event)
                    existing_ids.add(event["id"])
                    if len(featured_events) >= result_limit and not date:
                        break
        
        # 3. 如果还是不够（且没有指定日期，或者指定了日期但没数据），就补充任意赛事
        # 对于指定日期的情况，如果上面没数据，为了不显示空白，也显示当天的普通比赛
        if len(featured_events) == 0 or (not date and len(featured_events) < result_limit):
             needed = result_limit - len(featured_events)
             if date: needed = 100
             
             query_nav = supabase.table("events").select("*")
             query_nav = apply_time_filter(query_nav)
             query_nav = query_nav.order("event_time").limit(needed)
             
             result_nav = query_nav.execute()
             
             for event in result_nav.data:
                if event["id"] not in existing_ids:
                    featured_events.append(event)
                    existing_ids.add(event["id"])
                    if len(featured_events) >= result_limit and not date:
                        break
                        
        # 再次按时间排序
        featured_events.sort(key=lambda x: x["event_time"] or "")
        
        # 获取用户提醒状态
        reminders_result = supabase.table("user_reminders").select("event_id").eq("user_id", user_id).execute()
        reminded_event_ids = {r["event_id"] for r in reminders_result.data}
        
        response_events = []
        for event in featured_events:
            response_events.append(EventResponse(
                id=event["id"],
                sport=event["sport"],
                discipline=event["discipline"],
                title=event["title"],
                event_time=event["event_time"],
                location=event["location"],
                is_team_china=event["is_team_china"],
                type=event["type"],
                reminded=event["id"] in reminded_event_ids
            ))
        
        return response_events
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取精选赛事失败: {str(e)}")
