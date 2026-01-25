"""
提醒API路由
管理用户的赛事提醒设置
"""
from fastapi import APIRouter, HTTPException
from supabase import create_client, Client

from backend.config import SUPABASE_URL, SUPABASE_KEY
from backend.models import ReminderCreate, ReminderResponse

router = APIRouter(prefix="/api/reminders", tags=["reminders"])

def get_supabase() -> Client:
    """获取Supabase客户端"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


@router.post("", response_model=ReminderResponse)
async def create_reminder(request: ReminderCreate):
    """
    添加赛事提醒
    """
    supabase = get_supabase()
    
    try:
        # 检查是否已存在提醒
        existing = supabase.table("user_reminders").select("id").eq(
            "user_id", request.user_id
        ).eq("event_id", request.event_id).execute()
        
        if existing.data:
            # 已存在，返回现有记录
            return ReminderResponse(
                id=existing.data[0]["id"],
                event_id=request.event_id,
                user_id=request.user_id
            )
        
        # 创建新提醒
        result = supabase.table("user_reminders").insert({
            "user_id": request.user_id,
            "event_id": request.event_id
        }).execute()
        
        reminder = result.data[0]
        return ReminderResponse(
            id=reminder["id"],
            event_id=reminder["event_id"],
            user_id=reminder["user_id"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建提醒失败: {str(e)}")


@router.delete("/{event_id}")
async def delete_reminder(
    event_id: str,
    user_id: str = "default_user"
):
    """
    取消赛事提醒
    """
    supabase = get_supabase()
    
    try:
        supabase.table("user_reminders").delete().eq(
            "user_id", user_id
        ).eq("event_id", event_id).execute()
        
        return {"success": True, "message": "提醒已取消"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取消提醒失败: {str(e)}")
