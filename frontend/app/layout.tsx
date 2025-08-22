import './globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'Blackletter',
  description: 'Contract Intelligence Dashboard',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-950">{children}</body>
    </html>
  );
}
