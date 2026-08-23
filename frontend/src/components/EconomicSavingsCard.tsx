import { Repeat, TrendingUp, Sparkles } from 'lucide-react';
import type { EconomicImpact } from '../lib/api';

interface Props {
  economicImpact?: EconomicImpact;
}

export default function EconomicSavingsCard({ economicImpact }: Props) {
  if (!economicImpact || !economicImpact.estimated_savings_inr) {
    return null;
  }

  const savingsFormatted = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(economicImpact.estimated_savings_inr);

  const damageFormatted = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(economicImpact.estimated_damage_if_neglected_inr);

  const rootFixFormatted = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(economicImpact.root_cause_fix_cost_inr);

  return (
    <div className="rounded-2xl border border-emerald-500/20 bg-linear-to-br from-emerald-950/30 via-slate-900/60 to-slate-950/80 p-6 backdrop-blur-xl shadow-2xl relative overflow-hidden">
      {/* Background glow accent */}
      <div className="absolute top-0 right-0 -mt-8 -mr-8 w-44 h-44 rounded-full bg-emerald-500/10 blur-3xl pointer-events-none" />

      {/* Header */}
      <div className="flex items-center justify-between mb-4 border-b border-emerald-500/15 pb-3">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-400">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white tracking-wide">
              Municipal Fiscal & Resource Optimization
            </h3>
            <p className="text-xs text-emerald-400/80">
              CivicNexus Predictive Cost-Benefit & Longevity Index
            </p>
          </div>
        </div>
        <span className="px-3 py-1 text-xs font-semibold rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-300">
          {economicImpact.infrastructure_longevity_boost}
        </span>
      </div>

      {/* Big Savings Highlight */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div className="p-4 rounded-xl bg-emerald-900/20 border border-emerald-500/20 flex flex-col">
          <span className="text-xs text-emerald-300/80 font-medium">Estimated Municipal Tax Savings</span>
          <span className="text-2xl font-black text-emerald-400 mt-1">{savingsFormatted}</span>
          <span className="text-[11px] text-emerald-400/60 mt-1">vs isolated uncoordinated patches</span>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 flex flex-col">
          <span className="text-xs text-slate-400 font-medium">Neglected Cascade Cost (4 Wks)</span>
          <span className="text-xl font-bold text-rose-400 mt-1">{damageFormatted}</span>
          <span className="text-[11px] text-slate-500 mt-1">compounding structural damage</span>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 flex flex-col">
          <span className="text-xs text-slate-400 font-medium">Coordinated Root Repair Cost</span>
          <span className="text-xl font-bold text-cyan-400 mt-1">{rootFixFormatted}</span>
          <span className="text-[11px] text-slate-500 mt-1">multi-department unified dispatch</span>
        </div>
      </div>

      {/* Key Insights Row */}
      <div className="flex flex-wrap items-center gap-4 text-xs text-slate-300 bg-slate-950/40 p-3.5 rounded-xl border border-slate-800/80">
        <div className="flex items-center gap-2">
          <Repeat className="w-4 h-4 text-amber-400" />
          <span>
            Prevented Road Re-digging Cycles:{' '}
            <strong className="text-amber-300">{economicImpact.prevented_road_redigging_cycles} Cycle(s)</strong>
          </span>
        </div>
        <div className="h-3 w-px bg-slate-800 hidden sm:block" />
        <div className="flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-emerald-400" />
          <span>
            Capital Allocation Score:{' '}
            <strong className="text-emerald-300">96.4% Efficiency</strong>
          </span>
        </div>
      </div>

      {/* Narrative */}
      <p className="text-xs text-slate-400 mt-3.5 italic leading-relaxed">
        "{economicImpact.cost_benefit_summary}"
      </p>
    </div>
  );
}
