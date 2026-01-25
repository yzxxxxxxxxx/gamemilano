
import React, { useState, useEffect } from 'react';
import { NavTab } from './types';
import HomeView from './components/HomeView';
import MedalsView from './components/MedalsView';
import AISearchView from './components/AISearchView';
import ScheduleView from './components/ScheduleView';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<NavTab>(NavTab.HOME);
  const [isAISearchOpen, setIsAISearchOpen] = useState(false);

  return (
    <div className="flex flex-col min-h-screen bg-[#020617] max-w-md mx-auto relative shadow-2xl overflow-hidden border-x border-white/5">
      {/* Dynamic Header */}
      <header className="sticky top-0 z-50 glass-effect border-b border-white/10 px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 shrink-0">
            <span className="text-[16px] font-black italic tracking-tighter text-white">
              Game<span className="text-milan-blue">Milano</span>
            </span>
          </div>

          <div className="flex flex-col items-center text-center px-2 flex-1">
            <h2 className="text-white text-[16px] font-bold leading-tight tracking-wider">米兰-科尔蒂纳2026冬奥会</h2>
          </div>

          <div className="flex items-center shrink-0 w-8 justify-end">
            <button
              onClick={() => setIsAISearchOpen(true)}
              className="flex items-center justify-center p-1.5 hover:bg-white/5 rounded-full transition-all group"
            >
              <span className="material-symbols-outlined text-[24px] text-white group-hover:scale-110 transition-transform">search</span>
            </button>
          </div>
        </div>
      </header>

      {/* View Content */}
      <main className="flex-1 pb-24 overflow-y-auto no-scrollbar">
        {activeTab === NavTab.HOME && <HomeView onSwitchTab={setActiveTab} />}
        {activeTab === NavTab.MEDALS && <MedalsView />}
        {activeTab === NavTab.SCHEDULE && <ScheduleView />}
        {activeTab === NavTab.PROFILE && (
          <div className="flex flex-col items-center justify-center h-[60vh] text-slate-500">
            <span className="material-symbols-outlined text-4xl mb-2">construction</span>
            <p>该模块正在开发中</p>
          </div>
        )}
      </main>

      {/* AI Assistant Modal Overlay */}
      {isAISearchOpen && (
        <div className="fixed inset-0 z-[60] bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="w-full max-w-sm">
            <AISearchView onClose={() => setIsAISearchOpen(false)} />
          </div>
        </div>
      )}

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 inset-x-0 glass-effect border-t border-white/10 z-50">
        <div className="flex items-center justify-around max-w-md mx-auto py-3 px-2">
          <button
            onClick={() => setActiveTab(NavTab.HOME)}
            className={`flex flex-col items-center gap-1 transition-all ${activeTab === NavTab.HOME ? 'text-milan-blue' : 'text-white/40'}`}
          >
            <span className={`material-symbols-outlined ${activeTab === NavTab.HOME ? 'fill-1' : ''}`}>home</span>
            <span className="text-[10px] font-bold">首页</span>
          </button>
          <button
            onClick={() => setActiveTab(NavTab.MEDALS)}
            className={`flex flex-col items-center gap-1 transition-all ${activeTab === NavTab.MEDALS ? 'text-milan-blue' : 'text-white/40'}`}
          >
            <span className={`material-symbols-outlined ${activeTab === NavTab.MEDALS ? 'fill-1' : ''}`}>emoji_events</span>
            <span className="text-[10px] font-medium">奖牌榜</span>
          </button>
          <button
            onClick={() => setActiveTab(NavTab.SCHEDULE)}
            className={`flex flex-col items-center gap-1 transition-all ${activeTab === NavTab.SCHEDULE ? 'text-milan-blue' : 'text-white/40'}`}
          >
            <span className="material-symbols-outlined">event_note</span>
            <span className="text-[10px] font-medium">赛程</span>
          </button>
          <button
            onClick={() => setActiveTab(NavTab.PROFILE)}
            className={`flex flex-col items-center gap-1 transition-all ${activeTab === NavTab.PROFILE ? 'text-milan-blue' : 'text-white/40'}`}
          >
            <span className="material-symbols-outlined">person</span>
            <span className="text-[10px] font-medium">个人中心</span>
          </button>
        </div>
      </nav>
    </div>
  );
};

export default App;
