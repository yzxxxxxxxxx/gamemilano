
/**
 * 时间处理工具
 * 专门处理米兰 (UTC+1) 到北京 (UTC+8) 的时间转换
 * 以及倒计时逻辑
 */

// 米兰与北京的时差（小时）
// 米兰是 UTC+1, 北京是 UTC+8, 差 7 小时
const TIMEZONE_OFFSET_HOURS = 7;

/**
 * 将米兰时间字符串转换为北京时间 Date 对象
 * @param milanTimeStr 数据库中的时间字符串 (ISO format, assumed to be Milan time)
 * @returns Date object in local time (which we will assume represents Beijing time for display)
 */
export function convertMilanToBeijing(milanTimeStr: string | null): Date | null {
    if (!milanTimeStr) return null;
    const date = new Date(milanTimeStr);
    // 增加7小时
    date.setHours(date.getHours() + TIMEZONE_OFFSET_HOURS);
    return date;
}

/**
 * 格式化时间为 HH:mm
 */
export function formatTime(date: Date | null): string {
    if (!date) return '--:--';
    return date.toLocaleTimeString('zh-CN', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    });
}

/**
 * 计算距离目标时间的倒计时
 * @param targetDate 目标时间 (Date对象)
 * @returns { days, hrs, min, sec }
 */
export function calculateTimeLeft(targetDate: Date) {
    const now = new Date();
    const diff = targetDate.getTime() - now.getTime();

    if (diff <= 0) {
        return { days: '00', hrs: '00', min: '00', sec: '00' };
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hrs = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const min = Math.floor((diff / 1000 / 60) % 60);
    const sec = Math.floor((diff / 1000) % 60);

    return {
        days: days.toString().padStart(2, '0'),
        hrs: hrs.toString().padStart(2, '0'),
        min: min.toString().padStart(2, '0'),
        sec: sec.toString().padStart(2, '0')
    };
}

/**
 * 获取 2026年冬奥会日期范围 (2月4日 - 2月22日)
 */
export function getOlympicDates(): Date[] {
    const dates: Date[] = [];
    const startDay = 4;
    const endDay = 25;

    for (let i = startDay; i <= endDay; i++) {
        const date = new Date(2026, 1, i); // Month is 0-indexed, so 1 is February
        dates.push(date);
    }

    return dates;
}

/**
 * 格式化日期显示 (e.g. "04", "周三")
 */
export function formatDateDisplay(date: Date) {
    const day = date.getDate().toString().padStart(2, '0');
    const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    const weekday = weekdays[date.getDay()];
    const dateStr = date.toISOString().split('T')[0]; // YYYY-MM-DD

    return { day, weekday, dateStr };
}
