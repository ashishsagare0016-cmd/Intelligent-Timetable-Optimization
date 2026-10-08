import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import { LayoutDashboard, CalendarDays, Zap, GitCompare, ShieldAlert, Database, Menu, X, Sun, Moon } from 'lucide-react';
import { useState, useEffect } from 'react';

import Dashboard from './pages/Dashboard';
import Timetable from './pages/Timetable';
import Simulation from './pages/Simulation';
import Comparison from './pages/Comparison';
import Constraints from './pages/Constraints';
import DataManagement from './pages/DataManagement';

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('theme');
    return saved ? saved === 'dark' : true;
  });

  useEffect(() => {
    const root = document.documentElement;
    if (darkMode) {
      root.classList.remove('light');
      localStorage.setItem('theme', 'dark');
    } else {
      root.classList.add('light');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

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
      <div className="flex h-screen overflow-hidden" style={{ background: 'var(--bg-base)', color: 'var(--text-primary)' }}>
        {/* Sidebar */}
        <aside
          className={`w-64 flex-shrink-0 transition-transform duration-300 ease-in-out ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0 fixed md:static h-full z-40`}
          style={{ background: 'var(--bg-surface)', borderRight: '1px solid var(--border-color)' }}
        >
          <div className="h-16 flex items-center justify-between px-6" style={{ borderBottom: '1px solid var(--border-color)' }}>
            <div className="flex items-center">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center mr-3 shadow-lg shadow-blue-500/20">
                <Zap className="w-4 h-4 text-white" />
              </div>
              <span className="text-lg font-bold tracking-tight" style={{ color: 'var(--text-primary)' }}>IntelliTime</span>
            </div>
            <button className="md:hidden" style={{ color: 'var(--text-secondary)' }} onClick={() => setSidebarOpen(false)}>
              <X className="w-5 h-5" />
            </button>
          </div>

          <nav className="p-4 space-y-1 overflow-y-auto h-[calc(100vh-4rem)]">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center px-4 py-2.5 text-sm font-medium rounded-lg transition-all duration-150 ${
                    isActive
                      ? 'bg-blue-600/15 text-blue-500 shadow-sm'
                      : 'hover:bg-blue-600/5'
                  }`
                }
                style={({ isActive }) => ({
                  color: isActive ? undefined : 'var(--text-secondary)',
                })}
                onClick={() => setSidebarOpen(false)}
              >
                <item.icon className="w-[18px] h-[18px] mr-3" />
                {item.name}
              </NavLink>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
          <header
            className="h-14 flex items-center px-4 md:px-6 justify-between sticky top-0 z-30 backdrop-blur-md"
            style={{ background: 'var(--bg-surface)', borderBottom: '1px solid var(--border-color)' }}
          >
            <div className="flex items-center">
              <button
                className="p-2 -ml-2 mr-2 md:hidden rounded-md"
                style={{ color: 'var(--text-secondary)' }}
                onClick={() => setSidebarOpen(!sidebarOpen)}
              >
                <Menu className="w-5 h-5" />
              </button>
              <h1 className="text-base font-semibold hidden sm:block" style={{ color: 'var(--text-primary)' }}>
                Timetable Optimizer
              </h1>
            </div>
            <div className="flex items-center gap-3">
              <span className="flex items-center text-xs px-2.5 py-1 rounded-full font-medium"
                style={{ background: 'rgba(34,197,94,0.1)', color: '#22c55e', border: '1px solid rgba(34,197,94,0.2)' }}>
                <span className="w-1.5 h-1.5 rounded-full mr-1.5 animate-pulse" style={{ background: '#22c55e' }}></span>
                Live
              </span>
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="p-2 rounded-lg transition-all duration-200 hover:scale-105"
                style={{ background: 'var(--bg-input)', color: 'var(--text-secondary)', border: '1px solid var(--border-color)' }}
                title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
              >
                {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              </button>
            </div>
          </header>

          <main className="flex-1 overflow-auto p-4 md:p-6">
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
            className="fixed inset-0 z-30 md:hidden backdrop-blur-sm transition-opacity"
            style={{ background: 'rgba(0,0,0,0.5)' }}
            onClick={() => setSidebarOpen(false)}
          />
        )}
      </div>
    </BrowserRouter>
  );
}
