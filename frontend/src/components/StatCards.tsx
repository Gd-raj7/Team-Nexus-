import type { DashboardStats } from '../lib/api';
import { AlertCircle, CheckCircle2, ShieldAlert, FileWarning, RefreshCw, Layers } from 'lucide-react';

interface StatCardsProps {
  stats: DashboardStats;
}

export default function StatCards({ stats }: StatCardsProps) {
  const cards = [
    {
      label: 'Total Reports',
      value: stats.total_reports,
      icon: <Layers size={18} color="var(--text-secondary)" />,
    },
    {
      label: 'Active Incidents',
      value: stats.active_incidents,
      icon: <FileWarning size={18} color="var(--accent-blue)" />,
    },
    {
      label: 'Critical Priority',
      value: stats.critical_incidents,
      icon: <ShieldAlert size={18} color="var(--status-critical)" />,
      badge: stats.critical_incidents > 0 ? 'Urgent' : null,
      badgeColor: 'badge-critical',
    },
    {
      label: 'Resolved',
      value: stats.resolved_incidents,
      icon: <CheckCircle2 size={18} color="var(--status-resolved)" />,
    },
    {
      label: 'Reopened Cases',
      value: stats.reopened_incidents,
      icon: <RefreshCw size={18} color="var(--status-high)" />,
    },
    {
      label: 'Escalated SLAs',
      value: stats.escalated_incidents,
      icon: <AlertCircle size={18} color="var(--status-escalated)" />,
      badge: stats.escalated_incidents > 0 ? 'Breach' : null,
      badgeColor: 'badge-escalated',
    },
  ];

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
      gap: 12,
      marginBottom: 20,
    }}>
      {cards.map((card, i) => (
        <div key={i} className="card" style={{
          padding: 16,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          minHeight: 100,
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: 12, color: 'var(--text-secondary)', fontWeight: 500 }}>
              {card.label}
            </span>
            {card.icon}
          </div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginTop: 12 }}>
            <span className="font-mono" style={{ fontSize: 24, fontWeight: 700, color: 'var(--text-primary)' }}>
              {card.value}
            </span>
            {card.badge && (
              <span className={`badge ${card.badgeColor}`} style={{ fontSize: 9 }}>
                {card.badge}
              </span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
