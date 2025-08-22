import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { AuthProvider } from '@/contexts/AuthContext'
import { Navigation } from '@/components/Navigation'

// Load Inter font with all weights
const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

export const metadata: Metadata = {
  title: 'Blackletter Systems',
  description: 'Legal automation platform for contract analysis and compliance',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} ${inter.variable} font-sans h-full antialiased`}>
        <AuthProvider>
          <div className="flex min-h-screen flex-col bg-white">
            <header className="bg-[#0A2342] text-white py-4 shadow-md">
              <div className="container mx-auto px-4 flex justify-between items-center">
                <h1 className="text-xl font-bold">Blackletter Systems</h1>
                <Navigation />
              </div>
            </header>
            
            <main className="flex-grow container mx-auto px-4 py-8">
              {children}
            </main>
            
            <footer className="bg-[#0A2342] text-white py-6 mt-auto">
              <div className="container mx-auto px-4">
                <div className="flex flex-col md:flex-row justify-between">
                  <div>
                    <h2 className="text-lg font-semibold mb-2">Blackletter Systems</h2>
                    <p className="text-sm text-gray-300">Old rules. New game.</p>
                  </div>
                  <div className="mt-4 md:mt-0">
                    <p className="text-sm text-gray-300">&copy; {new Date().getFullYear()} Blackletter Systems</p>
                  </div>
                </div>
              </div>
            </footer>
          </div>
        </AuthProvider>
      </body>
    </html>
  )
}