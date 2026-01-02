// app/layout.tsx
import type { Metadata } from "next";
import AppShell from "../components/AppShell";

export const metadata: Metadata = {
  title: "TradeHub",
  description: "Jobs & payments for trades and services."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto" }}>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
