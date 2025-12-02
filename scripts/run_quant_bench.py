import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.quant.benchmark import benchmark_models

if __name__ == "__main__":
    models = [
        "llama3:instruct",
        "llama3:8b",
        "qwen2.5:7b",
        "qwen2.5:7b-instruct",
        "phi3:medium"
    ]

    prompt = "Explain the training failure: loss diverged to NaN after step 30."
    res = benchmark_models(models, prompt, tokens=256)

    print("\n=== Summary ===")
    for r in res:
        print(f"{r['model']:20s} | {r['tps']:.1f} tok/s | time={r['time']:.2f}s")
