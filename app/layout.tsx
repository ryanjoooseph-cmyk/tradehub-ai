import type { Metadata } from 'next';
import AppShell from '@/components/AppShell';
import React from 'react';

export const metadata: Metadata = {
  title: 'TradeHub',
  description: 'Trade & jobs platform'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: 'system-ui, -apple-system, Segoe UI, Roboto, sans-serif' }}>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
