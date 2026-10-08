import { useEffect, useState } from 'react';
import axios from 'axios';

interface SlotEntry {
  subject: string;
  teacher: string;
  room: string;
  division: string;
}

interface TimetableData {
  timetable: {
    days: string[];
    periods: string[];
    grid: Record<string, Record<string, SlotEntry | null>>;
    source: string;
    entries_count: number;
  };
}

const Card = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div
    className={`rounded-xl p-5 transition-all duration-200 ${className}`}
    style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', boxShadow: 'var(--shadow-card)' }}
  >
    {children}
  </div>
);

// Stable color palette
const subjectColors: Record<string, { bg: string; text: string; border: string }> = {};
const palette = [
  { bg: 'rgba(59,130,246,0.12)', text: '#3b82f6', border: 'rgba(59,130,246,0.25)' },
  { bg: 'rgba(139,92,246,0.12)', text: '#8b5cf6', border: 'rgba(139,92,246,0.25)' },
  { bg: 'rgba(34,197,94,0.12)', text: '#22c55e', border: 'rgba(34,197,94,0.25)' },
  { bg: 'rgba(245,158,11,0.12)', text: '#f59e0b', border: 'rgba(245,158,11,0.25)' },
  { bg: 'rgba(236,72,153,0.12)', text: '#ec4899', border: 'rgba(236,72,153,0.25)' },
  { bg: 'rgba(6,182,212,0.12)', text: '#06b6d4', border: 'rgba(6,182,212,0.25)' },
  { bg: 'rgba(249,115,22,0.12)', text: '#f97316', border: 'rgba(249,115,22,0.25)' },
  { bg: 'rgba(168,85,247,0.12)', text: '#a855f7', border: 'rgba(168,85,247,0.25)' },
];
let colorIdx = 0;
function getSubjectColor(subject: string) {
  if (!subjectColors[subject]) {
    subjectColors[subject] = palette[colorIdx % palette.length];
    colorIdx++;
  }
  return subjectColors[subject];
}

export default function Timetable() {
  const [data, setData] = useState<TimetableData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/dashboard')
      .then(res => setData(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!data?.timetable) {
    return <div className="text-center py-20" style={{ color: 'var(--text-muted)' }}>No timetable data available.</div>;
  }

  const { days, periods, grid, source, entries_count } = data.timetable;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div>
          <h2 className="text-xl font-bold tracking-tight" style={{ color: 'var(--text-primary)' }}>Generated Timetable</h2>
          <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>
            Source: {source} · {entries_count} classes assigned
          </p>
        </div>
      </div>

      <Card className="overflow-hidden !p-0">
        <div className="overflow-x-auto">
          <table className="w-full text-sm" style={{ minWidth: 700 }}>
            <thead>
              <tr>
                <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider"
                  style={{ color: 'var(--text-muted)', background: 'var(--bg-input)', borderBottom: '1px solid var(--border-color)' }}>
                  Period
                </th>
                {days.map(day => (
                  <th key={day} className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider"
                    style={{ color: 'var(--text-muted)', background: 'var(--bg-input)', borderBottom: '1px solid var(--border-color)' }}>
                    {day}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {periods.map((period) => (
                <tr key={period}>
                  <td className="px-4 py-3 font-semibold text-xs" style={{ color: 'var(--text-secondary)', borderBottom: '1px solid var(--border-color)' }}>
                    {period}
                  </td>
                  {days.map(day => {
                    const slot = grid[day]?.[period];
                    if (!slot) {
                      return (
                        <td key={day} className="px-4 py-3" style={{ borderBottom: '1px solid var(--border-color)' }}>
                          <div className="h-16 flex items-center justify-center rounded-lg text-xs"
                            style={{ background: 'var(--bg-input)', color: 'var(--text-muted)' }}>
                            —
                          </div>
                        </td>
                      );
                    }
                    const clr = getSubjectColor(slot.subject);
                    return (
                      <td key={day} className="px-4 py-3" style={{ borderBottom: '1px solid var(--border-color)' }}>
                        <div className="p-2.5 rounded-lg" style={{ background: clr.bg, border: `1px solid ${clr.border}` }}>
                          <p className="text-xs font-semibold leading-tight" style={{ color: clr.text }}>{slot.subject}</p>
                          <p className="text-[11px] mt-1 opacity-80" style={{ color: 'var(--text-secondary)' }}>{slot.teacher}</p>
                          <p className="text-[10px] mt-0.5 opacity-60" style={{ color: 'var(--text-muted)' }}>{slot.room}</p>
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
