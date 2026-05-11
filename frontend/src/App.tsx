import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LayoutDashboard, 
  Users, 
  Network, 
  Settings, 
  Search, 
  Bell, 
  Plus, 
  Activity, 
  ChevronRight,
  BrainCircuit,
  Zap,
  Clock,
  Menu,
  X
} from 'lucide-react';

// Mock Data for Demo
const AGENTS = [
  { id: '1', name: 'Sales Assistant', type: 'Sales', status: 'online', tasks: 12, performance: 98 },
  { id: '2', name: 'Legal Analyst', type: 'Legal', status: 'online', tasks: 8, performance: 95 },
  { id: '3', name: 'Dev Architect', type: 'Engineering', status: 'busy', tasks: 24, performance: 99 },
  { id: '4', name: 'Market Strategist', type: 'Marketing', status: 'offline', tasks: 0, performance: 92 },
];

const RECENT_TASKS = [
  { id: 'T1', title: 'Q4 Sales Analysis', agent: 'Sales Assistant', status: 'completed', time: '5m ago' },
  { id: 'T2', title: 'Trademark Review', agent: 'Legal Analyst', status: 'processing', time: 'Just now' },
  { id: 'T3', title: 'System Migration Plan', agent: 'Dev Architect', status: 'queued', time: '12m ago' },
];

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden">
      <div className="aurora"></div>
      
      {/* Sidebar */}
      <motion.aside 
        initial={false}
        animate={{ width: isSidebarOpen ? 260 : 80 }}
        className="glass border-r border-slate-800 flex flex-col z-50"
      >
        <div className="p-6 flex items-center gap-3">
          <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <BrainCircuit className="text-white" />
          </div>
          {isSidebarOpen && (
            <motion.h1 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="font-bold text-xl tracking-tight"
            >
              NEXUS <span className="text-indigo-400">AI</span>
            </motion.h1>
          )}
        </div>

        <nav className="flex-1 px-4 py-4 space-y-2">
          <NavItem 
            icon={<LayoutDashboard size={20} />} 
            label="Dashboard" 
            active={activeTab === 'dashboard'} 
            onClick={() => setActiveTab('dashboard')}
            collapsed={!isSidebarOpen}
          />
          <NavItem 
            icon={<Users size={20} />} 
            label="Agents" 
            active={activeTab === 'agents'} 
            onClick={() => setActiveTab('agents')}
            collapsed={!isSidebarOpen}
          />
          <NavItem 
            icon={<Network size={20} />} 
            label="Knowledge Graph" 
            active={activeTab === 'graph'} 
            onClick={() => setActiveTab('graph')}
            collapsed={!isSidebarOpen}
          />
          <NavItem 
            icon={<Settings size={20} />} 
            label="Settings" 
            active={activeTab === 'settings'} 
            onClick={() => setActiveTab('settings')}
            collapsed={!isSidebarOpen}
          />
        </nav>

        <div className="p-4 border-t border-slate-800">
          <button 
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="w-full flex items-center justify-center p-2 hover:bg-slate-800 rounded-lg transition-colors"
          >
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-20 flex items-center justify-between px-8 glass border-b border-slate-800">
          <div className="flex items-center gap-4 bg-slate-900/50 px-4 py-2 rounded-xl border border-slate-800">
            <Search size={18} className="text-slate-400" />
            <input 
              type="text" 
              placeholder="Query the Neural Mesh..." 
              className="bg-transparent border-none outline-none text-sm w-64"
            />
          </div>

          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2 px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
              <div className="pulse-dot"></div>
              <span className="text-xs font-medium text-emerald-400">SYSTEM OPERATIONAL</span>
            </div>
            <button className="relative p-2 hover:bg-slate-800 rounded-lg transition-colors">
              <Bell size={20} />
              <span className="absolute top-2 right-2 w-2 h-2 bg-indigo-500 rounded-full"></span>
            </button>
            <div className="w-10 h-10 bg-slate-800 rounded-full border border-slate-700 flex items-center justify-center font-bold">
              K
            </div>
          </div>
        </header>

        {/* Dashboard View */}
        <div className="flex-1 overflow-y-auto p-8">
          <AnimatePresence mode="wait">
            {activeTab === 'dashboard' && (
              <motion.div
                key="dashboard"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-8"
              >
                {/* Hero Stats */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <StatCard label="Active Agents" value="48" icon={<Users className="text-indigo-400" />} trend="+4 this week" />
                  <StatCard label="Tasks Completed" value="1.2k" icon={<Zap className="text-amber-400" />} trend="+12% vs last month" />
                  <StatCard label="Knowledge Nodes" value="8.4k" icon={<Network className="text-blue-400" />} trend="82 new relationships" />
                  <StatCard label="Avg. Efficiency" value="94%" icon={<Activity className="text-emerald-400" />} trend="+2.4% optimized" />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Agents List */}
                  <div className="lg:col-span-2 glass-card rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-6">
                      <h2 className="text-xl font-bold">Self-Organizing Swarm</h2>
                      <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-xl transition-all shadow-lg shadow-indigo-500/20 text-sm font-medium">
                        <Plus size={18} /> Deploy Agent
                      </button>
                    </div>
                    
                    <div className="space-y-4">
                      {AGENTS.map((agent, i) => (
                        <motion.div 
                          key={agent.id}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: i * 0.1 }}
                          className="flex items-center justify-between p-4 bg-slate-900/40 border border-slate-800/50 rounded-xl hover:border-indigo-500/30 transition-all group"
                        >
                          <div className="flex items-center gap-4">
                            <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                              agent.status === 'online' ? 'bg-emerald-500/10 text-emerald-400' : 
                              agent.status === 'busy' ? 'bg-amber-500/10 text-amber-400' : 'bg-slate-800 text-slate-500'
                            }`}>
                              <BrainCircuit size={24} />
                            </div>
                            <div>
                              <h3 className="font-semibold">{agent.name}</h3>
                              <p className="text-xs text-slate-400">{agent.type} Specialist</p>
                            </div>
                          </div>
                          <div className="flex items-center gap-8">
                            <div className="text-center">
                              <p className="text-xs text-slate-500 mb-1">Tasks</p>
                              <p className="font-bold">{agent.tasks}</p>
                            </div>
                            <div className="text-center">
                              <p className="text-xs text-slate-500 mb-1">Performance</p>
                              <p className="font-bold text-indigo-400">{agent.performance}%</p>
                            </div>
                            <ChevronRight size={20} className="text-slate-600 group-hover:text-indigo-400 transition-colors" />
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </div>

                  {/* Activity Feed */}
                  <div className="glass-card rounded-2xl p-6">
                    <h2 className="text-xl font-bold mb-6">Neural Activity</h2>
                    <div className="space-y-6">
                      {RECENT_TASKS.map((task, i) => (
                        <div key={task.id} className="relative pl-6 border-l border-slate-800 last:border-0 pb-6 last:pb-0">
                          <div className={`absolute top-0 left-[-4px] w-2 h-2 rounded-full ${
                            task.status === 'completed' ? 'bg-emerald-500' : 
                            task.status === 'processing' ? 'bg-amber-500' : 'bg-slate-600'
                          }`}></div>
                          <div className="flex justify-between items-start mb-1">
                            <h4 className="text-sm font-semibold">{task.title}</h4>
                            <span className="text-[10px] text-slate-500">{task.time}</span>
                          </div>
                          <p className="text-xs text-slate-400 mb-2">Assigned to <span className="text-indigo-400">{task.agent}</span></p>
                          <div className="flex items-center gap-2">
                            <span className={`text-[10px] px-2 py-0.5 rounded-full uppercase tracking-wider font-bold ${
                              task.status === 'completed' ? 'bg-emerald-500/10 text-emerald-400' : 
                              task.status === 'processing' ? 'bg-amber-500/10 text-amber-400' : 'bg-slate-800 text-slate-500'
                            }`}>
                              {task.status}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                    <button className="w-full mt-6 py-2 text-sm text-slate-400 hover:text-indigo-400 transition-colors flex items-center justify-center gap-2">
                      <Clock size={16} /> View All History
                    </button>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

function NavItem({ icon, label, active, onClick, collapsed }: any) {
  return (
    <button 
      onClick={onClick}
      className={`w-full flex items-center gap-3 p-3 rounded-xl transition-all duration-200 ${
        active 
          ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20' 
          : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-100'
      }`}
    >
      <div className={active ? 'text-white' : 'text-slate-400'}>{icon}</div>
      {!collapsed && <span className="font-medium">{label}</span>}
    </button>
  );
}

function StatCard({ label, value, icon, trend }: any) {
  return (
    <div className="glass-card rounded-2xl p-6 border border-slate-800/50">
      <div className="flex justify-between items-start mb-4">
        <div className="p-2 bg-slate-900 rounded-lg border border-slate-800">
          {icon}
        </div>
        <span className="text-[10px] font-bold text-emerald-400 bg-emerald-400/10 px-2 py-0.5 rounded-full">
          {trend}
        </span>
      </div>
      <h3 className="text-3xl font-bold mb-1 tracking-tight">{value}</h3>
      <p className="text-xs text-slate-500 font-medium">{label}</p>
    </div>
  );
}
