// app/page.tsx
import Link from "next/link";

export default function Home() {
  return (
    <div>
      <h2>Welcome</h2>
      <p>This is the starter UI scaffold.</p>
      <ul>
        <li><Link href="/jobs">Jobs</Link></li>
        <li><Link href="/market">Market</Link></li>
      </ul>
    </div>
  );
}
