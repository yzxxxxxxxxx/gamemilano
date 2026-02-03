"""
奖牌数据同步脚本
从百度体育爬取冬奥会奖牌数据并同步到 Supabase
"""
import httpx
from bs4 import BeautifulSoup
from supabase import create_client, Client
import asyncio
import logging
import traceback
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

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 国家名称到 ISO 编码的映射
COUNTRY_MAP = {
    "中国": "CN",
    "挪威": "NO",
    "德国": "DE",
    "美国": "US",
    "加拿大": "CA",
    "荷兰": "NL",
    "瑞典": "SE",
    "日本": "JP",
    "韩国": "KR",
    "瑞士": "CH",
    "奥地利": "AT",
    "法国": "FR",
    "意大利": "IT",
    "俄罗斯奥委会": "ROC",
    "俄罗斯奥运队": "ROC",
    "俄罗斯": "RU",
    "芬兰": "FI",
    "斯洛文尼亚": "SI",
    "匈牙利": "HU",
    "澳大利亚": "AU",
    "新西兰": "NZ",
    "斯洛伐克": "SK",
    "捷克": "CZ",
    "比利时": "BE",
    "西班牙": "ES",
    "乌克兰": "UA",
    "波兰": "PL",
    "拉脱维亚": "LV",
    "爱沙尼亚": "EE",
    "白俄罗斯": "BY",
    "大不列颠": "GB",
    "英国": "GB",
    "哈萨克斯坦": "KZ",
    "丹麦": "DK",
    "乌兹别克斯坦": "UZ",
    "保加利亚": "BG",
    "克罗地亚": "HR",
    "列支敦士登": "LI",
    "朝鲜": "KP",
    "罗马尼亚": "RO",
    "苏联": "URS",
    "德意志民主共和国": "GDR",
    "德意志联邦共和国": "FRG",
    "捷克斯洛伐克": "TCH",
    "南斯拉夫联盟共和国": "YUG",
    "独立国家联合体": "EUN",
    "俄罗斯奥林匹克运动员": "OAR",
}

def get_iso(country_name: str) -> str:
    """获取国家的 ISO 编码，如果不在映射中则生成一个临时的"""
    return COUNTRY_MAP.get(country_name, country_name[:2].upper())

async def scrape_medals():
    """从百度体育爬取奖牌数据"""
    url = "https://tiyu.baidu.com/al/major/home?page=home&match=2026%E5%B9%B4%E7%B1%B3%E5%85%B0%E5%86%AC%E5%A5%A5%E4%BC%9A&tab=%E5%A5%96%E7%89%8C%E6%A6%9C"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        async with httpx.AsyncClient(trust_env=False) as client:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有奖牌行
        rows = soup.select('.rankContainer.rankTable')
        if not rows:
            logger.warning("未能在页面中找到奖牌数据行。")
            return []
            
        medal_data = []
        for row in rows:
            try:
                country_name = row.select_one('.rankHeaderAreaName').text.strip()
                gold = int(row.select_one('.medalImg.gold').text.strip())
                silver = int(row.select_one('.medalImg.silver').text.strip())
                bronze = int(row.select_one('.medalImg.copper').text.strip())
                
                medal_data.append({
                    "country": country_name,
                    "iso": get_iso(country_name),
                    "gold": gold,
                    "silver": silver,
                    "bronze": bronze
                })
            except Exception as row_e:
                logger.error(f"解析这一行时出错: {row_e}")
                continue
                
        return medal_data
        
    except Exception as e:
        logger.error(f"同步奖牌数据时出错: {e}")
        traceback.print_exc()
        return []

async def sync_to_supabase(data):
    """同步数据到 Supabase"""
    if not data:
        return
        
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # 使用 upsert，基于 iso 字段
        # 批量更新
        for item in data:
            try:
                # 首先检查是否存在
                res = supabase.table("medals").select("id").eq("iso", item["iso"]).execute()
                if res.data:
                    # 更新
                    supabase.table("medals").update({
                        "country": item["country"],
                        "gold": item["gold"],
                        "silver": item["silver"],
                        "bronze": item["bronze"],
                        "updated_at": "now()"
                    }).eq("iso", item["iso"]).execute()
                else:
                    # 插入
                    supabase.table("medals").insert(item).execute()
            except Exception as item_e:
                logger.error(f"更新国家 {item['country']} 数据时出错: {item_e}")
        
        logger.info(f"成功同步了 {len(data)} 个国家的奖牌数据。")
        
    except Exception as e:
        logger.error(f"连接 Supabase 同步数据时出错: {e}")

async def run_sync():
    """导出给 main.py 调用的主函数"""
    logger.info("开始执行奖牌同步...")
    data = await scrape_medals()
    if data:
        await sync_to_supabase(data)
    else:
        logger.warning("未抓取到任何奖牌数据。")

if __name__ == "__main__":
    asyncio.run(run_sync())
