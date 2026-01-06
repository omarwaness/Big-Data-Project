"use client";
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Droplets, Thermometer, CloudSun } from 'lucide-react';

export default function Sidebar() {
  const pathname = usePathname();

  const menuItems = [
    { icon: <LayoutDashboard size={20}/>, label: 'Dashboard', href: '/' },
    { icon: <Droplets size={20}/>, label: 'Irrigation', href: '/irrigation' },
    { icon: <CloudSun size={20}/>, label: 'Weather', href: '/weather' },
    { icon: <Thermometer size={20}/>, label: 'Soil Analysis', href: '/soil' },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-900 h-screen p-6 flex flex-col sticky top-0">
      <div className="flex items-center gap-3 mb-10">
        <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center">
          <Droplets className="text-white" size={20} />
        </div>
        <h1 className="text-xl font-bold text-white tracking-tight">SmartFarm</h1>
      </div>
      
      <nav className="flex-1 space-y-2">
        {menuItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link 
              key={item.href} 
              href={item.href}
              className={`flex items-center gap-3 p-3 rounded-xl transition-all ${
                isActive ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20' : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`}
            >
              {item.icon}
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}