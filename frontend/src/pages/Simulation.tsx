import { useState, useEffect } from 'react';
import axios from 'axios';
import { Zap, ArrowRight, History, CheckCircle, XCircle } from 'lucide-react';

interface SimResult {
  subject: string;
  from_slot: string;
  to_slot: string;
  impact: {
    hard_before: number;
    hard_after: number;
    soft_before: number;
    soft_after: number;
    score_before: number;
    score_after: number;
  };
  recommendation: string;
  history?: { subject: string; target_slot: string; result: string; timestamp: string }[];
}

const Card = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div
    className={`rounded-xl p-5 transition-all duration-200 ${className}`}
    style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', boxShadow: 'var(--shadow-card)' }}
  >
    {children}
  </div>
);

export default function Simulation() {
  const [subjects, setSubjects] = useState<string[]>([]);
  const [days] = useState(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']);
  const [periods] = useState(['P1', 'P2', 'P3', 'P4', 'P5', 'P6']);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedDay, setSelectedDay] = useState('Monday');
  const [selectedPeriod, setSelectedPeriod] = useState('P1');
  const [result, setResult] = useState<SimResult | null>(null);
  const [history, setHistory] = useState<{ subject: string; target_slot: string; result: string; timestamp: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/dashboard')
      .then(res => {
        const grid = res.data?.timetable?.grid || {};
        const subjectSet = new Set<string>();
        Object.values(grid).forEach((daySlots: any) => {
          Object.values(daySlots).forEach((slot: any) => {
            if (slot?.subject) subjectSet.add(slot.subject);
          });
        });
        const list = Array.from(subjectSet);
        setSubjects(list);
        if (list.length > 0) setSelectedSubject(list[0]);
      })
      .catch(err => console.error(err));
  }, []);

  const runSimulation = () => {
    if (!selectedSubject) return;
    setLoading(true);
    setError('');
    setResult(null);

    axios.post('http://127.0.0.1:5000/api/simulate', {
      subject: selectedSubject,
      target_slot: `${selectedDay} ${selectedPeriod}`,
    })
      .then(res => {
        setResult(res.data);
        if (res.data.history) setHistory(res.data.history);
      })
      .catch(err => {
        setError(err.response?.data?.error || 'Simulation failed');
      })
      .finally(() => setLoading(false));
  };

  const selectStyle = {
    background: 'var(--bg-input)',
    border: '1px solid var(--border-color)',
    color: 'var(--text-primary)',
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight" style={{ color: 'var(--text-primary)' }}>What-If Simulation</h2>
        <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>Test slot reassignment and see constraint impact before committing.</p>
      </div>

      {/* Input Form */}
      <Card>
        <h3 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Configure Simulation</h3>
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-3">
          <div>
            <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-muted)' }}>Subject</label>
            <select
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
              className="w-full px-3 py-2 rounded-lg text-sm outline-none"
              style={selectStyle}
            >
              {subjects.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-muted)' }}>Target Day</label>
            <select
              value={selectedDay}
              onChange={(e) => setSelectedDay(e.target.value)}
              className="w-full px-3 py-2 rounded-lg text-sm outline-none"
              style={selectStyle}
            >
              {days.map(d => <option key={d} value={d}>{d}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium mb-1.5" style={{ color: 'var(--text-muted)' }}>Target Period</label>
            <select
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value)}
              className="w-full px-3 py-2 rounded-lg text-sm outline-none"
              style={selectStyle}
            >
              {periods.map(p => <option key={p} value={p}>{p}</option>)}
            </select>
          </div>
          <div className="flex items-end">
            <button
              onClick={runSimulation}
              disabled={loading || !selectedSubject}
              className="w-full px-4 py-2 rounded-lg text-sm font-medium text-white transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50"
              style={{ background: 'linear-gradient(135deg, #3b82f6, #6366f1)' }}
            >
              {loading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <>
                  <Zap className="w-4 h-4" />
                  Simulate
                </>
              )}
            </button>
          </div>
        </div>
      </Card>

      {error && (
        <div className="p-3 rounded-lg text-sm" style={{ background: 'rgba(239,68,68,0.1)', color: '#ef4444', border: '1px solid rgba(239,68,68,0.2)' }}>
          {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <Card>
          <h3 className="text-sm font-semibold mb-4" style={{ color: 'var(--text-primary)' }}>Simulation Result</h3>

          <div className="flex items-center gap-3 mb-4 p-3 rounded-lg" style={{ background: 'var(--bg-input)' }}>
            <span className="text-xs font-medium px-2.5 py-1 rounded-md" style={{ background: 'rgba(59,130,246,0.1)', color: '#3b82f6' }}>
              {result.from_slot || 'Unassigned'}
            </span>
            <ArrowRight className="w-4 h-4" style={{ color: 'var(--text-muted)' }} />
            <span className="text-xs font-medium px-2.5 py-1 rounded-md" style={{ background: 'rgba(139,92,246,0.1)', color: '#8b5cf6' }}>
              {result.to_slot}
            </span>
          </div>

          {result.impact && (
            <div className="grid grid-cols-3 gap-3 mb-4">
              <div className="p-3 rounded-lg text-center" style={{ background: 'var(--bg-input)' }}>
                <p className="text-[10px] uppercase tracking-wider mb-1" style={{ color: 'var(--text-muted)' }}>Hard Violations</p>
                <p className="text-sm">
                  <span style={{ color: 'var(--text-secondary)' }}>{result.impact.hard_before}</span>
                  <span className="mx-1" style={{ color: 'var(--text-muted)' }}>→</span>
                  <span className="font-bold" style={{ color: result.impact.hard_after <= result.impact.hard_before ? '#22c55e' : '#ef4444' }}>
                    {result.impact.hard_after}
                  </span>
                </p>
              </div>
              <div className="p-3 rounded-lg text-center" style={{ background: 'var(--bg-input)' }}>
                <p className="text-[10px] uppercase tracking-wider mb-1" style={{ color: 'var(--text-muted)' }}>Soft Violations</p>
                <p className="text-sm">
                  <span style={{ color: 'var(--text-secondary)' }}>{result.impact.soft_before}</span>
                  <span className="mx-1" style={{ color: 'var(--text-muted)' }}>→</span>
                  <span className="font-bold" style={{ color: result.impact.soft_after <= result.impact.soft_before ? '#22c55e' : '#f59e0b' }}>
                    {result.impact.soft_after}
                  </span>
                </p>
              </div>
              <div className="p-3 rounded-lg text-center" style={{ background: 'var(--bg-input)' }}>
                <p className="text-[10px] uppercase tracking-wider mb-1" style={{ color: 'var(--text-muted)' }}>Quality Score</p>
                <p className="text-sm">
                  <span style={{ color: 'var(--text-secondary)' }}>{result.impact.score_before}</span>
                  <span className="mx-1" style={{ color: 'var(--text-muted)' }}>→</span>
                  <span className="font-bold" style={{ color: result.impact.score_after >= result.impact.score_before ? '#22c55e' : '#ef4444' }}>
                    {result.impact.score_after}
                  </span>
                </p>
              </div>
            </div>
          )}

          <div className="p-3 rounded-lg text-xs" style={{ background: 'var(--bg-input)', color: 'var(--text-secondary)' }}>
            <strong style={{ color: 'var(--text-primary)' }}>Recommendation:</strong> {result.recommendation}
          </div>
        </Card>
      )}

      {/* History */}
      {history.length > 0 && (
        <Card>
          <div className="flex items-center gap-2 mb-3">
            <History className="w-4 h-4" style={{ color: 'var(--text-muted)' }} />
            <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>Simulation History</h3>
          </div>
          <div className="space-y-2">
            {history.slice().reverse().map((h, i) => (
              <div key={i} className="flex items-center justify-between p-2.5 rounded-lg text-xs" style={{ background: 'var(--bg-input)' }}>
                <div className="flex items-center gap-2">
                  {h.result === 'accepted' ? (
                    <CheckCircle className="w-3.5 h-3.5" style={{ color: '#22c55e' }} />
                  ) : (
                    <XCircle className="w-3.5 h-3.5" style={{ color: '#ef4444' }} />
                  )}
                  <span style={{ color: 'var(--text-primary)' }}>{h.subject}</span>
                  <span style={{ color: 'var(--text-muted)' }}>→ {h.target_slot}</span>
                </div>
                <span className="text-[10px]" style={{ color: 'var(--text-muted)' }}>{h.timestamp}</span>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
