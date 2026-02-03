"""
后端配置文件
管理Supabase和Gemini API的连接配置
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Supabase配置
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Gemini API配置
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# 智谱 AI 配置
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY") or os.getenv("ZHIPUAI_API_KEY") or "91a47cf56b854cf28df8ebda02f88522.2EwvbbSfNMQMHOrq"

# 博查 AI 配置
BOCHA_API_KEY = os.getenv("BOCHA_API_KEY", "sk-f372b5355bc74034a46ecb1f227089ee")

# 服务器配置
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# CORS配置 - 允许前端开发服务器访问
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:3002",
    "http://127.0.0.1:3002",
]
