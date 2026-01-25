"""
后端健康检查脚本
用于检测环境配置、依赖安装和数据库连接状态
"""
import os
import sys
from pathlib import Path

# 添加父目录到path以导入config
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

try:
    from dotenv import load_dotenv
    # explicitly load .env from backend dir
    load_dotenv(backend_dir / ".env")
except ImportError:
    print("❌ python-dotenv not installed. Run 'pip install python-dotenv'")
    sys.exit(1)

def check_health():
    print("=== GameMilano 后端健康检查 ===")
    
    # 1. 检查环境变量
    print("\n[1] 检查环境变量 (.env)...")
    required_vars = ["SUPABASE_URL", "SUPABASE_KEY", "GEMINI_API_KEY"]
    missing = []
    for var in required_vars:
        val = os.getenv(var)
        if not val:
            missing.append(var)
            print(f"  ❌ {var} 未设置或为空")
        else:
            masked = val[:4] + "..." + val[-4:] if len(val) > 8 else "***"
            print(f"  ✅ {var} 已设置")
    
    if missing:
        print("  ⚠️ 警告: 部分环境变量缺失，应用可能无法正常运行。")
    
    # 2. 检查核心依赖
    print("\n[2] 检查核心依赖库...")
    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("supabase", "Supabase Client"),
        ("httpx", "HTTPX Client")
    ]
    
    all_packages_ok = True
    for pkg_import, pkg_name in packages:
        try:
            __import__(pkg_import)
            print(f"  ✅ {pkg_name} 已安装")
        except ImportError:
            print(f"  ❌ {pkg_name} 未安装 ({pkg_import})")
            all_packages_ok = False
            
    if not all_packages_ok:
        print("  ⚠️ 请运行 'pip install -r requirements.txt' 安装缺失依赖")
        return

    # 3. 检查Supabase连接
    print("\n[3] 检查Supabase数据库连接...")
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if url and key:
        try:
            from supabase import create_client
            client = create_client(url, key)
            
            # 尝试查询medals表（应该存在）
            print(f"  正在尝试连接数据库...")
            
            # 使用head=True只回去count，轻量级
            try:
                # 尝试一个简单的select
                res = client.table("medals").select("id", count="exact").limit(1).execute()
                count = res.count if hasattr(res, 'count') else len(res.data)
                print(f"  ✅ 数据库连接成功！(Medals表记录数: {count}，如果不为0则说明有数据)")
            except Exception as e:
                 print(f"  ❌ 数据库查询失败: {str(e)}")
                 print("  提示: 请检查是否运行了 'scripts/supabase_schema.sql' 初始化数据库")

        except Exception as e:
            print(f"  ❌ 初始化Supabase客户端失败: {str(e)}")
    else:
        print("  ⏭️  跳过数据库检查 (缺少URL或KEY)")

    print("\n=== 检查完成 ===")
    print("如果以上检查全通过，你可以尝试运行: python main.py")

if __name__ == "__main__":
    check_health()
