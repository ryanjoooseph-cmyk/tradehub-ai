export const metadata = {
  title: "TradeHub",
  description: "Trade and job management platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ maxWidth: 960, margin: "0 auto", padding: "1.5rem" }}>
        <h1>TradeHub</h1>
        {children}
      </body>
    </html>
  );
}
