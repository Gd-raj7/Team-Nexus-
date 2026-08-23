import { Flame, MapPin, History } from 'lucide-react';
import type { HotspotItem, MemoryProfile } from '../lib/api';

interface Props {
  hotspots: HotspotItem[];
  selectedMemory?: MemoryProfile;
}

export default function HotspotsCard({ hotspots, selectedMemory }: Props) {
  return (
    <div className="card" style={{ padding: 16 }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: 14,
        paddingBottom: 10,
        borderBottom: '1px solid var(--border-primary)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Flame size={16} color="#f97316" />
          <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)' }}>
            City Vulnerability Hotspots & Memory
          </span>
        </div>
        <span style={{
          fontSize: 10,
          color: '#f97316',
          background: 'rgba(249, 115, 22, 0.12)',
          border: '1px solid rgba(249, 115, 22, 0.25)',
          padding: '1px 7px',
          borderRadius: 999,
          fontWeight: 600,
        }}>
          {hotspots.length} ACTIVE ZONES
        </span>
      </div>

      {/* Selected Incident Memory Insight Banner */}
      {selectedMemory && (
        <div style={{
          padding: '10px 12px',
          background: 'rgba(14, 165, 233, 0.08)',
          border: '1px solid rgba(14, 165, 233, 0.25)',
          borderRadius: 8,
          marginBottom: 12,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4 }}>
            <History size={13} color="#0ea5e9" />
            <span style={{ fontSize: 11, fontWeight: 700, color: '#38bdf8' }}>
              Spatial Memory Index ({Math.round(((selectedMemory as any).recurrence_rate || 0) * 100)}% Recurrence Risk)
            </span>
          </div>
          <p style={{ fontSize: 11, color: 'var(--text-secondary)', margin: 0, lineHeight: 1.4 }}>
            {(selectedMemory as any).insight || selectedMemory.civic_memory_insight}
          </p>
        </div>
      )}

      {/* Hotspots Grid / List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 8, maxHeight: 220, overflowY: 'auto' }}>
        {hotspots.length === 0 ? (
          <div style={{ fontSize: 11, color: 'var(--text-tertiary)', textAlign: 'center', padding: '12px 0' }}>
            No active spatial clusters detected.
          </div>
        ) : (
          hotspots.slice(0, 5).map((spot, idx) => {
            const isCrit = spot.severity === 'CRITICAL';
            const isHigh = spot.severity === 'HIGH';
            return (
              <div
                key={idx}
                style={{
                  padding: '8px 10px',
                  borderRadius: 6,
                  background: isCrit ? 'rgba(239, 68, 68, 0.06)' : 'var(--bg-tertiary)',
                  border: `1px solid ${isCrit ? 'rgba(239, 68, 68, 0.25)' : 'var(--border-primary)'}`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: 8,
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, overflow: 'hidden' }}>
                  <MapPin size={14} color={isCrit ? '#ef4444' : isHigh ? '#f59e0b' : '#3b82f6'} style={{ flexShrink: 0 }} />
                  <div style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                    <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-primary)', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>
                      {spot.location}
                    </span>
                    <span style={{ fontSize: 9, color: 'var(--text-tertiary)', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }}>
                      {spot.recurring ? 'Recurring Issue' : 'Single Issue'}
                    </span>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexShrink: 0 }}>
                  <span className="font-mono" style={{ fontSize: 11, fontWeight: 700, color: isCrit ? '#ef4444' : 'var(--text-primary)' }}>
                    {spot.incident_count} incidents
                  </span>
                  <span
                    className={`badge ${isCrit ? 'badge-critical' : isHigh ? 'badge-high' : 'badge-medium'}`}
                    style={{ fontSize: 8, padding: '1px 5px' }}
                  >
                    {spot.severity}
                  </span>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
