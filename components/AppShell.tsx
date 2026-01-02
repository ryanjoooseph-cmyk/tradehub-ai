'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import React from 'react';

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const LinkItem = ({ href, label }: { href: string; label: string }) => (
    <Link
      href={href}
      style={{
        padding: '8px 12px',
        borderRadius: 8,
        textDecoration: 'none',
        fontWeight: 600,
        opacity: pathname === href ? 1 : 0.6
      }}
    >
      {label}
    </Link>
  );

  return (
    <div style={{ maxWidth: 960, margin: '0 auto', padding: 16 }}>
      <header style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 16 }}>
        <div style={{ fontWeight: 800, fontSize: 18 }}>TradeHub</div>
        <nav style={{ display: 'flex', gap: 8 }}>
          <LinkItem href="/" label="Home" />
          <LinkItem href="/market" label="Market" />
          <LinkItem href="/jobs" label="Jobs" />
          <LinkItem href="/profile" label="Profile" />
        </nav>
      </header>
      <main>{children}</main>
    </div>
  );
}
