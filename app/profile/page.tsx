"use client";

import { useEffect, useState } from "react";
import { getBrowserClient } from "@/lib/supabase";

export default function ProfilePage() {
  const [ok] = useState(true);

  useEffect(() => {
    // verify the client can be created on the browser
    const sb = getBrowserClient();
    void sb; // no-op
  }, []);

  return (
    <main style={{ padding: 16 }}>
      <h1>TradeHub is up ✅</h1>
      <p>Profile page</p>
    </main>
  );
}
