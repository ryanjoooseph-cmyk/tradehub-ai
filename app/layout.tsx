import type { ReactNode } from "react";
import AppShell from "a/components/AppShell";

export const metadata = {
  title: "TradeHub",
  description: "TradeHub platform"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
