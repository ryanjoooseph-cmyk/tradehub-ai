import Link from 'next/link';
import { ReactNode } from 'react';
import { usePathname } from 'next/navigation';

function NavItem({ href, label }: { href: string; label: string }) {
  // Client-only hook use guard
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const pathname = typeof window === 'undefined' ? '' : (require('next/navigation') as any).usePathname();
  const active = pathname === href;
  return (
    <Link
      href={href}
      style={{
        display: 'block',
        padding: '10px 12px',
        borderRadius: 8,
        textDecoration: 'none',
        fontWeight: active ? 700 : 500,
        background: active ? '#f3f4f6' : 'transparent',
        color: '#111827',
      }}
    >
      {label}
    </Link>
  );
}

export default function AppShell({ children }: { children: ReactNode }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '260px 1fr', minHeight: '100vh' }}>
      <aside style={{ borderRight: '1px solid #e5e7eb', padding: 16 }}>
        <div style={{ fontSize: 18, fontWeight: 800, marginBottom: 12 }}>TradeHub</div>
        <nav style={{ display: 'grid', gap: 6 }}>
          <NavItem href="/" label="Dashboard" />
          <NavItem href="/market" label="Market" />
          <NavItem href="/post-job" label="Post a Job" />
          <NavItem href="/jobs" label="My Jobs" />
          <NavItem href="/payments" label="Payments" />
          <NavItem href="/messages" label="Messages" />
          <NavItem href="/profile" label="Profile / KYC" />
        </nav>
      </aside>
      <div>
        <header
          style={{
            position: 'sticky',
            top: 0,
            zIndex: 10,
            background: '#ffffff',
            borderBottom: '1px solid #e5e7eb',
            padding: '12px 16px',
          }}
        >
          <div style={{ fontWeight: 700 }}>TradeHub Platform</div>
        </header>
        <main style={{ padding: 16 }}>{children}</main>
      </div>
    </div>
  );
}
