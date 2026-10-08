import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { LayoutDashboard, CalendarDays, Zap, GitCompare, ShieldAlert, Database, Menu, X } from 'lucide-react';
import { useState } from 'react';

import Dashboard from './pages/Dashboard';
import Timetable from './pages/Timetable';
import Simulation from './pages/Simulation';
import Comparison from './pages/Comparison';
import Constraints from './pages/Constraints';
import DataManagement from './pages/DataManagement';

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Timetable', path: '/timetable', icon: CalendarDays },
    { name: 'Simulation', path: '/simulation', icon: Zap },
    { name: 'Comparison', path: '/comparison', icon: GitCompare },
    { name: 'Constraints', path: '/constraints', icon: ShieldAlert },
    { name: 'Data', path: '/data', icon: Database },
  ];

  return (
    <BrowserRouter>
      <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden font-sans">
        {/* Sidebar */}
        <aside className={`w-64 bg-slate-900 border-r border-slate-800 flex-shrink-0 transition-transform duration-300 ease-in-out ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0 fixed md:static h-full z-40`}>
          <div className="h-16 flex items-center justify-between px-6 border-b border-slate-800">
            <div className="flex items-center">
              <Zap className="w-6 h-6 text-blue-500 mr-2" />
              <span className="text-xl font-bold tracking-tight text-white">IntelliTime</span>
            </div>
            <button className="md:hidden text-slate-400 hover:text-white" onClick={() => setSidebarOpen(false)}>
              <X className="w-5 h-5" />
            </button>
          </div>
          <nav className="p-4 space-y-2 overflow-y-auto h-[calc(100vh-4rem)]">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors duration-150 ${
                    isActive
                      ? 'bg-blue-600/15 text-blue-400'
                      : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                  }`
                }
                onClick={() => setSidebarOpen(false)}
              >
                <item.icon className="w-5 h-5 mr-3" />
                {item.name}
              </NavLink>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden bg-slate-950">
          <header className="h-16 bg-slate-900/50 backdrop-blur-md border-b border-slate-800 flex items-center px-4 md:px-8 justify-between sticky top-0 z-30">
            <div className="flex items-center">
              <button
                className="p-2 -ml-2 mr-2 md:hidden text-slate-400 hover:text-white rounded-md hover:bg-slate-800"
                onClick={() => setSidebarOpen(!sidebarOpen)}
              >
                <Menu className="w-6 h-6" />
              </button>
              <h1 className="text-lg font-semibold text-white truncate hidden sm:block">Timetable Optimizer V2</h1>
            </div>
            <div className="flex items-center space-x-4">
               <span className="flex items-center text-xs px-2.5 py-1 bg-green-500/10 text-green-400 rounded-full font-medium border border-green-500/20">
                 <span className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span>
                 API Connected
               </span>
            </div>
          </header>
          
          <main className="flex-1 overflow-auto p-4 md:p-8">
            <div className="max-w-7xl mx-auto">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/timetable" element={<Timetable />} />
                <Route path="/simulation" element={<Simulation />} />
                <Route path="/comparison" element={<Comparison />} />
                <Route path="/constraints" element={<Constraints />} />
                <Route path="/data" element={<DataManagement />} />
              </Routes>
            </div>
          </main>
        </div>
        
        {/* Overlay for mobile */}
        {sidebarOpen && (
          <div 
            className="fixed inset-0 bg-slate-950/80 z-30 md:hidden backdrop-blur-sm transition-opacity"
            onClick={() => setSidebarOpen(false)}
          />
        )}
      </div>
    </BrowserRouter>
  );
}
