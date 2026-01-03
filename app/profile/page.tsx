"use client";

import { useEffect, useState } from "react";
import { getBrowserClient } from "@/lib/supabase";

type Profile = { id: string; full_name: string | null; bio: string | null };

export default function ProfilePage() {
  const [data, setData] = useState<Profile[] | null>(null);

  useEffect(() => {
    const supabase = getBrowserClient();
    supabase.from("profiles").select("*").then(({ data }) => setData(data as any));
  }, []);

  return <pre style={{ padding: 24 }}>{JSON.stringify(data, null, 2) || "null"}</pre>;
}
