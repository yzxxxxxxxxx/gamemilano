"""
数据库初始化脚本
在Supabase中创建表结构并插入示例数据
"""
from supabase import create_client
from datetime import datetime, timedelta
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SUPABASE_URL, SUPABASE_KEY

def init_database():
    """初始化数据库"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ 错误：请在.env文件中配置SUPABASE_URL和SUPABASE_KEY")
        return False
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase连接成功")
    
    # 注意：表结构需要在Supabase控制台中创建
    # 这里只插入示例数据
    
    # 插入示例赛事数据
    sample_events = [
        {
            "sport": "自由式滑雪",
            "discipline": "女子大跳台",
            "title": "自由式滑雪：女子大跳台决赛",
            "event_time": (datetime.now() + timedelta(hours=2)).isoformat(),
            "location": "科尔蒂纳公园",
            "is_team_china": True,
            "type": "final"
        },
        {
            "sport": "花样滑冰",
            "discipline": "双人滑短节目",
            "title": "花样滑冰：双人滑短节目",
            "event_time": (datetime.now() + timedelta(hours=4)).isoformat(),
            "location": "米兰冰上竞技场",
            "is_team_china": True,
            "type": "preliminary"
        },
        {
            "sport": "冰壶",
            "discipline": "男子小组赛",
            "title": "男子冰壶：加拿大 vs 瑞典",
            "event_time": (datetime.now() + timedelta(hours=6)).isoformat(),
            "location": "科尔蒂纳冰壶中心",
            "is_team_china": False,
            "type": "preliminary"
        },
        {
            "sport": "短道速滑",
            "discipline": "男子1000米",
            "title": "短道速滑：男子1000米决赛",
            "event_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "location": "米兰冰上竞技场",
            "is_team_china": True,
            "type": "final"
        },
        {
            "sport": "单板滑雪",
            "discipline": "女子U型场地",
            "title": "单板滑雪：女子U型场地资格赛",
            "event_time": (datetime.now() + timedelta(hours=8)).isoformat(),
            "location": "博尔米奥滑雪场",
            "is_team_china": True,
            "type": "preliminary"
        }
    ]
    
    # 插入示例奖牌数据
    sample_medals = [
        {"country": "挪威", "iso": "NO", "gold": 12, "silver": 8, "bronze": 6},
        {"country": "德国", "iso": "DE", "gold": 9, "silver": 10, "bronze": 4},
        {"country": "中国", "iso": "CN", "gold": 8, "silver": 4, "bronze": 5},
        {"country": "美国", "iso": "US", "gold": 7, "silver": 7, "bronze": 12},
        {"country": "加拿大", "iso": "CA", "gold": 6, "silver": 5, "bronze": 8},
        {"country": "荷兰", "iso": "NL", "gold": 6, "silver": 4, "bronze": 2},
        {"country": "瑞典", "iso": "SE", "gold": 5, "silver": 3, "bronze": 4},
        {"country": "日本", "iso": "JP", "gold": 4, "silver": 6, "bronze": 3},
        {"country": "韩国", "iso": "KR", "gold": 3, "silver": 2, "bronze": 5},
        {"country": "瑞士", "iso": "CH", "gold": 3, "silver": 4, "bronze": 3},
    ]
    
    try:
        # 清空并插入赛事数据
        print("📅 插入赛事数据...")
        supabase.table("events").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        result = supabase.table("events").insert(sample_events).execute()
        print(f"   ✅ 插入了 {len(result.data)} 条赛事")
        
        # 清空并插入奖牌数据
        print("🏅 插入奖牌数据...")
        supabase.table("medals").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        result = supabase.table("medals").insert(sample_medals).execute()
        print(f"   ✅ 插入了 {len(result.data)} 条奖牌记录")
        
        print("\n✅ 数据库初始化完成！")
        return True
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {str(e)}")
        print("\n请确保已在Supabase控制台创建以下表：")
        print("""
-- events表
CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sport VARCHAR(100) NOT NULL,
  discipline VARCHAR(100) NOT NULL,
  title VARCHAR(200) NOT NULL,
  event_time TIMESTAMP NOT NULL,
  location VARCHAR(200) NOT NULL,
  is_team_china BOOLEAN DEFAULT false,
  type VARCHAR(20) DEFAULT 'preliminary',
  created_at TIMESTAMP DEFAULT NOW()
);

-- medals表
CREATE TABLE medals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  country VARCHAR(100) NOT NULL,
  iso CHAR(2) NOT NULL,
  gold INTEGER DEFAULT 0,
  silver INTEGER DEFAULT 0,
  bronze INTEGER DEFAULT 0,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- user_reminders表
CREATE TABLE user_reminders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id VARCHAR(100) NOT NULL,
  event_id UUID REFERENCES events(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, event_id)
);
        """)
        return False


if __name__ == "__main__":
    init_database()
