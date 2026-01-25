"""
奖牌榜API路由
提供奖牌排行榜数据
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from supabase import create_client, Client
from datetime import datetime

from backend.config import SUPABASE_URL, SUPABASE_KEY
from backend.models import MedalResponse, ChinaMedalResponse

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
