
# 🧠 ai4sci - reasoning and interpretation for science
*A Modern Agentic AI + LLMOps Project *

---

## 🌍 Project Overview  
ai4sci is a **production-grade LLM Agent** designed to perform **agentic reasoning and interpretation for scientific discovery**.
Before jumping into research, we experiemnt and implement the tools used for agentic reasoning for two other tasks:

1. RCA analysis for ML engineer: given a bunch of logs, identify the root cause
2. ESG Intelligence: document scoring and auditing

## Tech Stack

- **Ollama + Llama 3.1** (local inference)
- **FastAPI** (async LLM server)
- **VectorDB-based retrieval pipeline**
- **Streaming evaluation + canary testing**
- **Custom monitoring layer**
- **Streamlit operations dashboard**
- **Dockerized deployment**
- **Simulated autoscaling**
- 
This is **Task 1** of a 3-part AI project:
1. **Root Cause Analysis (SciRCA) — Completed**  
2. **ESG Intelligence (GreenDocs) — Document parsing, ESG scoring, LLM-based auditing**  
3. **AI4Science Reasoning Module — Model-driven scientific insight & anomaly interpretation**

---


## 🏗 Architecture (High-Level)

```
                ┌────────────────────┐
                │    Client App       │
                │(Streamlit Dashboard)│
                └─────────┬──────────┘
                          │  HTTP
                          ▼
                ┌────────────────────┐
                │    FastAPI Server   │
                │ - RCA Endpoint      │
                │ - Monitoring Layer  │
                └───────┬────────────┘
                        │ Calls Agent
                        ▼
                ┌────────────────────┐
                │     RCA Agent      │
                │ - Tool calls       │
                │ - Multi-step plan  │
                └───────┬────────────┘
                        │ LLM Chat
                        ▼
                ┌────────────────────┐
                │   Llama 3.1 (8B)    │
                │     via Ollama      │
                └────────────────────┘
```

---

## 🔧 Tech Stack 
### **LLM / Agentic AI**
- Tool-using LLM agent (multi-step reasoning)
- Local inference via Ollama  
- Chat + tool call parsing  
- RAG pipeline integration  

### **LLMOps**
- FastAPI async server  
- Monitoring:  
  - request count  
  - latency  
  - error rate  
- Canary evaluation  
- Model registry  

### **Optimization**
- Quantized Llama models  
- Async batching of tool calls  
- Local GPU/Metal acceleration  

### **Visualization & Ops**
- Real-time dashboard (Streamlit)  
- Logs viewer  
- Inference tester  
- Latency charts  

### RAGs


### Reasoning
TODO

---


## 📦 Directory Structure

```
scirca/
│
├── src/
│   ├── agent/          ← RCA agent + LLM client
│   ├── retriever/      ← RAG embedding + search
│   ├── serve/          ← FastAPI server + monitors
│   ├── utils/          ← YAML loader, logger
│   └── models/         ← Model registry files
│
├── dashboard/
│   ├── app.py          ← Streamlit GUI
│   └── components/     ← metrics, logs, registry, tester
│
├── scripts/            ← CLI scripts (eval, run agent, benchmark)
├── requirements.txt
└── Dockerfile
```

---

## 🧪 Running Locally (macOS + Ollama)

### 1. Install Ollama
```bash
brew install ollama
```

### 2. Pull the model
```bash
ollama pull llama3.1:8b
```

### 3. Start Ollama
```bash
ollama serve
```

---

## 🚀 Start FastAPI Server

```bash
uvicorn src.serve.api:app --reload --port 8000
```

---

## 📊 Start Monitoring Dashboard

```bash
streamlit run dashboard/app.py
```

Open:  
👉 http://localhost:8501

Dashboard Features:
- Metrics (request rate, latency, errors)
- Logs viewer (Docker/FastAPI logs)
- Model registry viewer  
- Inference runner for RCA

---

## 🐳 Docker Deployment

### Build
```bash
docker build -t scirca-api .
```

### Run
```bash
docker run -p 8000:8000 scirca-api
```

### Run dashboard
```bash
streamlit run dashboard/app.py
```
---

## 🛠 Example API Call

```bash
curl -X POST http://localhost:8000/rca   -H "Content-Type: application/json"   -d '{
        "run_summary": "Training failed with NaN loss",
        "logs": ["loss=0.5", "loss=0.7", "loss=nan"],
        "metrics": {"loss": [0.5, 0.7, "nan"]},
        "model_tag": "rca-v2"
      }'
```


## Load testing via autoscaling
```bash
python scripts/load_test.py \
    --api http://localhost:8000 \
    --concurrency 50 \
    --total 500
```
or (this second one has been tested
```bash
bash scripts/run_load_test.sh
```
---

## 🧩 Roadmap (Task 2 & 3)

### **Task 2 — ESG Intelligence (GreenDocs)**
Planned capabilities:
- ESG report ingestion  
- Compliance summarisation  
- Automated ESG scoring  
- Greenwashing detection  
- Multi-document RAG  

### **Task 3 — AI4Science Reasoning Module**
Planned:
- Scientific anomaly reasoning  
- Embedding-based pattern detection  
- Hypothesis generation  
- LLM-assisted interpretation of experimental results  

---

