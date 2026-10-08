import { useEffect, useState } from 'react';
import axios from 'axios';
import { ShieldAlert, ShieldCheck, AlertTriangle, CheckCircle } from 'lucide-react';

interface ConstraintData {
  hard_constraints: { description: string; status: string; details: string }[];
  soft_constraints: { description: string; penalty: number; details: string }[];
  summary: { hard_violations: number; soft_violations: number; total_violations: number; quality_score: number };
}

const Card = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div
    className={`rounded-xl p-5 transition-all duration-200 ${className}`}
    style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', boxShadow: 'var(--shadow-card)' }}
  >
    {children}
  </div>
);

export default function Constraints() {
  const [data, setData] = useState<ConstraintData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/constraints')
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

  if (!data) {
    return <div className="text-center py-20" style={{ color: 'var(--text-muted)' }}>Unable to load constraint data.</div>;
  }

  const hard = data.hard_constraints || [];
  const soft = data.soft_constraints || [];
  const summary = data.summary || { hard_violations: 0, soft_violations: 0, total_violations: 0, quality_score: 0 };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight" style={{ color: 'var(--text-primary)' }}>Constraint Analysis</h2>
        <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>Hard and soft constraint violations in the generated timetable.</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: 'Hard Violations', value: summary.hard_violations, icon: ShieldAlert, color: '#ef4444', bg: 'rgba(239,68,68,0.1)' },
          { label: 'Soft Violations', value: summary.soft_violations, icon: AlertTriangle, color: '#f59e0b', bg: 'rgba(245,158,11,0.1)' },
          { label: 'Total', value: summary.total_violations, icon: ShieldCheck, color: '#8b5cf6', bg: 'rgba(139,92,246,0.1)' },
          { label: 'Quality Score', value: `${summary.quality_score}/100`, icon: CheckCircle, color: '#22c55e', bg: 'rgba(34,197,94,0.1)' },
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

      {/* Hard Constraints */}
      <Card>
        <div className="flex items-center gap-2 mb-4">
          <ShieldAlert className="w-4 h-4" style={{ color: '#ef4444' }} />
          <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>Hard Constraints</h3>
        </div>
        {hard.length === 0 ? (
          <p className="text-xs" style={{ color: 'var(--text-muted)' }}>No hard constraint data available.</p>
        ) : (
          <div className="space-y-2">
            {hard.map((c, i) => (
              <div key={i} className="flex items-start gap-3 p-3 rounded-lg" style={{ background: 'var(--bg-input)' }}>
                <div className="mt-0.5">
                  {c.status === 'violated' ? (
                    <AlertTriangle className="w-4 h-4" style={{ color: '#ef4444' }} />
                  ) : (
                    <CheckCircle className="w-4 h-4" style={{ color: '#22c55e' }} />
                  )}
                </div>
                <div>
                  <p className="text-xs font-medium" style={{ color: 'var(--text-primary)' }}>{c.description}</p>
                  <p className="text-[11px] mt-0.5" style={{ color: 'var(--text-secondary)' }}>{c.details}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>

      {/* Soft Constraints */}
      <Card>
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="w-4 h-4" style={{ color: '#f59e0b' }} />
          <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>Soft Constraints</h3>
        </div>
        {soft.length === 0 ? (
          <p className="text-xs" style={{ color: 'var(--text-muted)' }}>No soft constraint violations detected.</p>
        ) : (
          <div className="space-y-2">
            {soft.map((c, i) => (
              <div key={i} className="flex items-start justify-between gap-3 p-3 rounded-lg" style={{ background: 'var(--bg-input)' }}>
                <div>
                  <p className="text-xs font-medium" style={{ color: 'var(--text-primary)' }}>{c.description}</p>
                  <p className="text-[11px] mt-0.5" style={{ color: 'var(--text-secondary)' }}>{c.details}</p>
                </div>
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full flex-shrink-0"
                  style={{ background: 'rgba(245,158,11,0.1)', color: '#f59e0b' }}>
                  -{c.penalty}
                </span>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
