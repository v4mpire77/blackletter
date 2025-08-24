"use client";
import { useEffect, useState } from "react";
import type { ReviewResult } from "@/types/review";
import { getReview } from "@/lib/api";

interface Props {
  jobId: string;
}

export default function ReviewStatus({ jobId }: Props) {
  const [result, setResult] = useState<ReviewResult | null>(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      const data = await getReview(jobId);
      setResult(data);
    }, 1000);
    return () => clearInterval(interval);
  }, [jobId]);

  if (!result) return <p>Loading…</p>;
  return <pre>{JSON.stringify(result, null, 2)}</pre>;
}
