import { useState } from 'react';
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
  X,
  Cpu,
  ShieldCheck,
  Globe,
  Database
} from 'lucide-react';

// Mock Data
const AGENTS = [
  { id: '1', name: 'Sales Assistant', type: 'Sales', status: 'online', tasks: 12, performance: 98, color: '#6366f1' },
  { id: '2', name: 'Legal Analyst', type: 'Legal', status: 'online', tasks: 8, performance: 95, color: '#3b82f6' },
  { id: '3', name: 'Dev Architect', type: 'Engineering', status: 'busy', tasks: 24, performance: 99, color: '#a855f7' },
  { id: '4', name: 'Market Strategist', type: 'Marketing', status: 'offline', tasks: 0, performance: 92, color: '#64748b' },
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
    <div className="flex h-screen bg-[#020617] text-slate-100 overflow-hidden font-sans selection:bg-indigo-500/30">
      {/* Background Glows */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-indigo-500/10 blur-[120px] rounded-full" />
        <div className="absolute -bottom-[10%] -right-[10%] w-[40%] h-[40%] bg-purple-500/10 blur-[120px] rounded-full" />
      </div>
      
      {/* Sidebar */}
      <motion.aside 
        initial={false}
        animate={{ width: isSidebarOpen ? 280 : 88 }}
        className="relative z-50 bg-slate-900/50 backdrop-blur-xl border-r border-slate-800/50 flex flex-col transition-all duration-300"
      >
        <div className="p-6 flex items-center gap-4 mb-8">
          <div className="w-12 h-12 bg-indigo-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-500/40 shrink-0">
            <BrainCircuit className="text-white" size={28} />
          </div>
          {isSidebarOpen && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex flex-col">
              <span className="font-black text-xl tracking-tight">NEXUS <span className="text-indigo-400">OS</span></span>
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Alpha v3.0</span>
            </motion.div>
          )}
        </div>

        <nav className="flex-1 px-4 space-y-2">
          <NavItem 
            icon={<LayoutDashboard size={22} />} 
            label="Dashboard" 
            active={activeTab === 'dashboard'} 
            onClick={() => setActiveTab('dashboard')}
            collapsed={!isSidebarOpen}
          />
          <NavItem 
            icon={<Users size={22} />} 
            label="Agents" 
            active={activeTab === 'agents'} 
            onClick={() => setActiveTab('agents')}
            collapsed={!isSidebarOpen}
          />
          <NavItem 
            icon={<Network size={22} />} 
            label="Neural Graph" 
            active={activeTab === 'graph'} 
            onClick={() => setActiveTab('graph')}
            collapsed={!isSidebarOpen}
          />
          <NavItem 
            icon={<Database size={22} />} 
            label="Memory" 
            active={activeTab === 'memory'} 
            onClick={() => setActiveTab('memory')}
            collapsed={!isSidebarOpen}
          />
          <div className="h-px bg-slate-800/50 mx-2 my-6" />
          <NavItem 
            icon={<Settings size={22} />} 
            label="Settings" 
            active={activeTab === 'settings'} 
            onClick={() => setActiveTab('settings')}
            collapsed={!isSidebarOpen}
          />
        </nav>

        <div className="p-4">
          <button 
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="w-full flex items-center justify-center p-3 hover:bg-slate-800/50 text-slate-400 rounded-xl transition-colors cursor-pointer"
          >
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 relative z-10">
        {/* Header */}
        <header className="h-20 flex items-center justify-between px-8 bg-slate-900/30 backdrop-blur-md border-b border-slate-800/50">
          <div className="flex items-center gap-4 bg-slate-950/50 px-4 py-2 rounded-xl border border-slate-800/50 focus-within:border-indigo-500/50 transition-all">
            <Search size={18} className="text-slate-500" />
            <input 
              type="text" 
              placeholder="Search neural mesh..." 
              className="bg-transparent border-none outline-none text-sm w-64 text-slate-200"
            />
          </div>

          <div className="flex items-center gap-6">
            <div className="hidden lg:flex items-center gap-4">
              <HeaderMetric icon={<Cpu size={14} />} label="CPU" value="12%" />
              <HeaderMetric icon={<Activity size={14} />} label="MEM" value="0.8GB" />
            </div>
            <div className="flex items-center gap-3">
              <button className="p-2.5 hover:bg-slate-800 rounded-xl transition-all relative cursor-pointer">
                <Bell size={20} className="text-slate-400" />
                <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-indigo-500 rounded-full border-2 border-slate-900"></span>
              </button>
              <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center font-bold shadow-lg">K</div>
            </div>
          </div>
        </header>

        {/* Dashboard View */}
        <div className="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <AnimatePresence mode="wait">
            {activeTab === 'dashboard' ? (
              <motion.div
                key="dashboard"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="max-w-7xl mx-auto space-y-8"
              >
                <div className="flex flex-col gap-1">
                  <h2 className="text-3xl font-bold">Neural Hub</h2>
                  <p className="text-slate-400 text-sm">Orchestrate your autonomous agent swarms.</p>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <StatCard label="Active Agents" value="48" icon={<Users size={24} />} trend="+4" color="indigo" />
                  <StatCard label="Tasks Completed" value="1,240" icon={<Zap size={24} />} trend="+12%" color="amber" />
                  <StatCard label="Knowledge Nodes" value="8.4k" icon={<Network size={24} />} trend="+82" color="purple" />
                  <StatCard label="System Integrity" value="98%" icon={<ShieldCheck size={24} />} trend="Stable" color="emerald" />
                </div>

                <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                  {/* Agent List */}
                  <div className="xl:col-span-2 bg-slate-900/40 rounded-3xl p-8 border border-slate-800/50">
                    <div className="flex items-center justify-between mb-8">
                      <h3 className="text-xl font-bold">Active Swarm</h3>
                      <button className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 rounded-xl text-sm font-bold shadow-lg shadow-indigo-600/20 transition-all cursor-pointer">
                        Deploy Agent
                      </button>
                    </div>
                    <div className="grid gap-4">
                      {AGENTS.map((agent) => (
                        <div key={agent.id} className="flex items-center justify-between p-4 bg-slate-950/40 rounded-2xl border border-slate-800/50 hover:border-indigo-500/30 transition-all cursor-pointer group">
                          <div className="flex items-center gap-4">
                            <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-slate-900 border border-slate-800 group-hover:border-indigo-500/50 transition-all">
                              <BrainCircuit size={24} style={{ color: agent.color }} />
                            </div>
                            <div>
                              <p className="font-bold">{agent.name}</p>
                              <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">{agent.type}</p>
                            </div>
                          </div>
                          <div className="flex items-center gap-8 text-right">
                            <div className="hidden sm:block">
                              <p className="text-[10px] text-slate-500 uppercase font-bold">Tasks</p>
                              <p className="font-bold">{agent.tasks}</p>
                            </div>
                            <div>
                              <p className="text-[10px] text-slate-500 uppercase font-bold">Efficiency</p>
                              <p className="font-bold text-indigo-400">{agent.performance}%</p>
                            </div>
                            <ChevronRight size={18} className="text-slate-600 group-hover:text-indigo-400" />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Activity */}
                  <div className="bg-slate-900/40 rounded-3xl p-8 border border-slate-800/50">
                    <h3 className="text-xl font-bold mb-8">Recent Activity</h3>
                    <div className="space-y-6">
                      {RECENT_TASKS.map((task) => (
                        <div key={task.id} className="flex gap-4">
                          <div className={`mt-1.5 w-2 h-2 rounded-full shrink-0 ${
                            task.status === 'completed' ? 'bg-emerald-500' : 'bg-amber-500'
                          }`} />
                          <div>
                            <p className="text-sm font-bold">{task.title}</p>
                            <p className="text-xs text-slate-500">by {task.agent} • {task.time}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                    <button className="w-full mt-10 py-3 bg-slate-800/50 hover:bg-slate-800 rounded-xl text-xs font-bold text-slate-400 transition-all cursor-pointer">
                      View Full Audit Log
                    </button>
                  </div>
                </div>
              </motion.div>
            ) : (
              <div className="flex items-center justify-center h-full text-slate-500 italic">
                {activeTab} view is currently under development.
              </div>
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
      onClick={(e) => {
        e.preventDefault();
        onClick();
      }}
      className={`w-full flex items-center gap-4 p-4 rounded-xl transition-all duration-200 cursor-pointer ${
        active 
          ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20' 
          : 'text-slate-500 hover:bg-slate-800/50 hover:text-slate-200'
      }`}
    >
      <div className="shrink-0">{icon}</div>
      {!collapsed && <span className="font-bold text-sm">{label}</span>}
    </button>
  );
}

function HeaderMetric({ icon, label, value }: any) {
  return (
    <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-900/50 rounded-lg border border-slate-800/50">
      <div className="text-indigo-400">{icon}</div>
      <span className="text-[10px] font-bold text-slate-500">{label}</span>
      <span className="text-[11px] font-bold">{value}</span>
    </div>
  );
}

function StatCard({ label, value, icon, trend, color }: any) {
  const colorMap: any = {
    indigo: 'text-indigo-400 bg-indigo-400/10',
    amber: 'text-amber-400 bg-amber-400/10',
    purple: 'text-purple-400 bg-purple-400/10',
    emerald: 'text-emerald-400 bg-emerald-400/10'
  };

  return (
    <div className="bg-slate-900/40 rounded-3xl p-6 border border-slate-800/50 hover:border-indigo-500/30 transition-all">
      <div className="flex justify-between items-start mb-4">
        <div className={`p-3 rounded-2xl ${colorMap[color]}`}>{icon}</div>
        <span className={`text-[10px] font-bold px-2 py-1 rounded-lg ${colorMap[color]}`}>{trend}</span>
      </div>
      <p className="text-3xl font-bold">{value}</p>
      <p className="text-xs text-slate-500 font-bold uppercase tracking-widest">{label}</p>
    </div>
  );
}
