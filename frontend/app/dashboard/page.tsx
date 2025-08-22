'use client'

import { useAuth } from '@/contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import Link from 'next/link'
import { FileTextIcon, SearchIcon, ShieldCheckIcon, UploadIcon } from 'lucide-react'
import ProtectedRoute from '@/components/auth/ProtectedRoute'

export default function DashboardPage() {
  const { user } = useAuth()

  return (
    <ProtectedRoute>
      <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-3xl font-bold text-[#0A2342]">Welcome to Your Dashboard</h1>
        <p className="text-gray-600">
          Hello, {user?.user_metadata?.first_name || user?.email}! Manage your legal documents and compliance here.
        </p>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader className="text-center">
            <UploadIcon className="h-12 w-12 mx-auto text-[#0A2342] mb-2" />
            <CardTitle className="text-lg">Upload Documents</CardTitle>
            <CardDescription>Upload contracts and legal documents for analysis</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full bg-[#0A2342] hover:bg-[#0A2342]/90">
              <Link href="/upload">Start Upload</Link>
            </Button>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader className="text-center">
            <SearchIcon className="h-12 w-12 mx-auto text-[#0A2342] mb-2" />
            <CardTitle className="text-lg">Research</CardTitle>
            <CardDescription>Search through legal documents and precedents</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full bg-[#0A2342] hover:bg-[#0A2342]/90">
              <Link href="/research">Start Research</Link>
            </Button>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader className="text-center">
            <ShieldCheckIcon className="h-12 w-12 mx-auto text-[#0A2342] mb-2" />
            <CardTitle className="text-lg">Compliance</CardTitle>
            <CardDescription>Check compliance with regulations and standards</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full bg-[#0A2342] hover:bg-[#0A2342]/90">
              <Link href="/compliance">Check Compliance</Link>
            </Button>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader className="text-center">
            <FileTextIcon className="h-12 w-12 mx-auto text-[#0A2342] mb-2" />
            <CardTitle className="text-lg">Recent Documents</CardTitle>
            <CardDescription>View your recently uploaded and analyzed documents</CardDescription>
          </CardHeader>
          <CardContent>
            <Button className="w-full bg-[#0A2342] hover:bg-[#0A2342]/90" disabled>
              Coming Soon
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* User Info */}
      <Card>
        <CardHeader>
          <CardTitle>Account Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium text-gray-700">Email</label>
              <p className="mt-1 text-sm text-gray-900">{user?.email}</p>
            </div>
            {user?.user_metadata?.first_name && (
              <div>
                <label className="text-sm font-medium text-gray-700">Name</label>
                <p className="mt-1 text-sm text-gray-900">
                  {user.user_metadata.first_name} {user.user_metadata.last_name}
                </p>
              </div>
            )}
            {user?.user_metadata?.company && (
              <div>
                <label className="text-sm font-medium text-gray-700">Company</label>
                <p className="mt-1 text-sm text-gray-900">{user.user_metadata.company}</p>
              </div>
            )}
            <div>
              <label className="text-sm font-medium text-gray-700">Member Since</label>
              <p className="mt-1 text-sm text-gray-900">
                {new Date(user?.created_at || '').toLocaleDateString()}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
      </div>
    </ProtectedRoute>
  )
}