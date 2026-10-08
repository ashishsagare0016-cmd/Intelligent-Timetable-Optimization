import { useEffect, useState } from 'react';
import { BookOpen, AlertTriangle, CheckCircle, TrendingUp, Clock, BarChart3, Lightbulb } from 'lucide-react';
import axios from 'axios';

interface DashboardData {
  summary: {
    total_classes: number;
    conflict_edges: number;
    hard_violations: number;
    soft_violations: number;
    quality_score: number;
    slots_used: number;
  };
  constraints: {
    hard_violations: number;
    soft_violations: number;
    total_violations: number;
  };
  graph: {
    nodes: number;
    edges: number;
    max_degree: number;
    avg_degree: number;
  };
  key_results: string[];
  algorithms: {
    results: { name: string; quality_score: number; execution_time: number; total_violations: number }[];
    best_algorithm: string;
    observations: string[];
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

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
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

  if (!data) {
    return (
      <div className="text-center py-20" style={{ color: 'var(--text-muted)' }}>
        <p className="text-lg">Unable to connect to backend API.</p>
        <p className="text-sm mt-2">Make sure the Flask server is running on port 5000.</p>
      </div>
    );
  }

  const { summary, constraints, graph, key_results, algorithms } = data;

  const statCards = [
    { label: 'Total Classes', value: summary.total_classes, icon: BookOpen, color: '#3b82f6', bg: 'rgba(59,130,246,0.1)' },
    { label: 'Quality Score', value: `${summary.quality_score}/100`, icon: TrendingUp, color: '#22c55e', bg: 'rgba(34,197,94,0.1)' },
    { label: 'Hard Violations', value: constraints.hard_violations, icon: AlertTriangle, color: '#ef4444', bg: 'rgba(239,68,68,0.1)' },
    { label: 'Soft Violations', value: constraints.soft_violations, icon: CheckCircle, color: '#f59e0b', bg: 'rgba(245,158,11,0.1)' },
    { label: 'Conflict Edges', value: graph.edges, icon: BarChart3, color: '#8b5cf6', bg: 'rgba(139,92,246,0.1)' },
    { label: 'Slots Used', value: summary.slots_used, icon: Clock, color: '#06b6d4', bg: 'rgba(6,182,212,0.1)' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-bold tracking-tight" style={{ color: 'var(--text-primary)' }}>Dashboard Overview</h2>
        <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>Real-time metrics for your timetable optimization.</p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
        {statCards.map((card, i) => (
          <Card key={i}>
            <div className="flex items-center justify-between mb-3">
              <div className="p-2 rounded-lg" style={{ background: card.bg }}>
                <card.icon className="w-4 h-4" style={{ color: card.color }} />
              </div>
            </div>
            <p className="text-xs font-medium" style={{ color: 'var(--text-muted)' }}>{card.label}</p>
            <p className="text-xl font-bold mt-0.5" style={{ color: 'var(--text-primary)' }}>{card.value}</p>
          </Card>
        ))}
      </div>

      {/* Quality Score Bar */}
      <Card>
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>Overall Quality Score</h3>
          <span className="text-2xl font-bold" style={{ color: summary.quality_score >= 70 ? '#22c55e' : '#f59e0b' }}>
            {summary.quality_score}%
          </span>
        </div>
        <div className="w-full h-2.5 rounded-full overflow-hidden" style={{ background: 'var(--bg-input)' }}>
          <div
            className="h-full rounded-full transition-all duration-1000 ease-out"
            style={{
              width: `${summary.quality_score}%`,
              background: summary.quality_score >= 70
                ? 'linear-gradient(90deg, #22c55e, #10b981)'
                : 'linear-gradient(90deg, #f59e0b, #eab308)',
            }}
          />
        </div>
        <p className="text-xs mt-2" style={{ color: 'var(--text-muted)' }}>
          Best algorithm: {algorithms.best_algorithm}
        </p>
      </Card>

      {/* Algorithm Results + Key Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Algorithm Performance Table */}
        <Card>
          <h3 className="text-sm font-semibold mb-3" style={{ color: 'var(--text-primary)' }}>Algorithm Performance</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr style={{ color: 'var(--text-muted)' }}>
                  <th className="text-left pb-2 font-medium">Algorithm</th>
                  <th className="text-right pb-2 font-medium">Score</th>
                  <th className="text-right pb-2 font-medium">Violations</th>
                  <th className="text-right pb-2 font-medium">Time</th>
                </tr>
              </thead>
              <tbody>
                {algorithms.results.map((algo, i) => (
                  <tr key={i} className="transition-colors" style={{ borderTop: '1px solid var(--border-color)' }}>
                    <td className="py-2.5 font-medium" style={{ color: 'var(--text-primary)' }}>
                      {algo.name}
                      {algo.name === algorithms.best_algorithm && (
                        <span className="ml-1.5 text-[10px] px-1.5 py-0.5 rounded-full" style={{ background: 'rgba(34,197,94,0.1)', color: '#22c55e' }}>
                          Best
                        </span>
                      )}
                    </td>
                    <td className="py-2.5 text-right font-semibold" style={{ color: 'var(--text-primary)' }}>{algo.quality_score}</td>
                    <td className="py-2.5 text-right" style={{ color: algo.total_violations > 0 ? '#ef4444' : '#22c55e' }}>{algo.total_violations}</td>
                    <td className="py-2.5 text-right" style={{ color: 'var(--text-secondary)' }}>{(algo.execution_time * 1000).toFixed(1)}ms</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>

        {/* Key Results */}
        <Card>
          <div className="flex items-center gap-2 mb-3">
            <Lightbulb className="w-4 h-4" style={{ color: '#f59e0b' }} />
            <h3 className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>Key Insights</h3>
          </div>
          <div className="space-y-2.5">
            {key_results.map((insight, i) => (
              <div key={i} className="flex gap-2.5 text-xs leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
                <span className="mt-0.5 w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: '#3b82f6' }} />
                <span>{insight}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Graph Stats */}
      <Card>
        <h3 className="text-sm font-semibold mb-3" style={{ color: 'var(--text-primary)' }}>Conflict Graph Overview</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {[
            { label: 'Nodes', value: graph.nodes },
            { label: 'Edges', value: graph.edges },
            { label: 'Max Degree', value: graph.max_degree },
            { label: 'Avg Degree', value: graph.avg_degree.toFixed(1) },
          ].map((stat, i) => (
            <div key={i} className="text-center p-3 rounded-lg" style={{ background: 'var(--bg-input)' }}>
              <p className="text-lg font-bold" style={{ color: 'var(--text-primary)' }}>{stat.value}</p>
              <p className="text-xs" style={{ color: 'var(--text-muted)' }}>{stat.label}</p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
