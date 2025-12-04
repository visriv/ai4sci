# ---- Stage 1: builder ----
FROM python:3.10-slim AS builder

# Install python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Stage 2: runtime (tiny) ----
FROM python:3.10-slim

WORKDIR /app

# Copy installed packages
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy source code
COPY . .

EXPOSE 8000
CMD ["uvicorn", "src.serve.server:app", "--host", "0.0.0.0", "--port", "8000"]
