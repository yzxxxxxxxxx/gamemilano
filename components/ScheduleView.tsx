
import React, { useState, useEffect, useRef } from 'react';
import { getEvents, EventData, addReminder, removeReminder } from '../services/api';
import { convertMilanToBeijing, formatTime, getOlympicDates, formatDateDisplay, getInitialSelectedDate } from '../utils/time';

const ScheduleView: React.FC = () => {
    const [events, setEvents] = useState<EventData[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // 默认选中 "全部" 或者 今天 (如果今天在赛期内)
    // 这里默认为 null，表示"全部赛事"
    const [selectedDate, setSelectedDate] = useState<string | null>(getInitialSelectedDate());

    const dateScrollRef = useRef<HTMLDivElement>(null);

    // 自动滚动到选中日期
    useEffect(() => {
        if (dateScrollRef.current && selectedDate) {
            const timer = setTimeout(() => {
                const selectedElement = dateScrollRef.current?.querySelector('[data-selected="true"]');
                if (selectedElement) {
                    selectedElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'nearest',
                        inline: 'center'
                    });
                }
            }, 100);
            return () => clearTimeout(timer);
        }
    }, [selectedDate, loading]);

    // 加载数据
    useEffect(() => {
        const loadData = async () => {
            try {
                setLoading(true);
                setError(null);
                // 如果 selectedDate 为空，API 不传参即获取所有
                const data = await getEvents(selectedDate || undefined);

                // 前端排序：按时间，有时间的先排，没有时间的放后面
                data.sort((a, b) => {
                    const aTime = a.event_time ? new Date(a.event_time).getTime() : Infinity;
                    const bTime = b.event_time ? new Date(b.event_time).getTime() : Infinity;
                    return aTime - bTime;
                });

                setEvents(data);
            } catch (err) {
                console.error('加载赛程失败:', err);
                setError('加载失败，请重试');
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, [selectedDate]);

    // 切换提醒
    const toggleReminder = async (event: EventData) => {
        try {
            if (event.reminded) {
                await removeReminder(event.id);
            } else {
                await addReminder(event.id);
            }
            setEvents(prev => prev.map(e =>
                e.id === event.id ? { ...e, reminded: !e.reminded } : e
            ));
        } catch (err) {
            console.error('操作失败', err);
        }
    };

    // 获取运动图标 (Returns image path)
    const getSportIcon = (sport: string) => {
        const icons: Record<string, string> = {
            '自由式滑雪': '/sports/自由式滑雪.jpg',
            '花样滑冰': '/sports/花样滑冰.jpg',
            '冰壶': '/sports/冰壶.jpg',
            '短道速滑': '/sports/短道速滑.jpg',
            '单板滑雪': '/sports/单板滑雪.jpg',
            '高山滑雪': '/sports/高山滑雪.jpg',
            '越野滑雪': '/sports/越野滑雪.jpg',
            '跳台滑雪': '/sports/跳台滑雪.jpg',
            '北欧两项': '/sports/北欧两项.jpg',
            '冬季两项': '/sports/冬季两项.jpg',
            '雪车': '/sports/雪车.jpg',
            '钢架雪车': '/sports/钢架雪车.jpg',
            '无舵雪橇': '/sports/雪橇.jpg',
            '有舵雪橇': '/sports/雪车.jpg',
            '冰球': '/sports/冰球.jpg',
            '速度滑冰': '/sports/速度滑冰.jpg',
            '登山滑雪': '/sports/登山滑雪.jpg',
        };
        return icons[sport] || '/sports/冰球.jpg';
    };

    const olympicDates = getOlympicDates();

    return (
        <div className="flex flex-col h-full animate-in fade-in duration-500 pb-20">

            {/* 顶部日期选择 */}
            <div className="sticky top-0 z-40 backdrop-blur-md bg-[#020617]/80 border-b border-white/5 pt-2 pb-4">
                <div className="flex items-center justify-between px-4 mb-2">
                    <h2 className="text-lg font-bold text-white">赛程安排</h2>
                    <button
                        onClick={() => setSelectedDate(null)}
                        className={`text-xs font-bold px-3 py-1 rounded-full transition-all ${selectedDate === null ? 'bg-milan-blue text-white' : 'text-white/40 hover:text-white'}`}
                    >
                        全部赛事
                    </button>
                </div>

                <div
                    ref={dateScrollRef}
                    className="flex gap-2 px-4 overflow-x-auto no-scrollbar"
                >
                    {olympicDates.map((date) => {
                        const { day, weekday, dateStr } = formatDateDisplay(date);
                        const isSelected = selectedDate === dateStr;

                        return (
                            <button
                                key={dateStr}
                                data-selected={isSelected}
                                onClick={() => setSelectedDate(isSelected ? null : dateStr)}
                                className={`flex flex-col items-center min-w-[50px] py-2 rounded-xl transition-all shrink-0 ${isSelected ? 'milan-gradient shadow-lg shadow-milan-blue/20 scale-105' : 'bg-white/5 border border-white/5'}`}
                            >
                                <span className={`text-[9px] font-medium mb-0.5 ${isSelected ? 'text-white/90' : 'text-white/40'}`}>{weekday}</span>
                                <span className={`text-sm font-bold ${isSelected ? 'text-white' : 'text-white/70'}`}>{day}</span>
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* 列表内容 */}
            <div className="flex-1 px-4 py-4 space-y-3 min-h-0 overflow-y-auto">
                {loading ? (
                    <div className="flex justify-center py-20">
                        <div className="w-8 h-8 border-2 border-milan-blue/30 border-t-milan-blue rounded-full animate-spin"></div>
                    </div>
                ) : error ? (
                    <div className="text-center py-20 text-white/40">{error}</div>
                ) : events.length === 0 ? (
                    <div className="text-center py-20 text-white/40">当天暂无赛事</div>
                ) : (
                    events.map(event => {
                        const bjTime = convertMilanToBeijing(event.event_time);
                        const timeStr = formatTime(bjTime);

                        return (
                            <div key={event.id} className={`group relative ice-card rounded-2xl p-4 overflow-hidden transition-all hover:bg-white/5`}>
                                <div className="flex items-start gap-4 reltive z-10">
                                    {/* 左侧时间与日期 */}
                                    <div className="flex flex-col items-center justify-center w-12 shrink-0 pt-1">
                                        <span className="text-white font-bold text-sm tracking-widest">{timeStr}</span>
                                        {/* 如果是全部列表，显示日期 */}
                                        {!selectedDate && bjTime && (
                                            <span className="text-[9px] text-white/40 mt-1">{bjTime.getMonth() + 1}/{bjTime.getDate()}</span>
                                        )}
                                    </div>

                                    {/* 分隔线 */}
                                    <div className="w-[1px] self-stretch bg-white/10 mx-[-4px]"></div>

                                    {/* 右侧内容 */}
                                    <div className="flex-1 pl-2 min-w-0">
                                        <div className="flex items-center gap-2 mb-1">
                                            <div className="flex items-center gap-1.5 bg-milan-blue/10 px-1.5 py-0.5 rounded border border-milan-blue/20">
                                                <img
                                                    src={getSportIcon(event.sport)}
                                                    alt={event.sport}
                                                    className="w-4 h-4 rounded-sm object-cover"
                                                />
                                                <span className="text-milan-blue text-[10px] font-bold uppercase tracking-wider">
                                                    {event.sport}
                                                </span>
                                            </div>
                                            {event.is_team_china && (
                                                <span className="bg-china-red/10 text-china-red text-[10px] font-bold px-1.5 py-0.5 rounded border border-china-red/20 flex items-center gap-1">
                                                    <span className="w-1 h-1 bg-china-red rounded-full"></span> 中国队
                                                </span>
                                            )}
                                            {event.type === 'final' && event.sport !== '仪式' && (
                                                <span className="text-gold/80 text-[10px] font-bold border border-gold/20 px-1.5 py-0.5 rounded">🏅 金牌赛</span>
                                            )}
                                        </div>

                                        <h4 className="text-white font-bold text-sm leading-snug mb-1.5">{event.title}</h4>

                                        <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-2 text-white/50 text-[10px]">
                                                <span className="material-symbols-outlined text-[12px]">location_on</span>
                                                <span className="truncate max-w-[120px]">{event.location || '未知地点'}</span>
                                            </div>

                                            <button
                                                onClick={() => toggleReminder(event)}
                                                className={`flex items-center justify-center w-8 h-8 rounded-full transition-all ${event.reminded ? 'bg-milan-purple/20 text-milan-purple' : 'bg-white/5 text-white/30'}`}
                                            >
                                                <span className={`material-symbols-outlined text-[18px] ${event.reminded ? 'fill-1' : ''}`}>
                                                    {event.reminded ? 'notifications_active' : 'notifications'}
                                                </span>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        );
                    })
                )}
            </div>
        </div>
    );
};

export default ScheduleView;
