'use client';

import { useEffect } from 'react';
import getBrowserClient from '@/lib/supabase';

export default function ProfilePage() {
  useEffect(() => {
    // instantiate without querying tables (prevents runtime 404s)
    const supabase = getBrowserClient();
    void supabase; // no-op
  }, []);

  return <div>Profile</div>;
}
