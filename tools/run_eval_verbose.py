import traceback

try:
    from rag.eval import evaluate
    evaluate.main()
except Exception:
    traceback.print_exc()
    raise
