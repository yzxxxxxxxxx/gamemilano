
import React, { useState, useEffect } from 'react';
import { getHistoryEditions, getHistoryMedals, HistoricalMedalEntry } from '../services/api';
import { OlympicEdition } from '../types';

const HistoryView: React.FC = () => {
    const [editions, setEditions] = useState<OlympicEdition[]>([]);
    const [selectedYear, setSelectedYear] = useState<number | null>(null);
    const [historyMedals, setHistoryMedals] = useState<HistoricalMedalEntry[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchEditions = async () => {
            try {
                const data = await getHistoryEditions();
                setEditions(data);
            } catch (err) {
                console.error('获取历届列表失败:', err);
                setError('加载历届列表失败，请稍后重试');
            }
        };
        fetchEditions();
    }, []);

    const handleEditionClick = async (edition: OlympicEdition) => {
        setSelectedYear(edition.year);
        setLoading(true);
        setError(null);
        try {
            const data = await getHistoryMedals(edition.year);
            setHistoryMedals(data);
        } catch (err) {
            console.error(`获取 ${edition.year} 奖牌榜失败:`, err);
            setError(`加载 ${edition.year} 奖牌榜失败`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col min-h-full px-4 pt-4 pb-8">
            <div className="flex items-center gap-3 mb-6">
                <span className="material-symbols-outlined text-milan-blue text-[32px]">history</span>
                <h1 className="text-2xl font-black text-white italic tracking-tight">历届冬奥</h1>
            </div>

            {!selectedYear ? (
                <div className="grid grid-cols-1 gap-4">
                    {editions.map((edition) => (
                        <button
                            key={edition.year}
                            onClick={() => handleEditionClick(edition)}
                            className="group relative overflow-hidden rounded-2xl p-5 text-left transition-all active:scale-[0.98]"
                        >
                            {/* Card Background with Gradient */}
                            <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent opacity-50 group-hover:opacity-80 transition-opacity" />
                            <div className="absolute inset-x-0 bottom-0 h-[2px] bg-gradient-to-r from-transparent via-milan-blue/50 to-transparent" />

                            <div className="relative z-10 flex items-center justify-between">
                                <div>
                                    <div className="text-milan-blue font-black text-2xl italic tracking-tighter mb-1">
                                        {edition.year}
                                    </div>
                                    <div className="text-white font-bold text-lg">
                                        {edition.location}
                                    </div>
                                </div>
                                <div className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center text-white/30 group-hover:text-milan-blue group-hover:bg-white/10 transition-all">
                                    <span className="material-symbols-outlined">chevron_right</span>
                                </div>
                            </div>
                        </button>
                    ))}
                    {editions.length === 0 && !error && (
                        <div className="flex flex-col items-center justify-center py-20 text-white/20">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-milan-blue mb-4"></div>
                            <p className="font-medium">同步历史数据中...</p>
                        </div>
                    )}
                </div>
            ) : (
                <div className="flex flex-col">
                    {/* Back Header */}
                    <div className="flex items-center justify-between mb-6 sticky top-0 z-10 glass-effect py-2">
                        <button
                            onClick={() => setSelectedYear(null)}
                            className="flex items-center gap-1 text-slate-400 font-bold hover:text-white transition-colors"
                        >
                            <span className="material-symbols-outlined">arrow_back</span>
                            <span>返回列表</span>
                        </button>
                        <div className="text-right">
                            <div className="text-milan-blue font-black italic tracking-tighter">{selectedYear}</div>
                            <div className="text-white text-xs font-bold opacity-60 uppercase tracking-widest">
                                {editions.find(e => e.year === selectedYear)?.location}
                            </div>
                        </div>
                    </div>

                    {loading ? (
                        <div className="flex flex-col items-center justify-center py-20 text-white/20">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-milan-blue mb-4"></div>
                            <p>加载中...</p>
                        </div>
                    ) : error ? (
                        <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 text-red-500 text-center text-sm font-medium">
                            {error}
                        </div>
                    ) : (
                        <div className="space-y-1">
                            <div className="grid grid-cols-12 px-4 py-2 text-[10px] uppercase font-black tracking-widest text-[#94a3b8] opacity-60 border-b border-white/5 mb-1">
                                <div className="col-span-2">排名</div>
                                <div className="col-span-4">国家/地区</div>
                                <div className="col-span-1 text-center">金</div>
                                <div className="col-span-1 text-center">银</div>
                                <div className="col-span-1 text-center">铜</div>
                                <div className="col-span-3 text-right">总数</div>
                            </div>

                            {historyMedals.map((medal) => (
                                <div
                                    key={medal.country}
                                    className={`grid grid-cols-12 items-center px-4 py-4 rounded-xl transition-all hover:bg-white/[0.03] ${medal.rank <= 3 ? 'bg-white/[0.02]' : ''}`}
                                >
                                    <div className="col-span-2 flex items-center">
                                        {medal.rank === 1 && <span className="material-symbols-outlined text-yellow-500 text-[18px]">workspace_premium</span>}
                                        {medal.rank === 2 && <span className="material-symbols-outlined text-slate-300 text-[18px]">workspace_premium</span>}
                                        {medal.rank === 3 && <span className="material-symbols-outlined text-amber-600 text-[18px]">workspace_premium</span>}
                                        {medal.rank > 3 && <span className="text-[14px] font-black italic text-slate-500 ml-1">{medal.rank}</span>}
                                    </div>
                                    <div className="col-span-4 flex items-center gap-3">
                                        <img
                                            src={`https://flagsapi.com/${medal.iso === 'CN' ? 'CN' : medal.iso}/flat/64.png`}
                                            alt={medal.country}
                                            className="w-6 h-4 object-cover rounded-[2px] opacity-90 shadow-sm"
                                            onError={(e) => { e.currentTarget.style.display = 'none'; }}
                                        />
                                        <span className="text-[13px] font-bold text-white truncate">{medal.country}</span>
                                    </div>
                                    <div className="col-span-1 text-center font-black text-white text-[14px]">{medal.gold}</div>
                                    <div className="col-span-1 text-center font-bold text-slate-400 text-[13px]">{medal.silver}</div>
                                    <div className="col-span-1 text-center font-bold text-slate-500 text-[13px]">{medal.bronze}</div>
                                    <div className="col-span-3 text-right font-black text-milan-blue text-[14px]">{medal.total}</div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {error && !selectedYear && (
                <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 text-red-500 text-center text-sm font-medium mt-4">
                    {error}
                </div>
            )}
        </div>
    );
};

export default HistoryView;
