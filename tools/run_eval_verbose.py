import traceback
import sys

try:
    from rag.eval import evaluate
    evaluate.main()
except SystemExit as e:
    print(f"SystemExit: code={e.code}")
    sys.exit(e.code)
except Exception:
    traceback.print_exc()
    sys.exit(2)
