import { CheckCircle2, Circle, Loader2, AlertTriangle, ChevronRight } from 'lucide-react';

interface PipelineStage {
  id: string;
  name: string;
  agent: string;
  status: 'pending' | 'running' | 'complete' | 'error' | 'waiting';
  result?: string;
  confidence?: number;
}

interface AgentPipelineProps {
  stages: PipelineStage[];
}

const stageIcons = {
  pending: <Circle size={16} style={{ color: 'var(--text-tertiary)' }} />,
  running: <Loader2 size={16} style={{ color: 'var(--accent-blue)', animation: 'spin 1s linear infinite' }} />,
  complete: <CheckCircle2 size={16} style={{ color: 'var(--status-resolved)' }} />,
  error: <AlertTriangle size={16} style={{ color: 'var(--status-critical)' }} />,
  waiting: <Circle size={16} style={{ color: 'var(--status-high)' }} />,
};

const stageColors = {
  pending: 'var(--border-primary)',
  running: 'var(--accent-blue)',
  complete: 'var(--status-resolved)',
  error: 'var(--status-critical)',
  waiting: 'var(--status-high)',
};

export default function AgentPipeline({ stages }: AgentPipelineProps) {
  return (
    <div className="card" style={{ padding: 16 }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: 6,
        marginBottom: 16,
        paddingBottom: 12,
        borderBottom: '1px solid var(--border-primary)',
      }}>
        <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>
          Agent Pipeline
        </span>
        <span style={{
          fontSize: 10,
          color: 'var(--accent-blue)',
          background: 'rgba(37, 99, 235, 0.12)',
          padding: '1px 6px',
          borderRadius: 3,
          fontWeight: 600,
        }}>
          {stages.filter(s => s.status === 'complete').length}/{stages.length} COMPLETE
        </span>
      </div>

      {/* Pipeline visualization */}
      <div style={{
        display: 'flex',
        alignItems: 'stretch',
        gap: 0,
        overflowX: 'auto',
        padding: '4px 0',
      }}>
        {stages.map((stage, i) => (
          <div key={stage.id} style={{ display: 'flex', alignItems: 'center' }}>
            {/* Stage card */}
            <div
              className="animate-fade-in"
              style={{
                display: 'flex',
                flexDirection: 'column',
                padding: '10px 14px',
                borderRadius: 6,
                border: `1px solid ${stageColors[stage.status]}`,
                background: stage.status === 'running'
                  ? 'rgba(37, 99, 235, 0.08)'
                  : stage.status === 'complete'
                  ? 'rgba(16, 185, 129, 0.06)'
                  : 'var(--bg-tertiary)',
                minWidth: 130,
                animationDelay: `${i * 100}ms`,
                opacity: 0,
                transition: 'border-color 0.3s, background 0.3s',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6 }}>
                {stageIcons[stage.status]}
                <span style={{
                  fontSize: 11,
                  fontWeight: 600,
                  color: stage.status === 'pending' ? 'var(--text-tertiary)' : 'var(--text-primary)',
                }}>
                  {stage.name}
                </span>
              </div>

              <span className="font-mono" style={{
                fontSize: 10,
                color: 'var(--text-tertiary)',
                marginBottom: stage.result ? 4 : 0,
              }}>
                {stage.agent}
              </span>

              {stage.result && (
                <span style={{
                  fontSize: 11,
                  color: 'var(--text-secondary)',
                  marginTop: 4,
                  lineHeight: 1.3,
                }}>
                  {stage.result}
                </span>
              )}

              {stage.confidence !== undefined && stage.status === 'complete' && (
                <div style={{ marginTop: 6, display: 'flex', alignItems: 'center', gap: 4 }}>
                  <div style={{
                    width: 40,
                    height: 3,
                    borderRadius: 2,
                    background: 'var(--bg-primary)',
                    overflow: 'hidden',
                  }}>
                    <div style={{
                      width: `${stage.confidence * 100}%`,
                      height: '100%',
                      background: stage.confidence > 0.7 ? 'var(--status-resolved)' :
                                  stage.confidence > 0.4 ? 'var(--status-high)' : 'var(--status-critical)',
                      borderRadius: 2,
                      transition: 'width 0.5s ease-out',
                    }} />
                  </div>
                  <span className="font-mono" style={{ fontSize: 10, color: 'var(--text-tertiary)' }}>
                    {(stage.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              )}

              {stage.status === 'waiting' && (
                <span style={{
                  fontSize: 10,
                  color: 'var(--status-high)',
                  marginTop: 4,
                  fontWeight: 500,
                }}>
                  Awaiting approval
                </span>
              )}
            </div>

            {/* Connector */}
            {i < stages.length - 1 && (
              <div style={{
                display: 'flex',
                alignItems: 'center',
                padding: '0 2px',
              }}>
                <ChevronRight
                  size={16}
                  style={{
                    color: stage.status === 'complete'
                      ? 'var(--status-resolved)'
                      : 'var(--border-secondary)',
                    transition: 'color 0.3s',
                    flexShrink: 0,
                  }}
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

// Helper to build stages from pipeline result
export function buildPipelineStages(
  pipelineResult?: Record<string, { status: string; result: Record<string, unknown> }>,
  isRunning: boolean = false,
): PipelineStage[] {
  const stageConfig = [
    { id: 'perception', name: 'Perception', agent: 'perception_agent' },
    { id: 'clustering', name: 'Clustering', agent: 'clustering_agent' },
    { id: 'incident_detection', name: 'Detection', agent: 'incident_agent' },
    { id: 'root_cause', name: 'Root Cause', agent: 'root_cause_agent' },
    { id: 'impact', name: 'Impact', agent: 'impact_agent' },
    { id: 'response', name: 'Response', agent: 'response_agent' },
    { id: 'filing', name: 'Filing', agent: 'filing_agent' },
  ];

  if (!pipelineResult) {
    return stageConfig.map((s, i) => ({
      ...s,
      status: isRunning && i === 0 ? 'running' as const : 'pending' as const,
    }));
  }

  let foundIncomplete = false;
  return stageConfig.map((s) => {
    const stage = pipelineResult[s.id];
    if (!stage) {
      if (!foundIncomplete) {
        foundIncomplete = true;
        return { ...s, status: isRunning ? 'running' as const : 'pending' as const };
      }
      return { ...s, status: 'pending' as const };
    }

    const result = stage.result || {};
    let resultStr = '';
    let confidence: number | undefined;

    switch (s.id) {
      case 'perception':
        resultStr = `${result.issue_type || ''} · ${result.severity || ''}`;
        confidence = result.confidence as number;
        break;
      case 'clustering':
        resultStr = `${result.cluster_size || 0} related reports`;
        break;
      case 'incident_detection':
        resultStr = (result.classification as string || '').replace(/_/g, ' ');
        confidence = result.confidence as number;
        break;
      case 'root_cause': {
        const chain = result.chain as string[] || [];
        resultStr = chain.join(' → ');
        confidence = result.confidence as number;
        break;
      }
      case 'impact':
        resultStr = `${result.score || 0}/100 · ${result.priority || ''}`;
        break;
      case 'response': {
        const steps = result.steps as Array<Record<string, unknown>> || [];
        const approved = result.approved as boolean;
        resultStr = `${steps.length} steps`;
        if (approved) resultStr += ' · Approved';
        break;
      }
      case 'filing':
        resultStr = 'Complaint filed';
        break;
    }

    return {
      ...s,
      status: stage.status === 'complete' ? 'complete' as const : 'pending' as const,
      result: resultStr,
      confidence,
    };
  });
}
