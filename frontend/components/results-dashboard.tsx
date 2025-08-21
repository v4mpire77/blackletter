'use client'

import React, { useMemo, useState } from 'react'
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import { Label } from '@/components/ui/label'
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { Textarea } from '@/components/ui/textarea'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Separator } from '@/components/ui/separator'
import {
  BarChart as RBarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip as RTooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
} from 'recharts'
import {
  ShieldCheck,
  Gavel,
  Scale,
  FileText,
  Filter,
  Search,
  Download,
  RefreshCw,
  Sparkles,
  ExternalLink,
  ClipboardCheck,
  ChevronRight,
  AlertTriangle,
} from 'lucide-react'

import { 
  Issue, 
  ContractAnalysisResult, 
  IssueType, 
  Severity, 
  AnalysisKPIs,
  ChartDataPoint
} from '@/types/contract-analysis'

interface ResultsDashboardProps {
  analysisResult?: ContractAnalysisResult
  onAnalyze?: () => void
  isAnalyzing?: boolean
}

export function ResultsDashboard({ 
  analysisResult, 
  onAnalyze, 
  isAnalyzing = false 
}: ResultsDashboardProps) {
  const [query, setQuery] = useState('')
  const [selectedIssue, setSelectedIssue] = useState<Issue | null>(null)
  const [typeFilter, setTypeFilter] = useState<IssueType | 'All'>('All')
  const [severityFilter, setSeverityFilter] = useState<Severity | 'All'>('All')
  const [statusFilter, setStatusFilter] = useState<'All' | Issue['status']>('All')
  const [gdprFocus, setGdprFocus] = useState(false)
  const [hideResolved, setHideResolved] = useState(false)

  const issues = analysisResult?.issues || []

  const filteredIssues = useMemo(() => {
    return issues.filter((i) => {
      const matchQuery = query
        ? [i.docName, i.citation, i.snippet, i.recommendation, i.clausePath]
            .join(' ')
            .toLowerCase()
            .includes(query.toLowerCase())
        : true
      const matchType = typeFilter === 'All' ? true : i.type === typeFilter
      const matchSeverity = severityFilter === 'All' ? true : i.severity === severityFilter
      const matchStatus = statusFilter === 'All' ? true : i.status === statusFilter
      const matchGdpr = gdprFocus ? i.type === 'GDPR' : true
      const matchResolved = hideResolved ? i.status !== 'Resolved' : true
      return matchQuery && matchType && matchSeverity && matchStatus && matchGdpr && matchResolved
    })
  }, [issues, query, typeFilter, severityFilter, statusFilter, gdprFocus, hideResolved])

  const kpis = useMemo(() => {
    const totalDocs = analysisResult ? 1 : 0
    const high = issues.filter((i) => i.severity === 'High').length
    const medium = issues.filter((i) => i.severity === 'Medium').length
    const low = issues.filter((i) => i.severity === 'Low').length
    const avgConfidence = issues.reduce((a, b) => a + b.confidence, 0) / (issues.length || 1)
    return { totalDocs, high, medium, low, avgConfidence }
  }, [issues, analysisResult])

  const distByType = useMemo(() => {
    const base = { GDPR: 0, Statute: 0, 'Case Law': 0 } as Record<IssueType, number>
    for (const i of filteredIssues) base[i.type]++
    return Object.entries(base).map(([name, value]) => ({ name, value }))
  }, [filteredIssues])

  const distBySeverity = useMemo(() => {
    const base = { High: 0, Medium: 0, Low: 0 } as Record<Severity, number>
    for (const i of filteredIssues) base[i.severity]++
    return [
      { name: 'High', value: base['High'] },
      { name: 'Medium', value: base['Medium'] },
      { name: 'Low', value: base['Low'] },
    ]
  }, [filteredIssues])

  const toPercent = (x: number) => `${Math.round(x * 100)}%`

  const getSeverityColor = (severity: Severity) => {
    switch (severity) {
      case 'High':
        return 'text-red-600 bg-red-50 border-red-200'
      case 'Medium':
        return 'text-orange-600 bg-orange-50 border-orange-200'
      case 'Low':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200'
    }
  }

  const exportCSV = () => {
    const headers = ['ID', 'Document', 'Type', 'Severity', 'Confidence', 'Status', 'Citation', 'Issue', 'Recommendation']
    const rows = filteredIssues.map(i => [
      i.id,
      i.docName,
      i.type,
      i.severity,
      toPercent(i.confidence),
      i.status,
      i.citation,
      i.snippet.replace(/,/g, ';'),
      i.recommendation.replace(/,/g, ';')
    ])
    const csv = [headers, ...rows].map(row => row.join(',')).join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'contract-analysis.csv'
    a.click()
    URL.revokeObjectURL(url)
  }

  if (!analysisResult) {
    return (
      <div className="p-8 text-center">
        <div className="max-w-md mx-auto">
          <FileText className="h-16 w-16 mx-auto text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold mb-2">No Analysis Results</h3>
          <p className="text-muted-foreground mb-4">
            Upload and analyze a contract to see detailed results here.
          </p>
          {onAnalyze && (
            <Button onClick={onAnalyze} disabled={isAnalyzing}>
              {isAnalyzing ? (
                <>
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Sparkles className="h-4 w-4 mr-2" />
                  Start Analysis
                </>
              )}
            </Button>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">{analysisResult.contractName}</h1>
          <p className="text-muted-foreground">
            Analyzed on {new Date(analysisResult.uploadedAt).toLocaleDateString()}
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={exportCSV}>
            <Download className="h-4 w-4 mr-2" />
            Export CSV
          </Button>
          {onAnalyze && (
            <Button onClick={onAnalyze} disabled={isAnalyzing}>
              <RefreshCw className={`h-4 w-4 mr-2 ${isAnalyzing ? 'animate-spin' : ''}`} />
              Re-analyze
            </Button>
          )}
        </div>
      </div>

      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="issues">Issues</TabsTrigger>
          <TabsTrigger value="risk">Risk Analysis</TabsTrigger>
          <TabsTrigger value="compliance">Compliance</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          {/* KPI Cards */}
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Total Issues</CardTitle>
              </CardHeader>
              <CardContent className="text-2xl font-semibold">
                {analysisResult.totalIssues}
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Risk Score</CardTitle>
              </CardHeader>
              <CardContent className="text-2xl font-semibold text-red-600">
                {analysisResult.riskScore}/100
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Compliance Score</CardTitle>
              </CardHeader>
              <CardContent className="text-2xl font-semibold text-green-600">
                {analysisResult.complianceScore}/100
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Avg Confidence</CardTitle>
              </CardHeader>
              <CardContent className="text-2xl font-semibold">
                {toPercent(analysisResult.averageConfidence)}
              </CardContent>
            </Card>
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            <Card>
              <CardHeader className="pb-0">
                <CardTitle className="flex items-center gap-2 text-base">
                  <Gavel className="h-4 w-4" /> Issues by Type
                </CardTitle>
              </CardHeader>
              <CardContent className="h-56">
                <ResponsiveContainer width="100%" height="100%">
                  <RBarChart data={distByType}>
                    <XAxis dataKey="name" />
                    <YAxis allowDecimals={false} />
                    <RTooltip />
                    <Bar dataKey="value" fill="hsl(var(--primary))" />
                  </RBarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-0">
                <CardTitle className="flex items-center gap-2 text-base">
                  <AlertTriangle className="h-4 w-4" /> Severity Distribution
                </CardTitle>
              </CardHeader>
              <CardContent className="h-56">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={distBySeverity}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}`}
                    >
                      {distBySeverity.map((entry, index) => (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={entry.name === 'High' ? '#ef4444' : entry.name === 'Medium' ? '#f97316' : '#eab308'} 
                        />
                      ))}
                    </Pie>
                    <RTooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="issues" className="space-y-6">
          {/* Filters */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Filter className="h-4 w-4" />
                Filters & Search
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-wrap gap-4">
                <div className="flex-1 min-w-64">
                  <Label htmlFor="search">Search</Label>
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                    <Input
                      id="search"
                      placeholder="Search issues, citations, recommendations..."
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <Label>Type</Label>
                  <Select value={typeFilter} onValueChange={(v) => setTypeFilter(v as IssueType | 'All')}>
                    <SelectTrigger className="w-36">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="All">All Types</SelectItem>
                      <SelectItem value="GDPR">GDPR</SelectItem>
                      <SelectItem value="Statute">Statute</SelectItem>
                      <SelectItem value="Case Law">Case Law</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label>Severity</Label>
                  <Select value={severityFilter} onValueChange={(v) => setSeverityFilter(v as Severity | 'All')}>
                    <SelectTrigger className="w-32">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="All">All</SelectItem>
                      <SelectItem value="High">High</SelectItem>
                      <SelectItem value="Medium">Medium</SelectItem>
                      <SelectItem value="Low">Low</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div className="flex flex-wrap gap-4 items-center">
                <div className="flex items-center space-x-2">
                  <Switch
                    id="gdpr-focus"
                    checked={gdprFocus}
                    onCheckedChange={setGdprFocus}
                  />
                  <Label htmlFor="gdpr-focus">GDPR Focus</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Switch
                    id="hide-resolved"
                    checked={hideResolved}
                    onCheckedChange={setHideResolved}
                  />
                  <Label htmlFor="hide-resolved">Hide Resolved</Label>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Issues Table */}
          <Card>
            <CardHeader>
              <CardTitle>Issues ({filteredIssues.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Type</TableHead>
                    <TableHead>Severity</TableHead>
                    <TableHead>Issue</TableHead>
                    <TableHead>Confidence</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredIssues.map((issue) => (
                    <TableRow key={issue.id}>
                      <TableCell>
                        <Badge variant="outline">{issue.type}</Badge>
                      </TableCell>
                      <TableCell>
                        <Badge className={getSeverityColor(issue.severity)}>
                          {issue.severity}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div>
                          <div className="font-medium">{issue.clausePath}</div>
                          <div className="text-sm text-muted-foreground truncate max-w-xs">
                            {issue.snippet}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>{toPercent(issue.confidence)}</TableCell>
                      <TableCell>
                        <Badge variant="secondary">{issue.status}</Badge>
                      </TableCell>
                      <TableCell>
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button variant="outline" size="sm">
                              View
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="max-w-2xl">
                            <DialogHeader>
                              <DialogTitle>{issue.clausePath}</DialogTitle>
                            </DialogHeader>
                            <div className="space-y-4">
                              <div>
                                <Label className="text-sm font-medium">Citation</Label>
                                <p className="text-sm">{issue.citation}</p>
                              </div>
                              <div>
                                <Label className="text-sm font-medium">Issue</Label>
                                <p className="text-sm">{issue.snippet}</p>
                              </div>
                              <div>
                                <Label className="text-sm font-medium">Recommendation</Label>
                                <p className="text-sm">{issue.recommendation}</p>
                              </div>
                              <div className="flex gap-4">
                                <div>
                                  <Label className="text-sm font-medium">Confidence</Label>
                                  <p className="text-sm">{toPercent(issue.confidence)}</p>
                                </div>
                                <div>
                                  <Label className="text-sm font-medium">Status</Label>
                                  <p className="text-sm">{issue.status}</p>
                                </div>
                              </div>
                            </div>
                          </DialogContent>
                        </Dialog>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="risk" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Risk Analysis</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 border rounded-lg">
                  <div className="text-2xl font-bold text-red-600">
                    {analysisResult.highRiskIssues}
                  </div>
                  <div className="text-sm text-muted-foreground">High Risk Issues</div>
                </div>
                <div className="text-center p-4 border rounded-lg">
                  <div className="text-2xl font-bold text-orange-600">
                    {analysisResult.mediumRiskIssues}
                  </div>
                  <div className="text-sm text-muted-foreground">Medium Risk Issues</div>
                </div>
                <div className="text-center p-4 border rounded-lg">
                  <div className="text-2xl font-bold text-yellow-600">
                    {analysisResult.lowRiskIssues}
                  </div>
                  <div className="text-sm text-muted-foreground">Low Risk Issues</div>
                </div>
              </div>
              <div className="p-4 bg-muted rounded-lg">
                <h4 className="font-medium mb-2">Risk Summary</h4>
                <p className="text-sm text-muted-foreground">
                  {analysisResult.summary}
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="compliance" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Compliance Overview</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <ShieldCheck className="h-5 w-5 text-green-600" />
                    <span>GDPR Compliance</span>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-semibold">{analysisResult.complianceScore}%</div>
                    <div className="text-sm text-muted-foreground">
                      {issues.filter(i => i.type === 'GDPR').length} issues found
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <Scale className="h-5 w-5 text-blue-600" />
                    <span>UK Statute Compliance</span>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-semibold">
                      {Math.round((1 - issues.filter(i => i.type === 'Statute').length / 10) * 100)}%
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {issues.filter(i => i.type === 'Statute').length} issues found
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <Gavel className="h-5 w-5 text-purple-600" />
                    <span>Case Law Alignment</span>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-semibold">
                      {Math.round((1 - issues.filter(i => i.type === 'Case Law').length / 5) * 100)}%
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {issues.filter(i => i.type === 'Case Law').length} issues found
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}