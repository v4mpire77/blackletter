import Link from 'next/link'
import { FileTextIcon, ShieldCheckIcon, SearchIcon, UploadIcon, ArrowRightIcon } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-8 py-6">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-purple-600 rounded-lg flex items-center justify-center">
              <FileTextIcon className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Blackletter</h1>
              <p className="text-xs text-gray-400">CONTRACT INTELLIGENCE</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <Link
              href="/auth/login"
              className="text-gray-300 hover:text-white transition-colors"
            >
              Sign In
            </Link>
            <Link
              href="/auth/register"
              className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-8">
        <div className="max-w-6xl mx-auto text-center">
          <div className="space-y-6">
            <h1 className="text-5xl md:text-6xl font-bold tracking-tight">
              <span className="text-white">Blackletter</span>
              <span className="text-purple-400"> Systems</span>
            </h1>
            <p className="text-2xl text-[#D5A021] font-semibold">
              Old rules. New game.
            </p>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Practical legal automation for contract analysis, compliance, and research. 
              AI-powered insights that legal professionals can trust.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
              <Link
                href="/upload"
                className="inline-flex items-center justify-center bg-purple-600 hover:bg-purple-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-colors"
              >
                <UploadIcon className="w-5 h-5 mr-2" />
                Upload Contract
                <ArrowRightIcon className="w-5 h-5 ml-2" />
              </Link>
              <Link
                href="/dashboard"
                className="inline-flex items-center justify-center border border-gray-600 text-gray-300 hover:bg-gray-800 px-8 py-4 rounded-lg text-lg font-semibold transition-colors"
              >
                View Dashboard
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-8 bg-gray-800">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">Contract Intelligence Platform</h2>
            <p className="text-xl text-gray-300">Everything you need for modern legal practice</p>
          </div>
          
          <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-3">
            <div className="text-center p-8 bg-gray-700 rounded-lg border border-gray-600">
              <div className="w-16 h-16 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <FileTextIcon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-4">Contract Analysis</h3>
              <p className="text-gray-300">
                Upload contracts for automated review, risk scoring, and redlining based on custom playbooks.
              </p>
            </div>
            
            <div className="text-center p-8 bg-gray-700 rounded-lg border border-gray-600">
              <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <ShieldCheckIcon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-4">Compliance Checklist</h3>
              <p className="text-gray-300">
                Stay updated with regulatory changes from ICO, FCA, EU, and UK government sources.
              </p>
            </div>
            
            <div className="text-center p-8 bg-gray-700 rounded-lg border border-gray-600">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <SearchIcon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-4">Research Assistant</h3>
              <p className="text-gray-300">
                Semantic search over legal sources with paragraph-level citations and context-aware answers.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-6">Ready to Transform Your Legal Practice?</h2>
          <p className="text-xl text-gray-300 mb-8">
            Join leading law firms and legal departments using AI to work smarter, not harder.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/auth/register"
              className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-colors"
            >
              Start Free Trial
            </Link>
            <Link
              href="/dashboard"
              className="border border-gray-600 text-gray-300 hover:bg-gray-800 px-8 py-4 rounded-lg text-lg font-semibold transition-colors"
            >
              View Demo
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 py-12 px-8">
        <div className="max-w-6xl mx-auto text-center">
          <div className="flex items-center justify-center space-x-3 mb-6">
            <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
              <FileTextIcon className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Blackletter</h3>
              <p className="text-xs text-gray-400">CONTRACT INTELLIGENCE</p>
            </div>
          </div>
          <p className="text-gray-400 mb-4">
            © 2025 Blackletter Systems. All rights reserved.
          </p>
          <div className="flex justify-center space-x-6 text-sm text-gray-400">
            <Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link>
            <Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link>
            <Link href="/security" className="hover:text-white transition-colors">Security</Link>
            <Link href="/support" className="hover:text-white transition-colors">Support</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}