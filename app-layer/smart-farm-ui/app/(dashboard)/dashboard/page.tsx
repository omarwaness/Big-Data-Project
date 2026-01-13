import { connectDB } from "@/lib/db";
import mongoose from "mongoose";
import MetricCard from "@/components/MetricCard";
import ForecastList from "@/components/ForecastList";
import { Wind } from "lucide-react";
import { Activity } from "lucide-react";
import { Calendar } from "lucide-react";

async function getFarmData() {
  await connectDB();
  const db = mongoose.connection.db;

  // Fetching the latest data from all collections
  const currentSoil = await db
    ?.collection("soil_status")
    .findOne({}, { sort: { processed_at: -1 } });
  const irrigation = await db
    ?.collection("irrigation_logic")
    .findOne({}, { sort: { processed_at: -1 } });
  const weather = await db
    ?.collection("weather_stats")
    .findOne({}, { sort: { start_time: -1 } });

  // Fetching multiple documents for lists/trends
  const forecasts = await db
    ?.collection("forecast_audit")
    .find({})
    .sort({ forecast_time: -1 })
    .limit(5)
    .toArray();
  const dailyStats = await db
    ?.collection("daily_soil_stats")
    .find({})
    .sort({ reading_date: -1 })
    .limit(3)
    .toArray();

  return { currentSoil, irrigation, weather, forecasts, dailyStats };
}

export default async function Dashboard() {
  const data = await getFarmData();

  return (
    /* Removed the outer <div> wrapper to prevent layout nesting issues */
    <main className="h-full w-full p-8 space-y-8 overflow-y-auto scrollbar-hide bg-slate-950 rounded-2xl">
      <header>
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-3xl font-bold text-white tracking-tight">
              Farm Dashboard
            </h2>
            <p className="text-slate-400 mt-1">
              Status as of {new Date().toLocaleTimeString()}
            </p>
          </div>
          <div className="flex gap-4">
            <div className="bg-slate-900 border border-slate-800 px-4 py-2 rounded-xl flex items-center gap-2">
              <Wind className="text-emerald-500" size={18} />
              <span className="text-sm font-medium">
                {data.irrigation?.wind_speed} km/h
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* ROW 1: Real-time Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <MetricCard
          title="Soil Moisture"
          value={data.currentSoil?.soil_moisture}
          unit="%"
          status={data.currentSoil?.severity}
          color={data.currentSoil?.color_code}
        />
        <MetricCard
          title="Avg Soil pH"
          value={data.currentSoil?.soil_ph}
          unit="pH"
          status="Optimal"
          color="green"
        />
        <MetricCard
          title="Irrigation Priority"
          value={data.irrigation?.priority_score?.toFixed(0)}
          unit="Score"
          status={data.irrigation?.irrigation_need}
          color={
            data.irrigation?.irrigation_need === "HIGH" ? "amber" : "green"
          }
        />
        <MetricCard
          title="Air Temp"
          value={data.weather?.avg_temp?.toFixed(1)}
          unit="°C"
          status={data.weather?.description}
          color="green"
        />
      </div>

      {/* ROW 2: Forecast and Daily History */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <ForecastList forecasts={data.forecasts} />
        </div>

        <div className="space-y-6">
          <h3 className="font-bold text-lg text-white flex items-center gap-2">
            <Calendar size={20} className="text-emerald-500" />
            Daily Historical Averages
          </h3>
          <div className="space-y-4">
            {data.dailyStats?.map((stat: any) => (
              <div
                key={stat._id}
                className="bg-slate-900 border border-slate-800 p-4 rounded-2xl transition-hover hover:border-emerald-500/30"
              >
                <p className="text-emerald-500 text-xs font-bold mb-2">
                  {new Date(stat.reading_date).toLocaleDateString()}
                </p>
                <div className="grid grid-cols-3 gap-2">
                  <div>
                    <p className="text-[10px] text-slate-500 uppercase">
                      Moisture
                    </p>
                    <p className="text-sm font-semibold text-white">
                      {stat.avg_moisture.toFixed(1)}%
                    </p>
                  </div>
                  <div>
                    <p className="text-[10px] text-slate-500 uppercase">pH</p>
                    <p className="text-sm font-semibold text-white">
                      {stat.avg_ph.toFixed(1)}
                    </p>
                  </div>
                  <div>
                    <p className="text-[10px] text-slate-500 uppercase">Temp</p>
                    <p className="text-sm font-semibold text-white">
                      {stat.avg_temp_c.toFixed(1)}°C
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Alert Footer */}
      <div className="bg-emerald-500/10 border border-emerald-500/20 p-6 rounded-2xl flex items-center gap-4">
        <div className="p-3 bg-emerald-500/20 rounded-full text-emerald-500">
          <Activity size={24} />
        </div>
        <div className="flex-1">
          <h4 className="text-emerald-500 font-bold">
            Automation Logic Active
          </h4>
          <p className="text-slate-400 text-sm">
            System is currently in <b>{data.irrigation?.irrigation_need}</b>{" "}
            mode based on {data.irrigation?.wind_speed} km/h winds.
          </p>
        </div>
        <p className="text-slate-500 text-[10px] uppercase font-mono">
          Updated:{" "}
          {new Date(data.currentSoil?.processed_at).toLocaleTimeString()}
        </p>
      </div>
    </main>
  );
}
