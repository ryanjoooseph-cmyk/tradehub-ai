// components/AppShell.tsx
'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import React from 'react';

const tabs = [
  { href: '/', label: 'Dashboard' },
  { href: '/jobs', label: 'Jobs' },
  { href: '/market', label: 'Market' },
  { href: '/messages', label: 'Messages' },
  { href: '/profile', label: 'Profile' },
];

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '240px 1fr', minHeight: '100vh' }}>
      <aside style={{ borderRight: '1px solid #e5e7eb', padding: 16 }}>
        <div style={{ fontWeight: 700, fontSize: 18, marginBottom: 16 }}>TradeHub</div>
        <nav>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            {tabs.map(t => {
              const active = pathname === t.href || (t.href !== '/' && pathname.startsWith(t.href));
              return (
                <li key={t.href} style={{ marginBottom: 8 }}>
                  <Link
                    href={t.href}
                    style={{
                      display: 'block',
                      padding: '8px 10px',
                      borderRadius: 8,
                      textDecoration: 'none',
                      background: active ? '#eef2ff' : 'transparent',
                      color: active ? '#3730a3' : '#111827',
                      fontWeight: active ? 700 : 500,
                    }}
                  >
                    {t.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      </aside>
      <main style={{ padding: 24 }}>{children}</main>
    </div>
  );
}
