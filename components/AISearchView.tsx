
import React, { useState } from 'react';
import { getAthleteInsight, getEventPrediction } from '../services/api';

interface Props {
  onClose: () => void;
}

const AISearchView: React.FC<Props> = ({ onClose }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [type, setType] = useState<'athlete' | 'event'>('athlete');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setResult(null);

    let response;
    if (type === 'athlete') {
      response = await getAthleteInsight(query);
    } else {
      response = await getEventPrediction(query);
    }

    setResult(response);
    setLoading(false);
  };

  return (
    <div className="bg-[#1e293b] rounded-2xl p-6 border border-white/10 shadow-2xl animate-in zoom-in duration-300">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-white font-bold flex items-center gap-2">
          <span className="material-symbols-outlined text-milan-blue">auto_awesome</span>
          AI 助手
        </h2>
        <button onClick={onClose} className="text-white/40 hover:text-white">
          <span className="material-symbols-outlined">close</span>
        </button>
      </div>

      <div className="flex gap-2 mb-4">
        <button
          onClick={() => setType('athlete')}
          className={`flex-1 text-[10px] font-bold uppercase py-2 rounded-lg transition-all ${type === 'athlete' ? 'bg-milan-blue text-white' : 'bg-white/5 text-white/40'}`}
        >
          运动员简介
        </button>
        <button
          onClick={() => setType('event')}
          className={`flex-1 text-[10px] font-bold uppercase py-2 rounded-lg transition-all ${type === 'event' ? 'bg-milan-blue text-white' : 'bg-white/5 text-white/40'}`}
        >
          赛事预测
        </button>
      </div>

      <form onSubmit={handleSearch} className="mb-6">
        <div className="relative">
          <input
            autoFocus
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={type === 'athlete' ? "输入运动员姓名（如：苏翊鸣）" : "输入赛事名称"}
            className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white focus:ring-milan-blue focus:border-milan-blue placeholder:text-white/20"
          />
          <button
            type="submit"
            disabled={loading}
            className="absolute right-2 top-2 h-8 w-8 bg-milan-blue rounded-lg flex items-center justify-center text-white disabled:opacity-50"
          >
            {loading ? (
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            ) : (
              <span className="material-symbols-outlined text-sm">send</span>
            )}
          </button>
        </div>
      </form>

      {result && (
        <div className="bg-milan-purple/10 border border-milan-purple/30 rounded-xl p-4 animate-in fade-in duration-500">
          <p className="text-white/90 text-sm leading-relaxed italic">
            "{result}"
          </p>
        </div>
      )}

      {!result && !loading && (
        <div className="text-center text-white/30 text-[10px] uppercase tracking-widest mt-4">
          由 Gemini AI 提供支持
        </div>
      )}
    </div>
  );
};

export default AISearchView;
