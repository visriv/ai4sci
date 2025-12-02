from src.ingest.mock_runs import generate_mock_runs
from src.ingest.save_runs import save_runs

def main():
    runs = generate_mock_runs(12)   # create 12 sample experiments
    save_runs(runs, "data/rca_dataset/runs.jsonl")

if __name__ == "__main__":
    main()
