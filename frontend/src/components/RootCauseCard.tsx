import { ShieldAlert } from 'lucide-react';

interface RootCauseCardProps {
  hypothesis: string;
  confidence: number;
  evidence: string[];
  chain: string[];
  disclaimer: string;
}

export default function RootCauseCard({ hypothesis, confidence, evidence, chain, disclaimer }: RootCauseCardProps) {
  return (
    <div className="card" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <h3 style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>
          Root Cause Investigation
        </h3>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ fontSize: 10, color: 'var(--text-secondary)' }}>Confidence:</span>
          <span className="font-mono" style={{
            fontSize: 11,
            fontWeight: 600,
            color: confidence > 0.75 ? 'var(--status-resolved)' : confidence > 0.5 ? 'var(--status-high)' : 'var(--status-critical)'
          }}>
            {Math.round(confidence * 100)}%
          </span>
        </div>
      </div>

      {/* Causal Chain Visualization */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: 6,
        padding: '10px 12px',
        background: 'var(--bg-primary)',
        borderRadius: 6,
        border: '1px solid var(--border-primary)',
        marginBottom: 14,
      }}>
        {chain.map((item, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <span className="font-mono" style={{
              fontSize: 10,
              padding: '2px 6px',
              background: 'var(--bg-tertiary)',
              border: '1px solid var(--border-secondary)',
              borderRadius: 4,
              color: i === 0 ? 'var(--status-critical)' : 'var(--text-primary)',
              fontWeight: i === 0 ? 600 : 400,
            }}>
              {item.replace(/_/g, ' ')}
            </span>
            {i < chain.length - 1 && (
              <span style={{ fontSize: 10, color: 'var(--text-tertiary)' }}>➔</span>
            )}
          </div>
        ))}
      </div>

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 12 }}>
        <div>
          <span style={{ fontSize: 11, color: 'var(--text-secondary)', fontWeight: 600, display: 'block', marginBottom: 4 }}>
            HYPOTHESIS
          </span>
          <p style={{ fontSize: 12, color: 'var(--text-primary)', lineHeight: 1.4 }}>
            {hypothesis || 'Analyzing causal relationships...'}
          </p>
        </div>

        {evidence && evidence.length > 0 && (
          <div>
            <span style={{ fontSize: 11, color: 'var(--text-secondary)', fontWeight: 600, display: 'block', marginBottom: 4 }}>
              EVIDENCE & PROPAGATION MECHANISM
            </span>
            <ul style={{
              margin: 0,
              paddingLeft: 16,
              fontSize: 11,
              color: 'var(--text-secondary)',
              display: 'flex',
              flexDirection: 'column',
              gap: 4,
            }}>
              {evidence.map((item, i) => (
                <li key={i} style={{ lineHeight: 1.4 }}>{item}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {disclaimer && (
        <div style={{
          marginTop: 16,
          padding: '8px 12px',
          background: 'rgba(239, 68, 68, 0.06)',
          border: '1px dashed rgba(239, 68, 68, 0.25)',
          borderRadius: 6,
          display: 'flex',
          gap: 8,
          alignItems: 'flex-start',
        }}>
          <ShieldAlert size={14} color="var(--status-critical)" style={{ marginTop: 2, flexShrink: 0 }} />
          <span style={{ fontSize: 10, color: 'var(--text-secondary)', lineHeight: 1.3 }}>
            <strong>DISCLAIMER:</strong> {disclaimer}
          </span>
        </div>
      )}
    </div>
  );
}
