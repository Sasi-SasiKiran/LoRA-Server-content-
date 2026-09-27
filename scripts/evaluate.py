import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)
from peft import PeftModel


# ============================================================
# CONFIGURATION
# ============================================================

BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"

ADAPTER_PATH = "outputs/cloud-operations-lora"


# ============================================================
# GPU CHECK
# ============================================================

if not torch.cuda.is_available():
    raise RuntimeError("CUDA GPU is not available.")

print("=" * 60)
print("GPU")
print("=" * 60)

print("GPU:", torch.cuda.get_device_name(0))


# ============================================================
# LOAD TOKENIZER
# ============================================================

print()
print("=" * 60)
print("LOADING TOKENIZER")
print("=" * 60)

tokenizer = AutoTokenizer.from_pretrained(
    ADAPTER_PATH,
    local_files_only=True,
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("Tokenizer loaded.")


# ============================================================
# 4-BIT CONFIGURATION
# ============================================================

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)


# ============================================================
# LOAD BASE MODEL
# ============================================================

print()
print("=" * 60)
print("LOADING BASE MODEL")
print("=" * 60)

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map="auto",
    local_files_only=True,
)

base_model.config.use_cache = True

print("Base model loaded.")


# ============================================================
# LOAD LoRA ADAPTER
# ============================================================

print()
print("=" * 60)
print("LOADING LoRA ADAPTER")
print("=" * 60)

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_PATH,
)

model.eval()

print("LoRA adapter loaded successfully.")


# ============================================================
# GENERATION FUNCTION
# ============================================================

def generate_response(question):

    system_prompt = (
        "You are a Cloud and Server Operations Specialist. "
        "Analyze infrastructure incidents using evidence, metrics, "
        "logs, events and configuration. "
        "Do not guess when evidence is insufficient. "
        "Clearly separate observations, possible causes, "
        "verification steps, root cause and recommended remediation."
    )

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=False,
            temperature=0.0,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    )

    return response.strip()


# ============================================================
# TEST QUESTIONS
# ============================================================

questions = [

    "My server CPU usage is 95% while memory usage is 40%. How should I investigate this incident?",

    "A Docker container keeps restarting every few minutes. What evidence should I collect before taking action?",

    "A web application suddenly became slow, but CPU and memory usage are normal. How should I investigate?",

    "A server has almost no free disk space. What should I check and what remediation would you recommend?",

    "Network latency between the application and database has increased. What evidence should I collect?",

]


# ============================================================
# RUN TESTS
# ============================================================

print()
print("=" * 60)
print("LoRA MODEL TEST")
print("=" * 60)

for index, question in enumerate(questions, start=1):

    print()
    print("=" * 60)
    print(f"TEST {index}")
    print("=" * 60)

    print()
    print("QUESTION:")
    print(question)

    print()
    print("MODEL RESPONSE:")

    response = generate_response(question)

    print(response)


# ============================================================
# GPU MEMORY
# ============================================================

print()
print("=" * 60)
print("GPU MEMORY")
print("=" * 60)

allocated = torch.cuda.memory_allocated() / 1024**3
reserved = torch.cuda.memory_reserved() / 1024**3

print(f"Allocated: {allocated:.2f} GB")
print(f"Reserved:  {reserved:.2f} GB")


print()
print("=" * 60)
print("EVALUATION COMPLETE")
print("=" * 60)