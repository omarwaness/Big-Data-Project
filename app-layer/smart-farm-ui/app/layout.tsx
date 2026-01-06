import Sidebar from "@/components/Sidebar";
import "./globals.css";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-900 text-slate-100 flex min-h-screen">
        <Sidebar />
        <div className="flex-1 mt-4">{children}</div>
      </body>
    </html>
  );
}
