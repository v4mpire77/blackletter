// TypeScript interfaces for contract analysis system
export type IssueType = "GDPR" | "Statute" | "Case Law";
export type Severity = "High" | "Medium" | "Low";
export type IssueStatus = "Open" | "In Review" | "Resolved";

export interface ContractClause {
  id: string;
  path: string;
  text: string;
  issues: string[]; // issue IDs
}

export interface Issue {
  id: string;
  docId: string;
  docName: string;
  clausePath: string; // e.g., "2.1 → Data Processing → Subprocessors"
  type: IssueType;
  citation: string; // e.g., "UK GDPR Art. 28(3)(d)" or "Data Protection Act 2018 s.57" or case citation
  severity: Severity;
  confidence: number; // 0-1
  status: IssueStatus;
  owner?: string;
  snippet: string;
  recommendation: string;
  createdAt: string; // ISO timestamp
}

export interface ContractAnalysisResult {
  id: string;
  contractName: string;
  uploadedAt: string;
  status: "processing" | "completed" | "error";
  summary?: string;
  totalIssues: number;
  highRiskIssues: number;
  mediumRiskIssues: number;
  lowRiskIssues: number;
  averageConfidence: number;
  clauses: ContractClause[];
  issues: Issue[];
  riskScore: number; // 0-100
  complianceScore: number; // 0-100
}

export interface ProcessingStage {
  name: string;
  status: "pending" | "in_progress" | "completed" | "error";
  progress: number; // 0-100
  startTime?: string;
  endTime?: string;
  description: string;
}

export interface AnalysisKPIs {
  totalDocs: number;
  high: number;
  medium: number;
  low: number;
  avgConfidence: number;
}

export interface ChartDataPoint {
  name: string;
  value: number;
}

export interface TimelineDataPoint {
  date: string;
  issues: number;
}