export default function MetricCard({ title, value, unit, status, color }: any) {
  return (
    <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
      <p className="text-slate-400 text-sm font-medium">{title}</p>
      <div className="flex items-baseline gap-1 mt-2">
        <h3 className="text-2xl font-bold text-white">{value}</h3>
        <span className="text-slate-500 text-sm">{unit}</span>
      </div>
      <div className={`mt-3 text-xs font-semibold px-2 py-1 rounded-full w-fit ${color === 'green' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-amber-500/10 text-amber-500'}`}>
        {status}
      </div>
    </div>
  );
}