'use client'

import dynamic from 'next/dynamic'
import { useAuth } from '@/contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import Link from 'next/link'
import { 
  FileTextIcon, 
  SearchIcon, 
  ShieldCheckIcon, 
  UploadIcon,
  BarChart3Icon,
  ClockIcon,
  FileIcon,
  ZapIcon,
  UsersIcon,
  SettingsIcon,
  BellIcon,
  MessageCircleIcon,
  TrendingUpIcon,
  AlertTriangleIcon,
  ActivityIcon
} from 'lucide-react'
import ProtectedRoute from '@/components/auth/ProtectedRoute'

function DashboardPage() {
  const { user } = useAuth()

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-900 text-white">
        {/* Sidebar */}
        <div className="fixed left-0 top-0 h-full w-64 bg-gray-800 border-r border-gray-700">
          <div className="p-6">
            {/* Logo */}
            <div className="flex items-center space-x-3 mb-8">
              <div className="w-10 h-10 bg-purple-600 rounded-lg flex items-center justify-center">
                <FileTextIcon className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">Blackletter</h1>
                <p className="text-xs text-gray-400">CONTRACT INTELLIGENCE</p>
              </div>
            </div>

            {/* Navigation */}
            <nav className="space-y-2">
              <Link href="/dashboard" className="flex items-center space-x-3 px-3 py-2 bg-gray-700 rounded-lg text-white">
                <BarChart3Icon className="w-5 h-5" />
                <span>Dashboard</span>
              </Link>
              <Link href="/upload" className="flex items-center space-x-3 px-3 py-2 text-gray-300 hover:bg-gray-700 rounded-lg hover:text-white transition-colors">
                <FileIcon className="w-5 h-5" />
                <span>Contracts</span>
              </Link>
              <Link href="/review" className="flex items-center space-x-3 px-3 py-2 text-gray-300 hover:bg-gray-700 rounded-lg hover:text-white transition-colors">
                <ClockIcon className="w-5 h-5" />
                <span>Review Queue</span>
              </Link>
              <Link href="/templates" className="flex items-center space-x-3 px-3 py-2 text-gray-300 hover:bg-gray-700 rounded-lg hover:text-white transition-colors">
                <FileIcon className="w-5 h-5" />
                <span>Templates</span>
              </Link>
              <Link href="/insights" className="flex items-center space-x-3 px-3 py-2 text-gray-300 hover:bg-gray-700 rounded-lg hover:text-white transition-colors">
                <ZapIcon className="w-5 h-5" />
                <span>AI Insights</span>
              </Link>
              <Link href="/compliance" className="flex items-center space-x-3 px-3 py-2 text-gray-300 hover:bg-gray-700 rounded-lg hover:text-white transition-colors">
                <ShieldCheckIcon className="w-5 h-5" />
                <span>Compliance</span>
              </Link>
              <Link href="/workflows" className="flex items-center space-x-3 px-3 py-2 text-gray-300 hover:bg-gray-700 rounded-lg hover:text-white transition-colors">
                <ActivityIcon className="w-5 h-5" />
                <span>Workflows</span>
              </Link>
              <Link href="/reporting" className="flex items-center space-x-3 px-3 py-2 text-gray-300 hover:bg-gray-700 rounded-lg hover:text-white transition-colors">
                <BarChart3Icon className="w-5 h-5" />
                <span>Reporting</span>
              </Link>
              <Link href="/team" className="flex items-center space-x-3 px-3 py-2 text-gray-300 hover:bg-gray-700 rounded-lg hover:text-white transition-colors">
                <UsersIcon className="w-5 h-5" />
                <span>Team</span>
              </Link>
              <Link href="/settings" className="flex items-center space-x-3 px-3 py-2 text-gray-300 hover:bg-gray-700 rounded-lg hover:text-white transition-colors">
                <SettingsIcon className="w-5 h-5" />
                <span>Settings</span>
              </Link>
            </nav>

            {/* System Health */}
            <div className="mt-8 p-4 bg-gray-700 rounded-lg">
              <div className="flex items-center space-x-2 mb-2">
                <ActivityIcon className="w-4 h-4 text-green-400" />
                <span className="text-sm text-gray-300">System Health</span>
              </div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-2xl font-bold text-green-400">99.9%</span>
                <span className="text-xs text-green-400">All systems operational</span>
              </div>
              <div className="w-full bg-gray-600 rounded-full h-2">
                <div className="bg-green-400 h-2 rounded-full" style={{ width: '99.9%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="ml-64">
          {/* Header */}
          <header className="bg-gray-800 border-b border-gray-700 px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <h1 className="text-2xl font-bold text-white">Dashboard</h1>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span className="text-sm text-green-400">LIVE</span>
                </div>
              </div>

              {/* Search Bar */}
              <div className="flex-1 max-w-md mx-8">
                <div className="relative">
                  <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search contracts, clauses, parties..."
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg pl-10 pr-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* User Actions */}
              <div className="flex items-center space-x-4">
                <button 
                  className="relative p-2 text-gray-300 hover:text-white transition-colors"
                  aria-label="Messages"
                  title="Messages"
                >
                  <MessageCircleIcon className="w-5 h-5" />
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full"></div>
                </button>
                <button 
                  className="relative p-2 text-gray-300 hover:text-white transition-colors"
                  aria-label="Notifications"
                  title="Notifications"
                >
                  <BellIcon className="w-5 h-5" />
                  <div className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center">
                    <span className="text-xs font-bold">7</span>
                  </div>
                </button>
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-purple-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-bold">AC</span>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-white">Alex Chen</p>
                    <p className="text-xs text-gray-400">Senior Legal Counsel</p>
                  </div>
                </div>
              </div>
            </div>
          </header>

          {/* Dashboard Content */}
          <main className="p-8">
            {/* Welcome Section */}
            <div className="mb-8">
              <h2 className="text-3xl font-bold text-white mb-2">Welcome back, Alex</h2>
              <p className="text-gray-300 text-lg">
                You have <span className="text-purple-400 font-semibold">7 contracts</span> pending review and{' '}
                <span className="text-red-400 font-semibold">3 urgent items</span> requiring attention.
              </p>
              <div className="flex space-x-4 mt-4">
                <Button className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg flex items-center space-x-2">
                  <UploadIcon className="w-4 h-4" />
                  <span>+ New Contract</span>
                </Button>
                <Button variant="outline" className="border-gray-600 text-gray-300 hover:bg-gray-700 px-6 py-2 rounded-lg">
                  Schedule Review
                </Button>
              </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {/* Contracts Processed */}
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium text-gray-300">Contracts Processed</CardTitle>
                  <FileTextIcon className="h-4 w-4 text-purple-400" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-white">3,247</div>
                  <p className="text-xs text-gray-400">this month</p>
                  <div className="flex items-center space-x-2 mt-2">
                    <TrendingUpIcon className="w-4 h-4 text-green-400" />
                    <span className="text-sm text-green-400">+18%</span>
                  </div>
                </CardContent>
              </Card>

              {/* AI Risk Score */}
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium text-gray-300">AI Risk Score</CardTitle>
                  <AlertTriangleIcon className="h-4 w-4 text-red-400" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-white">2.1/10</div>
                  <p className="text-xs text-gray-400">avg this month</p>
                  <div className="flex items-center space-x-2 mt-2">
                    <TrendingUpIcon className="w-4 h-4 text-red-400 rotate-180" />
                    <span className="text-sm text-red-400">-24%</span>
                  </div>
                </CardContent>
              </Card>

              {/* Review Velocity */}
              <Card className="bg-gray-800 border-gray-700">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium text-gray-300">Review Velocity</CardTitle>
                  <ClockIcon className="h-4 w-4 text-orange-400" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-white">4.2h</div>
                  <p className="text-xs text-gray-400">avg turnaround</p>
                  <div className="flex items-center space-x-2 mt-2">
                    <TrendingUpIcon className="w-4 h-4 text-red-400 rotate-180" />
                    <span className="text-sm text-red-400">-31%</span>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Recent Activity */}
            <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-bold text-white">Recent Activity</h3>
                <Button variant="outline" className="border-gray-600 text-gray-300 hover:bg-gray-700">
                  View All
                </Button>
              </div>
              
              <div className="space-y-4">
                {/* Contract Items */}
                <div className="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center">
                      <FileTextIcon className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-white">Master Service Agreement - Microsoft Corp</h4>
                      <div className="flex items-center space-x-4 mt-1">
                        <span className="text-xs bg-red-500 text-white px-2 py-1 rounded">URGENT</span>
                        <span className="text-sm text-gray-300">MSA $2.4M • AI: 94%</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-gray-400">Under Review</div>
                    <div className="text-xs text-red-400">High Risk</div>
                  </div>
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center">
                      <FileTextIcon className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-white">Employment Agreement - Senior Developer</h4>
                      <div className="flex items-center space-x-4 mt-1">
                        <span className="text-sm text-gray-300">Employment $180K • AI: 98%</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-green-400">Approved</div>
                    <div className="text-xs text-green-400">Low Risk</div>
                  </div>
                </div>

                <div className="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-orange-600 rounded-lg flex items-center justify-center">
                      <FileTextIcon className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-white">SaaS License Agreement - Salesforce</h4>
                      <div className="flex items-center space-x-4 mt-1">
                        <span className="text-xs bg-red-500 text-white px-2 py-1 rounded">URGENT</span>
                        <span className="text-sm text-gray-300">Software License $500K • AI: 89%</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-orange-400">Needs Attention</div>
                    <div className="text-xs text-red-400">Critical</div>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </ProtectedRoute>
  )
}

export default dynamic(() => Promise.resolve(DashboardPage), {
  ssr: false
})