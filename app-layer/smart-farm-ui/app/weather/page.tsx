import { connectDB } from "@/lib/db";
import mongoose from "mongoose";
import ForecastList from "@/components/ForecastList";

export default async function WeatherPage() {
  await connectDB();
  const db = mongoose.connection.db;
  const current = await db
    ?.collection("weather_stats")
    .findOne({}, { sort: { start_time: -1 } });
  const forecasts = await db
    ?.collection("forecast_audit")
    .find()
    .sort({ forecast_time: 1 })
    .limit(10)
    .toArray();

  return (
    <main className="p-8 space-y-8 bg-slate-950 rounded-2xl">
      <header>
        <h2 className="text-3xl font-bold text-white">Weather Analysis</h2>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-slate-900 to-emerald-900/20 p-8 rounded-3xl border border-emerald-500/20">
          <p className="text-emerald-500 font-bold uppercase tracking-widest text-xs">
            Current Condition
          </p>
          <h1 className="text-5xl font-black text-white mt-2 capitalize">
            {current?.description}
          </h1>
          <div className="flex gap-8 mt-6">
            <div>
              <p className="text-slate-400 text-sm">Temperature</p>
              <p className="text-2xl font-bold">
                {current?.avg_temp.toFixed(1)}°C
              </p>
            </div>
            <div>
              <p className="text-slate-400 text-sm">Humidity</p>
              <p className="text-2xl font-bold">{current?.avg_humidity}%</p>
            </div>
          </div>
        </div>
      </div>

      <ForecastList forecasts={forecasts} />
    </main>
  );
}
