
/**
 * 时间处理工具
 * 专门处理米兰 (UTC+1) 到北京 (UTC+8) 的时间转换
 * 以及倒计时逻辑
 */

/**
 * 将米兰时间字符串转换为北京时间 Date 对象
 * 数据库存储的是意大利当地时间（无时区信息）
 * 意大利冬令时是 CET (UTC+1)
 * @param milanTimeStr 数据库中的时间字符串 (ISO format, 意大利当地时间)
 * @returns Date object，在用户本地时区环境下会自动显示正确的时间
 */
export function convertMilanToBeijing(milanTimeStr: string | null): Date | null {
    if (!milanTimeStr) return null;

    // 检查时间字符串是否已包含时区信息
    // 如果没有时区信息，添加意大利时区标记 +01:00 (CET)
    const hasTimezone = milanTimeStr.includes('+') || milanTimeStr.includes('Z') || milanTimeStr.includes('-', 10);
    const milanTimeWithTz = hasTimezone ? milanTimeStr : milanTimeStr + '+01:00';

    // JavaScript Date 会自动将此时间转换为用户本地时区
    // 在北京时区(UTC+8)的用户会看到正确的北京时间
    const date = new Date(milanTimeWithTz);
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
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    const weekday = weekdays[date.getDay()];
    const dateStr = `${year}-${month}-${day}`; // YYYY-MM-DD

    return { day, weekday, dateStr };
}

/**
 * 获取初始选中的日期
 * 如果当前日期在赛期内，返回当天日期字符串
 * 如果在赛期前，返回开幕式日期 (2月4日)
 * 如果在赛期后，返回闭幕式日期 (2月22日)
 */
export function getInitialSelectedDate(): string {
    const now = new Date();
    // 强制使用北京时间进行判断 (UTC+8)
    const year = 2026;
    const month = 1; // February

    const startDay = new Date(year, month, 4);
    const endDay = new Date(year, month, 22);

    if (now < startDay) {
        return '2026-02-04';
    } else if (now > endDay) {
        return '2026-02-22';
    } else {
        const { dateStr } = formatDateDisplay(now);
        return dateStr;
    }
}
