![image alt]([image_url](https://github.com/Sasi-SasiKiran/LoRA-Server-content-/blob/eed12b52abf2f857c60a2d6dd8354ef3621ed8dd/Screenshot%202026-09-27%20194802.png))
# LoRA Fine-Tuning Project

A local AI-powered infrastructure operations assistant built by fine-tuning Qwen2.5-1.5B-Instruct with LoRA/QLoRA-style 4-bit training.

The goal of this project is to build an evidence-driven Cloud and Server Operations Specialist that can eventually connect to real system telemetry through MCP (Model Context Protocol) and investigate infrastructure incidents using live CPU, memory, disk, network, process, Docker, monitoring, and log data.

**Current status:** The LoRA training pipeline is complete, the trained adapter has been saved successfully, and inference/evaluation has been tested. MCP integration is the next major development stage.

---

## 1. Project Overview

Traditional chatbots can explain infrastructure concepts, but they do not automatically know the current state of a user's machine or server.

This project separates two responsibilities:

**AI knowledge and reasoning** — The fine-tuned Qwen model learns how to:
- analyze infrastructure incidents
- organize evidence
- identify possible causes
- request missing evidence
- perform root-cause analysis
- recommend remediation
- express confidence
- avoid claiming a root cause when evidence is insufficient

**Live infrastructure information** — MCP tools will provide current information such as:
- CPU usage
- memory usage
- disk usage
- GPU usage
- running processes
- network statistics
- Docker containers
- Docker logs
- operating-system logs
- Prometheus metrics
- alerts
- historical telemetry
- deployment/change information

The model therefore does not need live machine information inside its weights.

**Intended architecture:**

```
                         USER
                           |
                           v
                 +-------------------+
                 |     AI AGENT      |
                 | Qwen + LoRA       |
                 +---------+---------+
                           |
                           v
                    MCP TOOL LAYER
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
      System            Docker           Monitoring
      Metrics            Tools              Tools
        |                  |                  |
        +------------------+------------------+
                           |
                           v
                    LIVE TELEMETRY
                           |
                           v
                   EVIDENCE CORRELATION
                           |
                           v
                    ROOT CAUSE ANALYSIS
                           |
                           v
                    RECOMMENDATION
                           |
                           v
                OPTIONAL USER APPROVAL
                           |
                           v
                       ACTION
                           |
                           v
                       VERIFY
```

---

## 2. Main Objective

Build a local AI operations assistant capable of:
- receiving an infrastructure incident
- determining what evidence is required
- collecting evidence through MCP tools
- correlating metrics, logs, events, and configuration
- generating possible causes
- identifying what still needs verification
- determining a likely root cause when evidence supports it
- reporting confidence
- recommending remediation
- optionally requesting user approval before making changes
- executing approved remediation through controlled tools
- verifying that the problem was resolved

The system should prefer evidence over assumptions.

---

## 3. Design Principles

### 3.1 Evidence First

The model should not immediately guess a root cause. Instead:

```
Incident
   |
   v
Observed facts
   |
   v
Evidence required
   |
   v
Collect evidence
   |
   v
Correlate evidence
   |
   v
Possible causes
   |
   v
Verify
   |
   v
Likely root cause
```

### 3.2 No Hallucinated Live Metrics

The model must never invent current machine values.

For example, if the user says:

> My laptop is slow.

The model should **not** claim:

```
CPU is 92%.
RAM is 80%.
```

unless an actual monitoring tool returned those values. Instead, it should request:

```
CPU usage
Memory usage
Running processes
Disk usage
Disk I/O
Network activity
```

### 3.3 Separate Knowledge From Telemetry

The LoRA adapter contains learned operational behavior. MCP supplies current state.

```
LoRA  =  How to analyze infrastructure
MCP   =  What is happening right now
```

This is a fundamental architectural decision.

---

## 4. Technology Stack

**AI / Machine Learning**
- Python 3.11
- PyTorch
- Hugging Face Transformers
- Qwen2.5-1.5B-Instruct
- PEFT
- LoRA
- TRL
- bitsandbytes
- Hugging Face Datasets
- 4-bit loading / NF4 quantization / double quantization / FP16 compute

**Infrastructure / Monitoring (Planned MCP integrations)**
- Windows system metrics
- Linux system metrics
- Docker
- Prometheus
- Grafana
- application logs
- system logs
- network diagnostics
- process information

**Development**
- Windows 11
- PowerShell
- VS Code
- Python virtual environment
- Git/GitHub

---

## 5. Hardware Environment

| Component | Details |
|-----------|---------|
| CPU | Intel Core i7-12700H |
| RAM | 16 GB |
| GPU | NVIDIA GeForce RTX 3050 Laptop GPU |
| GPU VRAM | 4 GB |
| OS | Windows 11 64-bit |

The model was selected specifically so that development and inference can be performed locally on this hardware.

---

## 6. Model

**Base model:** `Qwen/Qwen2.5-1.5B-Instruct`

The base model remains frozen during LoRA training. The project does not perform full-model fine-tuning.

```
Qwen2.5-1.5B
        |
        | frozen
        v
     Base model
        +
   Small LoRA adapter
        |
        v
Cloud Operations Specialist
```

---

## 7. Why LoRA

Full fine-tuning would require updating a very large number of model parameters. LoRA trains only small adapter matrices.

**Benefits:**
- much lower GPU memory usage
- faster training
- smaller output model
- original model remains unchanged
- adapter can be replaced independently
- suitable for a 4 GB GPU development environment

**Current LoRA configuration:**

| Parameter | Value |
|-----------|-------|
| Rank (r) | 16 |
| Alpha | 32 |
| Dropout | 0.05 |
| Bias | none |
| Task | CAUSAL_LM |

**Target modules:** `q_proj`, `k_proj`, `v_proj`, `o_proj`

---

## 8. 4-Bit Quantization

```
load_in_4bit = True
quant_type   = NF4
double_quant = True
compute      = FP16
```

This significantly reduces the memory required to load the base model. The base model is still frozen. The trainable component is the LoRA adapter.

---

## 9. Dataset

The dataset uses JSONL format. Each example follows the conversational structure:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a Cloud and Server Operations Specialist."
    },
    {
      "role": "user",
      "content": "..."
    },
    {
      "role": "assistant",
      "content": "..."
    }
  ]
}
```

**Current dataset size:**

| Split | Examples |
|-------|----------|
| Training | 400 |
| Validation | 50 |
| Testing | 50 |
| Total | 500 |

**Dataset files:**

```
data/
├── train.jsonl
├── validation.jsonl
└── test.jsonl
```

---

## 10. Dataset Domains

The dataset covers infrastructure and cloud operations topics including:
- Linux, Docker, Kubernetes
- Networking
- AWS, Azure, GCP
- Prometheus, Grafana, monitoring
- databases, security, CI/CD
- deployment, incident response, root-cause analysis

The dataset is designed around operational incidents rather than simple definitions.

Examples include:
- High CPU utilization
- Memory exhaustion
- Disk saturation
- Docker restart loops
- Application errors
- Network latency
- Database latency
- Deployment failures
- Monitoring alerts
- Security-related incidents
- Cloud resource problems
- Service availability problems

---

## 11. Dataset Quality

**Duplicate questions:**

| Split | Duplicates |
|-------|-----------|
| Training | 0 |
| Validation | 0 |
| Testing | 0 |

**Token length (Qwen tokenizer):**

| Split | Min | Max | Average |
|-------|-----|-----|---------|
| Training | 225 | 264 | 243.85 |
| Validation | 226 | 258 | 244.54 |
| Test | 224 | 264 | 244.80 |

No examples exceeded the configured 512-token maximum.

---

## 12. Expected Response Format

The model is trained to structure incident analysis using:

```
INCIDENT
OBSERVED
EVIDENCE / EVIDENCE NEEDED
POSSIBLE CAUSES
NEEDS VERIFICATION
LIKELY CAUSE
CONFIDENCE
RECOMMENDED ACTION
```

**Example:**

```
INCIDENT
High CPU utilization on the server.

OBSERVED
- CPU utilization is reported as 95%.
- Memory utilization is reported as 40%.

EVIDENCE / EVIDENCE NEEDED
- Process-level CPU utilization
- CPU utilization over time
- Recent deployments
- Application logs
- System load

POSSIBLE CAUSES
- CPU-intensive process
- Increased workload
- Runaway process
- Recent application change

NEEDS VERIFICATION
Identify the process consuming CPU and correlate it with
application and deployment events.

LIKELY CAUSE
Cannot be determined without process-level evidence.

CONFIDENCE
Low

RECOMMENDED ACTION
Collect process-level CPU data and recent application events
before restarting services.
```

---

## 13. Insufficient Evidence Behavior

The model must distinguish between an **observed fact** and a **hypothesis**.

- `CPU = 95%` is an observed fact if supplied by a monitoring tool.
- `A runaway process is causing the CPU problem.` is a hypothesis until process-level evidence confirms it.

When evidence is insufficient:

```
LIKELY CAUSE
Cannot be determined until the required evidence is collected.
```

---

## 14. Training Configuration

| Parameter | Value |
|-----------|-------|
| Epochs | 2 |
| Train batch size | 1 |
| Gradient accumulation | 8 |
| Learning rate | 2e-4 |
| Scheduler | cosine |
| Warmup steps | 20 |
| Maximum sequence length | 512 |
| Optimizer | paged_adamw_8bit |
| Gradient checkpointing | enabled |
| Packing | disabled |
| Seed | 42 |

AMP was disabled during the successful training run because the initial configuration caused a GradScaler/BF16 incompatibility. The successful configuration used:

```
fp16 = False
bf16 = False
```

The base model continued to use 4-bit NF4 quantization with FP16 computation.

---

## 15. Training Result

LoRA training completed successfully. The adapter was saved to:

```
outputs/cloud-operations-lora
```

**GPU memory usage during training:**

| Metric | Value |
|--------|-------|
| Allocated GPU memory | 1.54 GB |
| Reserved GPU memory | 2.88 GB |

The adapter is therefore ready for inference and further evaluation.

---

## 16. Project Structure

```
D:\LoRA\
│
├── data/
│   ├── train.jsonl
│   ├── validation.jsonl
│   └── test.jsonl
│
├── models/
│
├── outputs/
│   └── cloud-operations-lora/
│
├── scripts/
│   ├── generate_dataset.py
│   ├── build_real_dataset.py
│   ├── prepare_dataset.py
│   ├── check_dataset_quality.py
│   ├── check_token_lengths.py
│   ├── train_lora.py
│   ├── evaluate.py
│   ├── test_lora_setup.py
│   └── chat.py
│
├── venv/
├── requirements.txt
├── test_qwen.py
└── README.md
```

---

## 17. Important Scripts

**train_lora.py** — Responsible for:
- loading tokenizer
- loading Qwen
- configuring 4-bit quantization
- preparing the model for k-bit training
- configuring LoRA
- loading training/validation datasets
- creating the SFT trainer
- training the adapter
- saving the adapter

**test_lora_setup.py** — Used before training to verify:
- CUDA availability
- Qwen loading
- 4-bit quantization
- LoRA configuration
- trainable parameters
- GPU memory

**evaluate.py** — Used to:
- load the base model
- load the trained LoRA adapter
- generate responses
- test operational scenarios
- verify model behavior

**prepare_dataset.py** — Validates the JSONL dataset structure and message roles.

**check_dataset_quality.py** — Checks dataset quality characteristics such as duplicate user questions, answer length, and dataset distribution.

**check_token_lengths.py** — Checks token counts using the actual Qwen tokenizer.

**chat.py** — Interactive chat interface for the fine-tuned model.

---

## 18. How to Set Up the Project

```bash
# Create project directory
cd D:\
mkdir LoRA
cd LoRA

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Verify CUDA
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU')"
```

Expected output:
```
True
NVIDIA GeForce RTX 3050 Laptop GPU
```

---

## 19. Model Cache

The Qwen model is stored locally through the Hugging Face cache. The project uses:

```python
local_files_only=True
```

This prevents the training and evaluation scripts from requiring a network download when the model is already cached.

---

## 20. Inference Architecture

```
Qwen2.5-1.5B-Instruct
        +
cloud-operations-lora
```

The base model is loaded in 4-bit. The adapter is loaded separately.

```
Base Model
   |
   +---- LoRA Adapter
              |
              v
      Specialized Model
```

The adapter can therefore be updated without replacing the original Qwen model.

---

## 21. Interactive Chat Testing

The trained model can be tested directly from the terminal as a normal user.

This is the current user-facing testing stage before connecting the model to MCP and live system tools.

**Chat flow:**

```
User
 |
 v
Interactive Terminal Chat
 |
 v
Qwen2.5-1.5B-Instruct + LoRA Adapter
 |
 v
Cloud/Server Operations Specialist
 |
 v
Operational Response
```

The chat interface allows the user to enter infrastructure questions and receive responses from the fine-tuned model. The model does not automatically know the current state of the laptop.

**Chat system prompt:**

```
You are a Cloud and Server Operations Specialist.

Analyze infrastructure incidents using evidence, metrics, logs,
events and configuration.

Do not invent live system information.
Do not guess when evidence is insufficient.

Clearly separate:

INCIDENT
OBSERVED
EVIDENCE / EVIDENCE NEEDED
POSSIBLE CAUSES
NEEDS VERIFICATION
LIKELY CAUSE
CONFIDENCE
RECOMMENDED ACTION

When current system information is unavailable, explicitly state
what evidence should be collected.
```

**Run the chat:**

```bash
# From D:\LoRA
.\venv\Scripts\Activate.ps1
python scripts\chat.py
```

Expected startup:

```
Loading model...
Model loaded.
Type 'exit' or 'quit' to stop.

You:
```

**Example questions:**

High CPU:
```
You: My server CPU usage is very high. What should I investigate?
```

The model should identify relevant evidence such as: CPU utilization, process-level CPU usage, load average, recent deployments, application traffic, system logs, container resource usage, memory pressure, process restarts.

Docker containers restarting:
```
You: My Docker container keeps restarting. How should I investigate it?
```

The model should consider: container exit code, container logs, health-check failures, OOM kills, application startup errors, environment variables, mounted files, resource limits, recent image changes.

Database slowness:
```
You: The application became slow after a deployment. What evidence should I collect?
```

The model should consider: application latency, database query latency, slow queries, database connections, connection pool usage, CPU and memory, disk I/O, locks and waits, deployment changes, error rates.

Live information test:
```
You: What is my current CPU usage?
```

The model should not produce a made-up percentage. It should state that live CPU information is unavailable and explain how to collect it.

**What the model currently has:**
- learned operational patterns
- incident-analysis behavior
- evidence-first reasoning
- insufficient-evidence behavior
- structured response formatting
- domain knowledge from the training dataset

**What the model does not yet have:**
- current CPU, RAM, disk, GPU usage
- running processes
- Docker containers
- system logs
- Prometheus metrics
- Grafana data
- live network statistics

Those capabilities belong to the next stage, where MCP tools will provide live telemetry.

**Current development stage:**

```
Dataset
   |
   v
LoRA Training
   |
   v
Evaluation
   |
   v
Interactive Chat     <-- CURRENT STAGE
   |
   v
MCP Integration
   |
   v
Live System Monitoring
   |
   v
Agent-based Investigation
```

The project is currently complete through interactive local chat testing. MCP integration and live telemetry are intentionally not included in this version of the README.
