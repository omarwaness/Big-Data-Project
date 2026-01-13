import Link from "next/link";
import { ArrowRight, Leaf, Droplets, LineChart, Activity } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center p-6">
      {/* Hero Section */}
      <div className="max-w-4xl text-center space-y-6">
        <div className="flex justify-center">
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl text-emerald-500">
            <Leaf size={40} />
          </div>
        </div>

        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tighter">
          Smart Farming <span className="text-emerald-500">Simplified.</span>
        </h1>

        <p className="text-slate-400 text-lg md:text-xl max-w-2xl mx-auto">
          Monitor soil moisture, track irrigation logic, and get real-time
          weather forecasts for your farm in one powerful dashboard.
        </p>

        <div className="flex gap-4 justify-center pt-4">
          <Link
            href="/login"
            className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 px-8 py-4 rounded-xl font-bold flex items-center gap-2 transition-all"
          >
            Get Started <ArrowRight size={20} />
          </Link>
        </div>
      </div>

      {/* Features Preview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-24 max-w-5xl w-full">
        <FeatureCard
          icon={<Droplets className="text-emerald-500" />}
          title="Soil Analysis"
          desc="Real-time moisture and pH level monitoring."
        />
        <FeatureCard
          icon={<LineChart className="text-emerald-500" />}
          title="Predictive Trends"
          desc="5-day forecasts driven by historical data."
        />
        <FeatureCard
          icon={<Activity className="text-emerald-500" />}
          title="Automation"
          desc="Smart irrigation logic based on wind and temp."
        />
      </div>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  desc,
}: {
  icon: React.ReactNode;
  title: string;
  desc: string;
}) {
  return (
    <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl">
      <div className="mb-4">{icon}</div>
      <h3 className="text-lg font-bold mb-2">{title}</h3>
      <p className="text-slate-400 text-sm">{desc}</p>
    </div>
  );
}
