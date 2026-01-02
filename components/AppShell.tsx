// components/AppShell.tsx
import Link from "next/link";

export default function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ minHeight: "100vh", background: "#0a0b0d", color: "#e6e6e6" }}>
      <header style={{
        borderBottom: "1px solid #1b1f24",
        position: "sticky", top: 0, zIndex: 10, background: "#0a0b0d"
      }}>
        <div style={{
          maxWidth: 980, margin: "0 auto", display: "flex",
          alignItems: "center", justifyContent: "space-between", padding: "14px 16px"
        }}>
          <Link href="/" style={{ fontWeight: 700, fontSize: 18, letterSpacing: .4 }}>TradeHub</Link>
          <nav style={{ display: "flex", gap: 16, fontSize: 14 }}>
            <Link href="/market">Market</Link>
            <Link href="/messages">Messages</Link>
            <Link href="/jobs">Jobs</Link>
            <Link href="/profile">Profile</Link>
          </nav>
        </div>
      </header>
      <main style={{ maxWidth: 980, margin: "0 auto", padding: 16 }}>{children}</main>
      <footer style={{ borderTop: "1px solid #1b1f24", marginTop: 32, padding: 16, fontSize: 12, opacity: .7 }}>
        © {new Date().getFullYear()} TradeHub
      </footer>
    </div>
  );
}
