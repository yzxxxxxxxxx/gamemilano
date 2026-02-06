"""
奖牌榜API路由
提供奖牌排行榜数据
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from supabase import create_client, Client
from datetime import datetime

from backend.config import SUPABASE_URL, SUPABASE_KEY
from backend.models import MedalResponse, ChinaMedalResponse, HistoricalEditionResponse, HistoricalMedalResponse, HistoricalEventResponse
from backend.scripts.sync_medals import get_iso

router = APIRouter(prefix="/api/medals", tags=["medals"])

def get_supabase() -> Client:
    """获取Supabase客户端"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


@router.get("", response_model=List[MedalResponse])
async def get_medals(
    region: Optional[str] = Query(None, description="按地区筛选: 欧洲/北美洲/亚洲"),
    search: Optional[str] = Query(None, description="搜索国家名称")
):
    """
    获取奖牌榜
    按金牌数排序，返回所有国家的奖牌数据
    """
    supabase = get_supabase()
    
    try:
        # 获取所有奖牌数据
        query = supabase.table("medals").select("*")
        
        # 搜索筛选
        if search:
            query = query.ilike("country", f"%{search}%")
        
        # 按金牌数排序
        query = query.order("gold", desc=True).order("silver", desc=True).order("bronze", desc=True)
        
        result = query.execute()
        medals = result.data
        
        # 地区筛选映射（简化实现）
        region_countries = {
            "欧洲": ["NO", "DE", "NL", "CH", "AT", "FR", "IT", "SE", "FI"],
            "北美洲": ["US", "CA"],
            "亚洲": ["CN", "JP", "KR"]
        }
        
        if region and region in region_countries:
            medals = [m for m in medals if m["iso"] in region_countries[region]]
        
        # 组装响应，添加排名
        response_medals = []
        for idx, medal in enumerate(medals, 1):
            response_medals.append(MedalResponse(
                id=medal["id"],
                rank=idx,
                country=medal["country"],
                iso=medal["iso"],
                gold=medal["gold"],
                silver=medal["silver"],
                bronze=medal["bronze"]
            ))
        
        return response_medals
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取奖牌榜失败: {str(e)}")


@router.get("/china", response_model=ChinaMedalResponse)
async def get_china_medals():
    """
    获取中国队奖牌数据
    用于首页快速展示
    """
    supabase = get_supabase()
    
    try:
        # 获取中国队数据
        result = supabase.table("medals").select("*").eq("iso", "CN").single().execute()
        china = result.data
        
        if not china:
            return ChinaMedalResponse(
                rank=0,
                gold=0,
                silver=0,
                bronze=0,
                total=0,
                updated_at=datetime.now()
            )
        
        # 计算排名
        all_medals = supabase.table("medals").select("iso, gold").order("gold", desc=True).execute()
        rank = 1
        for idx, m in enumerate(all_medals.data, 1):
            if m["iso"] == "CN":
                rank = idx
                break
        
        return ChinaMedalResponse(
            rank=rank,
            gold=china["gold"],
            silver=china["silver"],
            bronze=china["bronze"],
            total=china["gold"] + china["silver"] + china["bronze"],
            updated_at=china.get("updated_at", datetime.now())
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取中国队奖牌数据失败: {str(e)}")


@router.get("/history", response_model=List[HistoricalEditionResponse])
async def get_history_editions():
    """获取所有历史届次列表"""
    supabase = get_supabase()
    try:
        # 同时从两个表获取数据并进行合并
        # history_medals_duplicate 包含完整的届次列表（从1924年开始）
        # history_events 包含部分届次（1960年以后）的国家数和项目数
        
        # 1. 获取完整的届次基础信息
        medals_res = supabase.table("history_medals_duplicate").select("Year, City").order("Year", desc=True).execute()
        
        # 2. 获取统计数据
        events_res = supabase.table("history_events").select("year, countries_count, events_count").execute()
        
        # 创建统计数据的字典方便查找
        stats_map = {}
        # 创建统计数据的字典方便查找
        stats_map = {}
        for item in events_res.data:
            year = item["year"]
            if year not in stats_map or (item.get("countries_count") and not stats_map[year]["countries"]):
                stats_map[year] = {
                    "countries": item.get("countries_count", 0),
                    "events": item.get("events_count", 0)
                }
        
        # 补充一些核心年份的兜底数据（特别是北京2022）
        fallback_stats = {
            2022: {"countries": 91, "events": 109},
            2018: {"countries": 92, "events": 102},
            2014: {"countries": 88, "events": 98},
            2010: {"countries": 82, "events": 86},
            2006: {"countries": 80, "events": 84},
        }
        
        # 3. 去重合并
        seen = set()
        editions = []
        for item in medals_res.data:
            year = item["Year"]
            if year not in seen:
                # 优先使用数据库数据，如果没有则使用兜底数据
                db_stats = stats_map.get(year, {"countries": 0, "events": 0})
                fb_stats = fallback_stats.get(year, {"countries": 0, "events": 0})
                
                final_countries = db_stats["countries"] or fb_stats["countries"]
                final_events = db_stats["events"] or fb_stats["events"]
                
                editions.append(HistoricalEditionResponse(
                    year=year, 
                    location=item["City"],
                    countries_count=final_countries,
                    events_count=final_events
                ))
                seen.add(year)
        
        return editions
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取历史届次失败: {str(e)}")


@router.get("/history/{year}/events", response_model=List[HistoricalEventResponse])
async def get_history_events_by_year(year: int):
    """获取指定年份的历史赛事列表（含奖牌获得国）"""
    supabase = get_supabase()
    try:
        # 获取该年份的所有赛事
        result = supabase.table("history_events").select("*").eq("year", year).execute()
        
        if not result.data:
            return []
            
        return [
            HistoricalEventResponse(
                id=str(item["id"]),
                sport_name=item["sport_name"],
                event_name=item["event_name"],
                gold_country=item.get("gold_country"),
                gold_iso=get_iso(item["gold_country"]) if item.get("gold_country") else None,
                silver_country=item.get("silver_country"),
                silver_iso=get_iso(item["silver_country"]) if item.get("silver_country") else None,
                bronze_country=item.get("bronze_country"),
                bronze_iso=get_iso(item["bronze_country"]) if item.get("bronze_country") else None
            ) for item in result.data
        ]
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取历史赛事列表失败: {str(e)}")



@router.get("/history/{year}", response_model=List[HistoricalMedalResponse])
async def get_history_by_year(year: int):
    """获取指定年份的历史奖牌榜"""
    supabase = get_supabase()
    try:
        # 修正：根据截图列名为 Year, Rank, Country, gold, silver, bronze
        result = supabase.table("history_medals_duplicate")\
            .select("*")\
            .eq("Year", year)\
            .order("Rank", desc=False)\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail=f"未找到 {year} 年的数据")
            
        return [
            HistoricalMedalResponse(
                rank=m["Rank"],
                country=m["Country"],
                iso=get_iso(m["Country"]),  # 从国家名映射 ISO
                gold=m["gold"],
                silver=m["silver"],
                bronze=m["bronze"],
                total=m["gold"] + m["silver"] + m["bronze"]
            ) for m in result.data
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史奖牌榜失败: {str(e)}")

