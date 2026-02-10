
import React, { useState, useEffect } from 'react';
import { NavTab } from '../types';
import { getFeaturedEvents, getEvents, getChinaMedals, addReminder, removeReminder, EventData, ChinaMedalData } from '../services/api';
import { calculateTimeLeft, convertMilanToBeijing, formatTime, getOlympicDates, formatDateDisplay, getInitialSelectedDate } from '../utils/time';

interface Props {
  onSwitchTab: (tab: NavTab) => void;
}

const HomeView: React.FC<Props> = ({ onSwitchTab }) => {
  const [timeLeft, setTimeLeft] = useState({ days: '00', hrs: '00', min: '00', sec: '00' });
  const [nextEvent, setNextEvent] = useState<EventData | null>(null);

  const [events, setEvents] = useState<EventData[]>([]);
  const [chinaStats, setChinaStats] = useState<ChinaMedalData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Date selection for Home View
  const [selectedDate, setSelectedDate] = useState<string | null>(getInitialSelectedDate());
  const dateScrollRef = React.useRef<HTMLDivElement>(null);

  // 自动滚动到选中日期
  useEffect(() => {
    if (dateScrollRef.current && selectedDate) {
      // 增加一点延时，确保 DOM 渲染完成
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
  }, [selectedDate, loading]); // Also trigger when loading finishes to ensure DOM is ready

  // Swipe logic
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);

  const minSwipeDistance = 50;

  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEndHandler = () => {
    if (!touchStart || !touchEnd) return;

    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    if (isLeftSwipe || isRightSwipe) {
      const olympicDates = getOlympicDates();
      const currentIndex = selectedDate
        ? olympicDates.findIndex(d => formatDateDisplay(d).dateStr === selectedDate)
        : -1; // -1 effectively means "no date selected" or logical start/end depending on requirement. 
      // But here user wants to swipe DATES. 
      // If selectedDate is null, maybe select first date? or today?
      // Let's assume we cycle through olympicDates.

      let newIndex = currentIndex;
      if (isLeftSwipe) {
        // Next Day
        newIndex = currentIndex + 1;
        if (newIndex >= olympicDates.length) newIndex = 0; // Loop or stop? User said "ensure select later dates", maybe loop or valid clamp.
        if (newIndex < 0) newIndex = 0;
      } else {
        // Prev Day
        newIndex = currentIndex - 1;
        if (newIndex < 0) newIndex = olympicDates.length - 1;
      }

      const newDate = formatDateDisplay(olympicDates[newIndex]).dateStr;
      setSelectedDate(newDate);
    }
  };

  // 加载数据
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        setError(null);

        const [eventsData, medalData, nextUpcoming] = await Promise.all([
          // Only fetch featured events (China/Finals), optionally filtered by date
          getFeaturedEvents(100, selectedDate), // Increase limit when filtering by date to show all matches
          getChinaMedals(),
          getFeaturedEvents(1, null) // Fetch the single nearest future featured event regardless of selected date
        ]);

        setEvents(eventsData);
        setChinaStats(medalData);

        // Find the next significant event for countdown
        // Priority: Nearest Team China/Featured event (independent of selected date)
        if (nextUpcoming && nextUpcoming.length > 0) {
          setNextEvent(nextUpcoming[0]);
        } else {
          // Fallback to searching in current list if global featured fetch failed (e.g. all games finished)
          const validEvents = eventsData.filter(e => e.event_time);
          let targetEvent = validEvents.find(e => e.is_team_china);
          if (!targetEvent && validEvents.length > 0) {
            targetEvent = validEvents[0];
          }
          setNextEvent(targetEvent || null);
        }

      } catch (err) {
        console.error('加载数据失败:', err);
        setError('数据加载失败，请稍后重试');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [selectedDate]);

  // 倒计时逻辑
  useEffect(() => {
    if (!nextEvent) return;

    const targetTime = convertMilanToBeijing(nextEvent.event_time);

    const timer = setInterval(() => {
      setTimeLeft(calculateTimeLeft(targetTime));
    }, 1000);

    return () => clearInterval(timer);
  }, [nextEvent]);

  // 切换提醒状态
  const toggleReminder = async (event: EventData) => {
    try {
      if (event.reminded) {
        await removeReminder(event.id);
      } else {
        await addReminder(event.id);
      }
      // 更新本地状态
      setEvents(prev => prev.map(e =>
        e.id === event.id ? { ...e, reminded: !e.reminded } : e
      ));
    } catch (err) {
      console.error('切换提醒失败:', err);
    }
  };

  // 获取运动图标
  // 获取运动图标 (Returns image path now)
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
      '无舵雪橇': '/sports/雪橇.jpg', // Map to Xue Qiao
      '有舵雪橇': '/sports/雪车.jpg', // Map to Xue Che or similar? file list had '雪橇.jpg' and '雪车.jpg'
      '冰球': '/sports/冰球.jpg',
      '速度滑冰': '/sports/速度滑冰.jpg',
      '登山滑雪': '/sports/登山滑雪.jpg',
    };
    return icons[sport] || '/sports/冰球.jpg'; // Default fallback
  };

  const olympicDates = getOlympicDates();

  return (
    <div className="flex flex-col gap-6 animate-in fade-in duration-500">
      {/* Countdown Card */}
      <section className="p-4">
        <div className="relative overflow-hidden rounded-2xl milan-gradient p-6 shadow-lg shadow-milan-purple/20">
          <div className="absolute top-0 right-0 p-3 opacity-15">
            <span className="material-symbols-outlined text-8xl">ac_unit</span>
          </div>
          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-2">
              <span className="bg-white text-milan-purple text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">即将直播</span>
              <span className="text-white/80 text-xs font-medium">下一场焦点战</span>
            </div>

            <h3 className="text-white text-xl font-bold mb-4 min-h-[56px] flex items-center">
              {nextEvent ? (
                <span>
                  {nextEvent.title}
                </span>
              ) : (
                "等待赛程更新..."
              )}
            </h3>

            <div className="flex gap-3">
              {[
                { label: '天', value: timeLeft.days },
                { label: '时', value: timeLeft.hrs },
                { label: '分', value: timeLeft.min },
                { label: '秒', value: timeLeft.sec },
              ].map((item, i) => (
                <div key={i} className="flex flex-col items-center gap-1">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-white/20 border border-white/30 backdrop-blur-sm">
                    <p className="text-white text-xl font-bold">{item.value}</p>
                  </div>
                  <p className="text-white/70 text-[10px] font-medium uppercase">{item.label}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Date Selector */}
      {/* Date Selector with Swipe */}
      <section
        className="touch-pan-y"
        onTouchStart={onTouchStart}
        onTouchMove={onTouchMove}
        onTouchEnd={onTouchEndHandler}
      >
        <div className="flex items-center justify-between px-4 mb-2">
          <h4 className="text-xs font-bold text-white/40 uppercase tracking-widest">2026年2月</h4>
        </div>
        <div
          ref={dateScrollRef}
          className="flex gap-3 px-4 overflow-x-auto no-scrollbar pb-2 scroll-smooth"
        >
          {olympicDates.map((date) => {
            const { day, weekday, dateStr } = formatDateDisplay(date);
            const isSelected = selectedDate === dateStr;
            // Auto scroll to selected could be added here via ref, but let's stick to basic render first
            return (
              <button
                key={dateStr}
                data-selected={isSelected}
                onClick={() => setSelectedDate(isSelected ? null : dateStr)}
                className={`flex flex-col items-center min-w-[56px] py-3 rounded-2xl transition-all ${isSelected ? 'milan-gradient shadow-lg shadow-milan-blue/20 scale-105' : 'ice-card'}`}
              >
                <span className={`text-[10px] font-medium mb-1 ${isSelected ? 'text-white/90' : 'text-white/40'}`}>{weekday}</span>
                <span className="text-lg font-bold text-white">{day}</span>
                {isSelected && <div className="h-1 w-1 bg-white rounded-full mt-1"></div>}
              </button>
            );
          })}
        </div>
      </section>

      {/* Featured Events */}
      <section className="px-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-white text-xl font-bold tracking-tight">精选赛事</h2>
          <button
            onClick={() => onSwitchTab(NavTab.SCHEDULE)}
            className="text-milan-blue text-xs font-bold hover:text-white transition-colors"
          >
            查看全部
          </button>
        </div>

        {loading ? (
          <div className="flex justify-center py-8">
            <div className="w-8 h-8 border-2 border-milan-blue/30 border-t-milan-blue rounded-full animate-spin"></div>
          </div>
        ) : error ? (
          <div className="text-center py-8 text-white/40">{error}</div>
        ) : events.length === 0 ? (
          <div className="text-center py-8 text-white/40">暂无赛事信息</div>
        ) : (
          <div className="space-y-3">
            {events.map(event => {
              // Convert time for display
              const bjTime = convertMilanToBeijing(event.event_time);
              const timeStr = formatTime(bjTime);

              return (
                <div key={event.id} className={`group relative ice-card rounded-2xl p-4 overflow-hidden transition-all hover:bg-white/5 ${!event.is_team_china ? 'opacity-90' : ''}`}>
                  <div className="flex items-start justify-between relative z-10">
                    <div className="flex gap-4 min-w-0">
                      <div className="size-12 rounded-xl bg-white/5 overflow-hidden border border-white/10 shrink-0">
                        <img
                          src={getSportIcon(event.sport)}
                          alt={event.sport}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div className="min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          {event.is_team_china && (
                            <span className="bg-china-red/10 text-china-red text-[10px] font-bold px-2 py-0.5 rounded flex items-center gap-1 border border-china-red/20 shrink-0">
                              <span className="w-1.5 h-1.5 bg-china-red rounded-full animate-pulse"></span> 中国队
                            </span>
                          )}
                          {(event.type === 'final' || event.title.includes('决赛')) && event.sport !== '仪式' && (
                            <span className="text-gold text-[10px] font-bold uppercase tracking-wider shrink-0 border border-gold/20 px-1 rounded">🏅 金牌赛</span>
                          )}
                        </div>
                        <div className="marquee-container w-full max-w-[260px]">
                          <div className={event.title.length > 12 ? "marquee-content" : ""}>
                            <h4 className="text-white font-bold text-base leading-snug">
                              {event.title}
                              {event.title.length > 12 && <span className="ml-24">{event.title}</span>}
                            </h4>
                          </div>
                        </div>
                        <div className="flex items-center gap-3 mt-2 text-white/60 text-xs">
                          <span className="flex items-center gap-1"><span className="material-symbols-outlined text-[14px]">schedule</span> {timeStr}</span>
                          <span className="flex items-center gap-1 truncate max-w-[100px]"><span className="material-symbols-outlined text-[14px]">location_on</span> {event.location || '未知地点'}</span>
                        </div>
                      </div>
                    </div>
                    <button
                      onClick={() => toggleReminder(event)}
                      className={`size-10 rounded-full flex items-center justify-center border transition-all shrink-0 ${event.reminded ? 'bg-milan-purple/20 border-milan-purple/40 text-milan-blue' : 'border-white/10 text-white/40 hover:border-milan-blue/50 bg-white/5'}`}
                    >
                      <span className={`material-symbols-outlined ${event.reminded ? 'fill-1' : ''}`}>
                        {event.reminded ? 'notifications_active' : 'notifications'}
                      </span>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* Quick Medal Summary */}
      <section className="p-4">
        <div
          onClick={() => onSwitchTab(NavTab.MEDALS)}
          className="ice-card rounded-2xl p-5 relative overflow-hidden cursor-pointer hover:border-milan-purple/50 transition-all group"
        >
          <div className="absolute -right-10 -bottom-10 w-40 h-40 bg-milan-purple/10 rounded-full blur-3xl group-hover:bg-milan-purple/20 transition-all"></div>
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-white font-bold text-lg flex items-center gap-2">
              <span className="material-symbols-outlined text-yellow-500 fill-1">emoji_events</span>
              实时奖牌榜
            </h3>
            <span className="text-white/40 text-[10px] font-bold uppercase">刚刚更新</span>
          </div>
          <div className="grid grid-cols-4 gap-2 items-center text-center">
            <div className="flex flex-col items-center">
              <div className="w-9 h-6 rounded-sm overflow-hidden mb-1.5 shadow-sm border border-white/10">
                <svg className="w-full h-full" viewBox="0 0 30 20">
                  <rect fill="#ee1c25" height="20" width="30"></rect>
                  <path d="M5 5l-1.033 3.178 2.704-1.964H3.329l2.704 1.964L5 5z" fill="#ffff00"></path>
                  <circle cx="10" cy="2" r="0.5" fill="#ffff00"></circle>
                  <circle cx="12" cy="4" r="0.5" fill="#ffff00"></circle>
                  <circle cx="12" cy="7" r="0.5" fill="#ffff00"></circle>
                  <circle cx="10" cy="9" r="0.5" fill="#ffff00"></circle>
                </svg>
              </div>
              <span className="text-white/90 text-[10px] font-bold tracking-tight uppercase">中国</span>
            </div>
            <div className="flex flex-col">
              <span className="text-white text-xl font-bold">{chinaStats?.gold ?? 0}</span>
              <span className="text-yellow-500 text-[8px] font-bold uppercase tracking-widest">金牌</span>
            </div>
            <div className="flex flex-col">
              <span className="text-white text-xl font-bold">{chinaStats?.silver ?? 0}</span>
              <span className="text-slate-300 text-[8px] font-bold uppercase tracking-widest">银牌</span>
            </div>
            <div className="flex flex-col">
              <span className="text-white text-xl font-bold">{chinaStats?.bronze ?? 0}</span>
              <span className="text-orange-400 text-[8px] font-bold uppercase tracking-widest">铜牌</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomeView;
