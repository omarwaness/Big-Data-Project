import { connectDB } from "@/lib/db";
import mongoose from "mongoose";
import MetricCard from "@/components/MetricCard";

export default async function IrrigationPage() {
  await connectDB();
  const db = mongoose.connection.db;
  const logs = await db
    ?.collection("irrigation_logic")
    .find()
    .sort({ processed_at: -1 })
    .limit(10)
    .toArray();
  const latest = logs?.[0];

  return (
    <main className="p-8 space-y-8 bg-slate-950 rounded-2xl">
      <header>
        <h2 className="text-3xl font-bold text-white">Irrigation Control</h2>
        <p className="text-slate-400 font-mono text-sm">
          Last Logic Join: {latest?.join_time}
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard
          title="Priority Score"
          value={latest?.priority_score.toFixed(2)}
          status="Calculated"
          color="green"
        />
        <MetricCard
          title="Irrigation Need"
          value={latest?.irrigation_need}
          status="Current State"
          color={latest?.irrigation_need === "HIGH" ? "amber" : "green"}
        />
        <MetricCard
          title="Wind Speed"
          value={latest?.wind_speed}
          unit="km/h"
          status="Active Factor"
          color="green"
        />
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-xl font-bold mb-4">Execution History</h3>
        <div className="space-y-3">
          {logs?.map((log: any) => (
            <div
              key={log._id.toString()}
              className="flex justify-between items-center p-4 bg-slate-800/40 rounded-xl border border-slate-700/50"
            >
              <div>
                <span className="text-emerald-500 font-bold">
                  {log.irrigation_need}
                </span>
                <span className="text-slate-500 text-xs ml-3">
                  {new Date(log.processed_at).toLocaleString()}
                </span>
              </div>
              <div className="text-slate-300 text-sm">
                Score: {log.priority_score.toFixed(1)} | Wind: {log.wind_speed}
                km/h
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
