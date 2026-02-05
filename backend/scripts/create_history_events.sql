-- 创建历史赛事详细数据表 (history_events)
-- 请在 Supabase SQL Editor 中运行此脚本

CREATE TABLE IF NOT EXISTS public.history_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    edition INTEGER,                  -- 届数
    year INTEGER,                     -- 年份
    host TEXT,                        -- 举办地
    city TEXT,                        -- 城市
    country TEXT,                     -- 国家/地区
    date_range TEXT,                  -- 举办时间区间
    countries_count INTEGER,          -- 参赛国家数量
    sports_count INTEGER,             -- 大项数量
    sport_name TEXT,                  -- 大项名称
    events_count INTEGER,             -- 小项数量
    event_name TEXT,                  -- 小项名称
    first_olympic_year INTEGER,       -- 首次入奥年
    gold_country TEXT,                -- 金牌国家
    silver_country TEXT,              -- 银牌国家
    bronze_country TEXT,              -- 铜牌国家
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 设置注释，方便后续维护
COMMENT ON TABLE public.history_events IS '历届冬奥会详细赛事记录及奖牌获得国家';

-- 开启 Row Level Security (RLS)
ALTER TABLE public.history_events ENABLE ROW LEVEL SECURITY;

-- 创建公共读取策略（所有用户可以查看）
CREATE POLICY "Allow public read access" ON public.history_events
    FOR SELECT USING (true);

-- 如果需要支持匿名用户通过 API 导入，可以临时开启写入权限 (不建议，建议使用 Dashboard 导入)
-- CREATE POLICY "Allow public insert access" ON public.history_events
--     FOR INSERT WITH CHECK (true);
