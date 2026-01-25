
import React, { useState, useEffect } from 'react';
import { getMedals, getChinaMedals, MedalData, ChinaMedalData } from '../services/api';

// 国旗图标组件 - 使用 flag-icons 库
// https://github.com/lipis/flag-icons
const FlagIcon: React.FC<{ iso: string }> = ({ iso }) => {
  // flag-icons 使用小写的 ISO 3166-1-alpha-2 代码
  const isoLower = iso.toLowerCase();

  return (
    <span
      className={`fi fi-${isoLower}`}
      style={{
        width: '32px',
        height: '20px',
        display: 'inline-block',
        borderRadius: '2px',
        border: '1px solid rgba(255,255,255,0.1)',
        backgroundSize: 'cover',
        flexShrink: 0
      }}
    />
  );
};

const MedalsView: React.FC = () => {
  const [search, setSearch] = useState('');
  const [activeRegion, setActiveRegion] = useState('总榜');
  const [medals, setMedals] = useState<MedalData[]>([]);
  const [chinaStats, setChinaStats] = useState<ChinaMedalData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 加载奖牌数据
  useEffect(() => {
    const loadMedals = async () => {
      try {
        setLoading(true);
        setError(null);

        const [medalsData, chinaData] = await Promise.all([
          getMedals(activeRegion, search),
          getChinaMedals()
        ]);

        setMedals(medalsData);
        setChinaStats(chinaData);
      } catch (err) {
        console.error('加载奖牌榜失败:', err);
        setError('数据加载失败，请稍后重试');
      } finally {
        setLoading(false);
      }
    };

    loadMedals();
  }, [activeRegion, search]);

  return (
    <div className="flex flex-col animate-in slide-in-from-right duration-500">
      {/* Featured Header Card */}
      <div className="p-4">
        <div
          className="relative overflow-hidden rounded-2xl shadow-2xl h-48 group"
        >
          {/* Background Image */}
          <div className="absolute inset-0">
            <img src="/medal_bg.png" alt="Background" className="w-full h-full object-cover" />
            <div className="absolute inset-0 bg-gradient-to-r from-black/90 via-black/50 to-transparent"></div>
          </div>

          <div className="relative z-10 flex flex-col justify-between h-full p-6">
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-2">
                <span className="bg-teal-500/20 text-teal-300 text-[10px] font-bold px-2 py-0.5 rounded border border-teal-500/30 backdrop-blur-md">
                  排名第 {chinaStats?.rank ?? '-'}
                </span>
                <span className="text-white/60 text-xs font-medium">2分钟前更新</span>
              </div>
              <h1 className="text-white text-3xl font-bold tracking-tight mt-2">
                中国 <span className="font-outfit font-normal opacity-90">Team China</span>
              </h1>
            </div>

            <div className="flex justify-between items-end">
              <div className="flex gap-8">
                <div className="flex flex-col items-center gap-1">
                  <span className="text-yellow-400 text-2xl font-bold font-outfit">{chinaStats?.gold ?? '-'}</span>
                  <span className="text-white/40 text-[10px] font-bold uppercase">金牌</span>
                </div>
                <div className="flex flex-col items-center gap-1">
                  <span className="text-slate-300 text-2xl font-bold font-outfit">{chinaStats?.silver ?? '-'}</span>
                  <span className="text-white/40 text-[10px] font-bold uppercase">银牌</span>
                </div>
                <div className="flex flex-col items-center gap-1">
                  <span className="text-orange-400 text-2xl font-bold font-outfit">{chinaStats?.bronze ?? '-'}</span>
                  <span className="text-white/40 text-[10px] font-bold uppercase">铜牌</span>
                </div>
              </div>

              <button className="flex items-center justify-center rounded-full h-12 w-12 bg-gradient-to-tr from-milan-blue to-blue-600 text-white shadow-lg shadow-blue-500/30">
                <span className="material-symbols-outlined text-2xl">chevron_right</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="px-4 py-2">
        <div className="flex w-full items-stretch rounded-xl h-12 ice-card">
          <div className="text-ice-blue/60 flex items-center justify-center pl-4">
            <span className="material-symbols-outlined">search</span>
          </div>
          <input
            className="flex w-full border-none bg-transparent text-white focus:ring-0 placeholder:text-white/30 px-4 text-base font-normal leading-normal"
            placeholder="搜索国家..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {/* Tabs */}
      <div className="mt-2">
        <div className="flex border-b border-white/5 px-4 gap-6 overflow-x-auto no-scrollbar">
          {['总榜', '欧洲', '北美洲', '亚洲'].map(region => (
            <button
              key={region}
              onClick={() => setActiveRegion(region)}
              className={`flex flex-col items-center justify-center border-b-2 pb-3 pt-2 transition-all ${activeRegion === region ? 'border-ice-blue text-ice-blue' : 'border-transparent text-white/40'}`}
            >
              <p className="text-sm font-bold tracking-wide whitespace-nowrap">{region}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Table Header */}
      <div className="px-4 pt-6 pb-2">
        <div className="grid grid-cols-12 gap-2 text-[10px] font-bold text-white/40 uppercase tracking-widest px-2">
          <div className="col-span-1">#</div>
          <div className="col-span-5">国家/地区</div>
          <div className="col-span-2 text-center">金</div>
          <div className="col-span-2 text-center">银</div>
          <div className="col-span-2 text-center">铜</div>
        </div>
      </div>

      {/* Table Body */}
      <div className="flex flex-col px-4 gap-2 pb-10">
        {loading ? (
          <div className="flex justify-center py-8">
            <div className="w-8 h-8 border-2 border-ice-blue/30 border-t-ice-blue rounded-full animate-spin"></div>
          </div>
        ) : error ? (
          <div className="text-center py-8 text-white/40">{error}</div>
        ) : medals.length === 0 ? (
          <div className="text-center py-8 text-white/40">暂无数据</div>
        ) : (
          medals.map(entry => (
            <div
              key={entry.id}
              className={`grid grid-cols-12 items-center p-3 rounded-xl transition-all ${entry.country === '中国' ? 'bg-royal-purple/20 backdrop-blur-xl border border-royal-purple/40 shadow-[0_0_15px_rgba(112,0,255,0.2)]' : 'ice-card'}`}
            >
              <div className={`col-span-1 text-sm font-bold ${entry.country === '中国' ? 'text-ice-blue' : 'text-white/60'}`}>{entry.rank}</div>
              <div className="col-span-5 flex items-center gap-3">
                <FlagIcon iso={entry.iso} />
                <span className="text-sm font-bold text-white truncate">{entry.country}</span>
              </div>
              <div className="col-span-2 text-center font-bold text-gold">{entry.gold}</div>
              <div className="col-span-2 text-center font-bold text-silver">{entry.silver}</div>
              <div className="col-span-2 text-center font-bold text-bronze">{entry.bronze}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default MedalsView;
