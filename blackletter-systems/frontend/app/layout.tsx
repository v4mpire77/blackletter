import './globals.css';

export const metadata = { title: "Blackletter" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="container">
          <div className="card">{children}</div>
        </div>
      </body>
    </html>
  );
}
