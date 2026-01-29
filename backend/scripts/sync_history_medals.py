"""
历史奖牌数据同步脚本
从百度体育爬取历届冬奥会奖牌数据并同步到 Supabase
"""
import httpx
from bs4 import BeautifulSoup
from supabase import create_client, Client
import asyncio
import logging
import sys
import os

# 禁用全局代理以避免 SSL 错误
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["NO_PROXY"] = "*"

# 将项目根目录添加到 python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.config import SUPABASE_URL, SUPABASE_KEY
from backend.scripts.sync_medals import get_iso

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 历届冬奥会列表 (年份, 举办地)
EDITIONS = [
    (2022, "北京"),
    (2018, "平昌"),
    (2014, "索契"),
    (2010, "温哥华"),
    (2006, "都灵"),
    (2002, "盐湖城"),
    (1998, "长野"),
    (1994, "利勒哈默尔"),
    (1992, "阿尔贝维尔"),
    (1988, "卡尔加里"),
    (1984, "萨拉热窝"),
    (1980, "普莱西德湖"),
    (1976, "因斯布鲁克"),
    (1972, "札幌"),
    (1968, "格勒诺布尔"),
    (1964, "因斯布鲁克"),
    (1960, "斯阔谷"),
    (1956, "科蒂纳丹佩佐"),
    (1952, "奥斯陆"),
    (1948, "圣莫里茨"),
    (1936, "加米施-帕滕基兴"),
    (1932, "普莱西德湖"),
    (1928, "圣莫里茨"),
    (1924, "夏慕尼")
]

async def scrape_historical_medals(year, location):
    """抓取指定届次的奖牌数据"""
    match_name = f"{year}年{location}冬奥会"
    url = f"https://tiyu.baidu.com/al/major/home?page=home&match={match_name}&tab=%E5%A5%96%E7%89%8C%E6%A6%9C"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        async with httpx.AsyncClient(trust_env=False) as client:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('.rankContainer.rankTable')
        
        if not rows:
            logger.warning(f"未找到 {year} {location} 的数据。")
            return []
            
        medal_data = []
        for row in rows:
            try:
                rank_span = row.select_one('.rankHeaderRanking span')
                rank = int(rank_span.text.strip()) if rank_span else 0
                
                country_name = row.select_one('.rankHeaderAreaName').text.strip()
                gold = int(row.select_one('.medalImg.gold').text.strip())
                silver = int(row.select_one('.medalImg.silver').text.strip())
                bronze = int(row.select_one('.medalImg.copper').text.strip())
                
                medal_data.append({
                    "year": year,
                    "location": location,
                    "country": country_name,
                    "iso": get_iso(country_name),
                    "gold": gold,
                    "silver": silver,
                    "bronze": bronze,
                    "rank": rank
                })
            except Exception as e:
                continue
                
        return medal_data
        
    except Exception as e:
        logger.error(f"抓取 {year} 数据失败: {e}")
        return []

async def sync_history():
    """全量同步历史数据"""
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    for year, location in EDITIONS:
        logger.info(f"正在处理 {year} {location}...")
        data = await scrape_historical_medals(year, location)
        
        if data:
            try:
                # 尝试批量写入，如果失败则尝试单条回退（处理冲突）
                res = supabase.table("historical_medals").upsert(data, on_conflict="year,iso").execute()
                logger.info(f"   ✅ 成功同步了 {len(data)} 条记录")
            except Exception as e:
                logger.error(f"   ❌ 同步 {year} 数据到数据库失败: {e}")
        
        # 避免请求过快
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(sync_history())
