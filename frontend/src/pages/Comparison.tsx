import { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart3, Clock, Trophy, AlertTriangle } from 'lucide-react';

interface AlgoResult {
  key: string;
  name: string;
  execution_time: number;
  quality_score: number;
  hard_violations: number;
  soft_violations: number;
  total_violations: number;
  is_feasible: boolean;
}

interface ComparisonData {
  results: AlgoResult[];
  best_algorithm: string;
  observations: string[];
}

const Card = ({ children, className = '' }: { children: React.ReactNode; className?: string }) => (
  <div
    className={`rounded-xl p-5 transition-all duration-200 ${className}`}
    style={{ background: 'var(--bg-card)', border: '1px solid var(--border-color)', boxShadow: 'var(--shadow-card)' }}
  >
    {children}
  </div>
);

export default function Comparison() {
  const [data, setData] = useState<ComparisonData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/comparison')
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
    return <div className="text-center py-20" style={{ color: 'var(--text-muted)' }}>Unable to load comparison data.</div>;
  }

  const maxScore = Math.max(...data.results.map(r => r.quality_score));

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight" style={{ color: 'var(--text-primary)' }}>Algorithm Comparison</h2>
        <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>Side-by-side performance analysis of all scheduling algorithms.</p>
      </div>

      {/* Algorithm Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {data.results.map((algo) => {
          const isBest = algo.name === data.best_algorithm;
          return (
            <Card key={algo.key} className={isBest ? '!border-blue-500/30' : ''}>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>{algo.name}</h3>
                {isBest && (
                  <span className="flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded-full"
                    style={{ background: 'rgba(59,130,246,0.15)', color: '#3b82f6' }}>
                    <Trophy className="w-3 h-3" /> Best
                  </span>
                )}
              </div>

              {/* Quality Score Bar */}
              <div className="mb-4">
                <div className="flex justify-between text-xs mb-1">
                  <span style={{ color: 'var(--text-muted)' }}>Quality Score</span>
                  <span className="font-bold" style={{ color: 'var(--text-primary)' }}>{algo.quality_score}/100</span>
                </div>
                <div className="w-full h-2 rounded-full overflow-hidden" style={{ background: 'var(--bg-input)' }}>
                  <div className="h-full rounded-full transition-all duration-700"
                    style={{
                      width: `${algo.quality_score}%`,
                      background: algo.quality_score === maxScore
                        ? 'linear-gradient(90deg, #3b82f6, #6366f1)'
                        : 'linear-gradient(90deg, #64748b, #94a3b8)',
                    }}
                  />
                </div>
              </div>

              {/* Stats grid */}
              <div className="grid grid-cols-2 gap-3">
                <div className="p-2.5 rounded-lg" style={{ background: 'var(--bg-input)' }}>
                  <div className="flex items-center gap-1.5 mb-1">
                    <Clock className="w-3 h-3" style={{ color: 'var(--text-muted)' }} />
                    <span className="text-[10px]" style={{ color: 'var(--text-muted)' }}>Time</span>
                  </div>
                  <p className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>{(algo.execution_time * 1000).toFixed(1)}ms</p>
                </div>
                <div className="p-2.5 rounded-lg" style={{ background: 'var(--bg-input)' }}>
                  <div className="flex items-center gap-1.5 mb-1">
                    <AlertTriangle className="w-3 h-3" style={{ color: 'var(--text-muted)' }} />
                    <span className="text-[10px]" style={{ color: 'var(--text-muted)' }}>Violations</span>
                  </div>
                  <p className="text-sm font-semibold" style={{ color: algo.total_violations > 0 ? '#ef4444' : '#22c55e' }}>{algo.total_violations}</p>
                </div>
                <div className="p-2.5 rounded-lg" style={{ background: 'var(--bg-input)' }}>
                  <div className="flex items-center gap-1.5 mb-1">
                    <BarChart3 className="w-3 h-3" style={{ color: 'var(--text-muted)' }} />
                    <span className="text-[10px]" style={{ color: 'var(--text-muted)' }}>Hard</span>
                  </div>
                  <p className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>{algo.hard_violations}</p>
                </div>
                <div className="p-2.5 rounded-lg" style={{ background: 'var(--bg-input)' }}>
                  <div className="flex items-center gap-1.5 mb-1">
                    <BarChart3 className="w-3 h-3" style={{ color: 'var(--text-muted)' }} />
                    <span className="text-[10px]" style={{ color: 'var(--text-muted)' }}>Soft</span>
                  </div>
                  <p className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>{algo.soft_violations}</p>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Observations */}
      <Card>
        <h3 className="text-sm font-semibold mb-3" style={{ color: 'var(--text-primary)' }}>Observations</h3>
        <div className="space-y-2">
          {data.observations.map((obs, i) => (
            <div key={i} className="flex gap-2.5 text-xs leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
              <span className="mt-1 w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: '#8b5cf6' }} />
              <span>{obs}</span>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
