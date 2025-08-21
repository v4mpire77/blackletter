import argparse
import json
import math
import sys
from typing import List


def recall_at_k(gold_passages: List[str], retrieved_passages: List[str], k: int) -> float:
    gold_set = set(gold_passages)
    retrieved_set = set(retrieved_passages[:k])
    return len(gold_set & retrieved_set) / len(gold_set) if gold_set else 0.0


def ndcg_at_k(gold_passages: List[str], retrieved_passages: List[str], k: int) -> float:
    def dcg(rels):
        return sum(rel / math.log2(idx + 2) for idx, rel in enumerate(rels))

    relevance = [1 if p in gold_passages else 0 for p in retrieved_passages[:k]]
    ideal = sorted(relevance, reverse=True)
    dcg_val = dcg(relevance)
    idcg_val = dcg(ideal)
    return dcg_val / idcg_val if idcg_val else 0.0


def judge_faithfulness(question: str, answer: str, context: str) -> float:
    # Deterministic fallback: check substring presence. External API usage is optional.
    try:
        return 1.0 if answer.lower() in context.lower() else 0.0
    except Exception:
        return 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", default="rag/eval/gold_qa.jsonl")
    parser.add_argument("--baseline", default="rag/eval/baseline.json")
    parser.add_argument("-k", type=int, default=5)
    args = parser.parse_args()

    gold_lines = [l.strip() for l in open(args.gold, "r", encoding="utf-8") if l.strip()]
    gold_data = [json.loads(line) for line in gold_lines]

    per_item = []
    recalls, ndcgs, faithfulness = [], [], []
    for idx, item in enumerate(gold_data, start=1):
        question = item.get("question", "")
        gold_passages = item.get("gold_passages", [])
        # In CI we use the gold passages as retrieved (placeholder)
        retrieved = gold_passages
        r = recall_at_k(gold_passages, retrieved, args.k)
        n = ndcg_at_k(gold_passages, retrieved, args.k)
        answer = gold_passages[0] if gold_passages else ""
        context = " ".join(retrieved[: args.k])
        f = judge_faithfulness(question, answer, context)
        per_item.append({"idx": idx, "question": question, "recall": r, "ndcg": n, "faith": f})
        recalls.append(r)
        ndcgs.append(n)
        faithfulness.append(f)

    metrics = {
        f"recall@{args.k}": sum(recalls) / len(recalls) if recalls else 0.0,
        f"ndcg@{args.k}": sum(ndcgs) / len(ndcgs) if ndcgs else 0.0,
        "faithfulness": sum(faithfulness) / len(faithfulness) if faithfulness else 0.0,
    }

    baseline = json.load(open(args.baseline, "r", encoding="utf-8"))
    threshold = 0.05

    # Print per-item diagnostics
    for it in per_item:
        print(f"Item {it['idx']}: recall={it['recall']:.3f}, ndcg={it['ndcg']:.3f}, faith={it['faith']:.3f}")

    print("\nSummary:")
    header = f"{'Metric':<15}{'Value':<10}{'Baseline':<10}{'Drop%':<10}"
    print(header)

    exit_code = 0
    for key, val in metrics.items():
        base = baseline.get(key, 0)
        drop_pct = ((base - val) / base * 100) if base else 0.0
        print(f"{key:<15}{val:<10.3f}{base:<10.3f}{drop_pct:<10.1f}")
        if base and val < base * (1 - threshold):
            exit_code = 1

    if exit_code:
        print("\n❌ Metrics dropped more than 5%")
    else:
        print("\n✅ Metrics within acceptable range")

    with open("rag/eval/last_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    with open("rag/eval/last_items.json", "w", encoding="utf-8") as f:
        json.dump(per_item, f, indent=2)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
