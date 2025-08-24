export type Severity = "High" | "Medium" | "Low";

export type Issue = {
  rule_id: string;
  description: string;
  compliant: boolean;
  severity: Severity;
  details?: string;
  citation?: string;
  clausePath?: string;
  recommendation?: string;
};

export type ReviewResult =
  | { job_id: string; status: "queued" | "processing"; progress?: number }
  | {
      job_id: string;
      status: "completed";
      summary: string;
      risk: "low" | "medium" | "high";
      issues: Issue[];
      metrics: { precision: number; recall: number; latency_ms: number };
      report: { html_url: string; pdf_url: string };
    };
