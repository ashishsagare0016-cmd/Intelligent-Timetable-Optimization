import { useEffect, useState } from 'react';
import { Users, BookOpen, MapPin, Calendar, Activity } from 'lucide-react';
import axios from 'axios';

export default function Dashboard() {
  const [stats, setStats] = useState({
    courses: 0,
    faculty: 0,
    rooms: 0,
    sections: 0,
    time_slots: 0
  });

  useEffect(() => {
    // Fetch data from Flask backend
    axios.get('http://127.0.0.1:5000/api/dashboard')
      .then(res => {
        setStats(res.data.stats);
      })
      .catch(err => console.error(err));
  }, []);

  const statCards = [
    { label: 'Total Courses', value: stats.courses, icon: BookOpen, color: 'text-blue-400', bg: 'bg-blue-400/10' },
    { label: 'Faculty Members', value: stats.faculty, icon: Users, color: 'text-indigo-400', bg: 'bg-indigo-400/10' },
    { label: 'Rooms Available', value: stats.rooms, icon: MapPin, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
    { label: 'Time Slots', value: stats.time_slots, icon: Calendar, color: 'text-amber-400', bg: 'bg-amber-400/10' },
    { label: 'Sections', value: stats.sections, icon: Activity, color: 'text-rose-400', bg: 'bg-rose-400/10' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-white">Dashboard Overview</h2>
        <p className="text-slate-400 mt-1">Real-time metrics for your timetable optimization.</p>
      </div>
      
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
        {statCards.map((card, i) => (
          <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-slate-700 transition-all duration-200 shadow-sm relative overflow-hidden group">
            <div className={`absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity duration-300 ${card.color}`}>
              <card.icon className="w-24 h-24 -mr-8 -mt-8" />
            </div>
            <div className="flex items-center">
              <div className={`p-3 rounded-lg ${card.bg} ${card.color}`}>
                <card.icon className="w-6 h-6" />
              </div>
            </div>
            <div className="mt-4">
              <h3 className="text-slate-400 text-sm font-medium">{card.label}</h3>
              <p className="text-3xl font-semibold text-white mt-1">{card.value}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
