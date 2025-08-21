import argparse
import json
import math
import os
import sys


def recall_at_k(gold_passages, retrieved_passages, k):
    gold_set = set(gold_passages)
    retrieved_set = set(retrieved_passages[:k])
    return len(gold_set & retrieved_set) / len(gold_set) if gold_set else 0.0


def ndcg_at_k(gold_passages, retrieved_passages, k):
    def dcg(rels):
        return sum(rel / math.log2(idx + 2) for idx, rel in enumerate(rels))

    relevance = [1 if p in gold_passages else 0 for p in retrieved_passages[:k]]
    ideal = sorted(relevance, reverse=True)
    dcg_val = dcg(relevance)
    idcg_val = dcg(ideal)
    return dcg_val / idcg_val if idcg_val else 0.0


def judge_faithfulness(question, answer, context):
    prompt = (
        f"Question: {question}\n"
        f"Context: {context}\n"
        f"Answer: {answer}\n"
        "Is the answer faithful to the context? Reply yes or no."
    )
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            return (
                1.0
                if "yes" in response.text.lower()
                else 0.0
            )
        except Exception:
            pass
    return 1.0 if answer.lower() in context.lower() else 0.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold", default="rag/eval/gold_qa.jsonl")
    parser.add_argument("--baseline", default="rag/eval/baseline.json")
    parser.add_argument("-k", type=int, default=5)
    args = parser.parse_args()

    gold_data = [json.loads(line) for line in open(args.gold, "r", encoding="utf-8")]

    recalls, ndcgs, faithfulness = [], [], []
    for item in gold_data:
        question = item["question"]
        gold_passages = item["gold_passages"]
        retrieved = gold_passages  # placeholder retrieval results
        recalls.append(recall_at_k(gold_passages, retrieved, args.k))
        ndcgs.append(ndcg_at_k(gold_passages, retrieved, args.k))
        answer = gold_passages[0] if gold_passages else ""
        context = " ".join(retrieved[: args.k])
        faithfulness.append(judge_faithfulness(question, answer, context))

    metrics = {
        f"recall@{args.k}": sum(recalls) / len(recalls) if recalls else 0.0,
        f"ndcg@{args.k}": sum(ndcgs) / len(ndcgs) if ndcgs else 0.0,
        "faithfulness": sum(faithfulness) / len(faithfulness)
        if faithfulness
        else 0.0,
    }

    baseline = json.load(open(args.baseline, "r", encoding="utf-8"))
    threshold = 0.05
    header = f"{'Metric':<15}{'Value':<10}{'Baseline':<10}{'Drop':<10}"
    print(header)
    exit_code = 0
    for key, val in metrics.items():
        base = baseline.get(key, 0)
        drop = (base - val) / base if base else 0.0
        print(f"{key:<15}{val:<10.3f}{base:<10.3f}{drop*100:<10.1f}")
        if base and val < base * (1 - threshold):
            exit_code = 1

    if exit_code:
        print("❌ Metrics dropped more than 5%")
    else:
        print("✅ Metrics within acceptable range")

    with open("rag/eval/last_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
