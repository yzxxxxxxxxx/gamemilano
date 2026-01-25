"""
插入2026冬奥会赛事数据
"""
from supabase import create_client
from datetime import datetime
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SUPABASE_URL, SUPABASE_KEY

def insert_events():
    """插入赛事数据"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ 错误：请在.env文件中配置SUPABASE_URL和SUPABASE_KEY")
        return False

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase连接成功")

    # 2026冬奥会赛事数据 (2026-02-06 到 2026-02-22)
    events_data = [
        # 2026-02-06
        {
            "sport": "冰球",
            "discipline": "男子冰球",
            "title": "男子冰球：小组赛 - 加拿大 vs 芬兰",
            "event_time": "2026-02-06T12:00:00Z",
            "location": "米兰体育馆",
            "is_team_china": False,
            "type": "preliminary"
        },
        {
            "sport": "花样滑冰",
            "discipline": "双人滑",
            "title": "花样滑冰：双人滑短节目",
            "event_time": "2026-02-06T14:30:00Z",
            "location": "米兰冰上竞技场",
            "is_team_china": True,
            "type": "preliminary"
        },
        {
            "sport": "自由式滑雪",
            "discipline": "空中技巧",
            "title": "自由式滑雪：女子空中技巧决赛",
            "event_time": "2026-02-06T16:00:00Z",
            "location": "科尔蒂纳公园",
            "is_team_china": True,
            "type": "final"
        },

        # 2026-02-07
        {
            "sport": "短道速滑",
            "discipline": "短道速滑",
            "title": "短道速滑：男子1500米决赛",
            "event_time": "2026-02-07T10:00:00Z",
            "location": "米兰冰上竞技场",
            "is_team_china": True,
            "type": "final"
        },
        {
            "sport": "单板滑雪",
            "discipline": "单板滑雪",
            "title": "单板滑雪：男子平行大回转决赛",
            "event_time": "2026-02-07T13:30:00Z",
            "location": "科尔蒂纳公园",
            "is_team_china": False,
            "type": "final"
        },
        {
            "sport": "冰壶",
            "discipline": "冰壶",
            "title": "冰壶：女子循环赛 - 中国 vs 瑞典",
            "event_time": "2026-02-07T15:00:00Z",
            "location": "科尔蒂纳冰壶中心",
            "is_team_china": True,
            "type": "preliminary"
        },

        # 2026-02-08
        {
            "sport": "速度滑冰",
            "discipline": "速度滑冰",
            "title": "速度滑冰：女子3000米决赛",
            "event_time": "2026-02-08T11:00:00Z",
            "location": "米兰奥林匹克椭圆形体育场",
            "is_team_china": False,
            "type": "final"
        },
        {
            "sport": "高山滑雪",
            "discipline": "高山滑雪",
            "title": "高山滑雪：男子滑降决赛",
            "event_time": "2026-02-08T14:00:00Z",
            "location": "科尔蒂纳公园",
            "is_team_china": False,
            "type": "final"
        },
        {
            "sport": "越野滑雪",
            "discipline": "越野滑雪",
            "title": "越野滑雪：女子10公里传统技术",
            "event_time": "2026-02-08T16:30:00Z",
            "location": "瓦尔迪菲安德伦纳",
            "is_team_china": False,
            "type": "preliminary"
        },

        # 2026-02-09
        {
            "sport": "冬季两项",
            "discipline": "冬季两项",
            "title": "冬季两项：男子10公里追逐赛",
            "event_time": "2026-02-09T12:00:00Z",
            "location": "安特霍尔茨",
            "is_team_china": False,
            "type": "preliminary"
        },
        {
            "sport": "跳台滑雪",
            "discipline": "跳台滑雪",
            "title": "跳台滑雪：男子标准台决赛",
            "event_time": "2026-02-09T14:30:00Z",
            "location": "普雷达佐",
            "is_team_china": False,
            "type": "final"
        },
        {
            "sport": "北欧两项",
            "discipline": "北欧两项",
            "title": "北欧两项：男子个人标准台/10公里",
            "event_time": "2026-02-09T16:00:00Z",
            "location": "普雷达佐",
            "is_team_china": False,
            "type": "final"
        },

        # 2026-02-10
        {
            "sport": "雪车",
            "discipline": "雪车",
            "title": "雪车：女子单人决赛",
            "event_time": "2026-02-10T13:00:00Z",
            "location": "科尔蒂纳公园",
            "is_team_china": False,
            "type": "final"
        },
        {
            "sport": "钢架雪车",
            "discipline": "钢架雪车",
            "title": "钢架雪车：男子决赛",
            "event_time": "2026-02-10T15:30:00Z",
            "location": "科尔蒂纳公园",
            "is_team_china": False,
            "type": "final"
        },
        {
            "sport": "无舵雪橇",
            "discipline": "无舵雪橇",
            "title": "无舵雪橇：女子单人决赛",
            "event_time": "2026-02-10T17:00:00Z",
            "location": "科尔蒂纳公园",
            "is_team_china": False,
            "type": "final"
        },

        # 2026-02-11
        {
            "sport": "冰球",
            "discipline": "冰球",
            "title": "冰球：女子决赛",
            "event_time": "2026-02-11T20:00:00Z",
            "location": "米兰体育馆",
            "is_team_china": False,
            "type": "final"
        }
    ]

    try:
        # 清空现有数据
        print("🗑️ 清空现有赛事数据...")
        supabase.table("events").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()

        # 插入新数据
        print("📅 插入赛事数据...")
        result = supabase.table("events").insert(events_data).execute()
        print(f"   ✅ 成功插入 {len(result.data)} 条赛事记录")

        print("\n✅ 赛事数据插入完成！")
        return True

    except Exception as e:
        print(f"\n❌ 插入失败: {str(e)}")
        return False

if __name__ == "__main__":
    insert_events()