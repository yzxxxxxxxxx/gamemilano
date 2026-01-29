-- GameMilano Supabase Database Schema
-- Run this SQL in your Supabase SQL Editor

-- ========================================
-- 1. Events Table (赛事表)
-- ========================================
CREATE TABLE IF NOT EXISTS events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sport VARCHAR(100) NOT NULL,
  discipline VARCHAR(100) NOT NULL,
  title VARCHAR(200) NOT NULL,
  event_time TIMESTAMP WITH TIME ZONE NOT NULL,
  location VARCHAR(200) NOT NULL,
  is_team_china BOOLEAN DEFAULT false,
  type VARCHAR(20) DEFAULT 'preliminary' CHECK (type IN ('final', 'preliminary', 'medal')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE events ENABLE ROW LEVEL SECURITY;

-- Allow public read access
CREATE POLICY "Allow public read access on events" ON events
  FOR SELECT USING (true);

-- Allow public insert access (for development)
CREATE POLICY "Allow public insert access on events" ON events
  FOR INSERT WITH CHECK (true);

-- ========================================
-- 2. Medals Table (奖牌榜)
-- ========================================
CREATE TABLE IF NOT EXISTS medals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  country VARCHAR(100) NOT NULL,
  iso CHAR(2) NOT NULL UNIQUE,
  gold INTEGER DEFAULT 0,
  silver INTEGER DEFAULT 0,
  bronze INTEGER DEFAULT 0,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE medals ENABLE ROW LEVEL SECURITY;

-- Allow public read access
CREATE POLICY "Allow public read access on medals" ON medals
  FOR SELECT USING (true);

-- Allow public insert access
CREATE POLICY "Allow public insert access on medals" ON medals
  FOR INSERT WITH CHECK (true);

-- Allow public update access
CREATE POLICY "Allow public update access on medals" ON medals
  FOR UPDATE USING (true);

-- ========================================
-- 3. User Reminders Table (用户提醒表)
-- ========================================
CREATE TABLE IF NOT EXISTS user_reminders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id VARCHAR(100) NOT NULL,
  event_id UUID REFERENCES events(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, event_id)
);

-- Enable Row Level Security
ALTER TABLE user_reminders ENABLE ROW LEVEL SECURITY;

-- Allow public access for now (would need auth in production)
CREATE POLICY "Allow public access on user_reminders" ON user_reminders
  FOR ALL USING (true);

-- ========================================
-- 4. Historical Medals Table (历史奖牌榜)
-- ========================================
CREATE TABLE IF NOT EXISTS historical_medals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  year INTEGER NOT NULL,
  location VARCHAR(100) NOT NULL,
  country VARCHAR(100) NOT NULL,
  iso CHAR(2) NOT NULL,
  gold INTEGER DEFAULT 0,
  silver INTEGER DEFAULT 0,
  bronze INTEGER DEFAULT 0,
  rank INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(year, iso)
);

-- Enable Row Level Security
ALTER TABLE historical_medals ENABLE ROW LEVEL SECURITY;

-- Allow public read access
CREATE POLICY "Allow public read access on historical_medals" ON historical_medals
  FOR SELECT USING (true);

-- Allow public insert access for synchronization
CREATE POLICY "Allow public insert access on historical_medals" ON historical_medals
  FOR INSERT WITH CHECK (true);

-- ========================================
-- 5. Insert Sample Data
-- ========================================

-- Insert sample events
INSERT INTO events (sport, discipline, title, event_time, location, is_team_china, type) VALUES
  ('自由式滑雪', '女子大跳台', '自由式滑雪：女子大跳台决赛', NOW() + INTERVAL '2 hours', '科尔蒂纳公园', true, 'final'),
  ('花样滑冰', '双人滑短节目', '花样滑冰：双人滑短节目', NOW() + INTERVAL '4 hours', '米兰冰上竞技场', true, 'preliminary'),
  ('冰壶', '男子小组赛', '男子冰壶：加拿大 vs 瑞典', NOW() + INTERVAL '6 hours', '科尔蒂纳冰壶中心', false, 'preliminary'),
  ('短道速滑', '男子1000米', '短道速滑：男子1000米决赛', NOW() + INTERVAL '1 hour', '米兰冰上竞技场', true, 'final'),
  ('单板滑雪', '女子U型场地', '单板滑雪：女子U型场地资格赛', NOW() + INTERVAL '8 hours', '博尔米奥滑雪场', true, 'preliminary');

-- Insert sample medal standings
INSERT INTO medals (country, iso, gold, silver, bronze) VALUES
  ('挪威', 'NO', 12, 8, 6),
  ('德国', 'DE', 9, 10, 4),
  ('中国', 'CN', 8, 4, 5),
  ('美国', 'US', 7, 7, 12),
  ('加拿大', 'CA', 6, 5, 8),
  ('荷兰', 'NL', 6, 4, 2),
  ('瑞典', 'SE', 5, 3, 4),
  ('日本', 'JP', 4, 6, 3),
  ('韩国', 'KR', 3, 2, 5),
  ('瑞士', 'CH', 3, 4, 3);
