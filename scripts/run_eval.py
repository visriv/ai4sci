import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.eval.evaluator import evaluate

if __name__ == "__main__":
    evaluate("data/rca_dataset/eval.jsonl")
