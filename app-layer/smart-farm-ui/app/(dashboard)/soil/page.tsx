import { connectDB } from "@/lib/db";
import mongoose from "mongoose";

export default async function SoilPage() {
  await connectDB();
  const db = mongoose.connection.db;
  const stats = await db
    ?.collection("daily_soil_stats")
    .find()
    .sort({ reading_date: -1 })
    .limit(10)
    .toArray();
  const current = await db
    ?.collection("soil_status")
    .findOne({}, { sort: { processed_at: -1 } });

  return (
    <main className="p-8 space-y-8 bg-slate-950 rounded-2xl">
      <header>
        <h2 className="text-3xl font-bold text-white">Soil Health</h2>
        <div
          className={`mt-2 inline-block px-3 py-1 rounded-full text-xs font-bold bg-${current?.color_code}-500/10 text-${current?.color_code}-500`}
        >
          System Status: {current?.severity}
        </div>
      </header>

      <div className="gap-8">
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
          <h3 className="text-lg font-bold mb-6">
            Historical Data (Daily Avg)
          </h3>
          <div className="space-y-4">
            {stats?.map((day: any) => (
              <div
                key={day._id.toString()}
                className="grid grid-cols-4 p-4 bg-slate-800/30 rounded-xl items-center"
              >
                <div className="text-sm font-medium">
                  {new Date(day.reading_date).toLocaleDateString()}
                </div>
                <div className="text-center text-xs text-slate-400">
                  💧 {day.avg_moisture.toFixed(1)}%
                </div>
                <div className="text-center text-xs text-slate-400">
                  🧪 {day.avg_ph.toFixed(1)}pH
                </div>
                <div className="text-center text-xs text-slate-400">
                  🌡️ {day.avg_temp_c.toFixed(1)}°C
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
