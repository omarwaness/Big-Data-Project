"use client";
import { useState } from "react";
import { User, Microscope, ArrowRight, AlertCircle } from "lucide-react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<"farmer" | "researcher">("farmer");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setError(""); // Reset error

    // Validation Logic
    if (activeTab === "farmer") {
      if (email === "farm@gmail.com" && password === "123") {
        router.push("/dashboard");
      } else {
        setError("Invalid farmer credentials (Try farm@gmail.com / 123)");
      }
    } else {
      if (email === "research@gmail.com" && password === "123") {
        router.push("/dashboard");
      } else {
        setError("Invalid researcher credentials (Try research@gmail.com / 123)");
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 p-4 font-sans">
      <div className="w-full max-w-md space-y-8 bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-2xl">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-white tracking-tight">Welcome Back</h2>
          <p className="text-slate-400 mt-2">Sign in to your farm portal</p>
        </div>

        {/* Tab Switcher */}
        <div className="flex p-1 bg-slate-950 rounded-xl border border-slate-800">
          <button
            onClick={() => {
                setActiveTab("farmer");
                setError("");
            }}
            className={`flex-1 flex items-center justify-center gap-2 py-2.5 text-sm font-semibold rounded-lg transition-all ${
              activeTab === "farmer" ? "bg-emerald-500 text-slate-950" : "text-slate-500 hover:text-slate-300"
            }`}
          >
            <User size={18} /> Farm User
          </button>
          <button
            onClick={() => {
                setActiveTab("researcher");
                setError("");
            }}
            className={`flex-1 flex items-center justify-center gap-2 py-2.5 text-sm font-semibold rounded-lg transition-all ${
              activeTab === "researcher" ? "bg-emerald-500 text-slate-950" : "text-slate-400 hover:text-slate-300"
            }`}
          >
            <Microscope size={18} /> Researcher
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/20 text-red-500 p-3 rounded-xl flex items-center gap-2 text-sm animate-in fade-in zoom-in duration-200">
            <AlertCircle size={16} /> {error}
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleLogin} className="space-y-5">
          <div className="space-y-2">
            <label className="text-xs uppercase font-bold text-slate-500 tracking-widest ml-1">
              Email Address
            </label>
            <input 
              type="email" 
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={activeTab === "farmer" ? "farm@gmail.com" : "research@gmail.com"}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3.5 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all"
            />
          </div>
          
          <div className="space-y-2">
            <label className="text-xs uppercase font-bold text-slate-500 tracking-widest ml-1">
              Password
            </label>
            <input 
              type="password" 
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3.5 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all"
            />
          </div>
          
          <button
            type="submit"
            className="w-full bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold py-4 rounded-xl flex items-center justify-center gap-2 transition-transform active:scale-95 mt-4"
          >
            Sign In as {activeTab === "farmer" ? "Farmer" : "Researcher"} 
            <ArrowRight size={20} />
          </button>
        </form>

        <p className="text-center text-slate-500 text-sm">
          Don't have an account? <span className="text-emerald-500 cursor-pointer hover:underline">Contact Admin</span>
        </p>
      </div>
    </div>
  );
}