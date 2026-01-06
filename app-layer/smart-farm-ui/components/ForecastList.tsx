export default function ForecastList({ forecasts }: any) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
      <div className="p-5 border-b border-slate-800 flex justify-between items-center">
        <h3 className="font-bold text-lg text-white">Weather Forecast & Risks</h3>
        <span className="text-xs text-emerald-500 bg-emerald-500/10 px-2 py-1 rounded">AI Predicted</span>
      </div>
      <table className="w-full text-left text-sm">
        <thead className="bg-slate-800/50 text-slate-400">
          <tr>
            <th className="p-4 font-medium">Time</th>
            <th className="p-4 font-medium">Condition</th>
            <th className="p-4 font-medium">Rain (mm)</th>
            <th className="p-4 font-medium">Risk Level</th>
            <th className="p-4 font-medium">Action Required</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {forecasts?.map((f: any) => (
            <tr key={f._id} className="hover:bg-slate-800/30 transition-colors">
              <td className="p-4 text-slate-300">{new Date(f.forecast_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</td>
              <td className="p-4 text-white capitalize">{f.desc}</td>
              <td className="p-4 text-slate-300">{f.rain}mm</td>
              <td className="p-4">
                <span className={`px-2 py-1 rounded-md text-[10px] font-bold ${f.risk_level.includes('LOW') ? 'bg-emerald-500/10 text-emerald-500' : 'bg-rose-500/10 text-rose-500'}`}>
                  {f.risk_level}
                </span>
              </td>
              <td className="p-4 text-slate-400 italic text-xs">{f.action_required}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}