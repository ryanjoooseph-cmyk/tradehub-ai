'use client';
import { useEffect, useState } from 'react';
import { getBrowserClient } from '@/lib/supabase';

type Profile = { id: string; full_name: string | null; bio: string | null };

export default function ProfilePage() {
  const [profiles, setProfiles] = useState<Profile[] | null>(null);

  useEffect(() => {
    const sb = getBrowserClient();
    sb.from('profiles').select('id, full_name, bio').then(({ data }) => {
      setProfiles((data as any) ?? []);
    });
  }, []);

  return (
    <main>
      <h1>Profile</h1>
      <pre>{JSON.stringify(profiles, null, 2)}</pre>
    </main>
  );
}
