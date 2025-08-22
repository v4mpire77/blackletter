'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

export function Navigation() {
  const { user, signOut, loading } = useAuth()
  const router = useRouter()

  const handleSignOut = async () => {
    await signOut()
    router.push('/')
  }

  return (
    <nav>
      <ul className="flex space-x-6 items-center">
        <li><Link href="/" className="hover:text-[#D5A021] transition-colors">Home</Link></li>
        {user && (
          <>
            <li><Link href="/upload" className="hover:text-[#D5A021] transition-colors">Upload</Link></li>
            <li><Link href="/research" className="hover:text-[#D5A021] transition-colors">Research</Link></li>
            <li><Link href="/compliance" className="hover:text-[#D5A021] transition-colors">Compliance</Link></li>
            <li><Link href="/dashboard" className="hover:text-[#D5A021] transition-colors">Dashboard</Link></li>
          </>
        )}
        {!loading && (
          <>
            {user ? (
              <li className="flex items-center space-x-4">
                <span className="text-sm">Welcome, {user.email}</span>
                <Button 
                  onClick={handleSignOut}
                  variant="outline"
                  size="sm"
                  className="text-white border-white hover:bg-white hover:text-[#0A2342]"
                >
                  Sign Out
                </Button>
              </li>
            ) : (
              <>
                <li>
                  <Link href="/auth/login" className="hover:text-[#D5A021] transition-colors">
                    Login
                  </Link>
                </li>
                <li>
                  <Button asChild size="sm" className="bg-[#D5A021] hover:bg-[#D5A021]/90 text-[#0A2342]">
                    <Link href="/auth/register">
                      Register
                    </Link>
                  </Button>
                </li>
              </>
            )}
          </>
        )}
      </ul>
    </nav>
  )
}
