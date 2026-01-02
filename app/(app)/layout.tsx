import './styles.css';
import AppShell from '@/components/AppShell';
import { ReactNode } from 'react';

export const metadata = { title: 'TradeHub' };

export default function Layout({ children }: { children: ReactNode }) {
  return <AppShell>{children}</AppShell>;
}
