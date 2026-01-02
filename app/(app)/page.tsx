export default function Dashboard() {
  const cards = [
    { title: 'Open Jobs', value: '—', hint: 'Connect real data next' },
    { title: 'Active Contracts', value: '—', hint: 'Milestones & escrow' },
    { title: 'Unread Messages', value: '—', hint: 'Realtime inbox' },
    { title: 'Balance (Escrow)', value: '$0.00', hint: 'Stripe/PayID later' },
  ];
  return (
    <div style={{ maxWidth: 1100, margin: '0 auto', display: 'grid', gap: 16 }}>
      <h1 style={{ fontSize: 28, fontWeight: 800 }}>Dashboard</h1>
      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(4, minmax(0,1fr))', gap: 12 }}>
        {cards.map((c) => (
          <div key={c.title} style={{ border: '1px solid #e5e7eb', borderRadius: 12, padding: 16 }}>
            <div style={{ fontSize: 12, opacity: 0.7 }}>{c.title}</div>
            <div style={{ fontSize: 24, fontWeight: 800, marginTop: 6 }}>{c.value}</div>
            <div style={{ fontSize: 12, opacity: 0.6, marginTop: 6 }}>{c.hint}</div>
          </div>
        ))}
      </section>
      <section style={{ border: '1px solid #e5e7eb', borderRadius: 12, padding: 16 }}>
        <div style={{ fontWeight: 700, marginBottom: 8 }}>Getting started</div>
        <ol style={{ margin: 0, paddingLeft: 18 }}>
          <li>Post a job and describe the scope.</li>
          <li>Receive quotes from verified tradies.</li>
          <li>Fund escrow and kick off milestones.</li>
          <li>Release payments on inspection approval.</li>
        </ol>
      </section>
    </div>
  );
}
