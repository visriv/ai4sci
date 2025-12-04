import json
from src.eval.evaluator import evaluate
from src.serve.registry import register_model, promote_model

def canary_evaluate(tag: str, model_name: str):
    # register new model temporarily
    register_model(tag, model_name)

    # run evaluation suite
    stats, _ = evaluate("data/rca_dataset/eval.jsonl")

    score = stats["overall_acc"]
    print(f"Model {model_name} got score {score:.3f}")

    # load the current best model score if exists
    try:
        with open("registry/best_score.json") as f:
            best_score = json.load(f)["acc"]
    except:
        best_score = 0.0

    # promote if better
    if score > best_score:
        print("Promoting new model to production")
        promote_model(tag)
        json.dump({"acc": score}, open("registry/best_score.json", "w"))
    else:
        print("New model did not beat current best")

if __name__ == "__main__":
    canary_evaluate("rca-v2", "llama3:8b-instruct")
