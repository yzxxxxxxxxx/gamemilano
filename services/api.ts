/**
 * API服务层
 * 封装所有后端API调用
 */

// 后端API基础URL
const API_BASE_URL = import.meta.env.DEV
  ? 'http://localhost:8000/api'  // 开发环境直接访问后端
  : '/api';  // 生产环境通过代理

/**
 * 通用请求函数
 */
async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultHeaders: HeadersInit = {
    'Content-Type': 'application/json',
  };

  const response = await fetch(url, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API请求失败: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

// ========== 赛事API ==========

export interface EventData {
  id: string;
  sport: string;
  discipline: string;
  title: string;
  event_time: string | null;
  location: string;
  is_team_china: boolean;
  type: string;
  reminded: boolean;
}

/**
 * 获取精选赛事
 */
/**
 * 获取精选赛事
 */
export async function getFeaturedEvents(limit: number = 5, date?: string | null): Promise<EventData[]> {
  const params = new URLSearchParams();
  params.append('limit', limit.toString());
  if (date) params.append('date', date);

  const queryString = params.toString();
  return request<EventData[]>(`/events/featured?${queryString}`);
}

/**
 * 获取赛事列表
 */
export async function getEvents(date?: string, teamChinaOnly?: boolean): Promise<EventData[]> {
  const params = new URLSearchParams();
  if (date) params.append('event_date', date);
  if (teamChinaOnly) params.append('team_china_only', 'true');

  const queryString = params.toString();
  return request<EventData[]>(`/events${queryString ? `?${queryString}` : ''}`);
}

// ========== 奖牌API ==========

export interface MedalData {
  id: string;
  rank: number;
  country: string;
  iso: string;
  gold: number;
  silver: number;
  bronze: number;
}

export interface ChinaMedalData {
  rank: number;
  gold: number;
  silver: number;
  bronze: number;
  total: number;
  updated_at: string;
}

/**
 * 获取奖牌榜
 */
export async function getMedals(region?: string, search?: string): Promise<MedalData[]> {
  const params = new URLSearchParams();
  if (region && region !== '总榜') params.append('region', region);
  if (search) params.append('search', search);

  const queryString = params.toString();
  return request<MedalData[]>(`/medals${queryString ? `?${queryString}` : ''}`);
}

/**
 * 获取中国队奖牌数据
 */
export async function getChinaMedals(): Promise<ChinaMedalData> {
  return request<ChinaMedalData>('/medals/china');
}

// ========== AI API ==========

export interface AIResponse {
  success: boolean;
  message: string;
}

/**
 * 获取运动员AI简介
 */
export async function getAthleteInsight(athleteName: string): Promise<string> {
  const response = await request<AIResponse>('/ai/athlete', {
    method: 'POST',
    body: JSON.stringify({ athlete_name: athleteName }),
  });
  return response.message;
}

/**
 * 获取赛事AI预测
 */
export async function getEventPrediction(eventTitle: string): Promise<string> {
  const response = await request<AIResponse>('/ai/event', {
    method: 'POST',
    body: JSON.stringify({ event_title: eventTitle }),
  });
  return response.message;
}

// ========== 提醒API ==========

/**
 * 添加赛事提醒
 */
export async function addReminder(eventId: string): Promise<void> {
  await request('/reminders', {
    method: 'POST',
    body: JSON.stringify({ event_id: eventId }),
  });
}

/**
 * 取消赛事提醒
 */
export async function removeReminder(eventId: string): Promise<void> {
  await request(`/reminders/${eventId}`, {
    method: 'DELETE',
  });
}
