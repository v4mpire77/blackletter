import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Blackletter Systems',
  description: 'AI Contract Review System',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
