import Link from "next/link";
import React from "react";

export default function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ maxWidth: 980, margin: "40px auto", padding: 16 }}>
      <header style={{ display: "flex", gap: 16, alignItems: "center", marginBottom: 24 }}>
        <strong>TradeHub</strong>
        <nav style={{ display: "flex", gap: 12 }}>
          <Link href="/">Home</Link>
          <Link href="/jobs">Jobs</Link>
          <Link href="/market">Market</Link>
        </nav>
      </header>
      <main>{children}</main>
      <footer style={{ marginTop: 48, fontSize: 12, opacity: 0.7 }}>
        © {new Date().getFullYear()} TradeHub
      </footer>
    </div>
  );
}
