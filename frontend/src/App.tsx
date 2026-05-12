import { useState, useEffect } from 'react';
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
  Database,
  Loader2
} from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://nexus-backend-production-a079.up.railway.app';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [agents, setAgents] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isDeploying, setIsDeploying] = useState(false);
  
  // Form State
  const [newAgent, setNewAgent] = useState({
    name: '',
    type: 'sales',
    description: '',
    metadata: {}
  });

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/`);
      if (response.ok) {
        const data = await response.json();
        setAgents(data);
      }
    } catch (error) {
      console.error('Failed to fetch agents:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeployAgent = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsDeploying(true);
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newAgent)
      });
      
      if (response.ok) {
        await fetchAgents();
        setIsModalOpen(false);
        setNewAgent({ name: '', type: 'sales', description: '', metadata: {} });
      } else {
        const err = await response.json();
        alert(`Deployment failed: ${err.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Deployment error:', error);
      alert('Failed to connect to Neural Mesh backend.');
    } finally {
      setIsDeploying(false);
    }
  };

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
          <NavItem icon={<LayoutDashboard size={22} />} label="Dashboard" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} collapsed={!isSidebarOpen} />
          <NavItem icon={<Users size={22} />} label="Agents" active={activeTab === 'agents'} onClick={() => setActiveTab('agents')} collapsed={!isSidebarOpen} />
          <NavItem icon={<Network size={22} />} label="Neural Graph" active={activeTab === 'graph'} onClick={() => setActiveTab('graph')} collapsed={!isSidebarOpen} />
          <NavItem icon={<Database size={22} />} label="Memory" active={activeTab === 'memory'} onClick={() => setActiveTab('memory')} collapsed={!isSidebarOpen} />
          <div className="h-px bg-slate-800/50 mx-2 my-6" />
          <NavItem icon={<Settings size={22} />} label="Settings" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} collapsed={!isSidebarOpen} />
        </nav>

        <div className="p-4">
          <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="w-full flex items-center justify-center p-3 hover:bg-slate-800/50 text-slate-400 rounded-xl transition-colors cursor-pointer">
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 relative z-10">
        <header className="h-20 flex items-center justify-between px-8 bg-slate-900/30 backdrop-blur-md border-b border-slate-800/50">
          <div className="flex items-center gap-4 bg-slate-950/50 px-4 py-2 rounded-xl border border-slate-800/50 focus-within:border-indigo-500/50 transition-all">
            <Search size={18} className="text-slate-500" />
            <input type="text" placeholder="Search neural mesh..." className="bg-transparent border-none outline-none text-sm w-64 text-slate-200" />
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

        <div className="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <AnimatePresence mode="wait">
            {activeTab === 'dashboard' ? (
              <motion.div key="dashboard" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="max-w-7xl mx-auto space-y-8">
                <div className="flex flex-col gap-1">
                  <h2 className="text-3xl font-bold">Neural Hub</h2>
                  <p className="text-slate-400 text-sm">Orchestrate your autonomous agent swarms.</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <StatCard label="Active Agents" value={agents.length.toString()} icon={<Users size={24} />} trend="+4" color="indigo" />
                  <StatCard label="Tasks Completed" value="1,240" icon={<Zap size={24} />} trend="+12%" color="amber" />
                  <StatCard label="Knowledge Nodes" value="8.4k" icon={<Network size={24} />} trend="+82" color="purple" />
                  <StatCard label="System Integrity" value="98%" icon={<ShieldCheck size={24} />} trend="Stable" color="emerald" />
                </div>

                <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                  <div className="xl:col-span-2 bg-slate-900/40 rounded-3xl p-8 border border-slate-800/50">
                    <div className="flex items-center justify-between mb-8">
                      <h3 className="text-xl font-bold">Active Swarm</h3>
                      <button 
                        onClick={() => setIsModalOpen(true)}
                        className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 rounded-xl text-sm font-bold shadow-lg shadow-indigo-600/20 transition-all cursor-pointer flex items-center gap-2"
                      >
                        <Plus size={18} /> Deploy Agent
                      </button>
                    </div>
                    
                    {isLoading ? (
                      <div className="flex flex-col items-center justify-center py-20 text-slate-500">
                        <Loader2 className="animate-spin mb-4" size={32} />
                        <p>Syncing with Neural Mesh...</p>
                      </div>
                    ) : agents.length === 0 ? (
                      <div className="flex flex-col items-center justify-center py-20 bg-slate-950/20 rounded-2xl border border-dashed border-slate-800">
                        <Users size={48} className="text-slate-800 mb-4" />
                        <p className="text-slate-500 text-sm">No agents active. Deploy your first intelligence node.</p>
                      </div>
                    ) : (
                      <div className="grid gap-4">
                        {agents.map((agent) => (
                          <div key={agent.id} className="flex items-center justify-between p-4 bg-slate-950/40 rounded-2xl border border-slate-800/50 hover:border-indigo-500/30 transition-all cursor-pointer group">
                            <div className="flex items-center gap-4">
                              <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-slate-900 border border-slate-800 group-hover:border-indigo-500/50 transition-all">
                                <BrainCircuit size={24} className="text-indigo-400" />
                              </div>
                              <div>
                                <p className="font-bold">{agent.name}</p>
                                <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">{agent.type}</p>
                              </div>
                            </div>
                            <div className="flex items-center gap-8 text-right">
                              <div className="hidden sm:block">
                                <p className="text-[10px] text-slate-500 uppercase font-bold">Tasks</p>
                                <p className="font-bold">{agent.tasks_completed || 0}</p>
                              </div>
                              <div>
                                <p className="text-[10px] text-slate-500 uppercase font-bold">Status</p>
                                <p className="font-bold text-emerald-400 uppercase text-[11px] tracking-tight">{agent.status}</p>
                              </div>
                              <ChevronRight size={18} className="text-slate-600 group-hover:text-indigo-400" />
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  <div className="bg-slate-900/40 rounded-3xl p-8 border border-slate-800/50">
                    <h3 className="text-xl font-bold mb-8">Recent Activity</h3>
                    <div className="space-y-6">
                      {[1, 2, 3].map((i) => (
                        <div key={i} className="flex gap-4">
                          <div className="mt-1.5 w-2 h-2 rounded-full shrink-0 bg-emerald-500" />
                          <div>
                            <p className="text-sm font-bold">System Pulse detected</p>
                            <p className="text-xs text-slate-500">Neural network synced • {i * 5}m ago</p>
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

      {/* Deploy Modal */}
      <AnimatePresence>
        {isModalOpen && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
            <motion.div 
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }} 
              exit={{ opacity: 0 }}
              onClick={() => setIsModalOpen(false)}
              className="absolute inset-0 bg-slate-950/80 backdrop-blur-sm"
            />
            <motion.div 
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="relative w-full max-w-lg bg-slate-900 rounded-[2rem] border border-slate-800 shadow-2xl overflow-hidden"
            >
              <div className="p-8">
                <div className="flex items-center justify-between mb-8">
                  <h3 className="text-2xl font-bold">Deploy Agent</h3>
                  <button onClick={() => setIsModalOpen(false)} className="p-2 hover:bg-slate-800 rounded-full transition-colors text-slate-400">
                    <X size={20} />
                  </button>
                </div>

                <form onSubmit={handleDeployAgent} className="space-y-6">
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">Agent Name</label>
                    <input 
                      required
                      value={newAgent.name}
                      onChange={(e) => setNewAgent({...newAgent, name: e.target.value})}
                      placeholder="e.g. Sales Intelligence Alpha"
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm focus:border-indigo-500 outline-none transition-all"
                    />
                  </div>

                  <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">Specialization</label>
                    <select 
                      value={newAgent.type}
                      onChange={(e) => setNewAgent({...newAgent, type: e.target.value})}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm focus:border-indigo-500 outline-none transition-all appearance-none"
                    >
                      <option value="sales">Sales & Marketing</option>
                      <option value="legal">Legal Analyst</option>
                      <option value="engineering">Software Engineer</option>
                      <option value="finance">Financial Strategist</option>
                      <option value="custom">Custom Agent</option>
                    </select>
                  </div>

                  <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">Description</label>
                    <textarea 
                      value={newAgent.description}
                      onChange={(e) => setNewAgent({...newAgent, description: e.target.value})}
                      placeholder="Define the agent's primary directive..."
                      rows={3}
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm focus:border-indigo-500 outline-none transition-all resize-none"
                    />
                  </div>

                  <button 
                    disabled={isDeploying}
                    className="w-full py-4 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-500 rounded-2xl font-bold shadow-lg shadow-indigo-600/20 transition-all flex items-center justify-center gap-3"
                  >
                    {isDeploying ? (
                      <>
                        <Loader2 className="animate-spin" size={20} />
                        DEPLOYING TO MESH...
                      </>
                    ) : (
                      <>
                        <Zap size={20} />
                        INITIALIZE DEPLOYMENT
                      </>
                    )}
                  </button>
                </form>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}

function NavItem({ icon, label, active, onClick, collapsed }: any) {
  return (
    <button onClick={onClick} className={`w-full flex items-center gap-4 p-4 rounded-xl transition-all duration-200 cursor-pointer ${active ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20' : 'text-slate-500 hover:bg-slate-800/50 hover:text-slate-200'}`}>
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
