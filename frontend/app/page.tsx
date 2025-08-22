import Link from 'next/link'

export default function Home() {
  return (
    <div className="flex flex-col items-center w-full">
      <section className="w-full py-12 md:py-24 lg:py-32">
        <div className="container mx-auto px-4 md:px-6">
          <div className="flex flex-col items-center space-y-6 text-center">
            <div className="space-y-3">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl">
                Blackletter Systems
              </h1>
              <p className="text-xl text-[#D5A021] font-semibold">
                Old rules. New game.
              </p>
              <p className="mx-auto max-w-[700px] text-gray-600 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                Practical legal automation for contract analysis, compliance, and research.
              </p>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 mt-4">
              <Link
                href="/upload"
                className="inline-flex h-10 items-center justify-center rounded-md bg-[#0A2342] px-8 text-sm font-medium text-white shadow transition-colors hover:bg-opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
              >
                Upload Contract
              </Link>
              <Link
                href="/research"
                className="inline-flex h-10 items-center justify-center rounded-md border border-gray-300 bg-white px-8 text-sm font-medium text-gray-700 shadow-sm transition-colors hover:bg-gray-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
              >
                Research
              </Link>
            </div>
          </div>
        </div>
      </section>

      <section className="w-full py-12 md:py-24 lg:py-32 bg-gray-50">
        <div className="container mx-auto px-4 md:px-6">
          <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-3 lg:gap-12">
            <div className="flex flex-col items-center space-y-4 text-center p-6 bg-white rounded-lg shadow-sm">
              <div className="rounded-full bg-[#0A2342] p-3 text-white">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-6 w-6">
                  <path d="M14 3v4a1 1 0 0 0 1 1h4"></path>
                  <path d="M17 21H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7l5 5v11a2 2 0 0 1-2 2z"></path>
                  <line x1="9" y1="9" x2="10" y2="9"></line>
                  <line x1="9" y1="13" x2="15" y2="13"></line>
                  <line x1="9" y1="17" x2="15" y2="17"></line>
                </svg>
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-bold">Contract Analysis</h3>
                <p className="text-sm text-gray-500">
                  Upload contracts for automated review, risk scoring, and redlining based on custom playbooks.
                </p>
              </div>
            </div>
            <div className="flex flex-col items-center space-y-4 text-center p-6 bg-white rounded-lg shadow-sm">
              <div className="rounded-full bg-[#0A2342] p-3 text-white">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-6 w-6">
                  <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                  <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                  <path d="M9 14l2 2 4-4"></path>
                </svg>
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-bold">Compliance Checklist</h3>
                <p className="text-sm text-gray-500">
                  Stay updated with regulatory changes from ICO, FCA, EU, and UK government sources.
                </p>
              </div>
            </div>
            <div className="flex flex-col items-center space-y-4 text-center p-6 bg-white rounded-lg shadow-sm">
              <div className="rounded-full bg-[#0A2342] p-3 text-white">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-6 w-6">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-bold">Research Assistant</h3>
                <p className="text-sm text-gray-500">
                  Semantic search over legal sources with paragraph-level citations and context-aware answers.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}