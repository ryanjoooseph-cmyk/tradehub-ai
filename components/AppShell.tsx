// components/AppShell.tsx
import Link from "next/link";
import React from "react";

export default function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ maxWidth: 820, margin: "40px auto", padding: 16 }}>
      <header style={{ marginBottom: 24 }}>
        <h1 style={{ margin: 0 }}>TradeHub</h1>
        <nav style={{ marginTop: 8, display: "flex", gap: 12 }}>
          <Link href="/">Home</Link>
          <Link href="/jobs">Jobs</Link>
          <Link href="/market">Market</Link>
        </nav>
      </header>
      <main>{children}</main>
    </div>
  );
}
