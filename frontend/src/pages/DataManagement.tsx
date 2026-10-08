import { useEffect, useState } from 'react';
import axios from 'axios';
import { Database, Users, BookOpen, MapPin, Clock, Layers } from 'lucide-react';

interface RawData {
  subjects: { name: string; teacher: string; division: string; hours_per_week: number }[];
  rooms: { name: string; capacity: number }[];
  days: string[];
  periods: string[];
}

const Card = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div
    className={`rounded-xl p-5 transition-all duration-200 ${className}`}
    style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', boxShadow: 'var(--shadow-card)' }}
  >
    {children}
  </div>
);

export default function DataManagement() {
  const [data, setData] = useState<RawData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch the raw dataset to display
    axios.get('http://127.0.0.1:5000/api/dashboard')
      .then(res => {
        // The dashboard endpoint gives us timetable info; we need to extract subjects from the grid
        // Let's also try to fetch the raw data from a dedicated endpoint
        return axios.get('http://127.0.0.1:5000/data').catch(() => res);
      })
      .catch(() => null)
      .finally(() => setLoading(false));

    // Fetch raw JSON directly
    fetch('http://127.0.0.1:5000/api/dashboard')
      .then(r => r.json())
      .then(dashData => {
        // Extract subject info from timetable grid
        const grid = dashData?.timetable?.grid || {};
        const subjectMap = new Map<string, { name: string; teacher: string; division: string; room: string }>();
        const roomSet = new Set<string>();

        Object.values(grid).forEach((daySlots: any) => {
          Object.values(daySlots).forEach((slot: any) => {
            if (slot) {
              subjectMap.set(slot.subject, {
                name: slot.subject,
                teacher: slot.teacher,
                division: slot.division,
                room: slot.room,
              });
              roomSet.add(slot.room);
            }
          });
        });

        setData({
          subjects: Array.from(subjectMap.values()).map(s => ({
            name: s.name,
            teacher: s.teacher,
            division: s.division,
            hours_per_week: 3,
          })),
          rooms: Array.from(roomSet).map(r => ({ name: r, capacity: 60 })),
          days: dashData?.timetable?.days || ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
          periods: dashData?.timetable?.periods || ['P1', 'P2', 'P3', 'P4', 'P5', 'P6'],
        });
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!data) {
    return <div className="text-center py-20" style={{ color: 'var(--text-muted)' }}>Unable to load data.</div>;
  }

  const teachers = [...new Set(data.subjects.map(s => s.teacher))];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight" style={{ color: 'var(--text-primary)' }}>Data Management</h2>
        <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>View and manage your timetable input data.</p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: 'Subjects', value: data.subjects.length, icon: BookOpen, color: '#3b82f6', bg: 'rgba(59,130,246,0.1)' },
          { label: 'Teachers', value: teachers.length, icon: Users, color: '#8b5cf6', bg: 'rgba(139,92,246,0.1)' },
          { label: 'Rooms', value: data.rooms.length, icon: MapPin, color: '#22c55e', bg: 'rgba(34,197,94,0.1)' },
          { label: 'Time Slots', value: data.days.length * data.periods.length, icon: Clock, color: '#f59e0b', bg: 'rgba(245,158,11,0.1)' },
        ].map((card, i) => (
          <Card key={i}>
            <div className="flex items-center gap-2 mb-2">
              <div className="p-2 rounded-lg" style={{ background: card.bg }}>
                <card.icon className="w-4 h-4" style={{ color: card.color }} />
              </div>
            </div>
            <p className="text-xs" style={{ color: 'var(--text-muted)' }}>{card.label}</p>
            <p className="text-xl font-bold mt-0.5" style={{ color: 'var(--text-primary)' }}>{card.value}</p>
          </Card>
        ))}
      </div>

      {/* Subjects Table */}
      <Card className="!p-0 overflow-hidden">
        <div className="px-5 py-4 flex items-center gap-2" style={{ borderBottom: '1px solid var(--border-color)' }}>
          <BookOpen className="w-4 h-4" style={{ color: '#3b82f6' }} />
          <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>Subjects</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr>
                {['Subject', 'Teacher', 'Division'].map(h => (
                  <th key={h} className="px-5 py-2.5 text-left font-medium uppercase tracking-wider"
                    style={{ color: 'var(--text-muted)', background: 'var(--bg-input)', borderBottom: '1px solid var(--border-color)' }}>
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.subjects.map((s, i) => (
                <tr key={i}>
                  <td className="px-5 py-3 font-medium" style={{ color: 'var(--text-primary)', borderBottom: '1px solid var(--border-color)' }}>{s.name}</td>
                  <td className="px-5 py-3" style={{ color: 'var(--text-secondary)', borderBottom: '1px solid var(--border-color)' }}>{s.teacher}</td>
                  <td className="px-5 py-3" style={{ borderBottom: '1px solid var(--border-color)' }}>
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-medium"
                      style={{ background: 'rgba(59,130,246,0.1)', color: '#3b82f6' }}>
                      {s.division}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Rooms */}
      <Card>
        <div className="flex items-center gap-2 mb-3">
          <MapPin className="w-4 h-4" style={{ color: '#22c55e' }} />
          <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>Available Rooms</h3>
        </div>
        <div className="flex flex-wrap gap-2">
          {data.rooms.map((r, i) => (
            <span key={i} className="px-3 py-1.5 rounded-lg text-xs font-medium"
              style={{ background: 'var(--bg-input)', color: 'var(--text-primary)', border: '1px solid var(--border-color)' }}>
              {r.name}
            </span>
          ))}
        </div>
      </Card>

      {/* Schedule Grid */}
      <Card>
        <div className="flex items-center gap-2 mb-3">
          <Layers className="w-4 h-4" style={{ color: '#f59e0b' }} />
          <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>Available Time Slots</h3>
        </div>
        <div className="grid grid-cols-5 gap-2">
          {data.days.map(day => (
            <div key={day}>
              <p className="text-[10px] font-semibold uppercase tracking-wider mb-2 text-center" style={{ color: 'var(--text-muted)' }}>{day}</p>
              <div className="space-y-1">
                {data.periods.map(period => (
                  <div key={period} className="text-center text-[11px] py-1.5 rounded-md"
                    style={{ background: 'var(--bg-input)', color: 'var(--text-secondary)' }}>
                    {period}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
