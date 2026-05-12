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

// Mock Data for Demo
const AGENTS = [
  { id: '1', name: 'Sales Assistant', type: 'Sales', status: 'online', tasks: 12, performance: 98, color: 'indigo' },
  { id: '2', name: 'Legal Analyst', type: 'Legal', status: 'online', tasks: 8, performance: 95, color: 'blue' },
  { id: '3', name: 'Dev Architect', type: 'Engineering', status: 'busy', tasks: 24, performance: 99, color: 'purple' },
  { id: '4', name: 'Market Strategist', type: 'Marketing', status: 'offline', tasks: 0, performance: 92, color: 'slate' },
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
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans selection:bg-indigo-500/30">
      <div className="aurora"></div>
      
      {/* Sidebar */}
      <motion.aside 
        initial={false}
        animate={{ width: isSidebarOpen ? 280 : 88 }}
        className="glass border-r border-slate-800/50 flex flex-col z-50 transition-all duration-300"
      >
        <div className="p-6 flex items-center gap-4 mb-4">
          <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-500/40 shrink-0">
            <BrainCircuit className="text-white" size={28} />
          </div>
          {isSidebarOpen && (
            <motion.div 
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex flex-col"
            >
              <h1 className="font-bold text-xl tracking-tight leading-none mb-1">
                NEXUS <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">OS</span>
              </h1>
              <span className="text-[10px] font-bold text-slate-500 tracking-widest uppercase">Neural Mesh v3.0</span>
            </motion.div>
          )}
        </div>

        <nav className="flex-1 px-4 space-y-2">
          <NavItem 
            icon={<LayoutDashboard size={22} />} 
            label="Neural Hub" 
            active={activeTab === 'dashboard'} 
            onClick={() => setActiveTab('dashboard')}
            collapsed={!isSidebarOpen}
          />
          <NavItem 
            icon={<Users size={22} />} 
            label="Agent Registry" 
            active={activeTab === 'agents'} 
            onClick={() => setActiveTab('agents')}
            collapsed={!isSidebarOpen}
          />
          <NavItem 
            icon={<Network size={22} />} 
            label="Synaptic Graph" 
            active={activeTab === 'graph'} 
            onClick={() => setActiveTab('graph')}
            collapsed={!isSidebarOpen}
          />
          <NavItem 
            icon={<Database size={22} />} 
            label="Vector Memory" 
            active={activeTab === 'memory'} 
            onClick={() => setActiveTab('memory')}
            collapsed={!isSidebarOpen}
          />
          <div className="h-px bg-slate-800/50 mx-2 my-6" />
          <NavItem 
            icon={<Settings size={22} />} 
            label="Core Config" 
            active={activeTab === 'settings'} 
            onClick={() => setActiveTab('settings')}
            collapsed={!isSidebarOpen}
          />
        </nav>

        <div className="p-4 mt-auto">
          <div className={`glass-card p-4 rounded-2xl border border-slate-800/50 overflow-hidden relative group ${!isSidebarOpen && 'hidden'}`}>
            <div className="absolute top-0 right-0 p-2 opacity-10 group-hover:opacity-20 transition-opacity">
              <Zap size={48} className="text-indigo-500" />
            </div>
            <p className="text-xs font-bold text-indigo-400 mb-1">PRO PLAN</p>
            <p className="text-[10px] text-slate-400 mb-3 leading-relaxed">Upgrade for unlimited agent deployment.</p>
            <button className="w-full py-2 bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 rounded-xl text-[10px] font-bold transition-all">
              UPGRADE NOW
            </button>
          </div>
          <button 
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="w-full flex items-center justify-center p-3 hover:bg-slate-800/50 text-slate-400 rounded-xl mt-4 transition-colors"
          >
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden relative">
        {/* Header */}
        <header className="h-20 flex items-center justify-between px-8 glass-card border-b border-slate-800/50 z-10">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3 bg-slate-900/80 px-4 py-2.5 rounded-2xl border border-slate-800/50 focus-within:border-indigo-500/50 transition-all shadow-inner">
              <Search size={18} className="text-slate-500" />
              <input 
                type="text" 
                placeholder="Search the Neural Mesh..." 
                className="bg-transparent border-none outline-none text-sm w-72 placeholder:text-slate-600"
              />
            </div>
          </div>

          <div className="flex items-center gap-6">
            <div className="hidden xl:flex items-center gap-4">
              <HeaderMetric icon={<Cpu size={14} />} label="CPU" value="24%" />
              <HeaderMetric icon={<Activity size={14} />} label="MEM" value="1.2GB" />
              <HeaderMetric icon={<Globe size={14} />} label="LAT" value="14ms" />
            </div>
            <div className="w-px h-8 bg-slate-800" />
            <div className="flex items-center gap-3">
              <button className="relative p-2.5 hover:bg-slate-800/80 rounded-xl transition-all border border-transparent hover:border-slate-700">
                <Bell size={20} className="text-slate-400" />
                <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-indigo-500 rounded-full border-2 border-slate-950"></span>
              </button>
              <div className="flex items-center gap-3 pl-2">
                <div className="text-right hidden sm:block">
                  <p className="text-xs font-bold leading-none">Admin Node</p>
                  <p className="text-[10px] text-emerald-400 mt-1 uppercase font-bold tracking-tighter">Verified Alpha</p>
                </div>
                <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl border border-white/10 flex items-center justify-center font-bold text-white shadow-lg">
                  K
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard View */}
        <div className="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <AnimatePresence mode="wait">
            {activeTab === 'dashboard' && (
              <motion.div
                key="dashboard"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="max-w-7xl mx-auto space-y-8"
              >
                <div className="flex flex-col gap-2">
                  <h2 className="text-4xl font-black tracking-tight">System <span className="text-indigo-400">Overview</span></h2>
                  <p className="text-slate-400 text-sm">Real-time status of your self-organizing agent mesh.</p>
                </div>

                {/* Hero Stats */}
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
                  <StatCard label="Active Agents" value="48" icon={<Users className="text-indigo-400" />} trend="+4" color="indigo" />
                  <StatCard label="Tasks/Hour" value="1.2k" icon={<Zap className="text-amber-400" />} trend="+12%" color="amber" />
                  <StatCard label="Total Nodes" value="8.4k" icon={<Network className="text-purple-400" />} trend="+82" color="purple" />
                  <StatCard label="System Integrity" value="94%" icon={<ShieldCheck className="text-emerald-400" />} trend="Stable" color="emerald" />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                  {/* Agents List */}
                  <div className="lg:col-span-8 glass-card rounded-[2.5rem] p-8 border border-slate-800/30">
                    <div className="flex items-center justify-between mb-8">
                      <div>
                        <h2 className="text-2xl font-bold mb-1">Neural Swarm</h2>
                        <p className="text-xs text-slate-500">Autonomous agents currently active in the mesh.</p>
                      </div>
                      <button className="flex items-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-2xl transition-all shadow-xl shadow-indigo-600/30 text-sm font-bold active:scale-95">
                        <Plus size={20} /> Deploy New Agent
                      </button>
                    </div>
                    
                    <div className="grid gap-4">
                      {AGENTS.map((agent, i) => (
                        <motion.div 
                          key={agent.id}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: i * 0.1 }}
                          className="flex items-center justify-between p-5 bg-slate-900/30 border border-slate-800/40 rounded-3xl hover:bg-indigo-500/[0.03] hover:border-indigo-500/30 transition-all group cursor-pointer"
                        >
                          <div className="flex items-center gap-5">
                            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center shadow-lg transition-transform group-hover:scale-110 duration-300 ${
                              agent.status === 'online' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 
                              agent.status === 'busy' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' : 
                              'bg-slate-800 text-slate-500 border border-slate-700'
                            }`}>
                              <BrainCircuit size={28} />
                            </div>
                            <div>
                              <h3 className="font-bold text-lg group-hover:text-indigo-400 transition-colors">{agent.name}</h3>
                              <div className="flex items-center gap-2">
                                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">{agent.type}</span>
                                <div className="w-1 h-1 rounded-full bg-slate-700" />
                                <div className="flex items-center gap-1.5">
                                  <div className={`w-1.5 h-1.5 rounded-full ${agent.status === 'online' ? 'bg-emerald-500' : agent.status === 'busy' ? 'bg-amber-500' : 'bg-slate-500'}`} />
                                  <span className="text-[10px] font-bold uppercase">{agent.status}</span>
                                </div>
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center gap-10">
                            <div className="text-right">
                              <p className="text-[10px] font-bold text-slate-500 mb-1 uppercase">Tasks</p>
                              <p className="font-black text-xl">{agent.tasks}</p>
                            </div>
                            <div className="text-right">
                              <p className="text-[10px] font-bold text-slate-500 mb-1 uppercase">Performance</p>
                              <p className="font-black text-xl text-indigo-400">{agent.performance}%</p>
                            </div>
                            <div className="w-10 h-10 flex items-center justify-center rounded-full border border-slate-800 group-hover:bg-indigo-500 group-hover:border-indigo-500 transition-all">
                              <ChevronRight size={18} className="group-hover:text-white" />
                            </div>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </div>

                  {/* Activity Feed */}
                  <div className="lg:col-span-4 glass-card rounded-[2.5rem] p-8 border border-slate-800/30">
                    <div className="flex items-center justify-between mb-8">
                      <h2 className="text-2xl font-bold">Live Activity</h2>
                      <div className="px-2 py-1 bg-emerald-500/10 rounded-lg flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                        <span className="text-[10px] font-bold text-emerald-500 uppercase tracking-tighter">Live</span>
                      </div>
                    </div>
                    <div className="space-y-8 relative">
                      <div className="absolute left-1.5 top-2 bottom-2 w-0.5 bg-slate-800/50" />
                      {RECENT_TASKS.map((task) => (
                        <div key={task.id} className="relative pl-8">
                          <div className={`absolute top-1.5 left-0 w-3 h-3 rounded-full border-2 border-slate-950 z-10 ${
                            task.status === 'completed' ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]' : 
                            task.status === 'processing' ? 'bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.5)]' : 'bg-slate-700'
                          }`} />
                          <div className="flex justify-between items-start mb-1">
                            <h4 className="text-sm font-bold tracking-tight">{task.title}</h4>
                            <span className="text-[10px] font-bold text-slate-500 font-mono">{task.time}</span>
                          </div>
                          <p className="text-[11px] text-slate-400 mb-3">
                            Delegated to <span className="text-indigo-400 font-bold">{task.agent}</span>
                          </p>
                          <div className={`inline-flex items-center px-3 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest ${
                            task.status === 'completed' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/10' : 
                            task.status === 'processing' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/10' : 'bg-slate-800 text-slate-500'
                          }`}>
                            {task.status}
                          </div>
                        </div>
                      ))}
                    </div>
                    <button className="w-full mt-10 py-4 text-xs font-bold text-slate-500 hover:text-indigo-400 hover:bg-indigo-400/5 border border-slate-800 rounded-2xl transition-all flex items-center justify-center gap-3 active:scale-95">
                      <Clock size={16} /> VIEW AUDIT LOG
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
      className={`w-full flex items-center gap-4 p-4 rounded-2xl transition-all duration-300 relative group overflow-hidden ${
        active 
          ? 'text-white' 
          : 'text-slate-500 hover:text-slate-200'
      }`}
    >
      {active && (
        <motion.div 
          layoutId="activeNav"
          className="absolute inset-0 bg-gradient-to-r from-indigo-600 to-indigo-500 shadow-lg shadow-indigo-600/30"
          initial={false}
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
        />
      )}
      <div className={`relative z-10 transition-transform group-hover:scale-110 ${active ? 'text-white' : 'text-slate-500'}`}>
        {icon}
      </div>
      {!collapsed && (
        <span className={`relative z-10 font-bold text-sm tracking-tight ${active ? 'opacity-100' : 'opacity-80'}`}>
          {label}
        </span>
      )}
      {active && !collapsed && (
        <motion.div 
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="absolute right-4 w-1.5 h-1.5 rounded-full bg-white shadow-[0_0_10px_rgba(255,255,255,0.8)] z-10"
        />
      )}
    </button>
  );
}

function HeaderMetric({ icon, label, value }: any) {
  return (
    <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-900/50 rounded-xl border border-slate-800/50">
      <div className="text-indigo-400">{icon}</div>
      <span className="text-[10px] font-bold text-slate-500">{label}</span>
      <span className="text-[11px] font-black text-slate-100">{value}</span>
    </div>
  );
}

function StatCard({ label, value, icon, trend, color }: any) {
  const colors: any = {
    indigo: 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20',
    amber: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
    purple: 'text-purple-400 bg-purple-500/10 border-purple-500/20',
    emerald: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
  };

  return (
    <div className="glass-card rounded-3xl p-6 border border-slate-800/40 hover:border-indigo-500/20 transition-all group overflow-hidden relative">
      <div className="absolute -right-4 -bottom-4 opacity-[0.03] group-hover:opacity-[0.06] transition-opacity rotate-12 group-hover:scale-125 duration-700">
        {icon}
      </div>
      <div className="flex justify-between items-start mb-6">
        <div className={`p-3 rounded-2xl border ${colors[color]}`}>
          {icon}
        </div>
        <div className={`px-2 py-1 rounded-lg text-[10px] font-black border ${colors[color]}`}>
          {trend}
        </div>
      </div>
      <h3 className="text-4xl font-black mb-1 tracking-tighter leading-none">{value}</h3>
      <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">{label}</p>
    </div>
  );
}
